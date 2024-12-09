import numpy as np
import string
import torch
from torch.distributed.tensor import distribute_tensor, DTensor, Replicate, Shard
from utils import to_local, to_dist

# adapted from https://github.com/ClashLuke/kron_torch/tree/main

torch._dynamo.config.cache_size_limit = 1_000_000

try:
    torch.backends.opt_einsum.strategy = "dynamic-programming"
except AttributeError:
    # opt_einsum backend is not available, so we'll skip setting the strategy
    pass

def is_tensor(x):
    return isinstance(x, torch.Tensor)

def get_q(state):
    return [q for q in (state["Q0"], state["Q1"], state["Q2"], state["Q3"]) if is_tensor(q)]


def precond_update_prob_schedule(
    max_prob=1.0, min_prob=0.03, decay=0.001, flat_start=250
):
    """Anneal preconditioner update probability during beginning of training.

    PSGD benefits from more preconditioner updates at the beginning of training,
    but once the preconditioner is learned the update probability can drop low.

    This schedule is an exponential anneal with a flat start. Default settings keep
    update probability at 1.0 for 200 steps then exponentially anneal down to
    `min_prob` by 4000 steps. Default settings work very well for most models and
    training regimes.
    """

    def _schedule(n):
        """Exponential anneal with flat start."""
        n = torch.tensor(n, dtype=torch.float32)
        prob = torch.minimum(
            torch.maximum(
                max_prob * torch.exp(-decay * (n - flat_start)), torch.tensor(min_prob)
            ),
            torch.tensor(max_prob),
        )
        return prob

    return _schedule


