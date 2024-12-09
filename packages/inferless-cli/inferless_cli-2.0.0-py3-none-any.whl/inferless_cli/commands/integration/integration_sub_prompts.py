import os
import rich
import typer

from inferless_cli.utils.exceptions import InferlessCLIError, ServerError
from inferless_cli.utils.helpers import log_exception
from inferless_cli.utils.services import add_integrations

app = typer.Typer(
    no_args_is_help=True,
)


@app.command(
    "HF",
    help="Add Huggingface integration to your workspace",
    no_args_is_help=True
)
def add_hf(

    integration_name: str = typer.Option(..., "--name", "-n", help="Integration name"),
    api_key: str = typer.Option(
            ...,
            "--api-key",
            help="API key for huggingface integration",
        ),
):
    try:
        payload = None
       

        if not api_key:
            raise InferlessCLIError("API key is required for Huggingface integration.")
        payload = {
            "account_type": "HUGGINGFACE",
            "name": integration_name,
            "credentials": {
                "api_key": api_key,
            },
        }
      
        if payload is not None:
            add_integrations(payload)
            rich.print(f"[green]Huggingface Integration added successfully[/green]\n\n")

    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red]: {error}")
        raise typer.Abort(1)


@app.command(
    "ECR",
    help="Add ECR integration to your workspace",
    no_args_is_help=True
)
def add_ecr(
 
    integration_name: str = typer.Option(..., "--name", "-n", help="Integration name"),
    access_key: str =  typer.Option(
            ...,
            "--access-key",
            help="Access key for aws integration.",
        ),  
    secret_key: str = typer.Option(
            ...,
            "--secret-key",
            help="Access key for aws integration.",
        ),
):
    try:
        payload = None


        if not access_key or not secret_key:
            raise InferlessCLIError("Access key and secret key are required for ECR integration.")
        payload = {
            "account_type": "DOCKER_AWS_ECR",
            "name": integration_name,
            "credentials": {
                "access_key": access_key,
                "secret_key": secret_key,
            },
        }
        
        if payload is not None:
            add_integrations(payload)
            rich.print(f"[green]AWS ECR Integration added successfully[/green]\n\n")

    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red]: {error}")
        raise typer.Abort(1)


@app.command(
    "DOCKERHUB",
    help="Add Dockerhub integration to your workspace",
    no_args_is_help=True
)
def add_dockerhub(

    integration_name: str = typer.Option(..., "--name", "-n", help="Integration name"),
    username:str = typer.Option(
            ...,
            "--username",
            help="Username for dockerhub integration",
        ),
    access_token: str = typer.Option(
            ...,
            "--access-token",
            help="Access token for dockerhub integration",
        ),
   
):
    try:
        payload = None
    
        if not username or not access_token:
            raise InferlessCLIError("Username and access token are required for DockerHub integration.")
        payload = {
            "account_type": "DOCKER_HUB",
            "name": integration_name,
            "credentials": {
                "username": username,
                "access_token": access_token,
            },
        }
      
        if payload is not None:
            add_integrations(payload)
            rich.print(f"[green]Docker Hub Integration added successfully[/green]\n\n")

    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red]: {error}")
        raise typer.Abort(1)
    
@app.command(
    "GCS",
    help="Add Google cloud storage integration to your workspace",
    no_args_is_help=True
)
def add_gcs(
    integration_name: str = typer.Option(..., "--name", "-n", help="Integration name"),
    gcp_json_path: str = typer.Option(
            ...,
            "--gcp-json-path",
            help="Path to the GCP JSON key file",
        )
):
    try:
        payload = None
        
        if not gcp_json_path or not os.path.exists(gcp_json_path):
            raise InferlessCLIError("A valid GCP JSON key file path is required for GCS integration.")
        with open(gcp_json_path, "r") as f:
            gcp_json = f.read()
            payload = {
                "account_type": "GCP_GS",
                "name": integration_name,
                "credentials": gcp_json,
            }

        if payload is not None:
            add_integrations(payload)
            rich.print(f"[green]GCS Integration added successfully[/green]\n\n")

    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red]: {error}")
        raise typer.Abort(1)
    


@app.command(
    "S3",
    help="Add S3/ECR Integration to your workspace",
    no_args_is_help=True
)
def add(
    integration_name: str = typer.Option(..., "--name", "-n", help="Integration name"),
    access_key: str =  typer.Option(
            ...,
            "--access-key",
            help="Access key for aws integration.",
        ),
    secret_key: str = typer.Option(
            ...,
            "--secret-key",
            help="Access key for aws integration.",
        ),
    
):
    try:
        payload = None

        if not access_key or not secret_key:
            raise InferlessCLIError("Access key and secret key are required for S3 integration.")
        payload = {
            "account_type": "AWS_S3",
            "name": integration_name,
            "credentials": {
                "access_key": access_key,
                "secret_key": secret_key,
            },
        }
        
        
        if payload is not None:
            add_integrations(payload)
            rich.print(f"[green]AWS Integration added successfully[/green]\n\n")

    except ServerError as error:
        log_exception(error)
        raise typer.Exit()
    except InferlessCLIError as error:
        log_exception(error)
        raise typer.Exit()
    except Exception as error:
        log_exception(error)
        rich.print(f"\n[red]Something went wrong[/red]: {error}")
        raise typer.Abort(1)
    


