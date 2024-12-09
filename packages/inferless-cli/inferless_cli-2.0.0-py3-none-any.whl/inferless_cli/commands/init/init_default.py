import os
import re
import typer
import rich
import base64

from inferless_cli.commands.integration.integration_prompt import get_account_status
from inferless_cli.utils.constants import DEFAULT_RUNTIME_YAML_DATA, GIT
from inferless_cli.utils.helpers import log_exception
from inferless_cli.utils.inferless_config_handler import InferlessConfigHandler
from inferless_cli.utils.services import (
    callback_with_auth_validation,
    get_hf_default_files_data,
)
from inferless_cli.utils.exceptions import (
    ConfigurationError,
    InferlessCLIError,
    ServerError,
)


# Subcommand groups
init_app = typer.Typer(
    help="Initialize a workflow or model. if subcommand is not provided, default to pythonic."
)


@init_app.callback(invoke_without_command=True, no_args_is_help=True)
def init_callback(
    ctx: typer.Context,
    name: str = typer.Option(
        None, "--name", "-n", help="Denotes the name of the model."
    ),
    source: str = typer.Option(
        "local",
        "--source",
        "-s",
        help="Not needed if local, else provide Github/Gitlab.",
    ),
    url: str = typer.Option(
        None,
        "--url",
        "-u",
        help="Denotes the URL of the repo. required if source is not local.",
    ),
    branch: str = typer.Option(
        None,
        "--branch",
        "-b",
        help="Denotes the branch where the model is located. required if source is not local.",
    ),
    autobuild: bool = typer.Option(
        False,
        "--autobuild",
        "-a",
        help="Enable autobuild for the model. will be False for local source.",
    ),
):
    """
    Deploy a Python workflow.
    """
    callback_with_auth_validation()
    if not ctx.invoked_subcommand:
        pythonic(name=name, source=source, url=url, branch=branch, autobuild=autobuild)