class Kron(torch.optim.Optimizer):
    """Implements PSGD Kron from https://github.com/lixilinx/psgd_torch.

    Args:
        params (iterable): Iterable of parameters to optimize or dicts defining
            parameter groups.
        lr (float): Learning rate.
        b1 (float): Momentum parameter.
        weight_decay (float): Weight decay (L2 penalty).
        preconditioner_update_probability (callable or float, optional): Probability of
            updating the preconditioner. If None, defaults to a schedule that anneals
            from 1.0 to 0.03 by 4000 steps.
        max_size_triangular (int): Max size for dim's preconditioner to be triangular.
        min_ndim_triangular (int): Minimum number of dimensions a layer needs
            to have triangular preconditioners.
        memory_save_mode: (string, optional), None, 'one_diag', or 'all_diag', None is default
            to set all preconditioners to be triangular, 'one_diag' sets the largest
            or last dim to be diagonal per layer, and 'all_diag' sets all preconditioners
            to be diagonal.
        mu_dtype (torch.dtype, optional): Dtype of the momentum accumulator.
        precond_dtype (torch.dtype, optional): Dtype of the preconditioner.
        trust_region_scale (float): Trust region on preconditioned grads. Normally this
            doesn't need to be changed but if things seem unstable you can try reducing
            this to 1.5.
    """

    def __init__(
        self,
        params,
        lr=0.001,
        b1=0.9,
        weight_decay=0.0,
        preconditioner_update_probability_schedule=True,
        max_size_triangular=8192,
        min_ndim_triangular=2,
        memory_save_mode=None,
        mu_dtype=None,
        precond_dtype=None,
        trust_region_scale=2.0,
        min_prob=0.03,
        max_prob=1.0,
        decay=0.001,
        flat_start=250,
        precond_lr=0.1,
        precond_init_scale=1.0,
    ):
        if not 0.0 <= lr:
            raise ValueError(f"Invalid learning rate: {lr}")
        if not 0.0 <= b1 < 1.0:
            raise ValueError(f"Invalid beta parameter: {b1}")
        if not 0.0 <= weight_decay:
            raise ValueError(f"Invalid weight_decay value: {weight_decay}")

        defaults = dict(
            lr=lr,
            b1=b1,
            weight_decay=weight_decay,
            max_size_triangular=max_size_triangular,
            min_ndim_triangular=min_ndim_triangular,
            memory_save_mode=memory_save_mode,
            precond_lr=precond_lr,
            precond_init_scale=precond_init_scale,
            mu_dtype=mu_dtype,
            precond_dtype=precond_dtype,
            trust_region_scale=trust_region_scale,
            preconditioner_update_probability_schedule=preconditioner_update_probability_schedule,

            # pickling for statedict is picky with what it will allow, only int, float, and tensor, no functions can be in state
            max_prob= max_prob,
            min_prob= min_prob,
            decay= decay,
            flat_start= flat_start,
        )
        super(Kron, self).__init__(params, defaults)

        self._tiny = torch.finfo(torch.bfloat16).tiny
        self._prob_step = 0
        self.expr_cache = {}

    def precond_update_prob_schedule(self, n,
        max_prob=1.0, min_prob=0.03, decay=0.001, flat_start=250
    ):
        """Anneal preconditioner update probability during beginning of training.

        PSGD benefits from more preconditioner updates at the beginning of training,
        but once the preconditioner is learned the update probability can drop low.

        This schedule is an exponential anneal with a flat start. Default settings keep
        update probability at 1.0 for 200 steps then exponentially anneal down to
        `min_prob` by 4000 steps. Default settings work very well for most models and
        training regimes.
        """

        """Exponential anneal with flat start."""
        n = torch.tensor(n, dtype=torch.float32)
        prob = torch.minimum(
            torch.maximum(
                max_prob * torch.exp(-decay * (n - flat_start)), torch.tensor(min_prob)
            ),
            torch.tensor(max_prob),
        )
        return prob
    
    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        total_momentum_size = 0
        total_momentum_mb = 0
        total_precond_size = 0
        total_precond_mb = 0

        # update preconditioners all together
        if self.param_groups[0]["preconditioner_update_probability_schedule"] is True:
            update_prob = self.precond_update_prob_schedule(self._prob_step, self.param_groups[0]["max_prob"], self.param_groups[0]["min_prob"], self.param_groups[0]["decay"], self.param_groups[0]["flat_start"])
        else:
            raise ValueError("Only True is supported for preconditioner_update_probability_schedule")
        device = self.param_groups[0]["params"][0].device
        do_update = torch.rand([], device=device) < update_prob
        self._prob_step += 1

        balance = torch.rand([], device=device) < 0.01 and do_update

        for group in self.param_groups:
            precond_dtype = group.get("precond_dtype", torch.float32)
            mu_dtype = group.get("mu_dtype")

            for p in group["params"]:
                if p.grad is None:
                    continue

                grad = p.grad
                state = self.state[p]

                if len(state) == 0:
                    state["step"] = 0
                    state["momentum_buffer"] = torch.zeros_like(
                        p, dtype=mu_dtype or p.dtype
                    )
                    q_state, exprs = init_Q_exprs(
                        p,
                        group["precond_init_scale"],
                        group["max_size_triangular"],
                        group["min_ndim_triangular"],
                        group["memory_save_mode"],
                        dtype=precond_dtype,
                    )
                    state["Q0"] = q_state[0]
                    state["Q1"] = q_state[1]
                    state["Q2"] = q_state[2]
                    state["Q3"] = q_state[3]
            
                    self.expr_cache[p._cdata] = exprs

                    # Print sizes
                    momentum_size = state["momentum_buffer"].numel()
                    momentum_mb = (
                        momentum_size
                        * state["momentum_buffer"].element_size()
                        / (2**20)
                    )
                    total_momentum_size += momentum_size
                    total_momentum_mb += momentum_mb

                    precond_size = sum(q.numel() for q in get_q(state))
                    precond_mb = sum(
                        q.numel() * q.element_size() for q in get_q(state)
                    ) / (2**20)
                    total_precond_size += precond_size
                    total_precond_mb += precond_mb

                state["step"] += 1

                # Update momentum buffer, elementwise so we can keep dtensor mode
                momentum_buffer = state["momentum_buffer"]
                momentum_buffer.mul_(group["b1"]).add_(grad, alpha=1 - group["b1"])
    
                # this time around, initializing the randn tensor and distributing it will not bode well, we would need to broadcast first
                # but this op is full of operations that fail with dtensor anyway and in-place bits so we'll do it all local anyway
                # we're likely better off just bringing everything local than just sharding back at the end
                # cant do max either
                momentum_buffer, mom_meta = to_local(momentum_buffer, keep_sharded=False)
                for i in range(4):
                    if is_tensor(state[f"Q{i}"]):
                        state[f"Q{i}"] = to_local(state[f"Q{i}"], keep_sharded=False)[0]

                # balance preconditioners about every 100 updates
                if grad.dim() > 1 and balance:
                    _balance_Q(get_q(state))

                # Update preconditioner
                if do_update:
                    update_precond(
                        get_q(state),
                        self.expr_cache[p._cdata],
                        torch.randn_like(momentum_buffer, dtype=precond_dtype),
                        momentum_buffer.to(dtype=precond_dtype, non_blocking=True),
                        group["precond_lr"],
                        self._tiny,
                    )

                # Precondition gradients
                pre_grad = _precond_grad(
                    get_q(state),
                    self.expr_cache[p._cdata],
                    momentum_buffer.to(dtype=precond_dtype, non_blocking=True),
                ).to(dtype=p.dtype, non_blocking=True)

                # now we can distribute again
                pre_grad = to_dist(pre_grad, 
                                **mom_meta
                                   )
                                   
                
                # Apply trust region
                pre_grad = (torch.tanh(pre_grad / group["trust_region_scale"]) * group["trust_region_scale"])

                for i in range(4):
                    if is_tensor(state[f"Q{i}"]):
                        state[f"Q{i}"] = to_dist(state[f"Q{i}"], 
                                                 **mom_meta
                                                 )
                state["momentum_buffer"] = to_dist(momentum_buffer, 
                                                   **mom_meta,
                                                   )

                # Apply weight decay and update parameters
                if group["weight_decay"] != 0 and p.dim() >= 2:
                    pre_grad.add_(p, alpha=group["weight_decay"])
                p.add_(pre_grad, alpha=-group["lr"])

                # Restore momentum dtype
                if mu_dtype is not None:
                    state["momentum_buffer"] = state["momentum_buffer"].to(dtype=mu_dtype, non_blocking=True)

        if total_momentum_size > 0:
            print(
                f"PSGD Momentum buffer size: {total_momentum_size} "
                f"elements, {total_momentum_mb:.2f} MB"
            )
            print(
                f"PSGD Preconditioners size: {total_precond_size} "
                f"elements, {total_precond_mb:.2f} MB"
            )

        return loss


