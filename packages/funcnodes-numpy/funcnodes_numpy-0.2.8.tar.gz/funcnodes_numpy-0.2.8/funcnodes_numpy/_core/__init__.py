import funcnodes as fn
from typing import Union, List, Optional, Iterable, Tuple, Sequence, Literal
from io import BytesIO
from exposedfunctionality import controlled_wrapper as wraps
import numpy
from .._dtypes import dtype_from_name, DTYPE_ENUM
from .._types import (
    array_like,
    ndarray,
    ndarray_or_number,
    shape_like,
    axis_like,
    scalar,
    indices_or_sections,
    ndarray_or_scalar,
    bitarray,
    int_bool_array,
    int_or_int_array,
    NoValue,
    buffer_like,
)
from ._fromnumeric import *  # noqa
from ._multiarray import *  # noqa
from ._defchararray import *  # noqa
from ._datetime import *  # noqa
from .ufuncs import *  # noqa


@fn.NodeDecorator(
    node_id="np.empty",
    name="empty",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.empty, wrapper_attribute="__fnwrapped__")
def empty(
    shape: shape_like,
    dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
    # order: OrderCF = "C",
    # like: Optional[array_like] = None,
):
    res = numpy.empty(
        shape=shape,
        dtype=dtype_from_name(dtype),
        # order=order,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.empty_like",
    name="empty_like",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.empty_like, wrapper_attribute="__fnwrapped__")
def empty_like(
    prototype: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = "K",
    # subok: Optional[bool] = True,
    # shape: Optional[shape_like] = None,
):  # params ['prototype'] ['dtype', 'order', 'subok'] []
    res = numpy.empty_like(
        prototype=prototype,
        dtype=dtype_from_name(dtype),
        # order=order,
        # subok=subok,
        # shape=shape,
    )
    return res


@fn.NodeDecorator(
    node_id="np.eye",
    name="eye",
    outputs=[{"name": "I", "type": "ndarray"}],
)
@wraps(numpy.eye, wrapper_attribute="__fnwrapped__")
def eye(
    N: int,
    M: Optional[int] = None,
    k: Optional[int] = 0,
    dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
    # order: OrderCF = "C",
    # like: Optional[array_like] = None,
):  # params ['N'] ['M', 'k', 'dtype', 'order', 'like'] []
    res = numpy.eye(
        N=N,
        M=M,
        k=k,
        dtype=dtype_from_name(dtype),
        # order=order,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.identity",
    name="identity",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.identity, wrapper_attribute="__fnwrapped__")
def identity(
    n: int,
    dtype: Optional[DTYPE_ENUM] = None,
    # like: Optional[array_like] = None,
):  # params ['n'] ['dtype', 'like'] []
    res = numpy.identity(
        n=n,
        dtype=dtype_from_name(dtype),
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ones",
    name="ones",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.ones, wrapper_attribute="__fnwrapped__")
def ones(
    shape: shape_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderCF = "C",
    # like: Optional[array_like] = None,
):  # params ['shape'] ['dtype', 'order', 'like'] []
    res = numpy.ones(
        shape=shape,
        dtype=dtype_from_name(dtype),
        # order=order,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ones_like",
    name="ones_like",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.ones_like, wrapper_attribute="__fnwrapped__")
def ones_like(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = "K",
    # subok: Optional[bool] = True,
    # shape: Optional[shape_like] = None,
):  # params ['a'] ['dtype', 'order', 'subok', 'shape'] []
    res = numpy.ones_like(
        a=a,
        dtype=dtype_from_name(dtype),
        # order=order,
        # subok=subok,
        # shape=shape,
    )
    return res


@fn.NodeDecorator(
    node_id="np.zeros",
    name="zeros",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.zeros, wrapper_attribute="__fnwrapped__")
def zeros(
    shape: shape_like,
    dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
    # order: OrderCF = "C",
    # like: Optional[array_like] = None,
):  # params ['shape'] ['dtype', 'order', 'like'] []
    res = numpy.zeros(
        shape=shape,
        dtype=dtype_from_name(dtype),
        # order=order,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.zeros_like",
    name="zeros_like",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.zeros_like, wrapper_attribute="__fnwrapped__")
def zeros_like(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = "K",
    # subok: Optional[bool] = True,
    # shape: Optional[shape_like] = None,
):  # params ['a'] ['dtype', 'order', 'subok', 'shape'] []
    res = numpy.zeros_like(
        a=a,
        dtype=dtype_from_name(dtype),
        # order=order,
        # subok=subok,
        # shape=shape,
    )
    return res


@fn.NodeDecorator(
    node_id="np.full",
    name="full",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.full, wrapper_attribute="__fnwrapped__")
def full(
    shape: shape_like,
    fill_value: ndarray_or_scalar,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderCF = "C",
    # like: Optional[array_like] = None,
):  # params ['shape', 'fill_value'] ['dtype', 'order', 'like'] []
    res = numpy.full(
        shape=shape,
        fill_value=fill_value,
        dtype=dtype_from_name(dtype),
        # order=order,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.full_like",
    name="full_like",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.full_like, wrapper_attribute="__fnwrapped__")
def full_like(
    a: array_like,
    fill_value: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = "K",
    # subok: Optional[bool] = True,
    # shape: Optional[shape_like] = None,
):  # params ['a', 'fill_value'] ['dtype', 'order'] []
    res = numpy.full_like(
        a=a,
        fill_value=fill_value,
        dtype=dtype_from_name(dtype),
        # order=order,
        # subok=subok,
        # shape=shape,
    )
    return res


@fn.NodeDecorator(
    node_id="np.meshgrid",
    name="meshgrid",
    outputs=[{"name": "XY", "type": "List[ndarray]"}],
)
@wraps(numpy.meshgrid, wrapper_attribute="__fnwrapped__")
def meshgrid(
    xi: List[array_like],
    indexing: Literal["xy", "ij"] = "xy",
    sparse: Optional[bool] = False,
):
    res = numpy.meshgrid(
        *xi,
        indexing=indexing,
        sparse=sparse,
    )
    return res


@fn.NodeDecorator(
    node_id="np.array",
    name="array",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.array, wrapper_attribute="__fnwrapped__")
def array(
    object: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    copy: Optional[bool] = True,
    # order: OrderKACF = "K",
    subok: Optional[bool] = False,
    ndmin: Optional[int] = 0,
    # like: Optional[array_like] = None,
):  # params ['object'] ['dtype', 'copy', 'order', 'subok'] []
    res = numpy.array(
        object=object,
        dtype=dtype_from_name(dtype),
        copy=copy,
        # order=order,
        # subok=subok,
        ndmin=ndmin,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.asarray",
    name="asarray",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.asarray, wrapper_attribute="__fnwrapped__")
def asarray(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = None,
    # like: Optional[array_like] = None,
):  # params ['a'] ['dtype', 'order', 'like'] []
    res = numpy.asarray(
        a=a,
        dtype=dtype_from_name(dtype),
        # order=order,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.asanyarray",
    name="asanyarray",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.asanyarray, wrapper_attribute="__fnwrapped__")
def asanyarray(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = None,
    # like: Optional[array_like] = None,
):  # params ['a'] ['dtype', 'order', 'like'] []
    res = numpy.asanyarray(
        a=a,
        dtype=dtype_from_name(dtype),
        # order=order,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ascontiguousarray",
    name="ascontiguousarray",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.ascontiguousarray, wrapper_attribute="__fnwrapped__")
def ascontiguousarray(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # like: Optional[array_like] = None,
):  # params ['a'] ['dtype', 'like'] []
    res = numpy.ascontiguousarray(
        a=a,
        dtype=dtype_from_name(dtype),
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.atleast_1d",
    name="atleast_1d",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.atleast_1d, wrapper_attribute="__fnwrapped__")
def atleast_1d(
    arr: array_like,
):
    res = numpy.atleast_1d(
        arr,
    )
    return res


@fn.NodeDecorator(
    node_id="np.atleast_2d",
    name="atleast_2d",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.atleast_2d, wrapper_attribute="__fnwrapped__")
def atleast_2d(
    arr: array_like,
):
    res = numpy.atleast_2d(
        arr,
    )
    return res


@fn.NodeDecorator(
    node_id="np.atleast_3d",
    name="atleast_3d",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.atleast_3d, wrapper_attribute="__fnwrapped__")
def atleast_3d(
    arr: array_like,
):
    res = numpy.atleast_3d(
        arr,
    )
    return res


@fn.NodeDecorator(
    node_id="np.copy",
    name="copy",
    outputs=[{"name": "arr", "type": "ndarray"}],
)
@wraps(numpy.copy, wrapper_attribute="__fnwrapped__")
def copy(
    a: array_like,
    # order: OrderKACF = "K",
    subok: Optional[bool] = False,
):  # params ['a'] ['order', 'subok'] []
    res = numpy.copy(
        a=a,
        # order=order,
        # subok=subok,
    )
    return res


@fn.NodeDecorator(
    node_id="np.frombuffer",
    name="frombuffer",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.frombuffer, wrapper_attribute="__fnwrapped__")
def frombuffer(
    buffer: buffer_like,
    dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
    count: Optional[int] = -1,
    offset: Optional[int] = 0,
    # like: Optional[array_like] = None,
):  # params ['buffer'] ['dtype', 'count', 'offset', 'like'] []
    res = numpy.frombuffer(
        buffer=buffer,
        dtype=dtype_from_name(dtype),
        count=count,
        offset=offset,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fromnpy",
    name="from npy",
)
def from_npy(data: bytes):
    with BytesIO(data) as buffer:
        return numpy.load(buffer)


@fn.NodeDecorator(
    node_id="np.from_dlpack",
    name="from_dlpack",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.from_dlpack, wrapper_attribute="__fnwrapped__")