# Common options for `inferless init`
@init_app.command("pythonic", no_args_is_help=True)
def pythonic(
    name: str = typer.Option(
        ..., "--name", "-n", help="Denotes the name of the model."
    ),
    source: str = typer.Option(
        "local",
        "--source",
        "-s",
        help="Not needed if local, else provide Github/Gitlab.",
    ),
    url: str = typer.Option(
        None,
        "--url",
        "-u",
        help="Denotes the URL of the repo. required if source is not local.",
    ),
    branch: str = typer.Option(
        None,
        "--branch",
        "-b",
        help="Denotes the branch where the model is located. required if source is not local.",
    ),
    autobuild: bool = typer.Option(
        False,
        "--autobuild",
        "-a",
        help="Enable autobuild for the model. will be False for local source.",
    ),
):
    """
    (Default) Deploy a Python workflow.
    """
    try:
        if not name:
            InferlessCLIError("Missing required options: --name")
        source = source.upper()
        if source not in ["LOCAL", "GITHUB", "GITLAB"]:
            InferlessCLIError(f"Invalid source: {source}")
        if source != "LOCAL" and (not url or not branch):
            InferlessCLIError("Missing required options: --url, and --branch.")

        if url:
            validate_url(url)

        config = InferlessConfigHandler()
        config.update_config("name", name)
        config.update_config("import_source", "LOCAL" if source == "LOCAL" else GIT)
        config.update_config("source_framework_type", "PYTORCH")

        if source != "LOCAL":
            integration_status = get_account_status(source)
            if not integration_status:
                raise InferlessCLIError(
                    f"Integration with {source} is not enabled. Please enable it first. you can do it from inferless console.\nhttps://console.inferless.com/user/integration"
                )
            config.update_config("provider", source)
            config.update_config("branch", branch)
            config.update_config("autobuild", autobuild)
            config.update_config("model_url", url)

        config.save_config()

        rich.print("\n[green]Model Initialized succesfully. Your model is ready for the deployment![/green]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except ConfigurationError as error:
        rich.print(f"\n[red]Error (inferless.yaml): [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red] {error}")
        raise typer.Abort(1)


def validate_url(url):
    # Use a regular expression to check if the input matches a valid URL pattern
    url_pattern = re.compile(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
    if not url_pattern.match(url):
        raise InferlessCLIError(message="Invalid URL. Please enter a valid URL.")
    return url


@init_app.command("hf", no_args_is_help=True)
def init_hf(
    name: str = typer.Option(
        ..., "--name", "-n", help="Denotes the name of the model."
    ),
    hfmodelname: str = typer.Option(
        ..., "--hfmodelname", "-m", help="Name of the Hugging Face repo."
    ),
    modeltype: str = typer.Option(
        ...,
        "--modeltype",
        "-t",
        help="Type of the model (transformer/diffuser).",
    ),
    tasktype: str = typer.Option(
        ..., "--tasktype", "-k", help="Task type of the model (text-generation)."
    ),
):
    """


    Load a model from Hugging Face. \n
    \n
    We will create new files called app.py, inferless_runtime_config.yaml and input_schema.py at your current directory.\n
    \n\nTransformers options: audio-classification, automatic-speech-recognition, conversational, depth-estimation, document-question-answering, feature-extraction, fill-mask, image-classification, image-segmentation, image-to-text, object-detection, question-answering, summarization, table-question-answering, text-classification, text-generation, text2text-generation, token-classification, translation, video-classification, visual-question-answering, zero-shot-classification, zero-shot-image-classification, zero-shot-object-detection
    \n
    \n\nDiffusers options: Depth-to-Image, Image-Variation, Image-to-Image, Inpaint, InstructPix2Pix,Stable-Diffusion-Latent-Upscaler

    """
    try:

        transformers_tasks = [
            "audio-classification",
            "automatic-speech-recognition",
            "conversational",
            "depth-estimation",
            "document-question-answering",
            "feature-extraction",
            "fill-mask",
            "image-classification",
            "image-segmentation",
            "image-to-text",
            "object-detection",
            "question-answering",
            "summarization",
            "table-question-answering",
            "text-classification",
            "text-generation",
            "text2text-generation",
            "token-classification",
            "translation",
            "video-classification",
            "visual-question-answering",
            "zero-shot-classification",
            "zero-shot-image-classification",
            "zero-shot-object-detection",
        ]

        diffusers_tasks = [
            "Depth-to-Image",
            "Image-Variation",
            "Image-to-Image",
            "Inpaint",
            "InstructPix2Pix",
            "Stable-Diffusion-Latent-Upscaler",
            "Super-Resolution",
            "Text-to-Image",
        ]

        integration_status = get_account_status("HUGGINGFACE")
        integration_status_github = get_account_status("GITHUB")
        if not integration_status:
                raise InferlessCLIError(
                    f"Integration with Hugging Face is not enabled. Please enable it first.\n You can refer to docs by running [green]inferless integration add HF --help[/green] and then enable it."
                )
        if not integration_status_github:
                raise InferlessCLIError(
                    f"Integration with Github is required. Please enable it first.\n You can do it from inferless console.\nhttps://console.inferless.com/user/integration."
                )

        if modeltype not in ["transformer", "diffuser"]:
            raise InferlessCLIError(
                f"Invalid model type: {modeltype} \n Available model types: transformer/diffuser"
            )

        if modeltype == "transformer" and tasktype not in transformers_tasks:
            raise InferlessCLIError(
                f"Invalid task type: {tasktype} \nAvailable tasks for transformer: {', '.join(transformers_tasks)}"
            )

        if modeltype == "diffuser" and tasktype not in diffusers_tasks:
            raise InferlessCLIError(
                f"\nInvalid task type: {tasktype} \n\n [green]Available tasks for diffuser:[/green] \n\n {', '.join(diffusers_tasks)}"
            )

        apppy_payload = {
            "task_type": tasktype,
            "huggingface_type": modeltype,
            "file_name": "app.py",
            "model_name": hfmodelname,
        }
        apppy_res = get_hf_default_files_data(apppy_payload)

        ioschema_payload = {
            "task_type": tasktype,
            "huggingface_type": modeltype,
            "file_name": "input_schema.py",
            "model_name": hfmodelname,
        }
        ioschema_res = get_hf_default_files_data(ioschema_payload)

        if apppy_res is None or ioschema_res is None:
            raise InferlessCLIError("Error getting default files from Hugging Face")
        else:
            create_files(
                base64.b64decode(apppy_res).decode('utf-8'),
                base64.b64decode(ioschema_res).decode('utf-8'),
            )

        config = InferlessConfigHandler()
        config.update_config("name", name)
        config.update_config("import_source", "HUGGINGFACE")
        config.update_config("source_framework_type", "PYTORCH")
        config.update_config("hf_model_name", hfmodelname)
        config.update_config("model_type", modeltype)
        config.update_config("task_type", tasktype)
        # config.update_config("autobuild", autobuild)
        config.save_config()
        rich.print("\nWe have created app.py and input_schema.py. \nInference code is present in app.py, input parameters can be updated in input_schema.py, if you import any new packages in app.py, you need to create a new runtime and add the packages.\n")
        rich.print("\n[green]Hugging Face model initialized successfully! Your model is ready for the deployment[/green]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except ConfigurationError as error:
        rich.print(f"\n[red]Error (inferless.yaml): [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red] {error}")
        raise typer.Abort(1)


def create_files( app_content, input_schema_content ):
    # File paths
    app_file_path = "app.py"
    input_schema_file_path = "input_schema.py"
    # config_file_path = "inferless_runtime_config.yaml"

    # Create and write to app.py
    with open(app_file_path, "w") as app_file:
        app_file.write(app_content)

    # Create and write to input_schema.py
    with open(input_schema_file_path, "w") as input_schema_file:
        input_schema_file.write(input_schema_content)

    # Create and write to inferless_runtime_config.yaml



@init_app.command("docker", no_args_is_help=True)
def init_docker(
    name: str = typer.Option(
        ..., "--name", "-n", help="Denotes the name of the model."
    ),
    type_: str = typer.Option(
        ..., "--type", "-t", help="Type for import: dockerimage/dockerfile."
    ),
    provider: str = typer.Option(
        ...,
        "--provider",
        "-p",
        help="Provider for the model dockerimage = (dockerhub/ecr) dockerfile = (github/gitlab).",
    ),
    url: str = typer.Option(
        ..., "--url", "-u", help="Docker image URL or GitHub/GitLab URL."
    ),
    branch: str = typer.Option(
        None,
        "--branch",
        "-b",
        help="Branch for Dockerfile import (GitHub/GitLab). required if type is dockerfile.",
    ),
    dockerfilepath: str = typer.Option(
        None,
        "--dockerfilepath",
        "-d",
        help="Path to the Dockerfile. required if type is dockerfile.",
    ),
    healthapi: str = typer.Option(
        ..., "--healthapi", "-h", help="Health check API endpoint."
    ),
    inferapi: str = typer.Option(
        ..., "--inferapi", "-i", help="Inference API endpoint."
    ),
    serverport: int = typer.Option(..., "--serverport", "-s", help="Server port."),
    autobuild: bool = typer.Option(
        False, "--autobuild", "-a", help="Enable autobuild for the model."
    ),
):
    """
    Initialize with Docker.
    """
    try:
        # Validate `name`
        if not name or len(name) > 32:
            raise InferlessCLIError(
                "The name is required and should be less than 32 characters."
            )

        # Validate and process `type_`
        type_ = type_.lower()
        if type_ not in ["dockerimage", "dockerfile"]:
            raise InferlessCLIError(
                "Type must be either 'dockerimage' or 'dockerfile'."
            )

        source_location = (
            "DOCKER_REGISTRY" if type_ == "dockerimage" else "DOCKERFILE_REPO"
        )

        # Validate and process `provider`
        provider = provider.lower()
        if source_location == "DOCKER_REGISTRY":
            if provider not in ["dockerhub", "ecr"]:
                raise InferlessCLIError(
                    "Provider must be either 'dockerhub' or 'ecr' for dockerimage."
                )
            integration_status = get_account_status("DOCKER_AWS_ECR" if provider == "ecr" else "DOCKER_HUB")
            command = "ECR" if provider == "ecr" else "DOCKERHUB"
            if not integration_status:
                    raise InferlessCLIError(
                        f"Integration with {provider} is not enabled. Please enable it first.\n You can refer to docs by running [green]inferless integration add {command} --help[/green] and then enable it."
                    )
            provider = "AMAZON_ECR" if provider == "ecr" else "DOCKER_HUB"
        else:  # source_location == "DOCKERFILE_REPO"
            if provider not in ["github", "gitlab"]:
                raise InferlessCLIError(
                    "Provider must be either 'github' or 'gitlab' for dockerfile."
                )
            provider = "GITHUB" if provider == "github" else "GITLAB"
            integration_status = get_account_status(provider)
            if not integration_status:
                raise InferlessCLIError(
                    f"Integration with {provider} is not enabled. Please enable it first. you can do it from inferless console.\nhttps://console.inferless.com/user/integration"
                )

        # Validate `url`
        if not url:
            raise InferlessCLIError("URL is required.")
        if source_location == "DOCKER_REGISTRY":
            pass
            # if provider == "AMAZON_ECR" and not url.startswith("https://"):
            #     raise InferlessCLIError("ECR URL must be a valid HTTPS URL.")
            # if provider == "DOCKER_HUB" and "/" not in url:
            #     raise InferlessCLIError("DockerHub URL must be in a valid format.")
        else:
            if not (
                url.startswith("https://github.com")
                or url.startswith("https://gitlab.com")
            ):
                raise InferlessCLIError(
                    "URL must be a valid GitHub or GitLab repository URL."
                )

        # Validate `branch` (only for GitHub or GitLab)
        if provider in ["GITHUB", "GITLAB"] and not branch:
            raise InferlessCLIError("Branch is required for GitHub or GitLab.")

        # Validate `dockerfilepath` (only for GitHub or GitLab)
        if provider in ["GITHUB", "GITLAB"] and not dockerfilepath:
            raise InferlessCLIError("Dockerfile path is required for GitHub or GitLab.")

        config = InferlessConfigHandler()
        config.update_config("name", name)
        config.update_config("import_source", "DOCKER")
        config.update_config("source_framework_type", "PYTORCH")
        config.update_config("source_location", source_location)
        config.update_config("provider", provider)
        config.update_config("model_url", url)
        if branch:
            config.update_config("branch", branch)
        if dockerfilepath:
            config.update_config("docker_file_path", dockerfilepath)
        config.update_config("health_api", healthapi)
        config.update_config("infer_api", inferapi)
        config.update_config("server_port", serverport)
        config.update_config("autobuild", autobuild)
        config.save_config()

        rich.print("\n[green]Docker model initialized successfully! Your model is ready for the deployment[/green]")
    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except ConfigurationError as error:
        rich.print(f"\n[red]Error (inferless.yaml): [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red] {error}")
        raise typer.Abort(1)


@init_app.command("file", no_args_is_help=True,
                  help="""
                  
Import a PyTorch, ONNX, or TensorFlow file for inference with Triton server.
\n\n   

The folder structure for the zip file should be as follows:
\n\n

┌───────────────────────────────────────────────┐\n
\n
│ .                                             │\n
\n
│ ├── config.pbtxt (optional)                   │\n
\n
│ ├── input.json                                │\n
\n
│ ├── output.json                               │\n
\n
│ ├── 1/                                        │\n
\n
│ │   ├── model.xxx (pt/onnx/savedmodel)        │\n
\n
└───────────────────────────────────────────────┘\n
\n
                  
"""
)
def init_file(
    name: str = typer.Option(
        ..., "--name", "-n", help="Denotes the name of the model."
    ),
    framework: str = typer.Option(
        "pytorch",
        "--framework",
        "-f",
        help="Framework of the model. [pytorch, onnx, tensorflow]",
    ),
    provider: str = typer.Option(
        "local", "--provider", "-p", help="Provider for the model (local/gcs/s3)."
    ),
    url: str = typer.Option(
        None, "--url", help="Provider URL. required if provider is not local."
    ),
):
   
    try:
        # Validate `name`
        if not name or len(name) > 32:
            raise InferlessCLIError(
                "The name is required and should be less than 32 characters."
            )
        valid_frameworks = ["PYTORCH", "ONNX", "TENSORFLOW"]
        framework = framework.upper()
        if framework not in valid_frameworks:
            raise InferlessCLIError(
                f"Invalid framework: {framework}. Supported frameworks: {', '.join(valid_frameworks)}"
            )

        # Validate provider
        if provider is None:
            raise InferlessCLIError("Provider is required.")
        provider = provider.lower()
        if provider not in ["local", "gcs", "s3"]:
            raise InferlessCLIError("Provider must be one of 'local', 'gcs', or 's3'.")

        # Map provider and source location
        if provider == "local":
            provider = "LOCAL"
            source_location = "LOCAL_FILE"
        elif provider == "s3":
            integration_status = get_account_status("AWS_S3")
            if integration_status:
                    raise InferlessCLIError(
                        f"Integration with {provider} is not enabled. Please enable it first.\n You can refer to docs by running [green]inferless integration add S3 --help[/green] and then enable it."
                    )
            provider = "AMAZON_S3"
            source_location = "CLOUD_URL"
        elif provider == "gcs":
            integration_status = get_account_status("GCP_GS")
            if not integration_status:
                    raise InferlessCLIError(
                        f"Integration with {provider} is not enabled. Please enable it first.\n You can refer to docs by running [green]inferless integration add GCS --help[/green] and then enable it."
                    )
            provider = "GOOGLE_GCS"
            source_location = "CLOUD_URL"

        # Validate URL for non-local providers
        if provider != "LOCAL" and not url:
            raise InferlessCLIError("URL is required for non-local providers (gcs/s3).")

        config = InferlessConfigHandler()
        config.update_config("name", name)
        config.update_config("import_source", "FILE")
        config.update_config("source_framework_type", framework)
        config.update_config("source_location", source_location)
        if source_location == "CLOUD_URL":
            config.update_config("provider", provider)
            config.update_config("model_url", url)
        config.save_config()
        rich.print("\n[green]Model initialized successfully! Your model is ready for the deployment[/green]")

    except ServerError as error:
        rich.print(f"\n[red]Inferless Server Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except ConfigurationError as error:
        rich.print(f"\n[red]Error (inferless.yaml): [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        rich.print(f"\n[red]Inferless CLI Error: [/red] {error}")
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red] {error}")
        raise typer.Abort(1)


if __name__ == "__main__":
    init_app()
