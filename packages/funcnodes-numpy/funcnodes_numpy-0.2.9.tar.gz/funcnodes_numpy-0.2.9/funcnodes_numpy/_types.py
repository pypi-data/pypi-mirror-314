import numpy
from typing import List, Union, Literal, Callable
from typing import TYPE_CHECKING

import exposedfunctionality.function_parser.types as exf_types

scalar = Union[float, int]
exf_types.add_type(Union[float, int], "scalar")
# exf_types.add_type(scalar, "scalar")
number = Union[complex, float, int]
exf_types.add_type(Union[complex, float, int], "number")
basic_types = Union[float, int, complex, str, bool]
exf_types.add_type(Union[float, int, complex, str, bool], "basic_types")
# exf_types.add_type(number, "number")

ndarray_or_scalar = Union[
    scalar,
    numpy.ndarray,
]
exf_types.add_type(Union[scalar, numpy.ndarray], "ndarray_or_scalar")
# exf_types.add_type(ndarray_or_scalar, "ndarray_or_scalar")

ndarray_or_number = Union[
    number,
    numpy.ndarray,
]
# exf_types.add_type(Union[numpy.ndarray, number], "ndarray_or_number")
exf_types.add_type(ndarray_or_number, "ndarray_or_number")

indices_or_sections = Union[int, List[int]]
# exf_types.add_type(Union[int, List[int]], "indices_or_sections")
exf_types.add_type(indices_or_sections, "indices_or_sections")

ndarray = numpy.ndarray
exf_types.add_type(ndarray, "ndarray")

shape_like = Union[numpy.ndarray, int, List[int]]
exf_types.add_type(shape_like, "shape_like")

axis_like = Union[int, List[int]]
exf_types.add_type(axis_like, "axis_like")


array_like = Union[basic_types, numpy.ndarray]
exf_types.add_type(array_like, "array_like")

int_array = ndarray
exf_types.add_type(int_array, "int_array")

bool_array = ndarray
exf_types.add_type(bool_array, "bool_array")

bitarray = ndarray  # uint8
exf_types.add_type(bitarray, "bitarray")

bool_or_bool_array = Union[bool, bool_array]
exf_types.add_type(bool_or_bool_array, "bool_or_bool_array")
# exf_types.add_type(bool_or_bool_array, "bool_or_bool_array")

int_bool_array = Union[int_array, bool_array]
exf_types.add_type(int_bool_array, "int_bool_array")
# exf_types.add_type(int_bool_array, "int_bool_array")

int_or_int_array = Union[int, int_array]
exf_types.add_type(int_or_int_array, "int_or_int_array")
# exf_types.add_type(int_or_int_array, "int_or_int_array")

real_array = ndarray
exf_types.add_type(real_array, "real_array")

matrix = ndarray
exf_types.add_type(matrix, "matrix")

OrderCF = Literal[None, "C", "F"]
exf_types.add_type(OrderCF, "OrderCF")
# exf_types.add_type(OrderCF, "OrderCF")

OrderKACF = Literal[None, "K", "A", "C", "F"]
exf_types.add_type(OrderKACF, "OrderKACF")
# exf_types.add_type(OrderKACF, "OrderKACF")

OrderACF = Literal[None, "A", "C", "F"]
exf_types.add_type(OrderACF, "OrderACF")
# exf_types.add_type(OrderACF, "OrderACF")

buffer_like = Union[bytes, bytearray, memoryview, ndarray]
exf_types.add_type(buffer_like, "buffer_like")
# exf_types.add_type(buffer_like, "buffer_like")

if TYPE_CHECKING:
    str_array = numpy._ArrayLikeStr_co
    exf_types.add_type(str_array, "str_array")
else:
    str_array = numpy._typing._ArrayLikeStr_co
    exf_types.add_type(str_array, "str_array")
# exf_types.add_type(str_array, "str_array")

UNSET = object()
NoValue = numpy._NoValue
exf_types.add_type(NoValue, "<no value>")
UnKnOWn = object()
casting_literal = Literal["no", "equiv", "safe", "same_kind", "unsafe"]
exf_types.add_type(casting_literal, "casting_literal")
# exf_types.add_type(casting_literal, "casting_literal")


Ufunc = Callable
exf_types.add_type(Ufunc, "Ufunc")
