import torch
import numpy as np
from torch.autograd import Variable
from NURBSDiff.curve_eval_cpp import forward as cpp_forward, backward as cpp_backward, pre_compute_basis as cpp_pre_compute_basis
from NURBSDiff.curve_eval_cuda import pre_compute_basis, forward, backward
from .utils import gen_knot_vector
torch.manual_seed(120)


class CurveEval(torch.nn.Module):
    """Evaluate control points and weights to sample points on the curvature.
    """

    def __init__(self, num_control_points: int, knot_vectors: torch.Tensor | None = None,
                 dimension: int = 3, order: int = 2, out_dim: int = 32, method: str = 'tc'):
        """Initialize the curve evaluation.

        Args:
            num_control_points (int):
                Number of control points for the curvature.
            knot_vectors (torch.Tensor, optional):
                Optional knot vectors of the curvature. If None are specified,
                it will be automatically generated. Defaults to None.
            dimension (int, optional):
                Dimension of the curvature. Defaults to 3.
            order (int, optional):
                Order of the curvature. Defaults to 2.
            out_dim (int, optional):
                Number of sampled points from the curvature. Defaults to 32.
            method (str, optional):
                Method to use. Choose from 'cpp' or 'tc'. 'cpp' refers to pre-compiled
                c++ code. 'tc' refers to tensor computation in python. Defaults to 'cpp'.
        """
        super(CurveEval, self).__init__()
        self.num_control_points = num_control_points
        self._dimension = dimension
        self.order = order
        if knot_vectors is not None:
            self.knot_vectors = knot_vectors
        else:
            self.knot_vectors = torch.Tensor(self._gen_knot_vector(self.order, self.num_control_points))
        self.curve_param = torch.linspace(0.0, 1.0, steps=out_dim, dtype=torch.float32)
        self.method = method
        self.curve_parameter_span_cpu, self.new_curve_param_cpu = cpp_pre_compute_basis(self.curve_param, self.knot_vectors, num_control_points, order, out_dim, self._dimension)
        # --- Induces illegal memory access issues when called repeatedly without kernel restart ---
        # todo: fix CPP code in `pre_compute_bases`
        #self.curve_parameter_span_cuda, self.new_curve_param_cuda = pre_compute_basis(self.curve_param.cuda(), self.knot_vectors.cuda(), num_control_points, order, out_dim, self._dimension)

        # --- Move the pre-computed parameters from cpu to gpu ---
        self.curve_parameter_span_cuda = self.curve_parameter_span_cpu.cuda()
        self.new_curve_param_cuda = self.new_curve_param_cpu.cuda()
                     
    def forward(self, input: torch.Tensor) -> torch.Tensor:
        """Forward pass of the module.

        Args:
            input (torch.Tensor):
                Control points and weights, shape would be
                (batch_size, num_control_points, control_points_dimension + 1 ),
                where 1 refers to the control point weights.

        Returns:
            torch.Tensor:
                Sampled points from the curvature.
        """
        # input will be of dimension (batch_size, num_control_points+1, n+1, dimension+1)
        device = input.device.type
        if device == 'cuda':
            curve_parameter_span = self.curve_parameter_span_cuda
            new_curve_param = self.new_curve_param_cuda
        else:
            curve_parameter_span = self.curve_parameter_span_cpu
            new_curve_param = self.new_curve_param_cpu

        if self.method == 'cpp':
            if self.curve_param.device.type != device:
                self.curve_param = self.curve_param.to(input.device)
            out = CurveEvalFunc.apply(input, curve_parameter_span, new_curve_param, self.curve_param, self.num_control_points, self.order, self._dimension, device)
            return out
        elif self.method == 'tc':
            # input[:,:,:self._dimension] = input[:,:,:self._dimension]*input[:,:,self._dimension].unsqueeze(-1)
            curves = new_curve_param[:, 0].unsqueeze(-1) * input[:, (curve_parameter_span - self.order).type(torch.LongTensor), :]
            for j in range(1, self.order + 1):
                curves += new_curve_param[:, j].unsqueeze(-1) * input[:, (curve_parameter_span - self.order + j).type(torch.LongTensor), :]
            return curves[:, :, :self._dimension] / curves[:, :, self._dimension].unsqueeze(-1)

    @staticmethod
    def _gen_knot_vector(order: int, num_control_points: int, delta: float = 1e-6) -> np.ndarray:
        """Generate knot vectors automatically.

        Args:
            order (int):
                Order of the curvature.
            num_control_points (int):
                Number of control points.
            delta (float, optional):
                Epsilon to avoid direct 0 value. Defaults to 1e-6.

        Returns:
            np.ndarray: _description_
        """
        # order: degree, n: number of control points; num_control_points+1: number of knots
        num_control_points = order + num_control_points + 1

        # Calculate a uniform interval for middle knots
        num_segments = (num_control_points - 2 * (order + 1) + 1)  # number of segments in the middle
        assert num_segments != 0, 'Number of control points has to be bigger than number of order.'
        spacing = (1.0) / (num_segments)  # spacing between the knots (uniform)

        # First degree+1 knots are "knot_min"
        knot_vector = [(j + 1) * delta for j in range(0, order)]

        # Middle knots
        knot_vector += [mid_knot for mid_knot in np.linspace(delta * (order + 1), 1, num_segments + 1)]

        # Last degree+1 knots are "knot_max"
        knot_vector += [float(1) for j in range(0, order)]

        # Return auto-generated knot vector
        return np.array(knot_vector)



