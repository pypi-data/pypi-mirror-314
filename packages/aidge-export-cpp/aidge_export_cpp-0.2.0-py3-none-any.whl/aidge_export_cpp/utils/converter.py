import numpy as np

def numpy_dtype2ctype(dtype):
    if dtype == np.int8:
        return "int8_t"
    elif dtype == np.int16:
        return "int16_t"
    elif dtype == np.int32:
        return "int32_t"
    elif dtype == np.int64:
        return "int64_t"
    elif dtype == np.float32:
        return "float"
    elif dtype == np.float64:
        return "double"
    # Add more dtype mappings as needed
    else:
        raise ValueError(f"Unsupported {dtype} dtype")