def from_dlpack(
    x: object,
):  # params ['x'] [] []
    res = numpy.from_dlpack(
        x,
    )
    return res


# @fn.NodeDecorator(
#     node_id="np.fromfile",
#     name="fromfile",
#     outputs=[],
# )
# @wraps(numpy.fromfile, wrapper_attribute="__fnwrapped__")
# def fromfile(
#     file: file or str or Path,
#     dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
#     count: int = -1,
#     sep: str = "",
#     offset: int = 0,
#    # like: Optional[array_like] = None,
# ):  # params ['file'] ['dtype', 'count', 'sep', 'offset', 'like'] []
#     res = numpy.fromfile(
#         file=file,
#         dtype=dtype_from_name(dtype),
#         count=count,
#         sep=sep,
#         offset=offset,
#         # like=like,
#     )
#     return res


# @fn.NodeDecorator(
#     node_id="np.fromfunction",
#     name="fromfunction",
#     outputs=[{"name": "fromfunction", "type": "ndarray_or_number"}],
# )
# @wraps(numpy.fromfunction, wrapper_attribute="__fnwrapped__")
# def fromfunction(
#     function: Callable,
#     shape: shape_like,
#     dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
#     # like: Optional[array_like] = None,
# ):  # params ['function', 'shape'] ['dtype', 'like'] []
#     res = numpy.fromfunction(
#         function=function,
#         shape=shape,
#         dtype=dtype_from_name(dtype),
#         # like=like,
#     )
#     return res


@fn.NodeDecorator(
    node_id="np.fromiter",
    name="fromiter",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.fromiter, wrapper_attribute="__fnwrapped__")
def fromiter(
    iter: Iterable,
    dtype: DTYPE_ENUM,
    count: Optional[int] = -1,
    # like: Optional[array_like] = None,
):  # params ['iter', 'dtype'] ['count', 'like'] []
    res = numpy.fromiter(
        iter=iter,
        dtype=dtype_from_name(dtype),
        count=count,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fromstring",
    name="fromstring",
    outputs=[{"name": "arr", "type": "ndarray"}],
)
@wraps(numpy.fromstring, wrapper_attribute="__fnwrapped__")
def fromstring(
    string: str,
    dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
    count: Optional[int] = -1,
    sep: Optional[str] = ",",
    # like: Optional[array_like] = None,
):  # params ['string'] ['dtype', 'count', 'like'] []
    res = numpy.fromstring(
        string=string,
        dtype=dtype_from_name(dtype),
        count=count,
        sep=sep,
        # like=like,
    )
    return res


# @fn.NodeDecorator(
#     node_id="np.loadtxt",
#     name="loadtxt",
#     outputs=[{"name": "out", "type": "ndarray"}],
# )
# @wraps(numpy.loadtxt, wrapper_attribute="__fnwrapped__")
# def loadtxt(
#     fname: file, str,
#     pathlib.Path, list of str, generator,
#     dtype:  DTYPE_ENUM = DTYPE_ENUM.float32,
#     comments: str or sequence of str or None,
#     optional = '#', delimiter: Optional[str] = None,
#     converters: dict or callable, optional = None,
#     skiprows: Optional[int]= 0, usecols: int or sequence, optional = None,
#     unpack: Optional[bool]= False,
#     ndmin: Optional[int]= 0,
#     encoding: Optional[str] = 'bytes',
#     max_rows: Optional[int]= None,
#     quotechar: unicode character or None,
#     optional = None,
#    # like: Optional[array_like] = None,
# ):  # params ['fname'] ['dtype', 'comments', 'delimiter'] []
#     res = numpy.loadtxt(
#         fname=fname,
#         dtype=dtype_from_name(dtype),
#         comments=comments,
#         delimiter=delimiter,
#         converters=converters,
#         skiprows=skiprows,
#         usecols=usecols,
#         unpack=unpack,
#         ndmin=ndmin,
#         encoding=encoding,
#         max_rows=max_rows,
#         quotechar=quotechar,
#         # like=like,
#     )
#     return res


@fn.NodeDecorator(
    node_id="np.arange",
    name="arange",
    outputs=[{"name": "arange", "type": "ndarray"}],
)
@wraps(numpy.arange, wrapper_attribute="__fnwrapped__")
def arange(
    stop: scalar,
    start: Optional[scalar] = 0,
    step: Optional[scalar] = 1,
    dtype: Optional[DTYPE_ENUM] = None,
    # like: Optional[array_like] = None,
):  # params ['stop'] ['start', 'step', 'dtype', 'like'] []
    res = numpy.arange(
        start=start,
        stop=stop,
        step=step,
        dtype=dtype_from_name(dtype),
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.linspace",
    name="linspace",
    outputs=[
        {"name": "samples", "type": "ndarray"},
        {"name": "step", "type": "float"},
    ],
)
@wraps(numpy.linspace, wrapper_attribute="__fnwrapped__")
def linspace(
    start: array_like,
    stop: array_like,
    num: Optional[int] = 50,
    endpoint: Optional[bool] = True,
    # retstep: Optional[bool] = False,
    dtype: Optional[DTYPE_ENUM] = None,
    axis: Optional[int] = 0,
):  # params ['start', 'stop'] ['num', 'endpoint'] []
    res = numpy.linspace(
        start=start,
        stop=stop,
        num=num,
        endpoint=endpoint,
        retstep=True,
        dtype=dtype_from_name(dtype),
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.logspace",
    name="logspace",
    outputs=[{"name": "samples", "type": "ndarray"}],
)
@wraps(numpy.logspace, wrapper_attribute="__fnwrapped__")
def logspace(
    start: array_like,
    stop: array_like,
    num: Optional[int] = 50,
    endpoint: Optional[bool] = True,
    base: Optional[ndarray_or_scalar] = 10.0,
    dtype: Optional[DTYPE_ENUM] = None,
    axis: Optional[int] = 0,
):  # params ['start', 'stop'] ['num', 'endpoint', 'base'] []
    res = numpy.logspace(
        start=start,
        stop=stop,
        num=num,
        endpoint=endpoint,
        base=base,
        dtype=dtype_from_name(dtype),
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.geomspace",
    name="geomspace",
    outputs=[{"name": "samples", "type": "ndarray"}],
)
@wraps(numpy.geomspace, wrapper_attribute="__fnwrapped__")
def geomspace(
    start: array_like,
    stop: array_like,
    num: Optional[int] = 50,
    endpoint: Optional[bool] = True,
    dtype: Optional[DTYPE_ENUM] = None,
    axis: Optional[int] = 0,
):  # params ['start', 'stop'] ['num', 'endpoint'] []
    res = numpy.geomspace(
        start=start,
        stop=stop,
        num=num,
        endpoint=endpoint,
        dtype=dtype_from_name(dtype),
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.diag",
    name="diag",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.diag, wrapper_attribute="__fnwrapped__")
def diag(
    v: array_like,
    k: Optional[int] = 0,
):  # params ['v'] ['k'] []
    res = numpy.diag(
        v=v,
        k=k,
    )
    return res


@fn.NodeDecorator(
    node_id="np.diagflat",
    name="diagflat",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.diagflat, wrapper_attribute="__fnwrapped__")
def diagflat(
    v: array_like,
    k: Optional[int] = 0,
):  # params ['v'] ['k'] []
    res = numpy.diagflat(
        v=v,
        k=k,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tri",
    name="tri",
    outputs=[{"name": "tri", "type": "ndarray"}],
)
@wraps(numpy.tri, wrapper_attribute="__fnwrapped__")
def tri(
    N: int,
    M: Optional[int] = None,
    k: Optional[int] = 0,
    dtype: DTYPE_ENUM = DTYPE_ENUM.float32,
    # like: Optional[array_like] = None,
):  # params ['N'] ['M', 'k', 'dtype', 'like'] []
    res = numpy.tri(
        N=N,
        M=M,
        k=k,
        dtype=dtype_from_name(dtype),
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tril",
    name="tril",
    outputs=[{"name": "tril", "type": "ndarray"}],
)
@wraps(numpy.tril, wrapper_attribute="__fnwrapped__")
def tril(
    m: ndarray,
    k: Optional[int] = 0,
):  # params ['m'] ['k'] []
    res = numpy.tril(
        m=m,
        k=k,
    )
    return res


@fn.NodeDecorator(
    node_id="np.triu",
    name="triu",
    outputs=[{"name": "triu", "type": "ndarray"}],
)
@wraps(numpy.triu, wrapper_attribute="__fnwrapped__")
def triu(
    m: ndarray,
    k: Optional[int] = 0,
):
    res = numpy.triu(
        m=m,
        k=k,
    )
    return res


@fn.NodeDecorator(
    node_id="np.vander",
    name="vander",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.vander, wrapper_attribute="__fnwrapped__")
def vander(
    x: array_like,
    N: Optional[int] = None,
    increasing: Optional[bool] = False,
):  # params ['x'] ['N', 'increasing'] []
    res = numpy.vander(
        x,
        N=N,
        increasing=increasing,
    )
    return res


@fn.NodeDecorator(
    node_id="np.bmat",
    name="bmat",
    outputs=[{"name": "out", "type": "matrix"}],
)
@wraps(numpy.bmat, wrapper_attribute="__fnwrapped__")
def bmat(
    obj: Union[str, ndarray],
    ldict: Optional[dict] = None,
    gdict: Optional[dict] = None,
):  # params ['obj'] ['ldict', 'gdict'] []
    res = numpy.bmat(
        obj=obj,
        ldict=ldict,
        gdict=gdict,
    )
    return res


