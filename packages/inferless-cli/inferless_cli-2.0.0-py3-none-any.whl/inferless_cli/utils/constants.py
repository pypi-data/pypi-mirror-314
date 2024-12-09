from inferless_cli.utils.credentials import select_url


BASE_URL_PROD = "https://api.inferless.com/api"
WEB_URL_PROD = "https://console.inferless.com"

BASE_URL_DEV = "https://devapi.inferless.com/api"
WEB_URL_DEV = "https://console-dev.inferless.com"

BASE_URL = select_url(BASE_URL_DEV, BASE_URL_PROD)
WEB_URL = select_url(WEB_URL_DEV, WEB_URL_PROD)

DOCS_URL = "https://docs.inferless.com"

# Browser endpoints
CLI_AUTH_URL = f"{WEB_URL}/user/keys"
IO_DOCS_URL = "https://docs.inferless.com/model-import/input-output-schema"
RUNTIME_DOCS_URL = "https://docs.inferless.com/model-import/bring-custom-packages"


# API endpoints
GET_CONNECTED_ACCOUNTS_URL = f"{BASE_URL}/accounts/list/connected/"
GET_ACCOUNTS_URL = f"{BASE_URL}/accounts/list/"
GET_WORKSPACE_REGIONS = f"{BASE_URL}/model_import/workspace/region-wise/"
GET_MACHINES = f"{BASE_URL}/model_import/machines/get/"
GET_VOLUMES_LIST_URL = f"{BASE_URL}/volumes/list/"
GET_VOLUME_INFO_URL = f"{BASE_URL}/volumes/fetch_volume_details_with_name/"
GET_VOLUME_INFO_BY_ID = f"{BASE_URL}/volumes/fetch_volume_details_with_id/"
GET_VOLUME_BY_NAME= f"{BASE_URL}/volumes/id/get/"
GET_RUNTIME_BY_NAME= f"{BASE_URL}/workspace/template/id/get/"
GET_SECRETS_BY_NAME= f"{BASE_URL}/users/secrets/id/get/"
GET_HF_DEFAULT_FILES_DATA= f"{BASE_URL}/model_import/huggingface/files/get/"
CREATE_VOLUME_URL = f"{BASE_URL}/volumes/create/"
DELETE_S3_VOLUME_URL = f"{BASE_URL}/volumes/s3-delete/"
DELETE_S3_VOLUME_TEMP_DIR = f"{BASE_URL}/volumes/s3-delete-temp-volume/"
SYNC_S3_TO_NFS = f"{BASE_URL}/volumes/s3-nfs-sync/"
SYNC_S3_TO_S3 = f"{BASE_URL}/volumes/s3-to-s3-sync/"
GET_TEMPLATES_LIST_URL = f"{BASE_URL}/workspace/models/templates/list/"
GET_WORKSPACE_MODELS_URL = f"{BASE_URL}/workspace/models/list/"
DELETE_MODEL_URL = f"{BASE_URL}/workspace/models/delete/"
DEACTIVATE_MODEL_URL = f"{BASE_URL}/models/deactivate/"
REBUILD_MODEL_URL = f"{BASE_URL}/model_import/rebuild_model/"
ACTIVATE_MODEL_URL = f"{BASE_URL}/models/activate/"
VALIDATE_TOKEN_URL = f"{BASE_URL}/cli-tokens/exchange/"
GET_WORKSPACES = f"{BASE_URL}/workspace/list"
IMPORT_MODEL_URL = f"{BASE_URL}/model_import/create_update/"
UPLOAD_IO_URL = f"{BASE_URL}/model_import/model_input_output_files/"
UPDATE_MODEL_CONFIGURATIONS_URL = f"{BASE_URL}/model_import/model_configuration/"
UPDATE_MAIN_MODEL_CONFIGURATIONS_URL = f"{BASE_URL}/models/config/update/"
START_IMPORT_URL = f"{BASE_URL}/model_import/start_import/"
GET_MODEL_DETAILS_URL = f"{BASE_URL}/model_import"
GET_MODEL_FULL_DETAILS_URL = f"{BASE_URL}/workspace/models/details/"
GET_USER_SECRETS_URL = f"{BASE_URL}/users/secrets/list/"
GET_VOLUMES_WORKSPACE_URL = f"{BASE_URL}/users/secrets/list/"
GET_VOLUMES_FILES_URL = f"{BASE_URL}/volumes/files/"
GET_MODEL_BUILD_LOGS_URL = f"{BASE_URL}/models/logs/build/v2/"
GET_MODEL_CALL_LOGS_URL = f"{BASE_URL}/models/logs/inference/v2/"
GET_MODEL_CODE_URL = f"{BASE_URL}/models/code/"
VALIDATE_IMPORT_MODEL_URL = f"{BASE_URL}/model_import/validate_model/"
VALIDATE_GITHUB_URL_PERMISIONS_URL = f"{BASE_URL}/model_import/check_git_permission/"
SET_VARIABLES_URL = f"{BASE_URL}/model_import/enviornment/update/"
INITILIZE_MODEL_UPLOAD_URL = (
    f"{BASE_URL}/model_import/uploads/initializeMultipartUpload/"
)
GET_SIGNED_URL_FOR_MODEL_UPLOAD_URL = (
    f"{BASE_URL}/model_import/uploads/getMultipartPreSignedUrls/"
)
SET_INTEGRATIONS_URL = f"{BASE_URL}/accounts/set"
COMPLETE_MODEL_UPLOAD_URL = f"{BASE_URL}/model_import/uploads/finalizeMultipartUpload/"
PRESIGNED_URL = f"{BASE_URL}/users/presigned-url"
SAVE_RUNTIME_URL = f"{BASE_URL}/workspace/models/templates/create_update/"
LIST_RUNTIME_VERSIONS = f"{BASE_URL}/workspace/models/templates/versions/list/"
GET_CLI_UTIL_FILES = f"{BASE_URL}/cli/file/get/"
GET_MODEL_IMPORT_DEPLOY_STATUS = f"{BASE_URL}/model_import/get/model_info/"
SET_ONBOARDING_STATUS = f"{BASE_URL}/users/onboarding/state/set/"
GET_ONBOARDING_STATUS = f"{BASE_URL}/users/onboarding/state/get/"

