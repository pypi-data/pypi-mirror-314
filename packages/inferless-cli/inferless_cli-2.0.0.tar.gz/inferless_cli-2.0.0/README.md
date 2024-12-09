# `inferless`

Inferless - Deploy Machine Learning Models in Minutes.

See the website at https://inferless.com/ for documentation and more information
about running code on Inferless.

**Usage**:

```console
$ inferless [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `deploy`: Deploy a model to Inferless
* `export`: Export the runtime configuration of...
* `init`: Initialize a new Inferless model
* `integration`: Manage Inferless integrations
* `log`: Inferless models logs (view build logs or...
* `login`: Login to Inferless
* `mode`: Change mode
* `model`: Manage Inferless models (list , delete ,...
* `region`: Manage Inferless regions
* `remote-run`: Remotely run code on inferless
* `run`: Run a model locally
* `runtime`: Manage Inferless runtimes (can be used to...
* `scaffold`: Scaffold a demo Inferless project
* `secret`: Manage Inferless secrets (list secrets)
* `token`: Manage Inferless tokens
* `volume`: Manage Inferless volumes (can be used to...
* `workspace`: Manage Inferless workspaces (can be used...

## `inferless deploy`

Deploy a model to Inferless

**Usage**:

```console
$ inferless deploy [OPTIONS]
```

**Options**:

* `--gpu TEXT`: Denotes the machine type (A10/A100/T4).  [required]
* `--region TEXT`: Inferless region. Defaults to Inferless default region.
* `--beta`: Deploys the model with v2 endpoints.
* `--fractional`: Use fractional machine type (default: dedicated).
* `--runtime TEXT`: Runtime name or file location. if not provided default Inferless runtime will be used.
* `--volume TEXT`: Volume name.
* `--volume-mount-path TEXT`: Custom volume mount path.
* `--env TEXT`: Key-value pairs for model environment variables.
* `--inference-timeout INTEGER`: Inference timeout in seconds.  [default: 180]
* `--scale-down-timeout INTEGER`: Scale down timeout in seconds.  [default: 600]
* `--container-concurrency INTEGER`: Container concurrency level.  [default: 1]
* `--secret TEXT`: Secret names to attach to the deployment.
* `--runtimeversion TEXT`: Runtime version (default: latest version of runtime).
* `--max-replica INTEGER`: Maximum number of replicas.  [default: 1]
* `--min-replica INTEGER`: Minimum number of replicas.  [default: 0]
* `-c, --config TEXT`: Inferless config file path to override from inferless.yaml  [default: inferless.yaml]
* `--help`: Show this message and exit.

## `inferless export`

Export the runtime configuration of another provider to Inferless runtime config

**Usage**:

```console
$ inferless export [OPTIONS]
```

**Options**:

* `-r, --runtime TEXT`: The runtime configuration file of another provider  [default: cog.yaml]
* `-d, --destination TEXT`: The destination file for the Inferless runtime configuration  [default: inferless-runtime-config.yaml]
* `-f, --from TEXT`: The provider from which to export the runtime configuration  [default: replicate]
* `--help`: Show this message and exit.

## `inferless init`

Initialize a new Inferless model

**Usage**:

```console
$ inferless init [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-n, --name TEXT`: Denotes the name of the model.
* `-s, --source TEXT`: Not needed if local, else provide Github/Gitlab.  [default: local]
* `-u, --url TEXT`: Denotes the URL of the repo. required if source is not local.
* `-b, --branch TEXT`: Denotes the branch where the model is located. required if source is not local.
* `-a, --autobuild`: Enable autobuild for the model. will be False for local source.
* `--help`: Show this message and exit.

**Commands**:

* `docker`: Initialize with Docker.
* `file`: Import a PyTorch, ONNX, or TensorFlow file...
* `hf`: Load a model from Hugging Face.
* `pythonic`: (Default) Deploy a Python workflow.

### `inferless init docker`

Initialize with Docker.

**Usage**:

```console
$ inferless init docker [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Denotes the name of the model.  [required]
* `-t, --type TEXT`: Type for import: dockerimage/dockerfile.  [required]
* `-p, --provider TEXT`: Provider for the model dockerimage = (dockerhub/ecr) dockerfile = (github/gitlab).  [required]
* `-u, --url TEXT`: Docker image URL or GitHub/GitLab URL.  [required]
* `-b, --branch TEXT`: Branch for Dockerfile import (GitHub/GitLab). required if type is dockerfile.
* `-d, --dockerfilepath TEXT`: Path to the Dockerfile. required if type is dockerfile.
* `-h, --healthapi TEXT`: Health check API endpoint.  [required]
* `-i, --inferapi TEXT`: Inference API endpoint.  [required]
* `-s, --serverport INTEGER`: Server port.  [required]
* `-a, --autobuild`: Enable autobuild for the model.
* `--help`: Show this message and exit.

### `inferless init file`

                  
Import a PyTorch, ONNX, or TensorFlow file for inference with Triton server.


   

The folder structure for the zip file should be as follows:




┌───────────────────────────────────────────────┐



│ .                                             │



│ ├── config.pbtxt (optional)                   │



│ ├── input.json                                │



│ ├── output.json                               │



│ ├── 1/                                        │



│ │   ├── model.xxx (pt/onnx/savedmodel)        │



└───────────────────────────────────────────────┘



                  

**Usage**:

```console
$ inferless init file [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Denotes the name of the model.  [required]
* `-f, --framework TEXT`: Framework of the model. [pytorch, onnx, tensorflow]  [default: pytorch]
* `-p, --provider TEXT`: Provider for the model (local/gcs/s3).  [default: local]
* `--url TEXT`: Provider URL. required if provider is not local.
* `--help`: Show this message and exit.

### `inferless init hf`

    Load a model from Hugging Face. 

    

    We will create new files called app.py, inferless_runtime_config.yaml and input_schema.py at your current directory.

    

Transformers options: audio-classification, automatic-speech-recognition, conversational, depth-estimation, document-question-answering, feature-extraction, fill-mask, image-classification, image-segmentation, image-to-text, object-detection, question-answering, summarization, table-question-answering, text-classification, text-generation, text2text-generation, token-classification, translation, video-classification, visual-question-answering, zero-shot-classification, zero-shot-image-classification, zero-shot-object-detection
    

    

Diffusers options: Depth-to-Image, Image-Variation, Image-to-Image, Inpaint, InstructPix2Pix,Stable-Diffusion-Latent-Upscaler

    

**Usage**:

```console
$ inferless init hf [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Denotes the name of the model.  [required]
* `-m, --hfmodelname TEXT`: Name of the Hugging Face repo.  [required]
* `-t, --modeltype TEXT`: Type of the model (transformer/diffuser).  [required]
* `-k, --tasktype TEXT`: Task type of the model (text-generation).  [required]
* `--help`: Show this message and exit.

### `inferless init pythonic`

(Default) Deploy a Python workflow.

**Usage**:

```console
$ inferless init pythonic [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Denotes the name of the model.  [required]
* `-s, --source TEXT`: Not needed if local, else provide Github/Gitlab.  [default: local]
* `-u, --url TEXT`: Denotes the URL of the repo. required if source is not local.
* `-b, --branch TEXT`: Denotes the branch where the model is located. required if source is not local.
* `-a, --autobuild`: Enable autobuild for the model. will be False for local source.
* `--help`: Show this message and exit.

## `inferless integration`

Manage Inferless integrations

**Usage**:

```console
$ inferless integration [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `add`: Add an integration to your workspace
* `list`: List all integrations

### `inferless integration add`

Add an integration to your workspace

**Usage**:

```console
$ inferless integration add [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `DOCKERHUB`: Add Dockerhub integration to your workspace
* `ECR`: Add ECR integration to your workspace
* `GCS`: Add Google cloud storage integration to...
* `HF`: Add Huggingface integration to your workspace
* `S3`: Add S3/ECR Integration to your workspace

#### `inferless integration add DOCKERHUB`

Add Dockerhub integration to your workspace

**Usage**:

```console
$ inferless integration add DOCKERHUB [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Integration name  [required]
* `--username TEXT`: Username for dockerhub integration  [required]
* `--access-token TEXT`: Access token for dockerhub integration  [required]
* `--help`: Show this message and exit.

#### `inferless integration add ECR`

Add ECR integration to your workspace

**Usage**:

```console
$ inferless integration add ECR [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Integration name  [required]
* `--access-key TEXT`: Access key for aws integration.  [required]
* `--secret-key TEXT`: Access key for aws integration.  [required]
* `--help`: Show this message and exit.

#### `inferless integration add GCS`

Add Google cloud storage integration to your workspace

**Usage**:

```console
$ inferless integration add GCS [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Integration name  [required]
* `--gcp-json-path TEXT`: Path to the GCP JSON key file  [required]
* `--help`: Show this message and exit.

#### `inferless integration add HF`

Add Huggingface integration to your workspace

**Usage**:

```console
$ inferless integration add HF [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Integration name  [required]
* `--api-key TEXT`: API key for huggingface integration  [required]
* `--help`: Show this message and exit.

#### `inferless integration add S3`

Add S3/ECR Integration to your workspace

**Usage**:

```console
$ inferless integration add S3 [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Integration name  [required]
* `--access-key TEXT`: Access key for aws integration.  [required]
* `--secret-key TEXT`: Access key for aws integration.  [required]
* `--help`: Show this message and exit.

### `inferless integration list`

List all integrations

**Usage**:

```console
$ inferless integration list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless log`

Inferless models logs (view build logs or call logs)

**Usage**:

```console
$ inferless log [OPTIONS] [MODEL_ID]
```

**Arguments**:

* `[MODEL_ID]`: Model id or model import id

**Options**:

* `-i, --import-logs`: Import logs
* `-t, --type TEXT`: Logs type [BUILD, CALL]]  [default: BUILD]
* `--help`: Show this message and exit.

## `inferless login`

Login to Inferless

**Usage**:

```console
$ inferless login [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless mode`

Change mode

**Usage**:

```console
$ inferless mode [OPTIONS] MODE
```

**Arguments**:

* `MODE`: The mode to run the application in, either 'DEV' or 'PROD'.  [required]

**Options**:

* `--help`: Show this message and exit.

## `inferless model`

Manage Inferless models (list , delete , activate , deactivate , rebuild the models)

**Usage**:

```console
$ inferless model [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `activate`: activate a model.
* `deactivate`: deactivate a model.
* `delete`: delete a model.
* `info`: Get model details.
* `list`: List all models.
* `patch`: patch model configuration.
* `rebuild`: rebuild a model.

### `inferless model activate`

activate a model. 

**Usage**:

```console
$ inferless model activate [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model deactivate`

deactivate a model. 

**Usage**:

```console
$ inferless model deactivate [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model delete`

delete a model.

**Usage**:

```console
$ inferless model delete [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model info`

Get model details.

**Usage**:

```console
$ inferless model info [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model list`

List all models.

**Usage**:

```console
$ inferless model list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `inferless model patch`

patch model configuration.

**Usage**:

```console
$ inferless model patch [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--gpu TEXT`: Denotes the machine type (A10/A100/T4).
* `--fractional`: Use fractional machine type (default: dedicated).
* `--volume TEXT`: Volume name.
* `--mount-path TEXT`: Volume Mount path for the volume.
* `--env TEXT`: Key-value pairs for model environment variables.
* `--inference-timeout INTEGER`: Inference timeout in seconds.
* `--scale-down-timeout INTEGER`: Scale down timeout in seconds.
* `--container-concurrency INTEGER`: Container concurrency level.
* `--secret TEXT`: Secret names to attach to the deployment.
* `--runtimeversion TEXT`: Runtime version (default: latest).
* `--max-replica INTEGER`: Maximum number of replicas.
* `--min-replica INTEGER`: Minimum number of replicas.
* `--help`: Show this message and exit.

### `inferless model rebuild`

rebuild a model. (If you have a inferless.yaml file in your current directory, you can use the --local or -l flag to redeploy the model locally.)

**Usage**:

```console
$ inferless model rebuild [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `-l, --local`: Local rebuild
* `--help`: Show this message and exit.

## `inferless region`

Manage Inferless regions

**Usage**:

```console
$ inferless region [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List available regions

### `inferless region list`

List available regions

**Usage**:

```console
$ inferless region list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless remote-run`

Remotely run code on inferless

**Usage**:

```console
$ inferless remote-run [OPTIONS] [FILE_PATH]
```

**Arguments**:

* `[FILE_PATH]`: The path to the file to run on Inferless

**Options**:

* `-c, --config TEXT`: The path to the Inferless config file
* `-e, --exclude TEXT`: The path to the file to exclude from the run, use .gitignore format. If not provided, .gitignore will be used if present in the directory.
* `--help`: Show this message and exit.

## `inferless run`

Run a model locally

**Usage**:

```console
$ inferless run [OPTIONS]
```

**Options**:

* `-r, --runtime TEXT`: custom runtime name or file location. if not provided default Inferless runtime will be used.
* `-t, --type TEXT`: Type of runtime to run [inferless, replicate]
* `-n, --name TEXT`: Name of the model to deploy on inferless  [default: inferless-model]
* `-f, --env-file TEXT`: Path to an env file containing environment variables (one per line in KEY=VALUE format)
* `-e, --env TEXT`: Environment variables to set for the runtime (e.g. 'KEY=VALUE'). If the env variable contains special chars please escape them.
* `-u, --docker-base-url TEXT`: Docker base url. Defaults to system default, feteched from env
* `--volume TEXT`: Volume name.
* `-f, --framework TEXT`: Framework type. (PYTORCH, ONNX, TENSORFLOW)  [default: PYTORCH]
* `-i, --input-schema TEXT`: Input schema path. (Default: input_schema.json)  [default: input_schema.py]
* `-i, --input TEXT`: Input json path
* `-o, --output TEXT`: Output json path
* `--runtimeversion TEXT`: Runtime version (default: latest).
* `--help`: Show this message and exit.

## `inferless runtime`

Manage Inferless runtimes (can be used to list runtimes and upload new runtimes)

**Usage**:

```console
$ inferless runtime [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a runtime.
* `generate`: use to generate a new runtime from your...
* `list`: List all runtimes.
* `patch`: Update the runtime with the config file.
* `version-list`: use to list the runtime versions

### `inferless runtime create`

Create a runtime.

**Usage**:

```console
$ inferless runtime create [OPTIONS]
```

**Options**:

* `-p, --path TEXT`: Path to the runtime
* `-n, --name TEXT`: Name of the runtime
* `--help`: Show this message and exit.

### `inferless runtime generate`

use to generate a new runtime from your local environment

**Usage**:

```console
$ inferless runtime generate [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `inferless runtime list`

List all runtimes.

**Usage**:

```console
$ inferless runtime list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `inferless runtime patch`

Update the runtime with the config file.

**Usage**:

```console
$ inferless runtime patch [OPTIONS]
```

**Options**:

* `-p, --path TEXT`: Path to the runtime
* `-i, --name TEXT`: ID of the runtime
* `--help`: Show this message and exit.

### `inferless runtime version-list`

use to list the runtime versions

**Usage**:

```console
$ inferless runtime version-list [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: runtime name
* `--help`: Show this message and exit.

## `inferless scaffold`

Scaffold a demo Inferless project

**Usage**:

```console
$ inferless scaffold [OPTIONS]
```

**Options**:

* `-d, --demo`: Demo name  [required]
* `--help`: Show this message and exit.

## `inferless secret`

Manage Inferless secrets (list secrets)

**Usage**:

```console
$ inferless secret [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all secrets.

### `inferless secret list`

List all secrets.

**Usage**:

```console
$ inferless secret list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless token`

Manage Inferless tokens

**Usage**:

```console
$ inferless token [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `set`: Set account credentials for connecting to...

### `inferless token set`

Set account credentials for connecting to Inferless. If not provided with the command, you will be prompted to enter your credentials.

**Usage**:

```console
$ inferless token set [OPTIONS]
```

**Options**:

* `--token-key TEXT`: Account CLI key  [required]
* `--token-secret TEXT`: Account CLI secret  [required]
* `--help`: Show this message and exit.

## `inferless volume`

Manage Inferless volumes (can be used to list volumes and create new volumes)

**Usage**:

```console
$ inferless volume [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `cp`: Add a file or directory to a volume.
* `create`: Create a new volume
* `list`: List all existing volumes
* `ls`: List files and directories within a volume
* `rm`: Specify the Inferless path to the file or...

### `inferless volume cp`

Add a file or directory to a volume.

**Usage**:

```console
$ inferless volume cp [OPTIONS]
```

**Options**:

* `-s, --source TEXT`: Specify the source path (either a local directory/file path or an Inferless path)
* `-d, --destination TEXT`: Specify the destination path (either a local directory/file path or an Inferless path)
* `-r, --recursive`: Recursively copy the contents of a directory to the destination.
* `--help`: Show this message and exit.

### `inferless volume create`

Create a new volume

**Usage**:

```console
$ inferless volume create [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Assign a name to the new volume.
* `--help`: Show this message and exit.

### `inferless volume list`

List all existing volumes

**Usage**:

```console
$ inferless volume list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `inferless volume ls`

List files and directories within a volume

**Usage**:

```console
$ inferless volume ls [OPTIONS] PATH
```

**Arguments**:

* `PATH`: Specify the infer path to the directory  [required]

**Options**:

* `-d, --directory`: List only directories.
* `-f, --files`: List only files.
* `-r, --recursive`: Recursively list contents of directories.
* `--help`: Show this message and exit.

### `inferless volume rm`

Specify the Inferless path to the file or directory you want to delete.

**Usage**:

```console
$ inferless volume rm [OPTIONS]
```

**Options**:

* `-p, --path TEXT`: Infer Path to the file/dir your want to delete
* `--help`: Show this message and exit.

## `inferless workspace`

Manage Inferless workspaces (can be used to switch between workspaces)

**Usage**:

```console
$ inferless workspace [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `use`

### `inferless workspace use`

**Usage**:

```console
$ inferless workspace use [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
