import numpy
from typing import Optional
from exposedfunctionality import controlled_wrapper as wraps
import funcnodes as fn
from .._types import (
    array_like,
    real_array,
    int_bool_array,
    int_array,
    ndarray_or_scalar,
    int_or_int_array,
)
from funcnodes_numpy._version import np_version
from .._dtypes import dtype_from_name, DTYPE_ENUM


@fn.NodeDecorator(
    node_id="np.absolute",
    name="absolute",
    outputs=[{"name": "absolute", "type": "ndarray"}],
)
@wraps(numpy.absolute, wrapper_attribute="__fnwrapped__")
def absolute(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.absolute(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.add",
    name="add",
    outputs=[{"name": "add", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.add, wrapper_attribute="__fnwrapped__")
def add(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting', 'order'] []
    res = numpy.add(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.arccos",
    name="arccos",
    outputs=[{"name": "angle", "type": "ndarray"}],
)
@wraps(numpy.arccos, wrapper_attribute="__fnwrapped__")
def arccos(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.arccos(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.arccosh",
    name="arccosh",
    outputs=[{"name": "arccosh", "type": "ndarray"}],
)
@wraps(numpy.arccosh, wrapper_attribute="__fnwrapped__")
def arccosh(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.arccosh(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.arcsin",
    name="arcsin",
    outputs=[{"name": "angle", "type": "ndarray"}],
)
@wraps(numpy.arcsin, wrapper_attribute="__fnwrapped__")
def arcsin(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.arcsin(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.arcsinh",
    name="arcsinh",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.arcsinh, wrapper_attribute="__fnwrapped__")
def arcsinh(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.arcsinh(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.arctan",
    name="arctan",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.arctan, wrapper_attribute="__fnwrapped__")
def arctan(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.arctan(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.arctan2",
    name="arctan2",
    outputs=[{"name": "angle", "type": "ndarray"}],
)
@wraps(numpy.arctan2, wrapper_attribute="__fnwrapped__")
def arctan2(
    x1: real_array,
    x2: real_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.arctan2(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.arctanh",
    name="arctanh",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.arctanh, wrapper_attribute="__fnwrapped__")
def arctanh(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.arctanh(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.bitwise_and",
    name="bitwise_and",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.bitwise_and, wrapper_attribute="__fnwrapped__")
def bitwise_and(
    x1: int_bool_array,
    x2: int_bool_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.bitwise_and(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


if np_version["major_int"] >= 2:

    @fn.NodeDecorator(
        node_id="np.bitwise_count",
        name="bitwise_count",
        outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
    )
    @wraps(numpy.bitwise_count, wrapper_attribute="__fnwrapped__")
    def bitwise_count(
        x: int_bool_array,
        # out: Optional[ndarray] = None,
        # where: Union[bool_array, bool] = True,
        # casting: casting_literal = "same_kind",
        # order: OrderKACF = "K",
        # dtype: Optional[DTYPE_ENUM] = None,
        # subok: bool = True,
        # signature: Any = None,
        # extobj: Any = None,
    ):
        return numpy.bitwise_count(x)


@fn.NodeDecorator(
    node_id="np.bitwise_or",
    name="bitwise_or",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.bitwise_or, wrapper_attribute="__fnwrapped__")
def bitwise_or(
    x1: int_bool_array,
    x2: int_bool_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.bitwise_or(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.bitwise_xor",
    name="bitwise_xor",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.bitwise_xor, wrapper_attribute="__fnwrapped__")
def bitwise_xor(
    x1: int_bool_array,
    x2: int_bool_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.bitwise_xor(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cbrt",
    name="cbrt",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.cbrt, wrapper_attribute="__fnwrapped__")
def cbrt(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.cbrt(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ceil",
    name="ceil",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.ceil, wrapper_attribute="__fnwrapped__")
def ceil(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.ceil(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.conj",
    name="conj",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.conj, wrapper_attribute="__fnwrapped__")
def conj(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.conj(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.conjugate",
    name="conjugate",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.conjugate, wrapper_attribute="__fnwrapped__")
def conjugate(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting'] []
    res = numpy.conjugate(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.copysign",
    name="copysign",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.copysign, wrapper_attribute="__fnwrapped__")
def copysign(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.copysign(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cos",
    name="cos",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.cos, wrapper_attribute="__fnwrapped__")
def cos(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.cos(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cosh",
    name="cosh",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.cosh, wrapper_attribute="__fnwrapped__")
def cosh(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.cosh(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.deg2rad",
    name="deg2rad",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.deg2rad, wrapper_attribute="__fnwrapped__")
def deg2rad(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.deg2rad(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.degrees",
    name="degrees",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.degrees, wrapper_attribute="__fnwrapped__")
def degrees(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.degrees(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.divide",
    name="divide",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.divide, wrapper_attribute="__fnwrapped__")
def divide(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.divide(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.divmod",
    name="divmod",
    outputs=[{"name": "out1", "type": "ndarray"}, {"name": "out2", "type": "ndarray"}],
)
@wraps(numpy.divmod, wrapper_attribute="__fnwrapped__")
def divmod(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # out1: Optional[ndarray] = None,
    # out2: Optional[ndarray] = None,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out'] ['out1', 'out2']
    res = numpy.divmod(
        x1,
        x2,
        # out=out,
        # where=where,
        # out1=out1,
        # out2=out2,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.equal",
    name="equal",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.equal, wrapper_attribute="__fnwrapped__")
def equal(
    x1: ndarray_or_scalar,
    x2: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):
    return numpy.equal(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
    )


@fn.NodeDecorator(
    node_id="np.e",
    name="e",
    outputs=[{"name": "e", "type": float}],
)
def e() -> float:
    """
    Returns the base of the natural logarithm, e.
    """
    return numpy.e


@fn.NodeDecorator(
    node_id="np.euler_gamma",
    name="euler_gamma",
    outputs=[{"name": "γ", "type": float}],
)
def euler_gamma() -> float:
    """
    Returns the Euler-Mascheroni constant, γ.
    """
    return numpy.euler_gamma


@fn.NodeDecorator(
    node_id="np.exp",
    name="exp",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.exp, wrapper_attribute="__fnwrapped__")
def exp(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.exp(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.exp2",
    name="exp2",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.exp2, wrapper_attribute="__fnwrapped__")
def exp2(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.exp2(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.expm1",
    name="expm1",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.expm1, wrapper_attribute="__fnwrapped__")
def expm1(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.expm1(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fabs",
    name="fabs",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.fabs, wrapper_attribute="__fnwrapped__")
def fabs(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.fabs(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.floor",
    name="floor",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.floor, wrapper_attribute="__fnwrapped__")
def floor(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.floor(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.floor_divide",
    name="floor_divide",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.floor_divide, wrapper_attribute="__fnwrapped__")
def floor_divide(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.floor_divide(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.float_power",
    name="float_power",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.float_power, wrapper_attribute="__fnwrapped__")
def float_power(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.float_power(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fmax",
    name="fmax",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.fmax, wrapper_attribute="__fnwrapped__")
def fmax(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.fmax(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fmin",
    name="fmin",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.fmin, wrapper_attribute="__fnwrapped__")
def fmin(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.fmin(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fmod",
    name="fmod",
    outputs=[{"name": "y", "type": "array_like"}],
)
@wraps(numpy.fmod, wrapper_attribute="__fnwrapped__")
def fmod(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.fmod(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.frexp",
    name="frexp",
    outputs=[
        {"name": "mantissa", "type": "ndarray"},
        {"name": "exponent", "type": "ndarray"},
    ],
)
@wraps(numpy.frexp, wrapper_attribute="__fnwrapped__")
def frexp(
    x: array_like,
    # out1: Union[ndarray, None],
    # out2: Union[ndarray, None],
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):
    res = numpy.frexp(
        x,
        # out1,
        # out2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


# @fn.NodeDecorator(
#     node_id="np.frompyfunc",
#     name="frompyfunc",
#     outputs=[{"name": "ufunc", "type": "Ufunc"}],
# )
# @wraps(numpy.frompyfunc, wrapper_attribute="__fnwrapped__")
# def frompyfunc(
#     func: Callable,
#     nin: int,
#     nout: int,
# ):
#     res = numpy.frompyfunc(
#         func,
#         nin=nin,
#         nout=nout,
#     )
#     return res


@fn.NodeDecorator(
    node_id="np.gcd",
    name="gcd",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.gcd, wrapper_attribute="__fnwrapped__")
def gcd(
    x1: int_array,
    x2: int_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting', 'order'] []
    res = numpy.gcd(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.greater",
    name="greater",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.greater, wrapper_attribute="__fnwrapped__")
def greater(
    x1: ndarray_or_scalar,
    x2: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):
    return numpy.greater(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
    )


@fn.NodeDecorator(
    node_id="np.greater_equal",
    name="greater_equal",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.greater_equal, wrapper_attribute="__fnwrapped__")
def greater_equal(
    x1: ndarray_or_scalar,
    x2: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):
    return numpy.greater_equal(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
    )


@fn.NodeDecorator(
    node_id="np.heaviside",
    name="heaviside",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.heaviside, wrapper_attribute="__fnwrapped__")
def heaviside(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.heaviside(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.hypot",
    name="hypot",
    outputs=[{"name": "z", "type": "ndarray"}],
)
@wraps(numpy.hypot, wrapper_attribute="__fnwrapped__")
def hypot(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.hypot(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.invert",
    name="invert",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.invert, wrapper_attribute="__fnwrapped__")
def invert(
    x: int_bool_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.invert(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isfinite",
    name="isfinite",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.isfinite, wrapper_attribute="__fnwrapped__")
def isfinite(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.isfinite(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isinf",
    name="isinf",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.isinf, wrapper_attribute="__fnwrapped__")
def isinf(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.isinf(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isnan",
    name="isnan",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.isnan, wrapper_attribute="__fnwrapped__")
def isnan(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.isnan(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isnat",
    name="isnat",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.isnat, wrapper_attribute="__fnwrapped__")
def isnat(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.isnat(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.lcm",
    name="lcm",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.lcm, wrapper_attribute="__fnwrapped__")
def lcm(
    x1: int_array,
    x2: int_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting', 'order'] []
    res = numpy.lcm(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ldexp",
    name="ldexp",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.ldexp, wrapper_attribute="__fnwrapped__")
def ldexp(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.ldexp(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.left_shift",
    name="left_shift",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.left_shift, wrapper_attribute="__fnwrapped__")
def left_shift(
    x1: int_or_int_array,
    x2: int_or_int_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.left_shift(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.less",
    name="less",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.less, wrapper_attribute="__fnwrapped__")
def less(
    x1: ndarray_or_scalar,
    x2: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):
    return numpy.less(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
    )


@fn.NodeDecorator(
    node_id="np.less_equal",
    name="less_equal",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.less_equal, wrapper_attribute="__fnwrapped__")
def less_equal(
    x1: ndarray_or_scalar,
    x2: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):
    return numpy.less_equal(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
    )


@fn.NodeDecorator(
    node_id="np.log",
    name="log",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.log, wrapper_attribute="__fnwrapped__")
def log(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.log(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.log10",
    name="log10",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.log10, wrapper_attribute="__fnwrapped__")
def log10(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.log10(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.log1p",
    name="log1p",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.log1p, wrapper_attribute="__fnwrapped__")
def log1p(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.log1p(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.log2",
    name="log2",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.log2, wrapper_attribute="__fnwrapped__")
def log2(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.log2(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.logaddexp",
    name="logaddexp",
    outputs=[{"name": "result", "type": "ndarray"}],
)
@wraps(numpy.logaddexp, wrapper_attribute="__fnwrapped__")
def logaddexp(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.logaddexp(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.logaddexp2",
    name="logaddexp2",
    outputs=[{"name": "result", "type": "ndarray"}],
)
@wraps(numpy.logaddexp2, wrapper_attribute="__fnwrapped__")
def logaddexp2(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.logaddexp2(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.logical_and",
    name="logical_and",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.logical_and, wrapper_attribute="__fnwrapped__")
def logical_and(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.logical_and(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.logical_not",
    name="logical_not",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.logical_not, wrapper_attribute="__fnwrapped__")
def logical_not(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting'] []
    res = numpy.logical_not(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.logical_or",
    name="logical_or",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.logical_or, wrapper_attribute="__fnwrapped__")
def logical_or(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.logical_or(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.logical_xor",
    name="logical_xor",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.logical_xor, wrapper_attribute="__fnwrapped__")
def logical_xor(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.logical_xor(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.maximum",
    name="maximum",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.maximum, wrapper_attribute="__fnwrapped__")
def maximum(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.maximum(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.minimum",
    name="minimum",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.minimum, wrapper_attribute="__fnwrapped__")
def minimum(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.minimum(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.mod",
    name="mod",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.mod, wrapper_attribute="__fnwrapped__")
def mod(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting', 'order'] []
    res = numpy.mod(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.modf",
    name="modf",
    outputs=[{"name": "y1", "type": "ndarray"}, {"name": "y2", "type": "ndarray"}],
)
@wraps(numpy.modf, wrapper_attribute="__fnwrapped__")
def modf(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # out1: Optional[ndarray] = None,
    # out2: Optional[ndarray] = None,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out'] ['out1', 'out2']
    res = numpy.modf(
        x,
        # out=out,
        # where=where,
        # out1,
        # out2,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.multiply",
    name="multiply",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.multiply, wrapper_attribute="__fnwrapped__")
def multiply(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.multiply(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.negative",
    name="negative",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.negative, wrapper_attribute="__fnwrapped__")
def negative(
    x: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.negative(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nextafter",
    name="nextafter",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.nextafter, wrapper_attribute="__fnwrapped__")
def nextafter(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.nextafter(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.not_equal",
    name="not_equal",
    outputs=[{"name": "y", "type": "bool_or_bool_array"}],
)
@wraps(numpy.not_equal, wrapper_attribute="__fnwrapped__")
def not_equal(
    x1: ndarray_or_scalar,
    x2: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):
    return numpy.not_equal(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
    )


@fn.NodeDecorator(
    node_id="np.pi",
    name="pi",
    outputs=[{"name": "π", "type": float}],
)
def pi() -> float:
    """
    Returns the constant π.
    """
    return numpy.pi


@fn.NodeDecorator(
    node_id="np.positive",
    name="positive",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.positive, wrapper_attribute="__fnwrapped__")
def positive(
    x: ndarray_or_scalar,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.positive(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.power",
    name="power",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.power, wrapper_attribute="__fnwrapped__")
def power(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.power(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.rad2deg",
    name="rad2deg",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.rad2deg, wrapper_attribute="__fnwrapped__")
def rad2deg(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.rad2deg(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.radians",
    name="radians",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.radians, wrapper_attribute="__fnwrapped__")
def radians(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.radians(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.reciprocal",
    name="reciprocal",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.reciprocal, wrapper_attribute="__fnwrapped__")
def reciprocal(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting'] []
    res = numpy.reciprocal(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.remainder",
    name="remainder",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.remainder, wrapper_attribute="__fnwrapped__")
def remainder(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.remainder(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.right_shift",
    name="right_shift",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.right_shift, wrapper_attribute="__fnwrapped__")
def right_shift(
    x1: int_or_int_array,
    x2: int_or_int_array,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.right_shift(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.rint",
    name="rint",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.rint, wrapper_attribute="__fnwrapped__")
def rint(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.rint(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.sign",
    name="sign",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.sign, wrapper_attribute="__fnwrapped__")
def sign(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.sign(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.signbit",
    name="signbit",
    outputs=[{"name": "result", "type": "ndarray"}],
)
@wraps(numpy.signbit, wrapper_attribute="__fnwrapped__")
def signbit(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.signbit(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.sin",
    name="sin",
    outputs=[{"name": "y", "type": "array_like"}],
)
@wraps(numpy.sin, wrapper_attribute="__fnwrapped__")
def sin(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.sin(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.sinh",
    name="sinh",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.sinh, wrapper_attribute="__fnwrapped__")
def sinh(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.sinh(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.spacing",
    name="spacing",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.spacing, wrapper_attribute="__fnwrapped__")
def spacing(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.spacing(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.sqrt",
    name="sqrt",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.sqrt, wrapper_attribute="__fnwrapped__")
def sqrt(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.sqrt(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.square",
    name="square",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.square, wrapper_attribute="__fnwrapped__")
def square(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.square(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.subtract",
    name="subtract",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.subtract, wrapper_attribute="__fnwrapped__")
def subtract(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where', 'casting'] []
    res = numpy.subtract(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tan",
    name="tan",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.tan, wrapper_attribute="__fnwrapped__")
def tan(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.tan(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tanh",
    name="tanh",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.tanh, wrapper_attribute="__fnwrapped__")
def tanh(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.tanh(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.true_divide",
    name="true_divide",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.true_divide, wrapper_attribute="__fnwrapped__")
def true_divide(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'where'] []
    res = numpy.true_divide(
        x1,
        x2,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.trunc",
    name="trunc",
    outputs=[{"name": "y", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.trunc, wrapper_attribute="__fnwrapped__")
def trunc(
    x: array_like,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x'] ['out', 'where', 'casting', 'order'] []
    res = numpy.trunc(
        x,
        # out=out,
        # where=where,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


def get_numpy_ufucs():
    from numpy._core import umath

    all_funcs = umath.__all__
    all_funcs = [
        func for func in all_funcs if not func.isupper() and not func.startswith("_")
    ]

    for i in ["geterrobj", "frompyfunc", "seterrobj"]:
        if i in all_funcs:
            all_funcs.remove(i)
    return all_funcs


if np_version["major_int"] >= 2 and np_version["minor_int"] >= 2:

    @fn.NodeDecorator(
        node_id="np.matvec",
        name="matvec",
        outputs=[{"name": "y", "type": "ndarray"}],
    )
    @wraps(numpy.matvec, wrapper_attribute="__fnwrapped__")
    def matvec(
        x1: array_like,
        x2: array_like,
        # out: Optional[ndarray] = None,
        # where: Union[bool_array, bool] = True,
        # casting: casting_literal = "same_kind",
        # order: OrderKACF = "K",
        dtype: Optional[DTYPE_ENUM] = None,
        # subok: bool = True,
        # signature: Any = None,
        # extobj: Any = None,
    ):
        return numpy.matvec(
            x1,
            x2,
            # out=out,
            # where=where,
            # casting=casting,
            # order=order,
            dtype=dtype_from_name(dtype),
            # subok=subok,
            # signature=signature,
            # extobj=extobj,
        )

    @fn.NodeDecorator(
        node_id="np.vecdot",
        name="vecdot",
        outputs=[{"name": "y", "type": "ndarray"}],
    )
    @wraps(numpy.vecdot, wrapper_attribute="__fnwrapped__")
    def vecdot(
        x1: array_like,
        x2: array_like,
        # out: Optional[ndarray] = None,
        # where: Union[bool_array, bool] = True,
        # casting: casting_literal = "same_kind",
        # order: OrderKACF = "K",
        dtype: Optional[DTYPE_ENUM] = None,
        # subok: bool = True,
        # signature: Any = None,
        # extobj: Any = None,
    ):
        return numpy.vecdot(
            x1,
            x2,
            # out=out,
            # where=where,
            # casting=casting,
            # order=order,
            dtype=dtype_from_name(dtype),
            # subok=subok,
            # signature=signature,
            # extobj=extobj,
        )

    @fn.NodeDecorator(
        node_id="np.vecmat",
        name="vecmat",
        outputs=[{"name": "y", "type": "ndarray"}],
    )
    @wraps(numpy.vecmat, wrapper_attribute="__fnwrapped__")
    def vecmat(
        x1: array_like,
        x2: array_like,
        # out: Optional[ndarray] = None,
        # where: Union[bool_array, bool] = True,
        # casting: casting_literal = "same_kind",
        # order: OrderKACF = "K",
        dtype: Optional[DTYPE_ENUM] = None,
        # subok: bool = True,
        # signature: Any = None,
        # extobj: Any = None,
    ):
        return numpy.vecmat(
            x1,
            x2,
            # out=out,
            # where=where,
            # casting=casting,
            # order=order,
            dtype=dtype_from_name(dtype),
            # subok=subok,
            # signature=signature,
            # extobj=extobj,
        )


NODE_SHELF = fn.Shelf(
    name="numpy_ufuncs",
    description="numpy ufuncs",
    nodes=[
        absolute,
        add,
        arccos,
        arccosh,
        arcsin,
        arcsinh,
        arctan,
        arctan2,
        arctanh,
        bitwise_and,
        bitwise_or,
        bitwise_xor,
        cbrt,
        ceil,
        conj,
        conjugate,
        copysign,
        cos,
        cosh,
        deg2rad,
        degrees,
        divide,
        divmod,
        e,
        equal,
        euler_gamma,
        exp,
        exp2,
        expm1,
        fabs,
        floor,
        floor_divide,
        float_power,
        fmax,
        fmin,
        fmod,
        frexp,
        gcd,
        greater,
        greater_equal,
        heaviside,
        hypot,
        invert,
        isfinite,
        isinf,
        isnan,
        isnat,
        lcm,
        ldexp,
        left_shift,
        less,
        less_equal,
        log,
        log10,
        log1p,
        log2,
        logaddexp,
        logaddexp2,
        logical_and,
        logical_not,
        logical_or,
        logical_xor,
        maximum,
        minimum,
        mod,
        modf,
        multiply,
        negative,
        nextafter,
        not_equal,
        pi,
        positive,
        power,
        rad2deg,
        radians,
        reciprocal,
        remainder,
        right_shift,
        rint,
        sign,
        signbit,
        sin,
        sinh,
        spacing,
        sqrt,
        square,
        subtract,
        tan,
        tanh,
        true_divide,
        trunc,
    ]
    + ([bitwise_count] if np_version["major_int"] >= 2 else [])
    + (
        [matvec, vecdot, vecmat]
        if np_version["major_int"] >= 2 and np_version["minor_int"] >= 2
        else []
    ),
    subshelves=[],
)
