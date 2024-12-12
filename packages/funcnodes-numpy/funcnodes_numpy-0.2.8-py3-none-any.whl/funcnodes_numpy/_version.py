import numpy


def get_version(raw_version: str) -> dict:
    major, minor, micro = (raw_version + ".0.0").replace("..", ".").split(".")[:3]

    major_int = int(major)
    minor_int = int(minor)
    try:
        micro_int = int(micro)
    except ValueError:
        micro_int = numpy.nan

    return {
        "version": raw_version,
        "major": major,
        "minor": minor,
        "micro": micro,
        "major_int": major_int,
        "minor_int": minor_int,
        "micro_int": micro_int,
    }


np_version = get_version(numpy.__version__)


version = "0.2.8"
