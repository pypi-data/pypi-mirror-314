import numpy
import funcnodes as fn
from typing import Literal, Sequence, Optional, Union
from exposedfunctionality import controlled_wrapper as wraps

from .._types import (
    ndarray,
    array_like,
    axis_like,
    ndarray_or_scalar,
)


@fn.NodeDecorator(
    node_id="np.multi_dot",
    name="multi_dot",
    outputs=[{"name": "output", "type": "ndarray"}],
)
@wraps(numpy.linalg.multi_dot, wrapper_attribute="__fnwrapped__")
def multi_dot(
    arrays: Sequence[array_like],
    out: Optional[ndarray] = None,
):  # params ['arrays'] ['out'] []
    res = numpy.linalg.multi_dot(
        arrays=arrays,
        out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.matrix_power",
    name="matrix_power",
    outputs=[{"name": "an", "type": "ndarray"}],
)
@wraps(numpy.linalg.matrix_power, wrapper_attribute="__fnwrapped__")
def matrix_power(
    a: array_like,
    n: int,
):  # params ['a', 'n'] [] []
    res = numpy.linalg.matrix_power(
        a=a,
        n=n,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cholesky",
    name="cholesky",
    outputs=[{"name": "L", "type": "ndarray"}],
)
@wraps(numpy.linalg.cholesky, wrapper_attribute="__fnwrapped__")
def cholesky(
    a: array_like,
):  # params ['a'] [] []
    res = numpy.linalg.cholesky(
        a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.qr",
    name="qr",
    outputs=[
        {
            "name": "Q",
            "type": "Optional[ndarray]",
            "description": "A matrix with orthonormal columns. When mode = 'complete' the result is an "
            "orthogonal/unitary matrix depending on whether or not a is real/complex. "
            "The determinant may be either +/- 1 in that case. In case the number of dimensions in the "
            "input array is greater than 2 then a stack of the matrices with above properties is returned.",
        },
        {
            "name": "R",
            "type": "Optional[ndarray]",
            "description": "The upper-triangular matrix or a stack of upper-triangular matrices if the "
            "number of dimensions in the input array is greater than 2",
        },
        {
            "name": "(h,tau)",
            "type": "Optional[Tuple[ndarray, ndarray]]",
            "description": "The array h contains the Householder reflectors that generate q along with r. "
            "The tau array contains scaling factors for the reflectors. "
            "In the deprecated 'economic' mode only h is returned.",
        },
    ],
)
@wraps(numpy.linalg.qr, wrapper_attribute="__fnwrapped__")
def qr(
    a: array_like,
    mode: Literal["reduced", "complete", "r", "raw"] = "reduced",
):  # params ['a'] ['mode'] []
    res = numpy.linalg.qr(
        a=a,
        mode=mode,
    )
    return res


@fn.NodeDecorator(
    node_id="np.svd",
    name="svd",
    outputs=[
        {
            "name": "U",
            "type": "ndarray",
            "description": "Unitary array(s). The first a.ndim - 2 dimensions have the same size as those of "
            "the input a. The size of the last two dimensions depends on the value of full_matrices. "
            "Only returned when compute_uv is True.",
        },
        {
            "name": "S",
            "type": "ndarray",
            "description": "Vector(s) with the singular values, within each vector sorted in descending order. "
            "The first a.ndim - 2 dimensions have the same size as those of the input a.",
        },
        {
            "name": "Vh",
            "type": "ndarray",
            "description": "Unitary array(s). The first a.ndim - 2 dimensions have the same size as those of the "
            "input a. The size of the last two dimensions depends on the value of full_matrices. "
            "Only returned when compute_uv is True.",
        },
    ],
)
@wraps(numpy.linalg.svd, wrapper_attribute="__fnwrapped__")
def svd(
    a: array_like,
    full_matrices: bool = True,
    # compute_uv: bool = True, # always True for consitent output
    hermitian: bool = False,
):  # params ['a'] ['full_matrices', 'compute_uv'] []
    res = numpy.linalg.svd(
        a=a,
        full_matrices=full_matrices,
        compute_uv=True,
        hermitian=hermitian,
    )
    return res


@fn.NodeDecorator(
    node_id="np.eig",
    name="eig",
    outputs=[
        {"name": "eigenvalues", "type": "ndarray"},
        {"name": "eigenvectors", "type": "ndarray"},
    ],
)
@wraps(numpy.linalg.eig, wrapper_attribute="__fnwrapped__")
def eig(
    a: ndarray,
):  # params ['a'] [] []
    res = numpy.linalg.eig(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.eigh",
    name="eigh",
    outputs=[
        {"name": "eigenvalues", "type": "ndarray"},
        {"name": "eigenvectors", "type": "ndarray"},
    ],
)
@wraps(numpy.linalg.eigh, wrapper_attribute="__fnwrapped__")
def eigh(a: ndarray, UPLO: Literal["L", "U"] = "L"):  # params ['a'] ['UPLO'] []
    res = numpy.linalg.eigh(
        a=a,
        UPLO=UPLO,
    )
    return res


@fn.NodeDecorator(
    node_id="np.eigvals",
    name="eigvals",
    outputs=[{"name": "w", "type": "ndarray"}],
)
@wraps(numpy.linalg.eigvals, wrapper_attribute="__fnwrapped__")
def eigvals(
    a: array_like,
):  # params ['a'] [] []
    res = numpy.linalg.eigvals(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.eigvalsh",
    name="eigvalsh",
    outputs=[{"name": "w", "type": "ndarray"}],
)
@wraps(numpy.linalg.eigvalsh, wrapper_attribute="__fnwrapped__")
def eigvalsh(
    a: array_like,
    UPLO: Literal["L", "U"] = "L",
):  # params ['a'] ['UPLO'] []
    res = numpy.linalg.eigvalsh(
        a=a,
        UPLO=UPLO,
    )
    return res