def init_Q_exprs(t, scale, max_size, min_ndim_triangular, memory_save_mode, dtype=None):
    """For a scalar or tensor t, we initialize its preconditioner Q and
    reusable einsum expressions for updating Q and preconditioning gradient.
    """
    letters = string.ascii_lowercase + string.ascii_uppercase

    dtype = dtype if dtype is not None else t.dtype
    shape = t.shape
    if len(shape) == 0:  # scalar
        if isinstance(t, DTensor):
            Q = [distribute_tensor(scale * torch.ones_like(t.full_tensor(), dtype=dtype), device_mesh=t.device_mesh, placements=t.placements)]
        else:
            Q = [scale * torch.ones_like(t, dtype=dtype)]
        for i in range(3):
            Q.append(-2)
        exprA = ",->,"
        exprGs = [",->"]
        exprP = ",,->,"
    else:  # tensor
        if len(shape) > 13:
            raise ValueError(
                f"Got tensor with dim {len(t.shape)}; Einstein runs out of letters!"
            )

        scale = scale ** (1 / len(shape))

        if memory_save_mode is None:
            dim_diag = [False for _ in shape]
        elif memory_save_mode == "one_diag":
            rev_sorted_dims = np.argsort(shape)[::-1]
            dim_diag = [False for _ in shape]
            dim_diag[rev_sorted_dims[0]] = True
        elif memory_save_mode == "all_diag":
            dim_diag = [True for _ in shape]
        else:
            raise ValueError(
                f"Invalid memory_save_mode: {memory_save_mode}, must be one of "
                "[None, 'one_diag', 'all_diag']"
            )

        Q = []
        piece1A, piece2A, piece3A = ([], "", "")
        exprGs = []
        piece1P, piece2P, piece3P, piece4P = ([], [], "", "")
        for i, (size, dim_d) in enumerate(zip(shape, dim_diag)):
            if (
                size == 1
                or size > max_size
                or len(shape) < min_ndim_triangular
                or dim_d
            ):
                # use diagonal matrix as preconditioner for this dim
                tensor = scale * torch.ones(size, dtype=dtype, device=t.device)
                if isinstance(t, DTensor):
                    # again special case where we dont need to broadcast because init matrix is same on all devices
                    tensor = distribute_tensor(tensor, device_mesh=t.device_mesh, placements=t.placements)
                Q.append(tensor)

                piece1A.append(letters[i])
                piece2A = piece2A + letters[i]
                piece3A = piece3A + letters[i]

                piece1 = "".join(
                    [
                        (letters[i + 13] if j == i else letters[j])
                        for j in range(len(shape))
                    ]
                )
                subscripts = piece1 + "," + piece1 + "->" + letters[i + 13]
                exprGs.append(subscripts)

                piece1P.append(letters[i + 13])
                piece2P.append(letters[i + 13])
                piece3P = piece3P + letters[i + 13]
                piece4P = piece4P + letters[i + 13]
            else:
                # use triangular matrix as preconditioner for this dim
                tensor = scale * torch.eye(size, dtype=dtype, device=t.device)
                if isinstance(t, DTensor):
                    tensor = distribute_tensor(tensor, device_mesh=t.device_mesh, placements=t.placements)
                Q.append(tensor)

                piece1A.append(letters[i] + letters[i + 13])
                piece2A = piece2A + letters[i + 13]
                piece3A = piece3A + letters[i]

                piece1 = "".join(
                    [
                        (letters[i + 13] if j == i else letters[j])
                        for j in range(len(shape))
                    ]
                )
                piece2 = "".join(
                    [
                        (letters[i + 26] if j == i else letters[j])
                        for j in range(len(shape))
                    ]
                )
                subscripts = (
                    piece1 + "," + piece2 + "->" + letters[i + 13] + letters[i + 26]
                )
                exprGs.append(subscripts)

                a, b, c = (letters[i], letters[i + 13], letters[i + 26])
                piece1P.append(a + b)
                piece2P.append(a + c)
                piece3P = piece3P + c
                piece4P = piece4P + b
                
        while len(Q) < 4:
            Q.append(-2)
        exprA = ",".join(piece1A) + "," + piece2A + "->" + piece3A
        exprP = (
            ",".join(piece1P) + "," + ",".join(piece2P) + "," + piece3P + "->" + piece4P
        )

    exprGs = tuple(exprGs)
    return [Q, (exprA, exprGs, exprP)]


