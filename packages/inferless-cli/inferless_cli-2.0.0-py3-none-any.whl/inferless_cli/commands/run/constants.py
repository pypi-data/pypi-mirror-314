MODEL_DATA_TYPE_MAPPING = {
    "BOOL": "TYPE_BOOL",
    "UINT8": "TYPE_UINT8",
    "UINT16": "TYPE_UINT16",
    "UINT32": "TYPE_UINT32",
    "UINT64": "TYPE_UINT64",
    "INT8": "TYPE_INT8",
    "INT16": "TYPE_INT16",
    "INT32": "TYPE_INT32",
    "INT64": "TYPE_INT64",
    "FP16": "TYPE_FP16",
    "FP32": "TYPE_FP32",
    "FP64": "TYPE_FP64",
    "BYTES": "TYPE_STRING",
    "STRING": "BYTES",
    "BF16": "TYPE_BF16",
}
MODEL_TRITON_DATA_TYPE_MAPPING = {
    "BOOL": "BOOL",
    "UINT8": "UINT8",
    "UINT16": "UINT16",
    "UINT32": "UINT32",
    "UINT64": "UINT64",
    "INT8": "INT8",
    "INT16": "INT16",
    "INT32": "INT32",
    "INT64": "INT64",
    "FP16": "FP16",
    "FP32": "FP32",
    "FP64": "FP64",
    "BYTES": "BYTES",
    "STRING": "BYTES",
    "BF16": "BF16",
}

MODEL_DIR_STRING = "##model_dir_path##"

BUILDING_DOCKER_MSG = "Building the Docker Image (Might take some time. Please wait...)"

HF_HOME = "/tmp/hf-cache"