# UI/UX constants
FRAMEWORKS = ["ONNX", "TENSORFLOW", "PYTORCH"]
UPLOAD_METHODS = ["GIT", "LOCAL"]
REGION_TYPES = ["region-1", "region-2"]
REGION_MAP = {
    "AZURE": "region-2",
    "AWS": "region-1",
    "SERVERLESS_AWS": "region-3",
    "SERVERLESS_GCP": "region-4",
    "AZURE-USEAST": "region-5",
}
REGION_MAP_KEYS = {
    "region-2": "AZURE",
    "region-1": "AWS",
    "region-3": "SERVERLESS_AWS",
    "region-4": "SERVERLESS_GCP",
    "region-5": "AZURE-USEAST",
}
REGION_MAP_VOLUME = {
    "AZURE": "region-2",
    "AWS": "region-1",
    "SERVERLESS_AWS": "region-3",
    "SERVERLESS_GCP": "region-4",
    "AZURE-USEAST": "region-5",
}
REGION_MAP_VOLUME_KEYS = {
    "region-2": "AZURE",
    "region-1": "AWS",
    "region-3": "SERVERLESS_AWS",
    "region-4": "SERVERLESS_GCP",
    "region-5": "AZURE-USEAST",
}
MACHINE_TYPE_SERVERS = ["SHARED", "DEDICATED"]
MACHINE_TYPE_SERVERS_DEF = [
    "SHARED - Efficiently running on half the capacity for optimal resource sharing.",
    "DEDICATED - Maximizing performance with full resource allocation.",
]

GITHUB = "GITHUB"
HUGGINGFACE = "HUGGINGFACE"
GIT = "GIT"