# @torch.compile(fullgraph=True)
def _balance_Q(Q_in):
    norms = torch.stack([torch.max(torch.abs(q)) for q in Q_in])
    geometric_mean = norms.prod() ** (1 / len(Q_in))
    for i, q in enumerate(Q_in):
        q.mul_(geometric_mean / norms[i])


def _lb(A, max_abs):
    A = A / max_abs
    aa = torch.real(A * A.conj())
    value0, i = torch.max(torch.sum(aa, dim=0), 0)
    value1, j = torch.max(torch.sum(aa, dim=1), 0)
    if value0 > value1:
        x = A[:, i].conj() @ A
        return max_abs * torch.linalg.vector_norm(
            (x / torch.linalg.vector_norm(x)) @ A.H
        )
    else:
        x = A @ A[j].conj()
        return max_abs * torch.linalg.vector_norm(
            A.H @ (x / torch.linalg.vector_norm(x))
        )


def _norm_lower_bound(A):
    """Cheap lower bound for the spectral norm of A."""
    max_abs = torch.max(torch.abs(A))
    return torch.where(max_abs > 0, _lb(A, max_abs), max_abs)


def _solve_triangular_right(X, A):
    """X @ inv(A)"""
    orig_dtype = X.dtype
    X = X.to(dtype=torch.float32, non_blocking=True)
    A = A.to(dtype=torch.float32, non_blocking=True)
    return torch.linalg.solve_triangular(A, X[None, :], upper=True, left=False).to(
        dtype=orig_dtype, non_blocking=True
    )[0]


# @torch.compile(fullgraph=True, dynamic=False)
def _calc_A_and_conjB(exprA, G, Q, V):
    A = torch.einsum(exprA, *Q, G)
    order = G.dim()
    p = list(range(order))
    conjB = torch.permute(V.conj(), p[1:] + p[:1])
    for i, q in enumerate(Q):
        conjB = conjB / q if q.dim() < 2 else _solve_triangular_right(conjB, q)
        if i < order - 1:
            conjB = torch.transpose(conjB, i, order - 1)
    return A, conjB


# @torch.compile(fullgraph=True, dynamic=False)
def _q_terms(exprGs, A, conjB):
    terms = []
    for exprG in exprGs:
        term1 = torch.einsum(exprG, A, A.conj())
        term2 = torch.einsum(exprG, conjB.conj(), conjB)
        terms.append((term1, term2))
    return terms


def update_precond(Q, exprs, V, G, step, tiny):
    """Update Kronecker product preconditioner Q with pair (V, G)."""
    exprA, exprGs, _ = exprs

    A, conjB = _calc_A_and_conjB(exprA, G, Q, V)

    terms = _q_terms(exprGs, A, conjB)

    for q, (term1, term2) in zip(Q, terms):
        if q.dim() < 2:
            q.sub_(
                step
                / (torch.max(torch.abs(term1 + term2)) + tiny)
                * (term1 - term2)
                * q
            )
        else:
            q.sub_(
                step
                / (_norm_lower_bound(term1 + term2) + tiny)
                * torch.triu(term1 - term2)
                @ q
            )

    


# @torch.compile(fullgraph=True, dynamic=False)
def _precond_grad(Q, exprs, G):
    """Precondition gradient G with preconditioner Q."""
    return torch.einsum(exprs[-1], *[q.conj() for q in Q], *Q, G)