@fn.NodeDecorator(
    node_id="np.norm",
    name="norm",
    outputs=[{"name": "n", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.linalg.norm, wrapper_attribute="__fnwrapped__")
def norm(
    x: array_like,
    ord: float | Literal["fro", "nuc"] | None = None,
    axis: Optional[axis_like] = None,
    keepdims: bool = False,
):  # params ['x'] ['ord', 'axis', 'keepdims'] []
    res = numpy.linalg.norm(
        x=x,
        ord=ord,
        axis=axis,
        keepdims=keepdims,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cond",
    name="cond",
    outputs=[{"name": "c", "type": "float"}],
)
@wraps(numpy.linalg.cond, wrapper_attribute="__fnwrapped__")
def cond(
    x: array_like,
    p: float | Literal["fro", "nuc"] | None = None,
):  # params ['x'] ['p'] []
    res = numpy.linalg.cond(
        x=x,
        p=p,
    )
    return res


@fn.NodeDecorator(
    node_id="np.det",
    name="det",
    outputs=[{"name": "det", "type": "array_like"}],
)
@wraps(numpy.linalg.det, wrapper_attribute="__fnwrapped__")
def det(
    a: array_like,
):  # params ['a'] [] []
    res = numpy.linalg.det(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.matrix_rank",
    name="matrix_rank",
    outputs=[{"name": "rank", "type": "array_like"}],
)
@wraps(numpy.linalg.matrix_rank, wrapper_attribute="__fnwrapped__")
def matrix_rank(
    A: array_like,
    tol: Union[float, array_like, None] = None,
    hermitian: bool = False,
):  # params ['A'] ['tol', 'hermitian'] []
    res = numpy.linalg.matrix_rank(
        A=A,
        tol=tol,
        hermitian=hermitian,
    )
    return res


@fn.NodeDecorator(
    node_id="np.slogdet",
    name="slogdet",
    outputs=[
        {"name": "sign", "type": "array_like"},
        {"name": "logabsdet", "type": "array_like"},
    ],
)
@wraps(numpy.linalg.slogdet, wrapper_attribute="__fnwrapped__")
def slogdet(
    a: array_like,
):  # params ['a'] [] []
    res = numpy.linalg.slogdet(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.solve",
    name="solve",
    outputs=[{"name": "x", "type": "ndarray"}],
)
@wraps(numpy.linalg.solve, wrapper_attribute="__fnwrapped__")
def solve(
    a: ndarray,
    b: ndarray,
):  # params ['a', 'b'] [] []
    res = numpy.linalg.solve(
        a=a,
        b=b,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tensorsolve",
    name="tensorsolve",
    outputs=[{"name": "x", "type": "ndarray"}],
)
@wraps(numpy.linalg.tensorsolve, wrapper_attribute="__fnwrapped__")
def tensorsolve(
    a: array_like,
    b: array_like,
    axes: Optional[axis_like] = None,
):  # params ['a', 'b'] ['axes'] []
    res = numpy.linalg.tensorsolve(
        a=a,
        b=b,
        axes=axes,
    )
    return res


@fn.NodeDecorator(
    node_id="np.lstsq",
    name="lstsq",
    outputs=[
        {"name": "x", "type": "ndarray"},
        {"name": "residuals", "type": "ndarray"},
        {"name": "rank", "type": "int"},
        {"name": "s", "type": "ndarray"},
    ],
)
@wraps(numpy.linalg.lstsq, wrapper_attribute="__fnwrapped__")
def lstsq(
    a: array_like,
    b: array_like,
    rcond: Optional[float] = None,
):  # params ['a', 'b'] ['rcond'] []
    res = numpy.linalg.lstsq(
        a=a,
        b=b,
        rcond=rcond,
    )
    return res


@fn.NodeDecorator(
    node_id="np.inv",
    name="inv",
    outputs=[{"name": "ainv", "type": "ndarray"}],
)
@wraps(numpy.linalg.inv, wrapper_attribute="__fnwrapped__")
def inv(
    a: array_like,
):  # params ['a'] [] []
    res = numpy.linalg.inv(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.pinv",
    name="pinv",
    outputs=[{"name": "B", "type": "ndarray"}],
)
@wraps(numpy.linalg.pinv, wrapper_attribute="__fnwrapped__")
def pinv(
    a: array_like,
    rcond: ndarray_or_scalar = 1e-15,
    hermitian: bool = False,
):  # params ['a'] ['rcond', 'hermitian'] []
    res = numpy.linalg.pinv(
        a=a,
        rcond=rcond,
        hermitian=hermitian,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tensorinv",
    name="tensorinv",
    outputs=[{"name": "b", "type": "ndarray"}],
)
@wraps(numpy.linalg.tensorinv, wrapper_attribute="__fnwrapped__")
def tensorinv(
    a: array_like,
    ind: int = 2,
):  # params ['a'] ['ind'] []
    res = numpy.linalg.tensorinv(
        a=a,
        ind=ind,
    )
    return res


NODE_SHELF = fn.Shelf(
    name="linalg",
    nodes=[
        multi_dot,
        matrix_power,
        cholesky,
        qr,
        svd,
        eig,
        eigh,
        eigvals,
        eigvalsh,
        norm,
        cond,
        det,
        matrix_rank,
        slogdet,
        solve,
        tensorsolve,
        lstsq,
        inv,
        pinv,
        tensorinv,
    ],
    subshelves=[],
    description="numpy.linalg functionalities for FuncNodes",
)
