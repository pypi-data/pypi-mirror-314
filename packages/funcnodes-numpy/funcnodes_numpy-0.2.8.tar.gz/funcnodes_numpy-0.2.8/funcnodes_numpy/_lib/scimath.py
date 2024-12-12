import numpy
from .._types import ndarray_or_scalar
from exposedfunctionality import controlled_wrapper as wraps
import funcnodes as fn


@fn.NodeDecorator(
    node_id="np.emath.sqrt",
    name="sqrt",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.sqrt, wrapper_attribute="__fnwrapped__")
def sqrt(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.sqrt(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.log",
    name="log",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.log, wrapper_attribute="__fnwrapped__")
def log(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.log(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.log2",
    name="log2",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.log2, wrapper_attribute="__fnwrapped__")
def log2(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.log2(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.logn",
    name="logn",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.logn, wrapper_attribute="__fnwrapped__")
def logn(
    n: int,
    x: ndarray_or_scalar,
):  # params ['n', 'x'] [] []
    res = numpy.emath.logn(
        n=n,
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.log10",
    name="log10",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.log10, wrapper_attribute="__fnwrapped__")
def log10(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.log10(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.power",
    name="power",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.power, wrapper_attribute="__fnwrapped__")
def power(
    x: ndarray_or_scalar,
    p: ndarray_or_scalar,
):  # params ['x', 'p'] [] []
    res = numpy.emath.power(
        x=x,
        p=p,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.arccos",
    name="arccos",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.arccos, wrapper_attribute="__fnwrapped__")
def arccos(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.arccos(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.arcsin",
    name="arcsin",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.arcsin, wrapper_attribute="__fnwrapped__")
def arcsin(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.arcsin(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.arctanh",
    name="arctanh",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.arctanh, wrapper_attribute="__fnwrapped__")
def arctanh(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.arctanh(
        x=x,
    )
    return res


NODE_SHELF = fn.Shelf(
    name="emath",
    nodes=[
        sqrt,
        log,
        log2,
        logn,
        log10,
        power,
        arccos,
        arcsin,
        arctanh,
    ],
    subshelves=[],
    description="emath functionalities for FuncNodes",
)
