import click
import os
import yaml
import glob
from checksumdir import dirhash
from typing import Any, Dict


from .datamodels.datamodels import *
from .datamodels.datamodels.cli import *
from .const import MAX_SIZE_MB, MAX_FILES, PRODUCT_TYPE
from .utils import run_command
from .client import send_request
from .utils import get_template, display_event_logs


@click.command()
@click.option("-c", "--config-file", type=click.STRING, required=False)
@click.option("-t", "--template-name", type=click.STRING, required=False)
@click.option("-q", "--quiet", is_flag=True)
def launch(config_file, template_name, quiet):
    """
    Launch a job using a config file or a template
    """
    """
     - Verifies the config
     - Fetches B2 keys if needed
     - Reads git repo details / Encrypts and uploads code to B2
     - Requests platform_api to launch the workload
    """

    ###
    # Parsing and validating config
    ###
    # template = None
    config_dict: Dict[str, Any] = {}
    is_simple_job: bool = False

    ### Templates ###
    if template_name:
        # Template name is provided

        # Verify whether the template exists
        config_dict = get_template(template_name)
        if not config_dict:
            click.echo(
                click.style(
                    f"The template provided: {template_name} does not exist or is not a Experiment / HPT template",
                    fg="red",
                ),
                err=True,
            )
            return

        # Remove name from template config
        config_dict["name"] = None

        if config_dict.get("experiment", {}).get("args", {}).get(" ", None) == [" "]:
            is_simple_job = True

    if config_file:

        config_path = config_file if config_file else "scaletorch.yml"
        config_path = os.path.join(os.getcwd(), config_path)

        if not os.path.exists(config_path):
            click.echo(
                click.style(
                    f"{config_path} not found. Please specify a valid config file path",
                    fg="red",
                ),
                err=True,
            )
            return

        with open(config_path, "r") as fp:
            config_yaml = fp.read()
            dict_from_yaml = yaml.safe_load(config_yaml)

        if template_name and config_dict:
            config_dict.update(dict_from_yaml)  # Override tempalte values
        else:
            config_dict = dict_from_yaml  # Use the config file as is

    try:
        # Add experiment section for simple jobs
        multiple = 1
        if config_dict.get("numNodes", -1) > 1:
            multiple: int = config_dict.get("numNodes", 1)

        if "experiment" not in config_dict:
            config_dict["experiment"] = {"args": {" ": [" "] * multiple}}
            is_simple_job = True

        config = ScaleTorchConfig(**config_dict)  # Valid config

    except Exception as e:
        click.echo(click.style(f"Validation Error: {e}", fg="red"), err=True)
        exit()

    assert config
    # print(config.json)
    # exit()

    if not config.customImage and not config.codeTransfer:
        if ".git" in os.listdir() and os.path.isdir(".git"):
            ###
            # Read the git repository
            ###
            commit = run_command("git rev-parse HEAD")
            repo = run_command("git config --get remote.origin.url")
            config.codeTransfer = CodeCopy(
                type=CodeCopyType.GITHUB, repo=repo, ref=commit
            )

        else:
            ###
            # Uploading code to B2
            ##
            raise Exception(
                'This folder is not a git repository. Please run the command in a git repository or provide the "codeTransfer" field in the config'
            )
            assert (
                os.path.exists(config.codeDir) == True
            ), "codeDir specified in config does not exist"

            # Check number of files
            all_files = glob.glob(f"{config.codeDir}/**", recursive=True)
            all_files = list(
                filter(lambda x: not os.path.isdir(x), all_files)
            )  # Excluding dir names

            if len(all_files) > MAX_FILES:
                click.echo(
                    click.style(
                        "Folder contains more than 2000 files. Please add the files to be ignored in the `ignore` section of the config",
                        fg="red",
                    ),
                    err=True,
                )
                return

            # Check folder size
            folder_size = sum([os.path.getsize(file) for file in all_files]) / (
                1024**2
            )  # Size in MB
            if folder_size > MAX_SIZE_MB:
                click.echo(
                    click.style(
                        "Folder size is more than 300 MB. Please add the files to be ignored in the `ignore` section of the config",
                        fg="red",
                    ),
                    err=True,
                )
                return

            ###
            # Encrypt and upload
            ###
            sha1_checksum = dirhash(config.codeDir, "sha1")
            # job_id = str(uuid.uuid1())
            # encrpyt_and_upload(files=all_files, checksum=sha1_checksum)

            # code_transfer = LocalCodeCopy(type='LOCAL', checksum=sha1_checksum)

    ###
    # Launch the workload
    ###
    if config.experiment:
        if is_simple_job:
            job_type = JobType.SIMPLE_JOB
        else:
            job_type = JobType.EXPERIMENT
    else:
        job_type = JobType.HPTOPT

    req_data = JobLaunchRequest(
        config=config, type=job_type, productType=ProductType(PRODUCT_TYPE)
    ).model_dump(mode="json")

    # print(req_data)
    # exit()

    resp = send_request("POST", "/job", data=req_data)
    job_id = ""

    if resp.status_code == 201:
        resp_data = resp.json()
        job_id = resp_data["message"]["job_id"]
        click.echo(click.style(f"Launched job - Id: {job_id}", fg="green"))
    else:
        resp_data = (
            resp.json() if resp.status_code != 500 else resp.content.decode("utf-8")
        )
        click.echo(
            click.style(f"Couldn't create workload: {resp_data}", fg="red"), err=True
        )
        return

    if not quiet:
        display_event_logs(job_id)
