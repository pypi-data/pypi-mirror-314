import os
from requests import HTTPError
import rich
import typer
from inferless_cli.utils.api import make_request
from inferless_cli.utils.constants import (
    CREATE_VOLUME_URL,
    DELETE_S3_VOLUME_TEMP_DIR,
    DELETE_S3_VOLUME_URL,
    GET_ACCOUNTS_URL,
    GET_CLI_UTIL_FILES,
    GET_CONNECTED_ACCOUNTS_URL,
    GET_HF_DEFAULT_FILES_DATA,
    GET_MACHINES,
    GET_MODEL_BUILD_LOGS_URL,
    GET_MODEL_CALL_LOGS_URL,
    GET_MODEL_IMPORT_DEPLOY_STATUS,
    GET_RUNTIME_BY_NAME,
    GET_SECRETS_BY_NAME,
    GET_USER_SECRETS_URL,
    GET_VOLUME_BY_NAME,
    GET_VOLUME_INFO_BY_ID,
    GET_VOLUME_INFO_URL,
    GET_VOLUMES_LIST_URL,
    GET_TEMPLATES_LIST_URL,
    GET_VOLUMES_FILES_URL,
    GET_WORKSPACE_REGIONS,
    LIST_RUNTIME_VERSIONS,
    PRESIGNED_URL,
    SAVE_RUNTIME_URL,
    SET_INTEGRATIONS_URL,
    SET_ONBOARDING_STATUS,
    SYNC_S3_TO_NFS,
    SYNC_S3_TO_S3,
    UPDATE_MAIN_MODEL_CONFIGURATIONS_URL,
    VALIDATE_TOKEN_URL,
    GET_WORKSPACES,
    GET_WORKSPACE_MODELS_URL,
    REBUILD_MODEL_URL,
    ACTIVATE_MODEL_URL,
    DEACTIVATE_MODEL_URL,
    DELETE_MODEL_URL,
    IMPORT_MODEL_URL,
    UPLOAD_IO_URL,
    SET_VARIABLES_URL,
    UPDATE_MODEL_CONFIGURATIONS_URL,
    VALIDATE_IMPORT_MODEL_URL,
    START_IMPORT_URL,
    GET_MODEL_CODE_URL,
    INITILIZE_MODEL_UPLOAD_URL,
    GET_SIGNED_URL_FOR_MODEL_UPLOAD_URL,
    COMPLETE_MODEL_UPLOAD_URL,
    GET_MODEL_DETAILS_URL,
    GET_MODEL_FULL_DETAILS_URL,
    VALIDATE_GITHUB_URL_PERMISIONS_URL,
)
from inferless_cli import __version__
from inferless_cli.utils.exceptions import (
    InferlessCLIError,
    ModelImportException,
    ServerError,
)
from inferless_cli.utils.helpers import (
    decrypt_cli_key,
    decrypt_tokens,
    log_exception,
    save_tokens,
    validate_jwt,
)

NO_DETAILS_MSG = "No details in response"
FAILED_TO_CREATE_MESSAGE = "Failed to create presigned url."