# @fn.NodeDecorator(
#     node_id="np.copyto",
#     name="copyto",
#     outputs=[],
# )
# @wraps(numpy.copyto, wrapper_attribute="__fnwrapped__")
# def copyto(
#     dst: ndarray,
#     src: array_like,
#     # casting: casting_literal = "same_kind",
#     # where: Union[bool_array, bool] = True,
# ):  # params ['dst', 'src'] ['casting', 'where'] []
#     res = numpy.copyto(
#         dst=dst,
#         src=src,
#         # casting=casting,
#         # where=where,
#     )
#     return res


@fn.NodeDecorator(
    node_id="np.shape",
    name="shape",
    outputs=[{"name": "shape", "type": "shape_like"}],
)
@wraps(numpy.shape, wrapper_attribute="__fnwrapped__")
def shape(
    a: array_like,
):  # params ['a'] [] []
    res = numpy.shape(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.size",
    name="size",
    outputs=[{"name": "size", "type": "Union[int, int_array]"}],
)
@wraps(numpy.size, wrapper_attribute="__fnwrapped__")
def size(
    a: array_like,
    axis: Optional[int] = None,
):
    res = numpy.size(
        a=a,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ndim",
    name="ndim",
    outputs=[{"name": "ndim", "type": "int"}],
)
@wraps(numpy.ndim, wrapper_attribute="__fnwrapped__")
def ndim(
    a: array_like,
):
    res = numpy.ndim(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.reshape",
    name="reshape",
    outputs=[{"name": "reshaped_array", "type": "ndarray"}],
)
@wraps(numpy.reshape, wrapper_attribute="__fnwrapped__")
def reshape(
    a: array_like,
    newshape: shape_like,
    # order: Optional[Literal["C", "F", "A"]] = "C",
):  # params ['a', 'newshape'] ['order'] []
    res = numpy.reshape(
        a,
        newshape=newshape,
        # order=order,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ravel",
    name="ravel",
    outputs=[{"name": "y", "type": "array_like"}],
)
@wraps(numpy.ravel, wrapper_attribute="__fnwrapped__")
def ravel(
    a: array_like,
    # order: Optional[Literal["C", "F", "A", "K"]] = "C",
):  # params ['a'] ['order'] []
    res = numpy.ravel(
        a=a,
        # order=order,
    )
    return res


@fn.NodeDecorator(
    node_id="np.moveaxis",
    name="moveaxis",
    outputs=[{"name": "result", "type": "ndarray"}],
)
@wraps(numpy.moveaxis, wrapper_attribute="__fnwrapped__")
def moveaxis(
    a: ndarray,
    source: axis_like,
    destination: axis_like,
):  # params ['a', 'source', 'destination'] [] []
    res = numpy.moveaxis(
        a=a,
        source=source,
        destination=destination,
    )
    return res


@fn.NodeDecorator(
    node_id="np.rollaxis",
    name="rollaxis",
    outputs=[{"name": "res", "type": "ndarray"}],
)
@wraps(numpy.rollaxis, wrapper_attribute="__fnwrapped__")
def rollaxis(
    a: ndarray,
    axis: int,
    start: Optional[int] = 0,
):  # params ['a', 'axis'] ['start'] []
    res = numpy.rollaxis(
        a=a,
        axis=axis,
        start=start,
    )
    return res


@fn.NodeDecorator(
    node_id="np.swapaxes",
    name="swapaxes",
    outputs=[{"name": "a_swapped", "type": "ndarray"}],
)
@wraps(numpy.swapaxes, wrapper_attribute="__fnwrapped__")
def swapaxes(
    a: array_like,
    axis1: int,
    axis2: int,
):  # params ['a', 'axis1', 'axis2'] [] []
    res = numpy.swapaxes(
        a=a,
        axis1=axis1,
        axis2=axis2,
    )
    return res


@fn.NodeDecorator(
    node_id="np.transpose",
    name="transpose",
    outputs=[{"name": "p", "type": "ndarray"}],
)
@wraps(numpy.transpose, wrapper_attribute="__fnwrapped__")
def transpose(
    a: array_like,
    axes: Optional[axis_like] = None,
):  # params ['a'] ['axes'] []
    res = numpy.transpose(
        a=a,
        axes=axes,
    )
    return res


@fn.NodeDecorator(
    node_id="np.broadcast_to",
    name="broadcast_to",
    outputs=[{"name": "broadcast", "type": "ndarray"}],
)
@wraps(numpy.broadcast_to, wrapper_attribute="__fnwrapped__")
def broadcast_to(
    array: array_like,
    shape: shape_like,
    subok: Optional[bool] = False,
):  # params ['array', 'shape'] ['subok'] []
    res = numpy.broadcast_to(
        array=array,
        shape=shape,
        # subok=subok,
    )
    return res


@fn.NodeDecorator(
    node_id="np.broadcast_arrays",
    name="broadcast_arrays",
    outputs=[{"name": "broadcasted", "type": "List[ndarray]"}],
)
@wraps(numpy.broadcast_arrays, wrapper_attribute="__fnwrapped__")
def broadcast_arrays(
    args: Sequence[array_like],
    subok: Optional[bool] = False,
):  # params [] ['args', 'subok'] []
    res = numpy.broadcast_arrays(
        *args,
        # subok=subok,
    )
    return res


@fn.NodeDecorator(
    node_id="np.expand_dims",
    name="expand_dims",
    outputs=[{"name": "result", "type": "ndarray"}],
)
@wraps(numpy.expand_dims, wrapper_attribute="__fnwrapped__")
def expand_dims(
    a: array_like,
    axis: axis_like,
):  # params ['a', 'axis'] [] []
    res = numpy.expand_dims(
        a=a,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.squeeze",
    name="squeeze",
    outputs=[{"name": "squeezed", "type": "ndarray"}],
)
@wraps(numpy.squeeze, wrapper_attribute="__fnwrapped__")
def squeeze(
    a: array_like,
    axis: Optional[axis_like] = None,
):  # params ['a'] ['axis'] []
    res = numpy.squeeze(
        a=a,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.asmatrix",
    name="asmatrix",
    outputs=[{"name": "mat", "type": "matrix"}],
)
@wraps(numpy.asmatrix, wrapper_attribute="__fnwrapped__")
def asmatrix(
    data: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
):  # params ['data'] ['dtype'] []
    res = numpy.asmatrix(
        data,
        dtype=dtype_from_name(dtype),
    )
    return res


@fn.NodeDecorator(
    node_id="np.asfortranarray",
    name="asfortranarray",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.asfortranarray, wrapper_attribute="__fnwrapped__")
def asfortranarray(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # like: Optional[array_like] = None,
):  # params ['a'] ['dtype', 'like'] []
    res = numpy.asfortranarray(
        a=a,
        dtype=dtype_from_name(dtype),
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.asarray_chkfinite",
    name="asarray_chkfinite",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.asarray_chkfinite, wrapper_attribute="__fnwrapped__")
def asarray_chkfinite(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = None,
):  # params ['a'] ['dtype', 'order'] []
    res = numpy.asarray_chkfinite(
        a=a,
        dtype=dtype_from_name(dtype),
        # order=order,
    )
    return res


@fn.NodeDecorator(
    node_id="np.require",
    name="require",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.require, wrapper_attribute="__fnwrapped__")
def require(
    a: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    requirements: Literal["F", "C", "A", "W", "O", "E"] = None,
    # like: Optional[array_like] = None,
):  # params ['a'] ['dtype', 'requirements', 'like'] []
    res = numpy.require(
        a=a,
        dtype=dtype_from_name(dtype),
        requirements=requirements,
        # like=like,
    )
    return res


