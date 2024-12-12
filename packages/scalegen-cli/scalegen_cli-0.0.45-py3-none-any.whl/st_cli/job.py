import glob
import click
import os


from .const import PRODUCT_TYPE
from .datamodels.datamodels.cli import JobLaunchRequest
from .client import send_request
from .datamodels.datamodels import *
from .utils import (
    CustomSpinner,
    get_template,
    run_command,
    zip_and_upload,
    display_event_logs,
    show_job_live_logs,
    is_repo_private,
)


@click.group(name="job", chain=True)
def job():
    """
    Create a job
    """
    pass


@job.command("create")
@click.option("--virtual_mount", type=click.STRING, required=False, multiple=True)
@click.option("-e", "--env_var", type=click.STRING, required=False, multiple=True)
@click.option("--exclude_dir", type=click.STRING, required=False, multiple=True)
@click.option("--cloud", type=ProviderEnum, required=False, multiple=True)
@click.option("--artifacts_storage", type=click.STRING, required=False)
@click.option("--name", type=click.STRING, required=False)
@click.option("--gpu_type", type=click.STRING, required=False, multiple=True)
@click.option("--gpus", type=click.INT, required=True)
@click.option("--cuda", type=click.FLOAT, required=False)
@click.option("--python_version", type=click.FLOAT, required=False)
@click.option("--image_template", type=click.STRING, required=False)
@click.option(
    "--requirements", type=click.STRING, required=False, default="requirements.txt"
)
@click.option("--pre_job_script", type=click.STRING, required=False, default="")
@click.option("--working_dir", type=click.STRING, required=False, default="")
@click.option("--ignore_git", is_flag=True)
@click.option("--use_env", is_flag=True)
@click.option("--epochs", type=click.INT, required=False, default=0)
@click.option("--use_spot", is_flag=True)
@click.option("--quiet", is_flag=True)
@click.option("--min_vcpus", type=click.INT, required=False, default=4)
@click.option("--min_memory", type=click.INT, required=False, default=8)
@click.argument("command", type=click.STRING, required=True)
def create(**kwargs):
    """
    Function to launch a job
    """

    entrypoint = os.path.join(
        kwargs.get("working_dir", ""), kwargs.get("command", "").split()[0]
    )
    requirements = os.path.join(
        kwargs.get("working_dir", ""), kwargs.get("requirements", "")
    )
    pre_job_script = kwargs.get("pre_job_script", "")

    # Verify script file
    if entrypoint not in glob.glob("**", recursive=True):
        click.echo(
            click.style(f"File: {entrypoint} does not exist", fg="red"), err=True
        )
        return

    # Verify requirements
    if (not requirements and not kwargs["image_template"]) or (
        requirements and requirements not in glob.glob("**", recursive=True)
    ):
        click.echo(
            click.style(
                f"Please specify a valid requirements file (--requirements) or --image_template",
                fg="red",
            ),
            err=True,
        )
        return

    # Prepare virtual mounts
    virtual_mounts_config = []
    for vmount in kwargs["virtual_mount"]:
        virtual_mounts_config.append({"name": vmount})

    # Prepare Artifacts storage
    as_config = None
    if kwargs["artifacts_storage"]:
        as_config = {"name": kwargs["artifacts_storage"]}

    # Cloud config
    cloud_config = []
    if kwargs["cloud"]:
        resp = send_request("GET", "/cloud")
        if resp.status_code == 200:
            reg_clouds = resp.json()
            for reg_cloud in reg_clouds:
                if ProviderEnum(reg_cloud["cloud_provider"]) in kwargs["cloud"]:
                    cloud_config.append(
                        {
                            "name": reg_cloud["cloud_provider"],
                            "regions": reg_cloud["regions"],
                        }
                    )

    # DAPP
    kwargs["use_dlop"] = kwargs["epochs"] > 0
    # click.echo(click.style(f"Please specify epochs with --epochs when use_dlop is enabled", fg="red"), err=True)
    # return

    # Upload code to B2 bucket via Lambda
    codeTransfer = None

    # Upload to git if the folder is not a git repo or the git repo has some un-commited changes
    if (
        ".git" in os.listdir()
        and os.path.isdir(".git")
        and not kwargs.get("ignore_git", False)
    ):
        ###
        # Read the git repository
        ###
        out = run_command("git status")
        if "modified" in out:
            codeTransfer = zip_and_upload(kwargs.get("working_dir", ""), kwargs.get("exclude_dir"))  # type: ignore

        commit = run_command("git rev-parse HEAD")
        repo = run_command("git config --get remote.origin.url")

        if is_repo_private():
            click.echo(
                click.style(
                    f"Current folder is a clone of a private git repository. Please pass --ignore_git to use the local copy of the folder",
                    fg="red",
                ),
                err=True,
            )
            return

        codeTransfer = CodeCopy(
            type=CodeCopyType.GITHUB,
            repo=repo,
            ref=commit,
            codeDir=kwargs.get("working_dir", ""),
        ).model_dump(mode="json")

    else:
        codeTransfer = zip_and_upload(kwargs.get("working_dir", ""), kwargs.get("exclude_dir"))  # type: ignore

    if not codeTransfer:
        # zip_and_upload function would have printed the error message
        return

    # Pre job commands
    pre_job_commands = []
    if pre_job_script:
        if pre_job_script not in glob.glob("**", recursive=True):
            click.echo(
                click.style(f"File: {pre_job_script} does not exist", fg="red"),
                err=True,
            )
            return
        else:
            with open(pre_job_script, "r") as fp:
                pre_job_commands = list(map(lambda x: x.strip("\n"), fp.readlines()))

    # Environment variables
    environment = {}
    if kwargs.get("use_env", False):
        environment = dict(os.environ)

    option_env_vars = {}
    for env_var in kwargs.get("env_var", []):
        if env_var.count("=") != 1:
            click.echo(
                click.style(
                    f"Env variables should be of the format 'KEY=VALUE'. For example '--env_var MY_KEY=MY_VALUE' and '-e MY_KEY=MY_VALUE'",
                    fg="red",
                ),
                err=True,
            )
            return
        key, val = env_var.split("=")
        if key == "CUDA_VISIBLE_DEVICES":
            click.echo(
                click.style(
                    f"WARNING: Environment variable 'CUDA_VISIBLE_DEVICES' will be ignored",
                    fg="yellow",
                )
            )

        option_env_vars[key] = val

    environment.update(option_env_vars)

    # Prepare other config
    if kwargs.get("gpus", 0) in {0, None}:
        sub_conf = {
            "maxCPUWorkers": 1,
        }
    else:
        sub_conf = {
            "gpusPerTrial": kwargs["gpus"],
            "maxGpus": kwargs["gpus"],
        }

    config = {
        "name": kwargs["name"],
        "cuda": kwargs.get("cuda", "11.6"),
        "gpuTypes": list(kwargs["gpu_type"]),
        "entrypoint": kwargs["command"],
        "requirements": kwargs["requirements"],
        "cloudProviders": cloud_config,
        "codeTransfer": codeTransfer,
        "experiment": {"args": {" ": [" "]}},
        "maxTrials": 1,
        "useDAPP": kwargs["use_dlop"],
        "virtualMounts": virtual_mounts_config,
        "artifactsDestination": as_config,
        "use_spot": kwargs["use_spot"],
        "preJobCommands": pre_job_commands,
        "dapp": {"epochs": kwargs["epochs"]},
        "minvCPUs": kwargs.get("min_vcpus", 4),
        "minMemory": kwargs.get("min_memory", 8),
        "environment": environment,
        "python_version": kwargs.get("python_version", 3.8),
    }
    config.update(sub_conf)

    # print(config)

    try:
        config_obj = ScaleTorchConfig(**config)  # Valid config
    except Exception as e:
        click.echo(click.style(f"Validation Error: {e}", fg="red"), err=True)
        exit()

    # print(config_obj)
    # exit()

    ###
    # Launch the workload
    ###
    job_type = JobType.SIMPLE_JOB
    req_data = JobLaunchRequest(
        config=config_obj, type=job_type, productType=ProductType(PRODUCT_TYPE)
    ).model_dump(mode="json")

    # print(req_data['config'])
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

    if not kwargs["quiet"]:
        display_event_logs(job_id)

        show_job_live_logs(job_id)
