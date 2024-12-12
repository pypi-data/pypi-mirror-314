from typing import Optional, Union
import numpy
from .._types import ndarray
from exposedfunctionality import controlled_wrapper as wraps
import funcnodes as fn


@fn.NodeDecorator(
    node_id="np.datetime64",
    name="datetime64",
    outputs=[{"name": "date", "type": "ndarray"}],
)
@wraps(numpy.datetime64, wrapper_attribute="__fnwrapped__")
def datetime64(
    x: Union[str, int, ndarray],
    unit: Optional[str] = None,
):
    a = (x,)
    if unit is not None:
        a += (unit,)
    res = numpy.datetime64(*a)
    return res
