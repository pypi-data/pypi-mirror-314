import numpy as np
import aidge_core


datatype_converter_aide2c = {
    aidge_core.dtype.float64 : "double",
    aidge_core.dtype.float32 : "float",
    aidge_core.dtype.float16 : "half_float::half",
    aidge_core.dtype.int8    : "int8_t",
    aidge_core.dtype.int16   : "int16_t",
    aidge_core.dtype.int32   : "int32_t",
    aidge_core.dtype.int64   : "int64_t",
    aidge_core.dtype.uint8   : "uint8_t",
    aidge_core.dtype.uint16  : "uint16_t",
    aidge_core.dtype.uint32  : "uint32_t",
    aidge_core.dtype.uint64  : "uint64_t"
}

def aidge2c(datatype):
    """Convert a aidge datatype to C type

    :param datatype: Aidge datatype to convert
    :type datatype: :py:object:`aidge_core.DataType`
    :return: A string representing the C type
    :rtype: string
    """
    if datatype in datatype_converter_aide2c:
        return datatype_converter_aide2c[datatype]
    else:
        raise ValueError(f"Unsupported {datatype} aidge datatype")
