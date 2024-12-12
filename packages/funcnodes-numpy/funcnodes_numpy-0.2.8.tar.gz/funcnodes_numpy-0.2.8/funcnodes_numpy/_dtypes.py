import numpy as np
from typing import Literal, Dict, List, Union
import enum

dtypes: List[np.dtype] = [
    np.dtype("?"),  # bool
    np.dtype("S"),  # bytes
    np.dtype("c"),  # bytes8
    np.dtype("F"),  # complex64
    np.dtype("D"),  # complex128
    np.dtype("M"),  # datetime64
    np.dtype("e"),  # float16
    np.dtype("f"),  # float32
    np.dtype("d"),  # float64
    np.dtype("b"),  # int8
    np.dtype("h"),  # int16
    np.dtype("i"),  # int32
    np.dtype("q"),  # int64
    np.dtype("O"),  # object
    np.dtype("U"),  # str
    np.dtype("m"),  # timedelta64
    np.dtype("B"),  # uint8
    np.dtype("H"),  # uint16
    np.dtype("I"),  # uint32
    np.dtype("Q"),  # uint64
    np.dtype("V"),  # void
]
dtype_name_literal = Literal[
    "bool",
    "bytes",
    "bytes8",
    "complex64",
    "complex128",
    "datetime64",
    "float16",
    "float32",
    "float64",
    "int8",
    "int16",
    "int32",
    "int64",
    "object",
    "str",
    "timedelta64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
    "void",
]


class DTYPE_ENUM(enum.Enum):
    bool = np.dtype("?")
    bytes = np.dtype("S")
    bytes8 = np.dtype("c")
    complex64 = np.dtype("F")
    complex128 = np.dtype("D")
    datetime64 = np.dtype("M")
    float16 = np.dtype("e")
    float32 = np.dtype("f")
    float64 = np.dtype("d")
    int8 = np.dtype("b")
    int16 = np.dtype("h")
    int32 = np.dtype("i")
    int64 = np.dtype("q")
    object = np.dtype("O")
    str = np.dtype("U")
    timedelta64 = np.dtype("m")
    uint8 = np.dtype("B")
    uint16 = np.dtype("H")
    uint32 = np.dtype("I")
    uint64 = np.dtype("Q")
    void = np.dtype("V")

    def __str__(self):
        return self.name


# generate via:
# import numpy as np
# import re

# types = {}
# for k in dir(np):
#     attr = getattr(np, k)
#     if type(attr) == type(np.int64):
#         if issubclass(attr, np.number):
#             if attr not in types:
#                 types[attr] = []
#             types[attr].append(k)

#             # iterate over all characters
# # Prepare to collect dtype information
# dtypes = set()
# # Loop through characters that could represent numpy dtypes
# for i in range(0, 256):
#     c = chr(i).strip()
#     try:
#         dtype = np.dtype(c)
#     except (TypeError, SyntaxError):
#         continue

#     dtypes.add(dtype)


# # Define a custom sorting function
# def dtype_sort_key(dtype):
#     # Split dtype name into text and number (if any)
#     match = re.match(r"([a-zA-Z]+)(\d*)", dtype.name)
#     if match:
#         name_part, num_part = match.groups()
#         num_part = (
#             int(num_part) if num_part else -1
#         )  # Treat missing number as -1 for sorting
#         return name_part, num_part
#     return dtype.name, -1


# sorted_dtypes = sorted(list(dtypes), key=dtype_sort_key)
# _dtype_list = "\n".join(
#     [f"   np.dtype('{dtype.char}'), # {dtype.name}" for dtype in sorted_dtypes]
# )
# dtypes_string = f"dtypes: List[np.dtype] = [\n{_dtype_list}\n]"
# dtype_name_literal = f"""dtype_name_literal = Literal[{', '.join([f'"{dtype.name}"' for dtype in sorted_dtypes])}]"""
# enum_data = "".join(
#     [f'    {dtype.name} = np.dtype("{dtype.char}")\n' for dtype in sorted_dtypes]
# )

# dtype_enum = f"""
# class DTYPE_ENUM(enum.Enum):
# {enum_data}
#     """
# print(dtypes_string)
# print(dtype_name_literal)
# print(dtype_enum)


dtype_names = [dtype.name for dtype in dtypes]
dtypes_char = [dtype.char for dtype in dtypes]

DTYPE_NAME_MAP: Dict[dtype_name_literal, np.dtype] = {
    **{str(dtype): dtype for dtype in dtypes},
    **{dtype.name: dtype for dtype in dtypes},
}

import exposedfunctionality.function_parser.types as exf_types

for k, v in DTYPE_NAME_MAP.items():
    exf_types.add_type(v, k)


def dtype_from_name(name: Union[DTYPE_ENUM, dtype_name_literal, np.dtype]) -> np.dtype:
    if isinstance(name, np.dtype):
        return name
    if isinstance(name, DTYPE_ENUM):
        return name.value
    if isinstance(name, str):
        return DTYPE_NAME_MAP.get(name, None)
