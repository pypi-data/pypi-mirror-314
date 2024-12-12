import funcnodes as fn
from typing import (
    Union,
    List,
    Optional,
    Iterable,
    Tuple,
    Sequence,
    Literal,
    Any,
    Callable,
)

from exposedfunctionality import controlled_wrapper as wraps
import numpy

from ._core.ufuncs import euler_gamma, pi, e

NODE_SHELF = fn.Shelf(
    name="constants",
    description="constants",
    nodes=[e, euler_gamma, pi],
    subshelves=[],
)
