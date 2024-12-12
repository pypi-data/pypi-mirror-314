import numpy
import funcnodes as fn
from io import BytesIO


@fn.NodeDecorator(
    node_id="np.tonpy",
    name="to npy",
)
def to_npy(data: numpy.ndarray) -> fn.types.databytes:
    buffer = BytesIO()
    numpy.save(buffer, data)

    bdata = buffer.getvalue()
    buffer.close()
    return fn.types.databytes(bdata)