@fn.NodeDecorator(
    node_id="np.concatenate",
    name="concatenate",
    outputs=[{"name": "res", "type": "ndarray"}],
)
@wraps(numpy.concatenate, wrapper_attribute="__fnwrapped__")
def concatenate(
    arrs: List[ndarray],
    axis: Optional[int] = 0,
    # out: Optional[ndarray] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params [] ['axis', 'out', 'dtype', 'casting'] []
    res = numpy.concatenate(
        arrs,
        axis=axis,
        # out=out,
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.concatenate2",
    name="concatenate2",
    outputs=[{"name": "res", "type": "ndarray"}],
)
@wraps(numpy.concatenate, wrapper_attribute="__fnwrapped__")
def concatenate2(
    a: ndarray,
    b: ndarray,
    axis: Optional[int] = 0,
    # out: Optional[ndarray] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params [] ['axis', 'out', 'dtype', 'casting'] []
    res = numpy.concatenate(
        (a, b),
        axis=axis,
        # out=out,
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.stack",
    name="stack",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.stack, wrapper_attribute="__fnwrapped__")
def stack(
    arrays: Sequence[array_like],
    axis: Optional[int] = 0,
    # out: Optional[ndarray] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['arrays'] ['axis', 'out', 'dtype', 'casting'] []
    res = numpy.stack(
        arrays=arrays,
        axis=axis,
        # out=out,
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.stack2",
    name="stack2",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.stack, wrapper_attribute="__fnwrapped__")
def stack2(
    a: array_like,
    b: array_like,
    axis: Optional[int] = 0,
    # out: Optional[ndarray] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['arrays'] ['axis', 'out', 'dtype', 'casting'] []
    res = numpy.stack(
        arrays=(a, b),
        axis=axis,
        # out=out,
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


# @fn.NodeDecorator(
#     node_id="np.block",
#     name="block",
#     outputs=[
#     {
#         "name": "block_array",
#         "type": "ndarray"
#     }
# ],
#     )
# @wraps(numpy.block, wrapper_attribute="__fnwrapped__")
# def block(arrays: nested list of array_like or scalars (but not tuples), ): # params ['arrays'] [] []
#     res = numpy.block(arrays=arrays, )
#     return res


@fn.NodeDecorator(
    node_id="np.vstack",
    name="vstack",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.vstack, wrapper_attribute="__fnwrapped__")
def vstack(
    tup: Sequence[ndarray],
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['tup'] ['dtype', 'casting'] []
    res = numpy.vstack(
        tup=tup,
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.vstack2",
    name="vstack2",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.vstack, wrapper_attribute="__fnwrapped__")
def vstack2(
    a: array_like,
    b: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['tup'] ['dtype', 'casting'] []
    res = numpy.vstack(
        tup=(a, b),
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.hstack",
    name="hstack",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.hstack, wrapper_attribute="__fnwrapped__")
def hstack(
    tup: Sequence[ndarray],
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['tup'] ['dtype', 'casting'] []
    res = numpy.hstack(
        tup=tup,
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.hstack2",
    name="hstack2",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.hstack, wrapper_attribute="__fnwrapped__")
def hstack2(
    a: array_like,
    b: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['tup'] ['dtype', 'casting'] []
    res = numpy.hstack(
        tup=(a, b),
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.dstack",
    name="dstack",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.dstack, wrapper_attribute="__fnwrapped__")
def dstack(
    tup: Sequence[ndarray],
):  # params ['tup'] [] []
    res = numpy.dstack(
        tup=tup,
    )
    return res


@fn.NodeDecorator(
    node_id="np.dstack2",
    name="dstack2",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.dstack, wrapper_attribute="__fnwrapped__")
def dstack2(
    a: array_like,
    b: array_like,
):  # params ['tup'] [] []
    res = numpy.dstack(
        tup=(a, b),
    )
    return res


@fn.NodeDecorator(
    node_id="np.column_stack",
    name="column_stack",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.column_stack, wrapper_attribute="__fnwrapped__")
def column_stack(
    tup: Sequence[ndarray],
):  # params ['tup'] [] []
    res = numpy.column_stack(
        tup=tup,
    )
    return res


@fn.NodeDecorator(
    node_id="np.column_stack2",
    name="column_stack2",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.column_stack, wrapper_attribute="__fnwrapped__")
def column_stack2(
    a: array_like,
    b: array_like,
):  # params ['tup'] [] []
    res = numpy.column_stack(
        tup=(a, b),
    )
    return res


@fn.NodeDecorator(
    node_id="np.row_stack",
    name="row_stack",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.row_stack, wrapper_attribute="__fnwrapped__")
def row_stack(
    tup: Sequence[ndarray],
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['tup'] ['dtype', 'casting'] []
    res = numpy.row_stack(
        tup=tup,
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.row_stack2",
    name="row_stack2",
    outputs=[{"name": "stacked", "type": "ndarray"}],
)
@wraps(numpy.row_stack, wrapper_attribute="__fnwrapped__")
def row_stack2(
    a: array_like,
    b: array_like,
    dtype: Optional[DTYPE_ENUM] = None,
    # casting: casting_literal = "same_kind",
):  # params ['tup'] ['dtype', 'casting'] []
    res = numpy.row_stack(
        tup=(a, b),
        dtype=dtype_from_name(dtype),
        # casting=casting,
    )
    return res


@fn.NodeDecorator(
    node_id="np.split",
    name="split",
    outputs=[{"name": "sub-arrays", "type": "List[ndarray]"}],
)
@wraps(numpy.split, wrapper_attribute="__fnwrapped__")
def split(
    ary: ndarray,
    indices_or_sections: indices_or_sections,
    axis: Optional[int] = 0,
):  # params ['ary', 'indices_or_sections'] ['axis'] []
    res = numpy.split(
        ary=ary,
        indices_or_sections=indices_or_sections,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.array_split",
    name="array_split",
    outputs=[{"name": "sub-arrays", "type": "List[ndarray]"}],
)
@wraps(numpy.array_split, wrapper_attribute="__fnwrapped__")
def array_split(
    ary: ndarray,
    indices_or_sections: shape_like,
    axis: Optional[int] = 0,
):
    res = numpy.array_split(
        ary=ary,
        indices_or_sections=indices_or_sections,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.dsplit",
    name="dsplit",
    outputs=[{"name": "sub-arrays", "type": "List[ndarray]"}],
)
@wraps(numpy.dsplit, wrapper_attribute="__fnwrapped__")
def dsplit(
    ary: ndarray,
    indices_or_sections: indices_or_sections,
):
    res = numpy.dsplit(
        ary=ary,
        indices_or_sections=indices_or_sections,
    )
    return res


@fn.NodeDecorator(
    node_id="np.hsplit",
    name="hsplit",
    outputs=[{"name": "sub-arrays", "type": "List[ndarray]"}],
)
@wraps(numpy.hsplit, wrapper_attribute="__fnwrapped__")
def hsplit(
    ary: ndarray,
    indices_or_sections: indices_or_sections,
):
    res = numpy.hsplit(
        ary=ary,
        indices_or_sections=indices_or_sections,
    )
    return res


@fn.NodeDecorator(
    node_id="np.vsplit",
    name="vsplit",
    outputs=[{"name": "sub-arrays", "type": "List[ndarray]"}],
)
@wraps(numpy.vsplit, wrapper_attribute="__fnwrapped__")
def vsplit(
    ary: ndarray,
    indices_or_sections: indices_or_sections,
):
    res = numpy.vsplit(
        ary=ary,
        indices_or_sections=indices_or_sections,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tile",
    name="tile",
    outputs=[{"name": "c", "type": "ndarray"}],
)
@wraps(numpy.tile, wrapper_attribute="__fnwrapped__")
def tile(
    A: array_like,
    reps: array_like,
):  # params ['A', 'reps'] [] []
    res = numpy.tile(
        A=A,
        reps=reps,
    )
    return res


@fn.NodeDecorator(
    node_id="np.repeat",
    name="repeat",
    outputs=[{"name": "repeated_array", "type": "ndarray"}],
)
@wraps(numpy.repeat, wrapper_attribute="__fnwrapped__")
def repeat(
    a: array_like,
    repeats: int_or_int_array,
    axis: Optional[int] = None,
):  # params ['a', 'repeats'] ['axis'] []
    res = numpy.repeat(
        a=a,
        repeats=repeats,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.delete",
    name="delete",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.delete, wrapper_attribute="__fnwrapped__")
def delete(
    arr: array_like,
    obj: int_or_int_array,
    axis: Optional[int] = None,
):  # params ['arr', 'obj'] ['axis'] []
    res = numpy.delete(
        arr=arr,
        obj=obj,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.insert",
    name="insert",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.insert, wrapper_attribute="__fnwrapped__")
def insert(
    arr: array_like,
    obj: int_or_int_array,
    values: array_like,
    axis: Optional[int] = None,
):  # params ['arr', 'obj', 'values'] ['axis'] []
    res = numpy.insert(
        arr=arr,
        obj=obj,
        values=values,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.append",
    name="append",
    outputs=[{"name": "append", "type": "ndarray"}],
)
@wraps(numpy.append, wrapper_attribute="__fnwrapped__")
def append(
    arr: array_like,
    values: array_like,
    axis: Optional[int] = None,
):  # params ['arr', 'values'] ['axis'] []
    res = numpy.append(
        arr=arr,
        values=values,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.pad",
    name="pad",
    outputs=[{"name": "padded", "type": "ndarray"}],
)
@wraps(numpy.pad, wrapper_attribute="__fnwrapped__")
def pad(
    array: array_like,
    pad_width: Union[int, Tuple[int, int], List[Tuple[int, int]]],
    mode: Literal[
        "constant",
        "edge",
        "linear_ramp",
        "maximum",
        "mean",
        "median",
        "minimum",
        "reflect",
        "symmetric",
        "wrap",
        "empty",
    ] = "constant",
    constant_values: Union[scalar, Tuple[scalar, scalar]] = 0,
):
    res = numpy.pad(
        array=array,
        pad_width=pad_width,
        mode=mode,
        constant_values=constant_values,
    )
    return res


@fn.NodeDecorator(
    node_id="np.resize",
    name="resize",
    outputs=[{"name": "reshaped_array", "type": "ndarray"}],
)
@wraps(numpy.resize, wrapper_attribute="__fnwrapped__")
def resize(
    a: array_like,
    new_shape: shape_like,
):  # params ['a', 'new_shape'] [] []
    res = numpy.resize(
        a.copy(),
        new_shape,
    )
    return res


@fn.NodeDecorator(
    node_id="np.trim_zeros",
    name="trim_zeros",
    outputs=[{"name": "trimmed", "type": "ndarray"}],
)
@wraps(numpy.trim_zeros, wrapper_attribute="__fnwrapped__")
def trim_zeros(
    filt: List[scalar],
    trim: Optional[str] = "fb",
):  # params ['filt'] ['trim'] []
    res = numpy.trim_zeros(
        filt=filt,
        trim=trim,
    )
    return res


@fn.NodeDecorator(
    node_id="np.unique",
    name="unique",
    outputs=[
        {"name": "unique", "type": "ndarray"},
        {"name": "unique_indices", "type": "Union[ndarray,None]"},
        {"name": "unique_inverse", "type": "Union[ndarray,None]"},
        {"name": "unique_counts", "type": "Union[ndarray,None]"},
    ],
)
@wraps(numpy.unique, wrapper_attribute="__fnwrapped__")
def unique(
    ar: array_like,
    return_index: Optional[bool] = False,
    return_inverse: Optional[bool] = False,
    return_counts: Optional[bool] = False,
    axis: Optional[int] = None,
    equal_nan: Optional[bool] = True,
):  # params ['ar'] ['return_index', 'return_inverse'] []
    res = numpy.unique(
        ar=ar,
        return_index=return_index,
        return_inverse=return_inverse,
        return_counts=return_counts,
        axis=axis,
        equal_nan=equal_nan,
    )
    _uq = res[0]
    ix = 1
    if return_index:
        _uq_ix = res[ix]
        ix += 1
    else:
        _uq_ix = None

    if return_inverse:
        _uq_inv = res[ix]
        ix += 1
    else:
        _uq_inv = None

    if return_counts:
        _uq_cnt = res[ix]
        ix += 1
    else:
        _uq_cnt = None

    return _uq, _uq_ix, _uq_inv, _uq_cnt


@fn.NodeDecorator(
    node_id="np.flip",
    name="flip",
    outputs=[{"name": "out", "type": "array_like"}],
)
@wraps(numpy.flip, wrapper_attribute="__fnwrapped__")
def flip(
    m: array_like,
    axis: Optional[axis_like] = None,
):  # params ['m'] ['axis'] []
    res = numpy.flip(
        m=m,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fliplr",
    name="fliplr",
    outputs=[{"name": "f", "type": "ndarray"}],
)
@wraps(numpy.fliplr, wrapper_attribute="__fnwrapped__")
def fliplr(
    m: array_like,
):  # params ['m'] [] []
    res = numpy.fliplr(
        m=m,
    )
    return res


@fn.NodeDecorator(
    node_id="np.flipud",
    name="flipud",
    outputs=[{"name": "out", "type": "array_like"}],
)
@wraps(numpy.flipud, wrapper_attribute="__fnwrapped__")
def flipud(
    m: array_like,
):  # params ['m'] [] []
    res = numpy.flipud(
        m=m,
    )
    return res


@fn.NodeDecorator(
    node_id="np.roll",
    name="roll",
    outputs=[{"name": "res", "type": "ndarray"}],
)
@wraps(numpy.roll, wrapper_attribute="__fnwrapped__")
def roll(
    a: array_like,
    shift: axis_like,
    axis: Optional[axis_like] = None,
):  # params ['a', 'shift'] ['axis'] []
    res = numpy.roll(
        a=a,
        shift=shift,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.rot90",
    name="rot90",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.rot90, wrapper_attribute="__fnwrapped__")
def rot90(
    m: array_like,
    k: int = 1,
    axes: axis_like = (0, 1),
):  # params ['m'] ['k', 'axes'] []
    res = numpy.rot90(
        m=m,
        k=k,
        axes=axes,
    )
    return res


@fn.NodeDecorator(
    node_id="np.packbits",
    name="packbits",
    outputs=[{"name": "packed", "type": "ndarray"}],
)
@wraps(numpy.packbits, wrapper_attribute="__fnwrapped__")
def packbits(
    a: int_bool_array,
    axis: Optional[int] = None,
    bitorder: Optional[Literal["big", "little"]] = "big",
):  # params ['a'] ['axis', 'bitorder'] []
    res = numpy.packbits(
        a,
        axis=axis,
        bitorder=bitorder,
    )
    return res


@fn.NodeDecorator(
    node_id="np.unpackbits",
    name="unpackbits",
    outputs=[{"name": "unpacked", "type": "bitarray"}],
)
@wraps(numpy.unpackbits, wrapper_attribute="__fnwrapped__")
def unpackbits(
    a: bitarray,
    axis: Optional[int] = None,
    count: Optional[int] = None,
    bitorder: Optional[Literal["big", "little"]] = "big",
):  # params ['a'] ['axis', 'count', 'bitorder'] []
    res = numpy.unpackbits(
        a,
        axis=axis,
        count=count,
        bitorder=bitorder,
    )
    return res


@fn.NodeDecorator(
    node_id="np.binary_repr",
    name="binary_repr",
    outputs=[{"name": "bin", "type": "str"}],
)
@wraps(numpy.binary_repr, wrapper_attribute="__fnwrapped__")
def binary_repr(
    num: int,
    width: Optional[int] = None,
):  # params ['num'] ['width'] []
    res = numpy.binary_repr(
        num=num,
        width=width,
    )
    return res


@fn.NodeDecorator(
    node_id="np.dot",
    name="dot",
    outputs=[{"name": "output", "type": "ndarray"}],
)
@wraps(numpy.dot, wrapper_attribute="__fnwrapped__")
def dot(
    a: array_like,
    b: array_like,
    # out: Optional[ndarray] = None,
):  # params ['a', 'b'] ['out'] []
    res = numpy.dot(
        a=a,
        b=b,
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.vdot",
    name="vdot",
    outputs=[{"name": "output", "type": "ndarray"}],
)
@wraps(numpy.vdot, wrapper_attribute="__fnwrapped__")
def vdot(
    a: array_like,
    b: array_like,
):  # params ['a', 'b'] [] []
    res = numpy.vdot(
        a,
        b,
    )
    return res


@fn.NodeDecorator(
    node_id="np.inner",
    name="inner",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.inner, wrapper_attribute="__fnwrapped__")
def inner(
    a: array_like,
    b: array_like,
):  # params ['a', 'b'] [] []
    res = numpy.inner(
        a,
        b,
    )
    return res


@fn.NodeDecorator(
    node_id="np.outer",
    name="outer",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.outer, wrapper_attribute="__fnwrapped__")
def outer(
    a: ndarray,
    b: ndarray,
    # out: Optional[ndarray] = None,
):  # params ['a', 'b'] ['out'] []
    res = numpy.outer(
        a=a,
        b=b,
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.matmul",
    name="matmul",
    outputs=[{"name": "y", "type": "ndarray"}],
)
@wraps(numpy.matmul, wrapper_attribute="__fnwrapped__")
def matmul(
    x1: array_like,
    x2: array_like,
    # out: Optional[ndarray] = None,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['x1', 'x2'] ['out', 'casting', 'order'] []
    res = numpy.matmul(
        x1,
        x2,
        # out=out,
        # casting=casting,
        # order=order,
        dtype=dtype_from_name(dtype),
        # subok=subok,
        # signature=signature,
        # extobj=extobj,
    )
    return res


@fn.NodeDecorator(
    node_id="np.tensordot",
    name="tensordot",
    outputs=[{"name": "output", "type": "ndarray"}],
)
@wraps(numpy.tensordot, wrapper_attribute="__fnwrapped__")
def tensordot(
    a: array_like,
    b: array_like,
    axes: axis_like = 2,
):  # params ['a', 'b'] ['axes'] []
    res = numpy.tensordot(
        a=a,
        b=b,
        axes=axes,
    )
    return res


@fn.NodeDecorator(
    node_id="np.einsum",
    name="einsum",
    outputs=[{"name": "output", "type": "ndarray"}],
)
@wraps(numpy.einsum, wrapper_attribute="__fnwrapped__")
def einsum(
    subscripts: str,
    operands: List[ndarray],
    # out: Optional[ndarray] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # order: OrderKACF = "K",
    # casting: casting_literal = "safe",
    optimize: Optional[Literal[False, True, "greedy", "optimal"]] = False,
):  # params ['subscripts'] ['operands', 'out', 'dtype'] []
    res = numpy.einsum(
        subscripts,
        *operands,
        # out=out,
        dtype=dtype_from_name(dtype),
        # order=order,
        # casting=casting,
        optimize=optimize,
    )
    return res


@fn.NodeDecorator(
    node_id="np.einsum_path",
    name="einsum_path",
    outputs=[
        {"name": "path", "type": "List[Tuple]"},
        {"name": "string_repr", "type": "str"},
    ],
)
@wraps(numpy.einsum_path, wrapper_attribute="__fnwrapped__")
def einsum_path(
    subscripts: str,
    operands: List[array_like],
    optimize: Optional[Literal[False, True, "greedy", "optimal"]] = "greedy",
):  # params ['subscripts'] ['operands', 'optimize'] []
    res = numpy.einsum_path(
        subscripts,
        *operands,
        optimize=optimize,
    )
    return res


@fn.NodeDecorator(
    node_id="np.kron",
    name="kron",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.kron, wrapper_attribute="__fnwrapped__")
def kron(
    a: array_like,
    b: array_like,
):  # params ['a', 'b'] [] []
    res = numpy.kron(
        a=a,
        b=b,
    )
    return res


@fn.NodeDecorator(
    node_id="np.trace",
    name="trace",
    outputs=[{"name": "sum_along_diagonals", "type": "ndarray"}],
)
@wraps(numpy.trace, wrapper_attribute="__fnwrapped__")
def trace(
    a: array_like,
    offset: Optional[int] = 0,
    axis1: Optional[int] = 0,
    axis2: Optional[int] = 1,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
):  # params ['a'] ['offset', 'axis1', 'axis2', 'dtype', 'out'] []
    res = numpy.trace(
        a=a,
        offset=offset,
        axis1=axis1,
        axis2=axis2,
        dtype=dtype_from_name(dtype),
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.all",
    name="all",
    outputs=[{"name": "all", "type": "bool_or_bool_array"}],
)
@wraps(numpy.all, wrapper_attribute="__fnwrapped__")
def all(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'keepdims', 'where'] []
    res = numpy.all(
        a=a,
        axis=axis,
        # out=out,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.any",
    name="any",
    outputs=[{"name": "any", "type": "bool_or_bool_array"}],
)
@wraps(numpy.any, wrapper_attribute="__fnwrapped__")
def any(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'keepdims', 'where'] []
    res = numpy.any(
        a=a,
        axis=axis,
        # out=out,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isneginf",
    name="isneginf",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.isneginf, wrapper_attribute="__fnwrapped__")
def isneginf(
    x: array_like,
    # out: Optional[array_like] = None,
):  # params ['x'] ['out'] []
    res = numpy.isneginf(
        x,
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isposinf",
    name="isposinf",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.isposinf, wrapper_attribute="__fnwrapped__")
def isposinf(
    x: array_like,
    # out: Optional[array_like] = None,
):  # params ['x'] ['out'] []
    res = numpy.isposinf(
        x,
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.iscomplex",
    name="iscomplex",
    outputs=[{"name": "out", "type": "bool_or_bool_array"}],
)
@wraps(numpy.iscomplex, wrapper_attribute="__fnwrapped__")
def iscomplex(
    x: array_like,
):  # params ['x'] [] []
    res = numpy.iscomplex(
        x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.iscomplexobj",
    name="iscomplexobj",
    outputs=[{"name": "iscomplexobj", "type": "bool"}],
)
@wraps(numpy.iscomplexobj, wrapper_attribute="__fnwrapped__")
def iscomplexobj(
    x: ndarray_or_number,
):  # params ['x'] [] []
    res = numpy.iscomplexobj(
        x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isfortran",
    name="isfortran",
    outputs=[{"name": "isfortran", "type": "bool"}],
)
@wraps(numpy.isfortran, wrapper_attribute="__fnwrapped__")
def isfortran(
    a: ndarray,
):  # params ['a'] [] []
    res = numpy.isfortran(
        a=a,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isreal",
    name="isreal",
    outputs=[{"name": "out", "type": "bool_or_bool_array"}],
)
@wraps(numpy.isreal, wrapper_attribute="__fnwrapped__")
def isreal(
    x: array_like,
):  # params ['x'] [] []
    res = numpy.isreal(
        x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isrealobj",
    name="isrealobj",
    outputs=[{"name": "y", "type": "bool"}],
)
@wraps(numpy.isrealobj, wrapper_attribute="__fnwrapped__")
def isrealobj(
    x: ndarray_or_number,
):  # params ['x'] [] []
    res = numpy.isrealobj(
        x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isscalar",
    name="isscalar",
    outputs=[{"name": "val", "type": "bool"}],
)
@wraps(numpy.isscalar, wrapper_attribute="__fnwrapped__")
def isscalar(
    element: ndarray_or_number,
):  # params ['element'] [] []
    res = numpy.isscalar(
        element=element,
    )
    return res


@fn.NodeDecorator(
    node_id="np.allclose",
    name="allclose",
    outputs=[{"name": "allclose", "type": "bool"}],
)
@wraps(numpy.allclose, wrapper_attribute="__fnwrapped__")
def allclose(
    a: array_like,
    b: array_like,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
):  # params ['a', 'b'] ['rtol', 'atol', 'equal_nan'] []
    res = numpy.allclose(
        a=a,
        b=b,
        rtol=rtol,
        atol=atol,
        equal_nan=equal_nan,
    )
    return res


@fn.NodeDecorator(
    node_id="np.isclose",
    name="isclose",
    outputs=[{"name": "y", "type": "array_like"}],
)
@wraps(numpy.isclose, wrapper_attribute="__fnwrapped__")
def isclose(
    a: array_like,
    b: array_like,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
):  # params ['a', 'b'] ['rtol', 'atol', 'equal_nan'] []
    res = numpy.isclose(
        a=a,
        b=b,
        rtol=rtol,
        atol=atol,
        equal_nan=equal_nan,
    )
    return res


@fn.NodeDecorator(
    node_id="np.array_equal",
    name="array_equal",
    outputs=[{"name": "b", "type": "bool"}],
)
@wraps(numpy.array_equal, wrapper_attribute="__fnwrapped__")
def array_equal(
    a1: array_like,
    a2: array_like,
    equal_nan: bool = False,
):  # params ['a1', 'a2'] ['equal_nan'] []
    res = numpy.array_equal(
        a1=a1,
        a2=a2,
        equal_nan=equal_nan,
    )
    return res


@fn.NodeDecorator(
    node_id="np.array_equiv",
    name="array_equiv",
    outputs=[{"name": "out", "type": "bool"}],
)
@wraps(numpy.array_equiv, wrapper_attribute="__fnwrapped__")
def array_equiv(
    a1: array_like,
    a2: array_like,
):  # params ['a1', 'a2'] [] []
    res = numpy.array_equiv(
        a1=a1,
        a2=a2,
    )
    return res


@fn.NodeDecorator(
    node_id="np.unwrap",
    name="unwrap",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.unwrap, wrapper_attribute="__fnwrapped__")
def unwrap(
    p: array_like,
    discont: Optional[float] = None,
    axis: Optional[int] = -1,
    period: Optional[float] = 6.283185307179586,
):  # params ['p'] ['discont', 'axis', 'period'] []
    res = numpy.unwrap(
        p=p,
        discont=discont,
        axis=axis,
        period=period,
    )
    return res


@fn.NodeDecorator(
    node_id="np.round",
    name="round",
    outputs=[{"name": "rounded_array", "type": "ndarray"}],
)
@wraps(numpy.round, wrapper_attribute="__fnwrapped__")
def round(
    a: array_like,
    decimals: Optional[int] = 0,
    # out: Optional[ndarray] = None,
):  # params ['a'] ['decimals', 'out'] []
    res = numpy.round(
        a=a,
        decimals=decimals,
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.fix",
    name="fix",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.fix, wrapper_attribute="__fnwrapped__")
def fix(
    x: array_like,
    # out: Optional[ndarray] = None,
):  # params ['x'] ['out'] []
    res = numpy.fix(
        x,
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.prod",
    name="prod",
    outputs=[{"name": "product_along_axis", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.prod, wrapper_attribute="__fnwrapped__")
def prod(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'keepdims'] []
    res = numpy.prod(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.sum",
    name="sum",
    outputs=[{"name": "sum_along_axis", "type": "ndarray"}],
)
@wraps(numpy.sum, wrapper_attribute="__fnwrapped__")
def sum(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'keepdims'] []
    res = numpy.sum(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanprod",
    name="nanprod",
    outputs=[{"name": "nanprod", "type": "ndarray"}],
)
@wraps(numpy.nanprod, wrapper_attribute="__fnwrapped__")
def nanprod(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'keepdims'] []
    res = numpy.nanprod(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nansum",
    name="nansum",
    outputs=[{"name": "nansum", "type": "ndarray."}],
)
@wraps(numpy.nansum, wrapper_attribute="__fnwrapped__")
def nansum(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'keepdims'] []
    res = numpy.nansum(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cumprod",
    name="cumprod",
    outputs=[{"name": "cumprod", "type": "ndarray"}],
)
@wraps(numpy.cumprod, wrapper_attribute="__fnwrapped__")
def cumprod(
    a: array_like,
    axis: Optional[int] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
):  # params ['a'] ['axis', 'dtype', 'out'] []
    res = numpy.cumprod(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cumsum",
    name="cumsum",
    outputs=[{"name": "cumsum_along_axis", "type": "ndarray."}],
)
@wraps(numpy.cumsum, wrapper_attribute="__fnwrapped__")
def cumsum(
    a: array_like,
    axis: Optional[int] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
):  # params ['a'] ['axis', 'dtype', 'out'] []
    res = numpy.cumsum(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nancumprod",
    name="nancumprod",
    outputs=[{"name": "nancumprod", "type": "ndarray"}],
)
@wraps(numpy.nancumprod, wrapper_attribute="__fnwrapped__")
def nancumprod(
    a: array_like,
    axis: Optional[int] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
):  # params ['a'] ['axis', 'dtype', 'out'] []
    res = numpy.nancumprod(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nancumsum",
    name="nancumsum",
    outputs=[{"name": "nancumsum", "type": "ndarray."}],
)
@wraps(numpy.nancumsum, wrapper_attribute="__fnwrapped__")
def nancumsum(
    a: array_like,
    axis: Optional[int] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
):  # params ['a'] ['axis', 'dtype', 'out'] []
    res = numpy.nancumsum(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
    )
    return res


@fn.NodeDecorator(
    node_id="np.diff",
    name="diff",
    outputs=[{"name": "diff", "type": "ndarray"}],
)
@wraps(numpy.diff, wrapper_attribute="__fnwrapped__")
def diff(
    a: array_like,
    n: Optional[int] = 1,
    axis: Optional[int] = -1,
    prepend: Optional[array_like] = NoValue,
    append: Optional[array_like] = NoValue,
):  # params ['a'] ['n', 'axis', 'prepend', 'append'] []
    res = numpy.diff(
        a=a,
        n=n,
        axis=axis,
        prepend=prepend,
        append=append,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ediff1d",
    name="ediff1d",
    outputs=[{"name": "ediff1d", "type": "ndarray"}],
)
@wraps(numpy.ediff1d, wrapper_attribute="__fnwrapped__")
def ediff1d(
    ary: array_like,
    to_end: Optional[array_like] = None,
    to_begin: Optional[array_like] = None,
):  # params ['ary'] ['to_end', 'to_begin'] []
    res = numpy.ediff1d(
        ary=ary,
        to_end=to_end,
        to_begin=to_begin,
    )
    return res


@fn.NodeDecorator(
    node_id="np.gradient",
    name="gradient",
    outputs=[{"name": "gradient", "type": "Union[ndarray, List[ndarray]]"}],
)
@wraps(numpy.gradient, wrapper_attribute="__fnwrapped__")
def gradient(
    f: array_like,
    varargs: Optional[List[ndarray_or_scalar]] = None,
    edge_order: Optional[Literal[1, 2]] = 1,
    axis: Optional[axis_like] = None,
):  # params ['f'] ['varargs', 'axis', 'edge_order'] []
    if varargs is None:
        varargs = []
    res = numpy.gradient(
        f,
        *varargs,
        edge_order=edge_order,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.cross",
    name="cross",
    outputs=[{"name": "c", "type": "ndarray"}],
)
@wraps(numpy.cross, wrapper_attribute="__fnwrapped__")
def cross(
    a: array_like,
    b: array_like,
    axisa: Optional[int] = -1,
    axisb: Optional[int] = -1,
    axisc: Optional[int] = -1,
    axis: Optional[int] = None,
):  # params ['a', 'b'] ['axisa', 'axisb', 'axisc', 'axis'] []
    res = numpy.cross(
        a=a,
        b=b,
        axisa=axisa,
        axisb=axisb,
        axisc=axisc,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.trapz",
    name="trapz",
    outputs=[{"name": "trapz", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.trapz, wrapper_attribute="__fnwrapped__")
def trapz(
    y: array_like,
    x: Optional[array_like] = None,
    dx: Optional[scalar] = 1.0,
    axis: Optional[int] = -1,
):  # params ['y'] ['x', 'dx', 'axis'] []
    res = numpy.trapz(
        y=y,
        x=x,
        dx=dx,
        axis=axis,
    )
    return res


@fn.NodeDecorator(
    node_id="np.i0",
    name="i0",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.i0, wrapper_attribute="__fnwrapped__")
def i0(
    x: ndarray,
):  # params ['x'] [] []
    res = numpy.i0(
        x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.sinc",
    name="sinc",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.sinc, wrapper_attribute="__fnwrapped__")
def sinc(
    x: ndarray,
):  # params ['x'] [] []
    res = numpy.sinc(
        x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.angle",
    name="angle",
    outputs=[{"name": "angle", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.angle, wrapper_attribute="__fnwrapped__")
def angle(
    z: array_like,
    deg: Optional[bool] = False,
):  # params ['z'] ['deg'] []
    res = numpy.angle(
        z=z,
        deg=deg,
    )
    return res


@fn.NodeDecorator(
    node_id="np.real",
    name="real",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.real, wrapper_attribute="__fnwrapped__")
def real(
    val: array_like,
):  # params ['val'] [] []
    res = numpy.real(
        val=val,
    )
    return res


@fn.NodeDecorator(
    node_id="np.imag",
    name="imag",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.imag, wrapper_attribute="__fnwrapped__")
def imag(
    val: array_like,
):  # params ['val'] [] []
    res = numpy.imag(
        val=val,
    )
    return res


@fn.NodeDecorator(
    node_id="np.max",
    name="max",
    outputs=[{"name": "max", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.max, wrapper_attribute="__fnwrapped__")
def max(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'keepdims', 'initial', 'where'] []
    res = numpy.max(
        a=a,
        axis=axis,
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanmax",
    name="nanmax",
    outputs=[{"name": "nanmax", "type": "ndarray"}],
)
@wraps(numpy.nanmax, wrapper_attribute="__fnwrapped__")
def nanmax(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'keepdims', 'initial', 'where'] []
    res = numpy.nanmax(
        a=a,
        axis=axis,
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.min",
    name="min",
    outputs=[{"name": "min", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.min, wrapper_attribute="__fnwrapped__")
def min(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'keepdims', 'initial', 'where'] []
    res = numpy.min(
        a=a,
        axis=axis,
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanmin",
    name="nanmin",
    outputs=[{"name": "nanmin", "type": "ndarray"}],
)
@wraps(numpy.nanmin, wrapper_attribute="__fnwrapped__")
def nanmin(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    initial: Optional[scalar] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'keepdims', 'initial', 'where'] []
    res = numpy.nanmin(
        a=a,
        axis=axis,
        # out=out,
        keepdims=keepdims,
        initial=initial,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.convolve",
    name="convolve",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.convolve, wrapper_attribute="__fnwrapped__")
def convolve(
    a: ndarray,
    v: ndarray,
    mode: Optional[Literal["full", "valid", "same"]] = "full",
):  # params ['a', 'v'] ['mode'] []
    res = numpy.convolve(
        a=a,
        v=v,
        mode=mode,
    )
    return res


@fn.NodeDecorator(
    node_id="np.clip",
    name="clip",
    outputs=[{"name": "clipped_array", "type": "ndarray"}],
)
@wraps(numpy.clip, wrapper_attribute="__fnwrapped__")
def clip(
    a: array_like,
    a_min: array_like or None,
    a_max: array_like or None,
    # out: Optional[ndarray] = None,
    # where: Union[bool_array, bool] = True,
    # casting: casting_literal = "same_kind",
    # order: OrderKACF = "K",
    dtype: Optional[DTYPE_ENUM] = None,
    # subok: bool = True,
    # signature: Any = None,
    # extobj: Any = None,
):  # params ['a', 'a_min', 'a_max'] ['out'] []
    res = numpy.clip(
        a=a,
        a_min=a_min,
        a_max=a_max,
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
    node_id="np.nan_to_num",
    name="nan_to_num",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.nan_to_num, wrapper_attribute="__fnwrapped__")
def nan_to_num(
    x: ndarray_or_scalar,
    copy: Optional[bool] = True,
    nan: Union[float, int] = 0.0,
    posinf: Union[float, int, None] = None,
    neginf: Union[float, int, None] = None,
):  # params ['x'] ['copy', 'nan', 'posinf', 'neginf'] []
    res = numpy.nan_to_num(
        x,
        copy=copy,
        nan=nan,
        posinf=posinf,
        neginf=neginf,
    )
    return res


@fn.NodeDecorator(
    node_id="np.real_if_close",
    name="real_if_close",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.real_if_close, wrapper_attribute="__fnwrapped__")
def real_if_close(
    a: array_like,
    tol: float = 100,
):  # params ['a'] ['tol'] []
    res = numpy.real_if_close(
        a=a,
        tol=tol,
    )
    return res


@fn.NodeDecorator(
    node_id="np.interp",
    name="interp",
    outputs=[{"name": "y", "type": "ndarray_or_number"}],
)
@wraps(numpy.interp, wrapper_attribute="__fnwrapped__")
def interp(
    x: array_like,
    xp: Sequence[float],
    fp: Sequence[float],
    left: Optional[float] = None,
    right: Optional[float] = None,
    period: Optional[float] = None,
):  # params ['x', 'xp', 'fp'] ['left', 'right', 'period'] []
    res = numpy.interp(
        x,
        xp=xp,
        fp=fp,
        left=left,
        right=right,
        period=period,
    )
    return res


@fn.NodeDecorator(
    node_id="np.ptp",
    name="ptp",
    outputs=[{"name": "ptp", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.ptp, wrapper_attribute="__fnwrapped__")
def ptp(
    a: array_like,
    axis: Optional[axis_like] = None,
    out: array_like = None,
    keepdims: Optional[bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'keepdims'] []
    res = numpy.ptp(
        a=a,
        axis=axis,
        # out=out,
        keepdims=keepdims,
    )
    return res


@fn.NodeDecorator(
    node_id="np.percentile",
    name="percentile",
    outputs=[{"name": "percentile", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.percentile, wrapper_attribute="__fnwrapped__")
def percentile(
    a: ndarray,
    q: ndarray,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    overwrite_input: Optional[bool] = False,
    method: Optional[str] = "linear",
    keepdims: Optional[bool] = False,
    interpolation: Optional[str] = None,
):  # params ['a', 'q'] ['axis', 'out'] []
    res = numpy.percentile(
        a=a,
        q=q,
        axis=axis,
        # out=out,
        overwrite_input=overwrite_input,
        method=method,
        keepdims=keepdims,
        interpolation=interpolation,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanpercentile",
    name="nanpercentile",
    outputs=[{"name": "percentile", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.nanpercentile, wrapper_attribute="__fnwrapped__")
def nanpercentile(
    a: array_like,
    q: ndarray,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    overwrite_input: Optional[bool] = False,
    method: Optional[str] = "linear",
    keepdims: Optional[bool] = NoValue,
    interpolation: Optional[str] = None,
):  # params ['a', 'q'] ['axis', 'out'] []
    res = numpy.nanpercentile(
        a=a,
        q=q,
        axis=axis,
        # out=out,
        overwrite_input=overwrite_input,
        method=method,
        keepdims=keepdims,
        interpolation=interpolation,
    )
    return res


@fn.NodeDecorator(
    node_id="np.quantile",
    name="quantile",
    outputs=[{"name": "quantile", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.quantile, wrapper_attribute="__fnwrapped__")
def quantile(
    a: ndarray,
    q: ndarray,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    overwrite_input: Optional[bool] = False,
    method: Optional[str] = "linear",
    keepdims: Optional[bool] = False,
    interpolation: Optional[str] = None,
):  # params ['a', 'q'] ['axis', 'out', 'overwrite_input'] []
    res = numpy.quantile(
        a=a,
        q=q,
        axis=axis,
        # out=out,
        overwrite_input=overwrite_input,
        method=method,
        keepdims=keepdims,
        interpolation=interpolation,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanquantile",
    name="nanquantile",
    outputs=[{"name": "quantile", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.nanquantile, wrapper_attribute="__fnwrapped__")
def nanquantile(
    a: array_like,
    q: ndarray,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    overwrite_input: Optional[bool] = False,
    method: Optional[str] = "linear",
    keepdims: Optional[bool] = NoValue,
    interpolation: Optional[str] = None,
):  # params ['a', 'q'] ['axis', 'out'] []
    res = numpy.nanquantile(
        a=a,
        q=q,
        axis=axis,
        # out=out,
        overwrite_input=overwrite_input,
        method=method,
        keepdims=keepdims,
        interpolation=interpolation,
    )
    return res


@fn.NodeDecorator(
    node_id="np.median",
    name="median",
    outputs=[{"name": "median", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.median, wrapper_attribute="__fnwrapped__")
def median(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    overwrite_input: Optional[bool] = False,
    keepdims: Optional[bool] = False,
):  # params ['a'] ['axis', 'out', 'overwrite_input', 'keepdims'] []
    res = numpy.median(
        a=a,
        axis=axis,
        # out=out,
        overwrite_input=overwrite_input,
        keepdims=keepdims,
    )
    return res


@fn.NodeDecorator(
    node_id="np.average",
    name="average",
    outputs=[
        {"name": "retval", "type": "ndarray_or_scalar"},
        {"name": "sum_of_weights", "type": "ndarray_or_scalar"},
    ],
)
@wraps(numpy.average, wrapper_attribute="__fnwrapped__")
def average(
    a: array_like,
    axis: Optional[axis_like] = None,
    weights: Optional[array_like] = None,
    # returned: Optional[bool] = False,
    # keepdims: Optional[bool] = NoValue,
):  # params ['a'] ['axis', 'weights', 'returned', 'keepdims'] []
    res = numpy.average(
        a=a,
        axis=axis,
        weights=weights,
        returned=True,
        # returned=returned,
        # keepdims=keepdims,
    )
    print("AAA", res)
    return res


@fn.NodeDecorator(
    node_id="np.mean",
    name="mean",
    outputs=[{"name": "m", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.mean, wrapper_attribute="__fnwrapped__")
def mean(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'keepdims', 'where'] []
    res = numpy.mean(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.std",
    name="std",
    outputs=[{"name": "standard_deviation", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.std, wrapper_attribute="__fnwrapped__")
def std(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    ddof: Optional[int] = 0,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'ddof', 'keepdims', 'where'] []
    res = numpy.std(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        ddof=ddof,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.var",
    name="var",
    outputs=[{"name": "variance", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.var, wrapper_attribute="__fnwrapped__")
def var(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    ddof: Optional[int] = 0,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'ddof', 'keepdims', 'where'] []
    res = numpy.var(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        ddof=ddof,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanmedian",
    name="nanmedian",
    outputs=[{"name": "median", "type": "ndarray"}],
)
@wraps(numpy.nanmedian, wrapper_attribute="__fnwrapped__")
def nanmedian(
    a: array_like,
    axis: Optional[axis_like] = None,
    # out: Optional[ndarray] = None,
    overwrite_input: Optional[bool] = False,
    keepdims: Optional[bool] = NoValue,
):  # params ['a'] ['axis', 'out', 'overwrite_input'] []
    res = numpy.nanmedian(
        a=a,
        axis=axis,
        # out=out,
        overwrite_input=overwrite_input,
        keepdims=keepdims,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanmean",
    name="nanmean",
    outputs=[{"name": "m", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.nanmean, wrapper_attribute="__fnwrapped__")
def nanmean(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'keepdims', 'where'] []
    res = numpy.nanmean(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanstd",
    name="nanstd",
    outputs=[{"name": "standard_deviation", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.nanstd, wrapper_attribute="__fnwrapped__")
def nanstd(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    ddof: Optional[int] = 0,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'ddof'] []
    res = numpy.nanstd(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        ddof=ddof,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.nanvar",
    name="nanvar",
    outputs=[{"name": "variance", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.nanvar, wrapper_attribute="__fnwrapped__")
def nanvar(
    a: array_like,
    axis: Optional[axis_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
    # out: Optional[ndarray] = None,
    ddof: Optional[int] = 0,
    keepdims: Optional[bool] = NoValue,
    # where: Union[bool_array, bool] = NoValue,
):  # params ['a'] ['axis', 'dtype', 'out', 'ddof'] []
    res = numpy.nanvar(
        a=a,
        axis=axis,
        dtype=dtype_from_name(dtype),
        # out=out,
        ddof=ddof,
        keepdims=keepdims,
        # where=where,
    )
    return res


@fn.NodeDecorator(
    node_id="np.corrcoef",
    name="corrcoef",
    outputs=[{"name": "R", "type": "ndarray"}],
)
@wraps(numpy.corrcoef, wrapper_attribute="__fnwrapped__")
def corrcoef(
    x: array_like,
    y: Optional[array_like] = None,
    rowvar: Optional[bool] = True,
    dtype: Optional[DTYPE_ENUM] = None,
):  # params ['x'] ['y', 'rowvar', 'bias', 'ddof', 'dtype'] []
    res = numpy.corrcoef(
        x,
        y=y,
        rowvar=rowvar,
        dtype=dtype_from_name(dtype),
    )
    return res


@fn.NodeDecorator(
    node_id="np.correlate",
    name="correlate",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.correlate, wrapper_attribute="__fnwrapped__")
def correlate(
    a: array_like,
    v: array_like,
    mode: Optional[Literal["valid", "same", "full"]] = "valid",
):
    res = numpy.correlate(a=a, v=v, mode=mode)
    return res


@fn.NodeDecorator(
    node_id="np.cov",
    name="cov",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.cov, wrapper_attribute="__fnwrapped__")
def cov(
    m: array_like,
    y: Optional[array_like] = None,
    rowvar: Optional[bool] = True,
    bias: Optional[bool] = False,
    ddof: Optional[int] = None,
    fweights: Union[array_like, int, None] = None,
    aweights: Optional[array_like] = None,
    dtype: Optional[DTYPE_ENUM] = None,
):  # params ['m'] ['y', 'rowvar', 'bias', 'ddof', 'fweights'] []
    res = numpy.cov(
        m=m,
        y=y,
        rowvar=rowvar,
        bias=bias,
        ddof=ddof,
        fweights=fweights,
        aweights=aweights,
        dtype=dtype_from_name(dtype),
    )
    return res


@fn.NodeDecorator(
    node_id="np.histogram",
    name="histogram",
    outputs=[
        {"name": "hist", "type": "ndarray"},
        {"name": "bin_edges", "type": "ndarray"},
    ],
)
@wraps(numpy.histogram, wrapper_attribute="__fnwrapped__")
def histogram(
    a: array_like,
    bins: Union[int, Union[Sequence[scalar], Sequence[str]]] = 10,
    range: Optional[Tuple[float, float]] = None,
    weights: Optional[array_like] = None,
    density: Optional[bool] = None,
):  # params ['a'] ['bins', 'range', 'density', 'weights'] []
    res = numpy.histogram(
        a=a,
        bins=bins,
        range=range,
        weights=weights,
        density=density,
    )
    return res


@fn.NodeDecorator(
    node_id="np.histogram2d",
    name="histogram2d",
    outputs=[
        {"name": "H", "type": "ndarray"},
        {"name": "xedges", "type": "ndarray"},
        {"name": "yedges", "type": "ndarray"},
    ],
)
@wraps(numpy.histogram2d, wrapper_attribute="__fnwrapped__")
def histogram2d(
    x: array_like,
    y: array_like,
    bins: Union[int, ndarray, Tuple[Union[int, ndarray], Union[int, ndarray]]] = 10,
    range: Optional[array_like] = None,
    density: Optional[bool] = None,
    weights: Optional[array_like] = None,
):  # params ['x', 'y'] ['bins', 'range', 'density'] []
    res = numpy.histogram2d(
        x,
        y=y,
        bins=bins,
        range=range,
        density=density,
        weights=weights,
    )
    return res


@fn.NodeDecorator(
    node_id="np.histogramdd",
    name="histogramdd",
    outputs=[{"name": "H", "type": "ndarray"}, {"name": "edges", "type": "list"}],
)
@wraps(numpy.histogramdd, wrapper_attribute="__fnwrapped__")
def histogramdd(
    sample: array_like,
    bins: Union[int, Sequence[int]] = 10,
    range: Optional[Sequence[Tuple[float, float]]] = None,
    density: Optional[bool] = None,
    weights: Optional[ndarray] = None,
):  # params ['sample'] ['bins', 'range', 'density'] []
    res = numpy.histogramdd(
        sample=sample,
        bins=bins,
        range=range,
        density=density,
        weights=weights,
    )
    return res


@fn.NodeDecorator(
    node_id="np.bincount",
    name="bincount",
    outputs=[{"name": "out", "type": "int_array"}],
)
@wraps(numpy.bincount, wrapper_attribute="__fnwrapped__")
def bincount(
    x: bitarray,
    weights: Optional[array_like] = None,
    minlength: Optional[int] = 0,
):  # params ['x'] ['weights', 'minlength'] []
    res = numpy.bincount(
        x,
        weights=weights,
        minlength=minlength,
    )
    return res


@fn.NodeDecorator(
    node_id="np.histogram_bin_edges",
    name="histogram_bin_edges",
    outputs=[{"name": "bin_edges", "type": "ndarray"}],
)
@wraps(numpy.histogram_bin_edges, wrapper_attribute="__fnwrapped__")
def histogram_bin_edges(
    a: array_like,
    bins: Union[int, Union[Sequence[scalar], Sequence[str]]] = 10,
    range: Optional[Tuple[float, float]] = None,
    weights: Optional[array_like] = None,
):  # params ['a'] ['bins', 'range', 'weights'] []
    res = numpy.histogram_bin_edges(
        a=a,
        bins=bins,
        range=range,
        weights=weights,
    )
    return res


@fn.NodeDecorator(
    node_id="np.digitize",
    name="digitize",
    outputs=[{"name": "indices", "type": "int_array"}],
)
@wraps(numpy.digitize, wrapper_attribute="__fnwrapped__")
def digitize(
    x: array_like,
    bins: array_like,
    right: Optional[bool] = False,
):  # params ['x', 'bins'] ['right'] []
    res = numpy.digitize(
        x,
        bins=bins,
        right=right,
    )
    return res


@fn.NodeDecorator(
    node_id="np.where",
    name="where",
    outputs=[{"name": "out", "type": "ndarray"}],
)
@wraps(numpy.where, wrapper_attribute="__fnwrapped__")
def where(
    condition: Union[array_like],
    x: Optional[array_like] = None,
    y: Optional[array_like] = None,
):
    args = condition
    if x is not None and y is not None:
        args += (x, y)

    res = numpy.where(
        *args,
    )
    return res