class CurveEvalFunc(torch.autograd.Function):
    """Autograd function for curve evaluation.
    """

    @staticmethod
    def forward(ctx: torch.Tensor, control_points: torch.Tensor, curve_parameter_span: torch.Tensor,
                new_curve_parameter: torch.Tensor, curve_parameter: torch.Tensor,
                num_control_points: int, order: int, _dimension: int, _device: str) -> torch.Tensor:
        """Receive control points, generate curves, and sample points from the curves.

        Args:
            ctx (torch.Tensor):
                Context object.
            control_points (torch.Tensor):
                Control points and the weights of the curvature.
            curve_parameter_span (torch.Tensor):
                Space of the curve parameters.
            new_curve_parameter (torch.Tensor):
                New curve parameters.
            curve_parameter (torch.Tensor):
                Curve parameters.
            num_control_points (int):
                Number of control points.
            order (int):
                Order of the curvature.
            _dimension (int):
                Dimension of the curvature.
            _device (str):
                Device of tensor.

        Returns:
            torch.Tensor:
                Sampled points from the curvature.
        """
        ctx.save_for_backward(control_points)
        ctx.curve_parameter_span = curve_parameter_span
        ctx.new_curve_parameter = new_curve_parameter
        ctx.curve_parameter = curve_parameter
        ctx.num_control_points = num_control_points
        ctx.order = order
        ctx._dimension = _dimension
        ctx._device = _device
        if _device == 'cuda':
            curves = forward(control_points, curve_parameter_span, new_curve_parameter, curve_parameter, num_control_points, order, _dimension)
        else:
            curves = cpp_forward(control_points.cpu(), curve_parameter_span.cpu(), new_curve_parameter.cpu(), curve_parameter.cpu(), num_control_points, order, _dimension)
        ctx.curves = curves
        return curves[:, :, :_dimension] / curves[:, :, _dimension].unsqueeze(-1)

    @staticmethod
    def backward(ctx: torch.Tensor, grad_output: torch.Tensor) -> tuple[Variable, None, None, None, None, None, None, None]:
        """Backward computation of the function.

        Args:
            ctx (torch.Tensor):
                Context objects.
            grad_output (torch.Tensor):
                Gradient outputs

        Returns:
            tuple[Variable, None, None, None, None, None, None, None]:
                The backwards calculation for each of the forward input.
                Everything else is None because they don't need gradients.
        """
        control_points, = ctx.saved_tensors
        curve_parameter_span = ctx.curve_parameter_span
        new_curve_parameter = ctx.new_curve_parameter
        curve_parameter = ctx.curve_parameter
        num_control_points = ctx.num_control_points
        order = ctx.order
        _device = ctx._device
        _dimension = ctx._dimension
        curves = ctx.curves
        grad_cw = torch.zeros((grad_output.size(0), grad_output.size(1), _dimension + 1), dtype=torch.float32)
        if _device == 'cuda':
            grad_cw = grad_cw.cuda()
        grad_cw[:, :, :_dimension] = grad_output
        for d in range(_dimension):
            grad_cw[:, :, _dimension] += grad_output[:, :, d] / curves[:, :, _dimension]
        if _device == 'cuda':
            grad_control_points = backward(grad_cw, control_points, curve_parameter_span, new_curve_parameter, curve_parameter, num_control_points, order, _dimension)
        else:
            grad_control_points = cpp_backward(grad_cw, control_points, curve_parameter_span, new_curve_parameter, curve_parameter, num_control_points, order, _dimension)

        return Variable(grad_control_points[0]), None, None, None, None, None, None, None
