import numpy as np

np_map = {
    np.dtype('uint8'): "UINT8",
    np.dtype('uint16'): "UINT16",
    np.dtype('uint32'): "UINT32",
    np.dtype('uint64'): "UINT64",
    np.dtype('int8'): "INT8",
    np.dtype('int16'): "INT16",
    np.dtype('int32'): "INT32",
    np.dtype('int64'): "INT64",
    np.dtype('float16'): "FP16",
    np.dtype('float32'): "FP32",
    np.dtype('float64'): "FP64"
}


def create_data(prompts, is_batch=False):
    inputs = {
        "inputs": []
    }
    for key, value in prompts.items():
        data, data_type, shape = extract_data(value)
        if is_batch:
            shape = [1] + shape
        inputs["inputs"].append(
            {
                "data": data,
                "name": key,
                "shape": shape,
                "datatype": data_type,
            }
        )

    return inputs


def extract_data(data):
    shape = []
    item = data
    if isinstance(item, np.ndarray):
        shape = list(item.shape)
        data = item.tolist()
        data_type = np_map.get(item.dtype)
        return data, data_type, shape
    elif isinstance(item, list):
        while isinstance(item, list):
            shape.append(len(item))
            item = item[0]
        if isinstance(item, str):
            data_type = "BYTES"
        elif isinstance(item, int):
            data_type = "INT64"
        elif isinstance(item, float):
            data_type = "FP64"
        elif isinstance(item, bool):
            data_type = "BOOL"
        else:
            raise ValueError("Data type not supported, supported types are str, int, float, bool. Use data instead of "
                             "prompts to provide custom data")
        return data, data_type, shape
    elif isinstance(item, str):
        return [item], "BYTES", [1]
    elif isinstance(item, int):
        return [item], "INT64", [1]
    elif isinstance(item, float):
        return [item], "FP64", [1]
    elif isinstance(item, bool):
        return [item], "BOOL", [1]
    else:
        raise ValueError("Data type not supported, supported types are list, np array, str, int, float, bool. "
                         "Use inputs instead of data to provide custom inputs")