DEFAULT_YAML_FILE_NAME = "inferless.yaml"
DEFAULT_INPUT_FILE_NAME = "input.json"
DEFAULT_OUTPUT_FILE_NAME = "output.json"
DEFAULT_RUNTIME_FILE_NAME = "inferless-runtime-config.yaml"
DEFAULT_MACHINE_VALUES = {
    "shared": {
        "SERVERLESS_AWS": {
            "T4": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
            "A10": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
            "A100": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
        },
        "SERVERLESS_GCP": {
            "T4": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
            "A10": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
            "A100": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
        },
        "AWS": {
            "T4": {
                "min_cpu": "1.5",
                "max_cpu": "1.5",
                "cpu": "1.5",
                "memory": "7",
                "min_memory": "7",
                "max_memory": "7",
            },
            "A10": {
                "min_cpu": "3",
                "max_cpu": "3",
                "cpu": "3",
                "memory": "15",
                "min_memory": "15",
                "max_memory": "15",
            },
            "A100": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
        },
        "AZURE": {
            "T4": {
                "min_cpu": "1.5",
                "max_cpu": "1.5",
                "cpu": "1.5",
                "memory": "10",
                "min_memory": "10",
                "max_memory": "10",
            },
            "A100": {
                "min_cpu": "10",
                "max_cpu": "10",
                "cpu": "10",
                "memory": "100",
                "min_memory": "100",
                "max_memory": "100",
            },
            "A10": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
        },
    },
    "dedicated": {
        "SERVERLESS_AWS": {
            "T4": {
                "min_cpu": "3",
                "max_cpu": "3",
                "cpu": "3",
                "memory": "14",
                "min_memory": "14",
                "max_memory": "14",
            },
            "A10": {
                "min_cpu": "7",
                "max_cpu": "7",
                "cpu": "7",
                "memory": "30",
                "min_memory": "30",
                "max_memory": "30",
            },
            "A100": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
        },
        "SERVERLESS_GCP": {
            "T4": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
            "A10": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
            "A100": {
                "min_cpu": "20",
                "max_cpu": "20",
                "cpu": "20",
                "memory": "200",
                "min_memory": "200",
                "max_memory": "200",
            },
        },
        "AWS": {
            "T4": {
                "min_cpu": "3",
                "max_cpu": "3",
                "cpu": "3",
                "memory": "14",
                "min_memory": "14",
                "max_memory": "14",
            },
            "A10": {
                "min_cpu": "7",
                "max_cpu": "7",
                "cpu": "7",
                "memory": "30",
                "min_memory": "30",
                "max_memory": "30",
            },
            "A100": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
        },
        "AZURE": {
            "T4": {
                "min_cpu": "3",
                "max_cpu": "3",
                "cpu": "3",
                "memory": "20",
                "min_memory": "20",
                "max_memory": "20",
            },
            "A100": {
                "min_cpu": "20",
                "max_cpu": "20",
                "cpu": "20",
                "memory": "200",
                "min_memory": "200",
                "max_memory": "200",
            },
            "A10": {
                "min_cpu": "",
                "max_cpu": "",
                "cpu": "",
                "memory": "",
                "min_memory": "",
                "max_memory": "",
            },
        },
    },
}


DEFAULT_INFERLESS_YAML_FILE = """\
# Inferless config file (version: 2.0.0)
version: 2.0.0

name: TEST
import_source: GIT

# you can choose the options between ONNX, TENSORFLOW, PYTORCH, Only applicable for FILE type import.
source_framework_type: PYTORCH
"""



DEFAULT_INFERLESS_RUNTIME_YAML_FILE = """\
build:
  # cuda_version: we currently support 12.1.1 and 11.8.0.
  cuda_version: 12.1.1
  python_packages:
    # you can add more python packages here
  system_packages:
    # - "libssl-dev" #example
    # you can add system packages here
"""

GLITCHTIP_DSN = "https://7d9a4e0478da4efaa34b1f5c8191b820@app.glitchtip.com/5058"


PROVIDER_CHOICES = ["replicate", "inferless"]
PROVIDER_EXPORT_CHOICES = list(set(PROVIDER_CHOICES) - {"inferless"})


SPINNER_DESCRIPTION = "[progress.description]{task.description}"


DEFAULT_RUNTIME_YAML_DATA = """
build:
  cuda_version: '12.1.1'
  system_packages:
    - 'libssl-dev'
    - 'tesseract-ocr'
    - 'libtesseract-dev'
    - 'ffmpeg'
  python_packages:
    - 'accelerate==0.24.1'
    - 'boto3==1.28.1'
    - 'diffusers==0.24.0'
    - 'entrypoints==0.4'
    - 'ftfy==6.1.1'
    - 'jmespath==1.0.1'
    - 'mediapipe==0.10.1'
    - 'numpy==1.24.3'
    - 'onnx==1.14.0'
    - 'onnxruntime==1.15.1'
    - 'optimum==1.9.1'
    - 'pandas==2.0.3'
    - 'Pillow==10.0.0'
    - 'pydantic==1.10.11'
    - 'pytesseract==0.3.10'
    - 'python-multipart==0.0.6'
    - 'requests==2.31.0'
    - 'safetensors==0.4.1'
    - 'soundfile==0.12.1'
    - 'tensorflow==2.13.0'
    - 'torch==2.0.1'
    - 'transformers==4.35.2'
    - 'xformers==0.0.20'
"""