def get_connected_accounts(import_source):
    try:
        payload = {
            "import_source": import_source,
        }

        response = make_request(
            GET_CONNECTED_ACCOUNTS_URL, method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get connected accounts.")

def get_accounts():
    try:
        response = make_request(
            GET_ACCOUNTS_URL, method="GET", auth=True
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get connected accounts.")



def get_workspaces_list():
    try:
        response = make_request(GET_WORKSPACES, method="POST", auth=True)
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get workspaces")


def get_volumes_list(workspace_id: str):
    try:
        payload = {"workspace_id": workspace_id}

        response = make_request(
            GET_VOLUMES_LIST_URL, method="POST", auth=True, data=payload
        )

        if not response.json().get("details"):
            raise InferlessCLIError("Failed to get data from API.")

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get volume list.")


def get_volume_info(workspace_id: str, name: str, region: str):
    try:
        payload = {"workspace_id": workspace_id, "volume_name": name, "region": region}

        response = make_request(
            GET_VOLUME_INFO_URL, method="POST", auth=True, data=payload
        )

        if not response.json().get("details"):
            raise InferlessCLIError(NO_DETAILS_MSG)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get volume info")


def get_volume_info_with_id(workspace_id: str, id: str):
    try:
        payload = {"workspace_id": workspace_id, "volume_id": id}

        response = make_request(
            GET_VOLUME_INFO_BY_ID, method="POST", auth=True, data=payload
        )

        if not response.json().get("details"):
            raise InferlessCLIError(NO_DETAILS_MSG)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get volume info")


def create_volume(workspace_id: str, name: str, region: str):
    try:
        payload = {
            "workspace_id": workspace_id,
            "name": name,
            "region": region,
        }

        response = make_request(
            CREATE_VOLUME_URL, method="POST", auth=True, data=payload
        )

        if not response.json().get("details"):
            raise InferlessCLIError(NO_DETAILS_MSG)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to create volume")


def get_templates_list(workspace_id: str):
    try:
        payload = {"workspace_id": workspace_id}

        response = make_request(
            GET_TEMPLATES_LIST_URL, method="POST", auth=True, data=payload
        )

        response_json = response.json()

        return response_json["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get templates list.")


def create_presigned_url(
    payload,
    uuid,
    name,
    region,
    file_name,
    path,
    workspace_id,
    is_patch=False,
    runtime_id=None,
):

    try:
        response = make_request(PRESIGNED_URL, method="POST", auth=True, data=payload)
        data = response.json()
        if "details" in data:
            return upload_runtime(
                data["details"],
                uuid,
                name,
                region,
                file_name,
                path,
                workspace_id,
                is_patch,
                runtime_id,
            )
        raise ModelImportException(NO_DETAILS_MSG)
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def create_presigned_download_url(payload):
    try:
        response = make_request(PRESIGNED_URL, method="POST", auth=True, data=payload)

        response_json = response.json()

        return response_json["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def create_presigned_upload_url(payload, path):
    try:
        response = make_request(PRESIGNED_URL, method="POST", auth=True, data=payload)

        data = response.json()
        if data:
            return upload_volume_file(data["details"], path)
        raise InferlessCLIError(
            f"Upload failed with status code {response.status_code}"
        )
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def delete_volume_files_url(payload):
    try:
        response = make_request(
            DELETE_S3_VOLUME_URL, method="POST", auth=True, data=payload
        )
        if not response.json().get("details"):
            raise InferlessCLIError(NO_DETAILS_MSG)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def delete_volume_temp_dir(payload):
    try:
        response = make_request(
            DELETE_S3_VOLUME_TEMP_DIR, method="POST", auth=True, data=payload
        )
        if not response.json().get("details"):
            raise InferlessCLIError(NO_DETAILS_MSG)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def upload_volume_file(url, path):
    try:
        file_size = os.path.getsize(path)
        rich.print(f"Uploading {path}")
        with open(path, "rb") as file:
            response = make_request(
                url,
                method="PUT",
                data="" if file_size == 0 else file,
                auth=False,
                convert_json=False,
            )
            if response.status_code == 200:
                return {
                    "status": "success",
                }

            raise ModelImportException(
                f"Upload failed with status code {response.status_code}"
            )
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def get_file_download(url):
    try:
        response = make_request(
            url,
            method="GET",
            auth=False,
            convert_json=False,
        )
        return response
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to download the file. ")


def upload_runtime(
    url,
    uuid,
    name,
    region,
    file_name,
    path,
    workspace_id,
    is_patch,
    runtime_id,
):
    try:
        with open(path, "rb") as file:
            headers = {
                "Content-Type": "application/x-yaml",
                "x-amz-acl": "bucket-owner-full-control",
            }
            response = make_request(
                url,
                method="PUT",
                data=file,
                auth=False,
                headers=headers,
                convert_json=False,
            )
            if response.status_code == 200:
                payload = {
                    "workspace_id": workspace_id,
                    "name": name,
                    "template_url": f"{uuid}/{file_name}",
                    "region": region,
                }
                if is_patch and runtime_id:
                    payload["template_id"] = runtime_id
                    del payload["region"]

                return save_runtime(payload)

            raise ModelImportException(
                f"Upload failed with status code {response.status_code}"
            )
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(f"Upload failed with status code {response.status_code}")


def save_runtime(payload):
    try:
        response = make_request(
            SAVE_RUNTIME_URL, method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(f"Upload failed with status code {response.status_code}. ")


def list_runtime_versions(payload):
    try:
        response = make_request(
            LIST_RUNTIME_VERSIONS, method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(f"Upload failed with status code {response.status_code}. ")


def validate_cli_token(key, secret):
    try:
        payload = {"access_key": key, "secret_key": secret}
        headers = {"Content-Type": "application/json"}

        response = make_request(
            VALIDATE_TOKEN_URL, method="POST", headers=headers, auth=False, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to validate CLI Token")


def callback_with_auth_validation():
    min_version_required()
    get_auth_validation()


def get_auth_validation():
    try:
        error_statement = (
            "\n[red]Please login to Inferless using `inferless login`[/red]\n"
        )
        token, _, user_id, workspace_id, workspace_name = decrypt_tokens()
        if token is None:
            rich.print(error_statement)
            raise typer.Exit(1)

        key, secret = decrypt_cli_key()

        if not key or not secret:
            rich.print(error_statement)
            raise typer.Exit(1)

        if not validate_jwt(token):
            details = validate_cli_token(key, secret)
            if details["access"] and details["refresh"]:
                save_tokens(
                    details["access"],
                    details["refresh"],
                    user_id,
                    workspace_id,
                    workspace_name,
                )
    except InferlessCLIError as e:
        rich.print(e)
        raise typer.Exit(1)
    except Exception as e:
        log_exception(e)
        raise typer.Exit(1)


def min_version_required():
    try:
        error_statement = "Please update Inferless CLI using [bold][red]`pip install inferless-cli --upgrade`[/red][/bold] \n\n"
        version = get_latest_version()

        errmsg, error = compare_versions(__version__, version)
    except Exception as e:
        log_exception(e)
    if error:
        rich.print(f"{errmsg} \n\n{error_statement}")
        raise typer.Exit(1)


def compare_versions(current_version, latest_version):
    try:
        current_components = list(map(int, current_version.split(".")))
        latest_components = list(map(int, latest_version.split(".")))

        # Pad the shorter version with zeros to ensure equal length
        while len(current_components) < len(latest_components):
            current_components.append(0)
        while len(latest_components) < len(current_components):
            latest_components.append(0)

        # Compare each component
        for current, latest in zip(current_components, latest_components):
            if current < latest:
                return (
                    f"\ncurrent version ([blue]{current_version}[/blue]) is older than minimum required version ([blue]{latest_version}[/blue])",
                    True,
                )
            if current > latest:
                return f"{current_version} is newer than {latest_version}", False

        return f"{current_version} is the same as {latest_version}", False
    except Exception as e:
        log_exception(e)
        return "Something went wrong while checking versions", True


def get_latest_version():
    try:
        response = make_request(
            "https://pypi.org/pypi/inferless-cli/json", method="GET", auth=False
        )
        return response.json()["info"]["version"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        return None


def get_workspace_models(workspace_id, workspace_filter="NONE"):
    try:
        payload = {
            "filter_by": workspace_filter,
            "search": "",
            "sort_by": "-updated_at",
            "workspace_id": workspace_id,
        }
        response = make_request(
            GET_WORKSPACE_MODELS_URL, method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to fetch models")


def rebuild_model(model_id):
    try:
        payload = {
            "id": model_id,
        }
        response = make_request(
            REBUILD_MODEL_URL, method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to rebuild model. ")


def delete_model(model_id):
    try:
        payload = {
            "model_id": model_id,
        }
        response = make_request(
            DELETE_MODEL_URL, method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to delete model.")


def activate_model(model_id):
    try:
        payload = {
            "min_replica": 0,
            "max_replica": 1,
            "model_id": model_id,
        }
        response = make_request(
            ACTIVATE_MODEL_URL, method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to activate model. ")


def deactivate_model(model_id):
    try:
        payload = {
            "min_replica": 0,
            "max_replica": 0,
            "model_id": model_id,
        }
        response = make_request(
            DEACTIVATE_MODEL_URL, method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to deactivate model. ")


def import_model(data):
    try:
        response = make_request(IMPORT_MODEL_URL, method="POST", auth=True, data=data)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to import model. ")


def upload_io(data):
    try:
        response = make_request(UPLOAD_IO_URL, method="POST", auth=True, data=data)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Error in Inputs and Outputs")


def update_model_configuration(data):
    try:
        response = make_request(
            UPDATE_MODEL_CONFIGURATIONS_URL, method="POST", auth=True, data=data
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to update model configuration. ")
    
def update_main_model_configuration(data):
    try:
        response = make_request(
            UPDATE_MAIN_MODEL_CONFIGURATIONS_URL, method="POST", auth=True, data=data
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to update model configuration. ")


def validate_import_model(data):
    try:
        response = make_request(
            VALIDATE_IMPORT_MODEL_URL, method="POST", auth=True, data=data
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to validate import model. ")


def set_env_variables(data):
    try:
        response = make_request(SET_VARIABLES_URL, method="POST", auth=True, data=data)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to set environment variables. ")


def start_import_model(data):
    try:
        response = make_request(START_IMPORT_URL, method="POST", auth=True, data=data)

        return response.json()["details"]
    except HTTPError as http_err:
        if http_err.response.status_code == 404:
            raise ModelImportException("Model Import Id not found")
        log_exception(http_err)
        raise ServerError("Failed to start import model.")
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to start import model.")


def get_model_import_status(id):
    try:
        data = {
            "model_import_id": id
        }
        response = make_request(
           GET_MODEL_IMPORT_DEPLOY_STATUS, method="POST", auth=True ,data=data
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get model import details.")

def get_model_import_details(id):
    try:
        response = make_request(
            f"{GET_MODEL_DETAILS_URL}/{id}/get/", method="GET", auth=True
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get model import details.")


def get_model_code(id):
    try:
        payload = {
            "model_id": id,
        }
        response = make_request(
            f"{GET_MODEL_CODE_URL}", method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get model code. ")


def get_model_details(id):
    try:
        payload = {
            "model_id": id,
        }
        response = make_request(
            f"{GET_MODEL_FULL_DETAILS_URL}", method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get model details.")


def get_user_secrets():
    try:
        payload = {}
        response = make_request(
            f"{GET_USER_SECRETS_URL}", method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get user secrets.")


def validate_github_url_permissions(url):
    try:
        payload = {
            "url": url,
        }
        response = make_request(
            VALIDATE_GITHUB_URL_PERMISIONS_URL, method="POST", auth=True, data=payload
        )

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to validate github url permissions.")


def initialize_model_upload(key):
    try:
        payload = {
            "key": key,
        }
        response = make_request(
            INITILIZE_MODEL_UPLOAD_URL, method="POST", auth=True, data=payload
        )

        return response.json()
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to initialize model upload.")


def get_signed_url_for_model_upload(key, upload_id, no_of_parts):
    try:
        payload = {
            "key": key,
            "upload_id": upload_id,
            "no_of_parts": no_of_parts,
        }
        response = make_request(
            GET_SIGNED_URL_FOR_MODEL_UPLOAD_URL, method="POST", auth=True, data=payload
        )

        return response.json()
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get signed url for model upload. ")


def complate_model_upload(key, upload_id, parts):
    try:
        payload = {
            "key": key,
            "upload_id": upload_id,
            "parts": parts,
        }
        response = make_request(
            COMPLETE_MODEL_UPLOAD_URL, method="POST", auth=True, data=payload
        )

        return response
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to complete model upload. ")


def upload_file(selected_file, key, file_size, upload_type="ZIP"):
    try:
        initialize_data = initialize_model_upload(key)
        if initialize_data.get("status") == "success" and initialize_data.get(
            "details", {}
        ).get("upload_id"):
            chunk_size = 50 * 1024**2  # 50 MiB
            chunk_count = file_size // chunk_size + (file_size % chunk_size > 0)
            signed_url_data = get_signed_url_for_model_upload(
                key, initialize_data["details"]["upload_id"], chunk_count
            )
            if signed_url_data.get("status") == "success":
                signed_urls = signed_url_data.get("details", {}).get("urls", [])
                multi_upload_array = []

                max_retries = 3  # Maximum number of retries for each chunk upload

                for upload_count in range(1, chunk_count + 1):
                    retries = 0
                    while retries < max_retries:
                        if upload_count < chunk_count or (
                            upload_count == chunk_count and file_size % chunk_size != 0
                        ):
                            file_blob = selected_file.read(chunk_size)
                        else:
                            file_blob = (
                                selected_file.read()
                            )  # Read the remainder of the file for the last chunk

                        pre_signed_url = signed_urls[upload_count - 1].get(
                            "signed_url", ""
                        )
                        if pre_signed_url:
                            headers = (
                                {"Content-Type": "application/zip"}
                                if upload_type == "ZIP"
                                else {}
                            )
                            upload_response = make_request(
                                pre_signed_url,
                                method="PUT",
                                data=file_blob,
                                auth=False,
                                headers=headers,
                                convert_json=False,
                            )

                            if upload_response.status_code == 200:
                                rich.print(
                                    f"Uploaded -->> PART - {upload_count} of {chunk_count}"
                                )
                                multi_upload_array.append(
                                    {
                                        "PartNumber": upload_count,
                                        "ETag": upload_response.headers.get(
                                            "ETag"
                                        ).replace('"', ""),
                                    }
                                )
                                break  # Break out of the retry loop on success

                            rich.print(
                                f"Retry {retries + 1} for PART - {upload_count} of {chunk_count}"
                            )
                            retries += 1

                        if retries == max_retries:
                            rich.print(
                                f"[red]Failed to upload PART - {upload_count} after {max_retries} retries.[/red]"
                            )
                            raise InferlessCLIError(
                                f"Failed to upload PART - {upload_count} after {max_retries} retries."
                            )
                if multi_upload_array:
                    complete_response = complate_model_upload(
                        key, initialize_data["details"]["upload_id"], multi_upload_array
                    )
                    if complete_response.status_code == 200:
                        return signed_urls[0]["signed_url"].split("?")[0]
                    raise InferlessCLIError("multi upload complete failed")
                raise InferlessCLIError("Failed to complete model upload")
            raise InferlessCLIError("Failed to get signed urls")
        return None
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise typer.Exit(1)


def get_build_logs(payload):
    try:
        response = make_request(
            f"{GET_MODEL_BUILD_LOGS_URL}", method="POST", auth=True, data=payload
        )
        return response.json()
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get build logs. ")


def get_call_logs(payload):
    try:
        response = make_request(
            f"{GET_MODEL_CALL_LOGS_URL}", method="POST", auth=True, data=payload
        )
        return response.json()
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get call logs. ")


def get_volume_files(payload):
    try:
        response = make_request(
            f"{GET_VOLUMES_FILES_URL}", method="POST", auth=True, data=payload
        )
        return response.json()
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get volume files")


def sync_s3_to_nfs(payload):
    try:
        response = make_request(
            f"{SYNC_S3_TO_NFS}", method="POST", auth=True, data=payload
        )
        return response.json()
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to sync s3 to nfs.")


def sync_s3_to_s3(payload):
    try:
        response = make_request(
            f"{SYNC_S3_TO_S3}", method="POST", auth=True, data=payload
        )
        return response.json()
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to sync s3 to s3.")


def get_cli_files(name: str):
    try:
        payload = {"file": name}

        response = make_request(
            GET_CLI_UTIL_FILES, method="POST", auth=True, data=payload
        )

        if not response.json().get("details"):
            raise Exception(NO_DETAILS_MSG)

        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get required utils file.")


def create_presigned_io_upload_url(payload, path):
    try:
        response = make_request(PRESIGNED_URL, method="POST", auth=True, data=payload)

        data = response.json()
        if data:
            return upload_io_file(data["details"], path)
        raise Exception(f"Upload failed with status code {response.status_code}")
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def upload_io_file(url, path):
    try:
        file_size = os.path.getsize(path)
        with open(path, "rb") as file:
            response = make_request(
                url,
                method="PUT",
                data="" if file_size == 0 else file,
                auth=False,
                convert_json=False,
                headers={
                    "Content-Type": "text/json",
                },
            )
            if response.status_code == 200:
                return {
                    "status": "success",
                }

            raise Exception(f"Upload failed with status code {response.status_code}")
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)


def get_workspace_regions(payload):
    try:
        response = make_request(
            f"{GET_WORKSPACE_REGIONS}", method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get workspace regions.")


def get_machines():
    try:
        response = make_request(f"{GET_MACHINES}", method="GET", auth=True)
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get machines.")

def get_volume_by_name(workspace_id, volume_name):
    try:
        payload={"workspace_id": workspace_id, "volume_name": volume_name}
        response = make_request(f"{GET_VOLUME_BY_NAME}", method="POST", auth=True,data=payload)
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to volume details.")

def get_runtime_by_name(workspace_id, runtime_name):
    try:
        payload={"workspace_id": workspace_id, "template_name": runtime_name}
        response = make_request(f"{GET_RUNTIME_BY_NAME}", method="POST", auth=True, data=payload)
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(f"Failed to get runtime details.{e}")

def get_secrets_by_name(secret_name):
    try:
        payload={ "secret_name": secret_name}
        response = make_request(f"{GET_SECRETS_BY_NAME}", method="POST", auth=True, data=payload )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get secret details")


def get_hf_default_files_data(payload):
    try:
        response = make_request(
            f"{GET_HF_DEFAULT_FILES_DATA}", method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to get hf default files.")
    

def create_presigned_upload_url_hf_files_upload(payload, path):
    try:
        response = make_request(PRESIGNED_URL, method="POST", auth=True, data=payload)

        data = response.json()
        if data:
            return upload_hf_file(data["details"], path)
        raise InferlessCLIError(
            f"Upload failed with status code {response.status_code}"
        )
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)

def upload_hf_file(url, path):
    try:
        file_size = os.path.getsize(path)
        rich.print(f"Uploading {path}")
        with open(path, "rb") as file:
            response = make_request(
                url,
                method="PUT",
                data="" if file_size == 0 else file,
                auth=False,
                convert_json=False,
            )
            if response.status_code == 200:
                return {
                    "status": "success",
                }

            raise ModelImportException(
                f"Upload failed with status code {response.status_code}"
            )
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception(FAILED_TO_CREATE_MESSAGE)
    


def add_integrations(payload):
    try:
        response = make_request(
            f"{SET_INTEGRATIONS_URL}", method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to add integrations.")
    

def set_onboarding_status(payload):
    try:
        response = make_request(
            f"{SET_ONBOARDING_STATUS}", method="POST", auth=True, data=payload
        )
        return response.json()["details"]
    except HTTPError as http_err:
        raise ServerError(http_err)
    except Exception as e:
        log_exception(e)
        raise Exception("Failed to set onboarding status.")