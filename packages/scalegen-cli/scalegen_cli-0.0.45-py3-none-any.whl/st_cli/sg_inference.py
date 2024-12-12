# Standard modules
from datetime import timezone
import json
import os
from datetime import timezone
from typing import Any, Dict, List

# Third-party modules
import click
import dateutil.parser
import yaml
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Product modules
from .client import get_garb, send_request
from .datamodels.datamodels.api import (
    InferenceDeploymentAutoscalingConfig,
    InferenceControllerCloudConfig,
    InferenceControllerOnPremConfig,
    InferenceDeploymentIn,
    InferenceDeploymentStatus,
    InferenceDeploymentAutoscalingConfig,
    LLMLoraConfig,
    ProviderEnum,
)
from .utils import CategorizedMutuallyExclusiveOption, PatchedCommand

DEFAULT_AUTOSCALING_CONFIG = InferenceDeploymentAutoscalingConfig()


def get_deployment(inf_id: str) -> Dict[str, Any]:
    console = Console()

    with console.status(f"[bold green]Getting deployment with inf_id {inf_id}...") as _:

        resp = send_request("GET", f"/sg_inf/{inf_id}")

    if resp.status_code == 204:
        click.echo(
            click.style(f"Deployment with inf_id {inf_id} not found", fg="red"),
            err=True,
        )
        exit()

    elif resp.status_code != 200:
        click.echo(click.style(f"Could not fetch deployment", fg="red"), err=True)
        exit()

    deployment = resp.json()
    return deployment


def get_deployments(should_exist: bool = True) -> List[Dict[str, Any]]:
    console = Console()

    with console.status("[bold green]Getting existing deployments...") as _:

        resp = send_request("GET", "/sg_inf/list")

    if resp.status_code == 204:
        if should_exist:
            click.echo(
                click.style(
                    f"No deployments found. Create one with 'scalegen infer create'",
                    fg="blue",
                ),
                err=should_exist,
            )
        return []

    elif resp.status_code != 200:
        click.echo(click.style(f"Could not fetch deployments", fg="red"), err=True)
        exit()

    deployments: List[Dict[str, Any]] = resp.json()
    deployments.sort(key=lambda dep: dep["name"])

    return deployments


def print_inference_deployments(
    deployments: List[Dict[str, Any]],
    table_title: str = "Inference Deployments",
    plain: bool = False,
):
    table = Table(
        show_header=True,
        # header_style='bold #2070b2',
        # title='[bold] Jobs',
        title=table_title,
        box=None if plain else box.DOUBLE_EDGE,
    )

    col_names = [
        "Inference ID",
        "Name",
        "Model",
        "Allow Spot Instances",
        "Current Price Per Hour",
        "Status",
        # "API Gateway",
    ]

    for col in col_names:
        table.add_column(col)

    provisioning = sorted(
        [
            d
            for d in deployments
            if d["status"] == InferenceDeploymentStatus.PROVISIONING
        ],
        key=lambda dep: dateutil.parser.parse(dep["timestamp"]).replace(
            tzinfo=timezone.utc
        ),
        reverse=True,
    )
    active = sorted(
        [d for d in deployments if d["status"] == InferenceDeploymentStatus.ACTIVE],
        key=lambda dep: dateutil.parser.parse(dep["timestamp"]).replace(
            tzinfo=timezone.utc
        ),
        reverse=True,
    )
    inactive = sorted(
        [d for d in deployments if d["status"] == InferenceDeploymentStatus.INACTIVE],
        key=lambda dep: dateutil.parser.parse(dep["timestamp"]).replace(
            tzinfo=timezone.utc
        ),
        reverse=True,
    )
    deleted = sorted(
        [
            d
            for d in deployments
            if d["status"]
            not in [
                InferenceDeploymentStatus.PROVISIONING,
                InferenceDeploymentStatus.ACTIVE,
                InferenceDeploymentStatus.INACTIVE,
            ]
        ],
        key=lambda dep: dateutil.parser.parse(dep["timestamp"]).replace(
            tzinfo=timezone.utc
        ),
        reverse=True,
    )

    deployments = provisioning + active + inactive + deleted

    for depl in deployments:
        row = [
            depl["id"],
            depl["name"],
            depl["model"],
            str(depl["allow_spot_instances"]),
            str(round(depl["current_price_per_hour"], 3)),
            depl["status"],
            # depl["link"],
        ]
        # if row[-1] is None:
        #     row[-1] = "Unavailable"
        # else:
        #     row[-1] = print_to_string(
        #         f"[link={depl['link'] + '/inference'}]Inference link[/link]\n"
        #         f"[link={depl['link'] + '/metrics'}]Metrics link[/link]",
        #         end="",
        #     )

        table.add_row(*row)

    console = Console()

    if table.row_count <= 15 or plain:
        console.print(table, justify="left")
    else:
        with console.pager():
            console.print(table, justify="left")


def verify_cloud_config_options(kwargs: Dict[str, Any]):
    # If controller_on_prem_id is provided, then warn that all other controller_cloud options will be ignored
    if kwargs["controller_on_prem_node_id"]:
        if (
            kwargs["controller_cloud_provider"]
            or kwargs["controller_cloud_region"]
            or kwargs["vpc_id"]
            or kwargs["use_api_gateway"]
        ):
            click.echo(
                click.style(
                    "Warning: All other controller cloud options will be ignored since controller_on_prem_node_id is provided",
                    fg="yellow",
                ),
                err=True,
            )
        return InferenceControllerOnPremConfig(
            use_ssl=kwargs.get("use_ssl", True),
            on_prem_node_id=kwargs["controller_on_prem_node_id"],
        )
    else:
        # At least controller_cloud_provider and controller_cloud_region should be provided
        if (
            not kwargs["controller_cloud_provider"]
            or not kwargs["controller_cloud_region"]
        ):
            click.echo(
                click.style(
                    "Error: controller_cloud_provider and controller_cloud_region must be provided",
                    fg="red",
                ),
                err=True,
            )
            exit()

        return InferenceControllerCloudConfig(
            public_url=kwargs["use_public_url"],
            use_ssl=kwargs["use_ssl"],
            use_api_gateway=kwargs["use_api_gateway"],
            vpc_id=kwargs["vpc_id"],
            cloud_provider=kwargs["controller_cloud_provider"],
            region=kwargs["controller_cloud_region"],
        )


def verify_lora_options(kwargs: Dict[str, Any]):
    name_token_dict = {}
    for lora_name, hf_token in kwargs["lora_adapter_hf_token"]:
        name_token_dict[lora_name] = hf_token

    lora_configs = []
    for lora_name, repo in kwargs["lora_adapter"]:
        lora_configs.append(
            LLMLoraConfig(
                name=lora_name,
                hf_repo=repo,
                hf_token=name_token_dict.get(lora_name, None),
            )
        )

    return lora_configs


@click.group(name="infer", chain=True)
def infer():
    """
    ScaleGen commands for managing inference deployments
    """
    pass


def create_inf_dep(
    inf_dep_req_data: InferenceDeploymentIn, quiet: bool = False, force: bool = False
):

    console = Console()

    with console.status("[bold green]Creating new deployment...") as status:
        resp = send_request(
            "POST", "/sg_inf/create", data=inf_dep_req_data.model_dump(mode="json")
        )
        inf_id = ""

    if resp.status_code == 200:
        resp_data = resp.json()
        # P-API returns dict for CREATE request
        inf_id = resp_data["message"]["inf_id"]
        click.echo(click.style(f"Created deployment - Id: {inf_id}", fg="green"))

    elif resp.status_code == 500:
        resp_data = resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"Something went wrong: {resp_data}. Please try creating deployment later",
                fg="red",
            ),
            err=True,
        )
        exit()

    else:
        try:
            resp_data = resp.json()
            click.echo(
                click.style(f"Couldn't not create deployment: {resp_data}", fg="red"),
                err=True,
            )
        except Exception as e:
            click.echo(
                click.style(f"Couldn't not create deployment", fg="red"), err=True
            )
        exit()

    # Exit if quiet was passed
    if not quiet:
        print_inference_deployments(
            [get_deployment(inf_id)],
            table_title="New Deployment Added",
        )


@infer.command(
    "create",
    cls=PatchedCommand,
    context_settings=dict(max_content_width=150),
)
# ******************************* COMMON OPTIONS *******************************
@click.option(
    "--name", type=click.STRING, required=True, help="Inference deployment name to use."
)
@click.option("--model", type=click.STRING, required=True, help="Model to use.")
@click.option(
    "--base_model", type=click.STRING, required=False, help="Base model to use."
)
@click.option(
    "--inf_type",
    type=click.Choice(["embedding", "llm", "tti", "vlm"]),
    required=True,
    help="Inference deployment type to use.",
)
@click.option(
    "--engine",
    type=click.Choice(["vllm", "tei", "nim", "lmdeploy", "nos", "friendli"]),
    required=False,
    default=None,
    help="Inference engine to use",
)
@click.option(
    "--hf_token",
    type=click.STRING,
    required=False,
    help="Hugging Face token to use.",
)
@click.option(
    "--logs_store", type=click.STRING, required=False, help="Logs store to use."
)
@click.option(
    "--max_price_per_hour",
    type=click.INT,
    required=False,
    help="The maximum price you are willing to spend per hour.",
)
@click.option("-f", "--force", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
# ******************************* CLOUD PROVIDER OPTIONS *******************************
@click.option(
    "--cloud_regions",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    multiple=True,
    help="Specify cloud region in following style <PROVIDER>:<region>. "
    + click.style("Example: AWS:us-east-1.", italic=True),
    category="Cloud provider options",
)
@click.option(
    "--use_spot",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Use spot instances.",
    category="Cloud provider options",
)
# ******************************* AUTO-SCALING OPTIONS *******************************
@click.option(
    "--enable_fast_autoscaling",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Enable fast auto scaling with stopped spare nodes.",
    category="Auto-scaling options",
)
@click.option(
    "--scale_to_zero",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Enable scaling to zero.",
    category="Auto-scaling options",
)
@click.option(
    "--lower_allowed_threshold",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.lower_allowed_threshold,
    help="Lower allowed threshold to use. Seconds for ttft strategy and RPS for rps_per_worker strategy.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--upper_allowed_threshold",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.upper_allowed_threshold,
    help="Lower allowed threshold to use. Seconds for ttft strategy and RPS for rps_per_worker strategy.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scale_to_zero_timeout_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scale_to_zero_timeout_sec,
    help="Scaling down to zero timeout in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scaling_down_timeout_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scaling_down_timeout_sec,
    help="Scaling down timeout in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scaling_up_timeout_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scaling_up_timeout_sec,
    help="Scaling up timeout in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scale_down_time_window_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scale_down_time_window_sec,
    help="Scaling down time window in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scale_up_time_window_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scale_up_time_window_sec,
    help="Scaling up time window in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--autoscaling_strategy",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.Choice(["rps_per_worker", "ttft_latency_sec", "e2e_latency_sec"]),
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.autoscaling_strategy,
    help="Autoscaling strategy to use.",
    category="Auto-scaling options",
    show_default=True,
)
# ******************************* MIN THROUGHPUT CONFIGURATION OPTIONS *******************************
@click.option(
    "--min_throughput_rate",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    help="The minimum throughput rate you need to.",
    mutually_exclusive=[
        "min_workers",
        "use_same_gpus_when_scaling",
        "initial_workers_gpu_num",
        "initial_workers_gpu_type",
        "instance_types",
    ],
    category="Minimum throughput configuration options",
)
# ******************************* OPTIMAL WORKER CONFIGURATION OPTIONS *******************************
@click.option(
    "--min_workers",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    default=0,
    help="The minimum number of workers to scale down to.",
    category="Optimal worker configuration options",
    mutually_exclusive=["min_throughput_rate"],
    show_default=True,
)
@click.option(
    "--use_same_gpus_when_scaling",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Enable to use same GPU type when scaling up.",
    category="Optimal worker configuration options",
    mutually_exclusive=["min_throughput_rate"],
)
@click.option(
    "--initial_workers_gpu_num",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    help="Initial number of GPUs per worker.",
    category="Optimal worker configuration options",
    mutually_exclusive=["min_throughput_rate"],
)
@click.option(
    "--initial_workers_gpu_type",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    help="Inital Type of worker eg. A10G",
    category="Options responsible for optimal worker configuration",
    mutually_exclusive=["min_throughput_rate"],
)
@click.option(
    "--strict_gpu_types",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    help="For A100, H100 GPUs, this option when set includes PCIE, SXM and NVLINK variants.",
    category="Options responsible for optimal worker configuration",
    mutually_exclusive=["min_throughput_rate"],
)
@click.option(
    "--instance_types",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    multiple=True,
    help="Provide space-separated list of instance types.",
    category="Optimal worker configuration options",
    mutually_exclusive=[
        "min_throughput_rate",
        "initial_workers_gpu_type",
        "initial_workers_gpu_num",
        "use_same_gpus_when_scaling",
    ],
)
# ******************************* CONTROLLER CONFIGUARION OPTIONS *******************************
@click.option(
    "--use_ssl",
    cls=CategorizedMutuallyExclusiveOption,
    help="Specify whether to use SSL for the inference API. Will be ignored if use_api_gateway is True.",
    is_flag=True,
    category="Controller node configuration options",
)
@click.option(
    "--use_public_url",
    cls=CategorizedMutuallyExclusiveOption,
    help="Specify whether to use public URL for the inference API. Will be ignored if use_api_gateway is True.",
    is_flag=True,
    category="Controller node configuration options",
)
@click.option(
    "--use_api_gateway",
    cls=CategorizedMutuallyExclusiveOption,
    help="Specify whether to use API Gateway for the inference API. Only supported for AWS.",
    is_flag=True,
    category="Controller node configuration options",
)
@click.option(
    "--controller_cloud_provider",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    default=ProviderEnum.AWS.value,
    help="Specify controller cloud provider. "
    + click.style("Example: AWS", italic=True),
    show_default=True,
    category="Controller node configuration options",
)
@click.option(
    "--controller_cloud_region",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    default="us-east-1",
    help="Specify controller cloud region. "
    + click.style("Example: us-east-1", italic=True),
    show_default=True,
    category="Controller node configuration options",
)
@click.option(
    "--vpc_id",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    help="Specify VPC ID to be used for controller and api_gateway (if specified). Only supported for AWS.",
    show_default=True,
    category="Controller node configuration options",
)
@click.option(
    "--controller_on_prem_node_id",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    help="Specify the on prem node to be used as controller",
    show_default=True,
    category="Controller node configuration options",
)
# ******************************* OPTIMAL WORKER CONFIGURATION OPTIONS *******************************
@click.option(
    "--lora_adapter",
    "-la",
    type=(str, str),
    required=False,
    help="Specify the lora name and hf repo of the lora adapter to use, ex: --lora_adapter example_name <hf_repo>",
    show_default=True,
    multiple=True,
)
@click.option(
    "--lora_adapter_hf_token",
    type=(str, str),
    required=False,
    help="Specify the HF Hub token for the lora adapter repo, usage ex: --lora_adapter_hf_token example_name <hf_token>",
    show_default=True,
    multiple=True,
)
# ******************************* Miscellaneous options *******************************
@click.option(
    "--max_model_len",
    type=int,
    required=False,
    help="Max Sequence length to be used by the inference engine",
)
@click.option(
    "--throughput_optimized",
    is_flag=True,
    required=False,
    help="Enable throughput optimization",
)
@click.option("-f", "--force", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
def create_impl(**inference_kwargs: Any):
    """
    Create an inference deployment
    """

    if inference_kwargs["min_workers"] > 0 and inference_kwargs["scale_to_zero"]:
        click.echo(
            click.style(
                f"\nUsing two conflicting arguments --min_workers and --scale_to_zero. "
                f"To solve conflict disable --scale_to_zero option or set --min_workers to 0 (default value).",
                fg="red",
            ),
            err=True,
        )
        exit()

    # Verify controller_config
    controller_config = verify_cloud_config_options(inference_kwargs)

    # Verify lora config
    lora_config = verify_lora_options(inference_kwargs)

    # Get existing deployments
    deployments: List[Dict[str, Any]] = get_deployments(should_exist=False)

    # Check if there is already a deployment with the same model
    similar_deployments: List[str] = list(
        map(
            lambda x: x["id"],
            filter(
                lambda x: x["model"] == inference_kwargs["model"]
                and x["status"] == "RUNNING",
                deployments,
            ),
        )
    )
    if similar_deployments and not inference_kwargs["force"]:
        # If exists, Warn the user
        if not click.confirm(
            click.style(
                f"This model is already deployed and is active with id(s): {similar_deployments}. Do you want to continue?",
                fg="yellow",
            )
        ):
            exit()

    # Make request to P-API
    if not inference_kwargs["inf_type"] in ["llm", "embedding", "tti"]:
        click.echo(
            click.style(
                f"\nType value must be one of [ llm , embedding, tti]",
                fg="red",
            ),
            err=True,
        )
        exit()

    cloud_providers = []
    if inference_kwargs["cloud_regions"]:
        cloud_providers_dict: Dict[str, List[str]] = {}
        for cloud_region in inference_kwargs["cloud_regions"]:
            cloud, region = str(cloud_region).split(":")

            if cloud not in cloud_providers_dict:
                cloud_providers_dict[cloud] = [region]
            else:
                cloud_providers_dict[cloud].append(region)

        cloud_providers = [
            {"name": key, "regions": value}
            for key, value in cloud_providers_dict.items()
        ]

    data = {
        "name": inference_kwargs["name"],
        "model": inference_kwargs["model"],
        "base_model": inference_kwargs["base_model"],
        "llm_loras": lora_config,
        "inf_type": inference_kwargs["inf_type"],
        "engine": inference_kwargs["engine"],
        "hf_token": inference_kwargs["hf_token"],
        "allow_spot_instances": inference_kwargs["use_spot"],
        "logs_store": inference_kwargs["logs_store"],
        "cloud_providers": cloud_providers,
        "initial_worker_config": {
            "min_workers": inference_kwargs["min_workers"],
            "initial_workers_gpu": inference_kwargs["initial_workers_gpu_type"],
            "initial_workers_gpu_num": inference_kwargs["initial_workers_gpu_num"],
            "use_other_gpus": not inference_kwargs["use_same_gpus_when_scaling"],
            "instance_types": inference_kwargs["instance_types"],
            "expand_gpu_types": not bool(inference_kwargs["strict_gpu_types"]),
        },
        "autoscaling_config": {
            "enable_fast_autoscaling": inference_kwargs["enable_fast_autoscaling"],
            "scale_to_zero": inference_kwargs["scale_to_zero"],
            "scale_up_time_window_sec": inference_kwargs["scale_up_time_window_sec"],
            "scale_down_time_window_sec": inference_kwargs[
                "scale_down_time_window_sec"
            ],
            "upper_allowed_threshold": inference_kwargs["upper_allowed_threshold"],
            "lower_allowed_threshold": inference_kwargs["lower_allowed_threshold"],
            "scaling_up_timeout_sec": inference_kwargs["scaling_up_timeout_sec"],
            "scaling_down_timeout_sec": inference_kwargs["scaling_down_timeout_sec"],
            "scale_to_zero_timeout_sec": inference_kwargs["scale_to_zero_timeout_sec"],
            "autoscaling_strategy": inference_kwargs["autoscaling_strategy"],
        },
        "controller_cloud_config": (
            controller_config
            if isinstance(controller_config, InferenceControllerCloudConfig)
            else None
        ),
        "controller_on_prem_config": (
            controller_config
            if isinstance(controller_config, InferenceControllerOnPremConfig)
            else None
        ),
        "max_price_per_hour": inference_kwargs["max_price_per_hour"],
        "min_throughput_rate": inference_kwargs["min_throughput_rate"],
        "max_model_len": inference_kwargs["max_model_len"],
        "throughput_optimized": inference_kwargs["throughput_optimized"],
    }

    inf_dep_req_data = InferenceDeploymentIn(**data)

    # print(inf_dep_req_data.model_dump_json(indent=3))
    # exit()

    create_inf_dep(
        inf_dep_req_data,
        quiet=inference_kwargs["quiet"],
        force=inference_kwargs["force"],
    )


@infer.command("launch")
@click.argument("config_file", type=click.STRING, required=True)
@click.option("-f", "--force", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
def launch_impl(config_file, force, quiet):
    """
    Launch an inference deployment using a config YAML file
    """
    # check if config_file is an absolute path
    config_path = config_file
    if not os.path.isabs(config_file):
        config_path = os.path.join(os.getcwd(), config_file)

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

    try:
        inf_dep_create_req = InferenceDeploymentIn(**dict_from_yaml)  # Valid config
    except Exception as e:
        click.echo(click.style(f"Validation Error: {e}", fg="red"), err=True)
        exit()

    create_inf_dep(inf_dep_create_req, quiet, force)


@infer.command("start")
@click.argument("inf_id", type=click.STRING, required=True)
@click.option("-f", "--force", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
def start_impl(inf_id: str, force: bool, quiet: bool):
    """
    Allows user to make the InferenceDeployment Active in case
    its been scaled to zero because of no-requests (status is INACTIVE)
    """

    dep = get_deployment(inf_id)
    if dep["status"] == InferenceDeploymentStatus.ACTIVE and not force:
        click.echo(
            click.style(f"Deployment with inf_id {inf_id} is already active", fg="red"),
            err=True,
        )
        exit()

    console = Console()

    with console.status(f"[bold green]Scaling deployment with inf_id {inf_id}...") as _:

        resp = send_request("POST", f"/sg_inf/{inf_id}/scale/up")

    if resp.status_code == 200:
        resp_data = resp.json()
        click.echo(
            click.style(
                f"\nScale up request for deployment: {inf_id} was sent successfully",
                fg="green",
            )
        )
    elif resp.status_code == 500:
        resp_data = resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"\nSomething went wrong: {resp_data}. Please try scaling deployment later",
                fg="red",
            ),
            err=True,
        )
        exit()
    else:
        try:
            resp_data = resp.json()
            click.echo(
                click.style(f"\nCould not scale up deployment: {resp_data}", fg="red"),
                err=True,
            )
        except Exception as e:
            click.echo(
                click.style(f"\nCould not scale up deployment", fg="red"), err=True
            )
        exit()

    # Exit if quiet was passed
    if not quiet:
        print_inference_deployments(
            [get_deployment(inf_id)],
            table_title="Deployment started!",
        )


@infer.command("stop")
@click.option("-f", "--force", is_flag=True)
@click.argument("inf_id", type=click.STRING, required=True)
def stop_impl(inf_id: str, force: bool = False):
    """
    Allows user to make the InferenceDeployment go to INACTIVE state
    """

    dep = get_deployment(inf_id)
    if dep["status"] != InferenceDeploymentStatus.ACTIVE and not force:
        click.echo(
            click.style(f"Deployment with inf_id {inf_id} is not active", fg="red"),
            err=True,
        )
        exit()

    console = Console()
    with console.status(f"[bold green]Scaling deployment with inf_id {inf_id}...") as _:
        resp = send_request(
            "POST", f"/sg_inf/{inf_id}/scale/zero", params={"force": force}
        )

    if resp.status_code == 200:
        resp_data = resp.json()
        click.echo(
            click.style(
                f"Stop/Scale to Zero request for deployment: {inf_id} was sent successfully",
                fg="green",
            )
        )
    else:
        resp_data = resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"\nSomething went wrong: {resp_data}. Please try scaling deployment later",
                fg="red",
            ),
            err=True,
        )
        exit()


@infer.command("delete")
@click.argument("inf_id", type=click.STRING, required=True)
@click.option("-q", "--quiet", is_flag=True)
@click.option("-f", "--force", is_flag=True)
def delete_impl(inf_id: str, quiet: bool, force: bool = False):
    """
    Delete an inference deployment
    """

    console = Console()

    with console.status(
        f"[bold green]Deleting deployment with inf_id {inf_id}..."
    ) as status:

        resp = send_request("DELETE", f"/sg_inf/{inf_id}", params={"force": force})

    if resp.status_code == 200:
        resp_data = resp.json()
        click.echo(
            click.style(
                f"\nDelete request for deployment with id: {inf_id} is successful",
                fg="green",
            )
        )
    elif resp.status_code == 500:
        resp_data = resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"\nSomething went wrong: {resp_data}. Please try deleting deployment later",
                fg="red",
            ),
            err=True,
        )
        exit()
    else:
        try:
            resp_data = resp.json()
            click.echo(
                click.style(f"\nCould not delete deployment: {resp_data}", fg="red"),
                err=True,
            )
        except Exception as e:
            click.echo(
                click.style(f"\nCould not delete deployment", fg="red"), err=True
            )
        exit()

    if not quiet:
        print_inference_deployments(
            [get_deployment(inf_id)],
            table_title="Deployment deleted!",
        )


@infer.command("list")
@click.option("-p", "--plain", is_flag=True)
def list_impl(plain: bool):
    """
    Print the list of existing inference deployments
    """

    # Get existing deployments
    deployments = get_deployments(should_exist=True)

    print_inference_deployments(deployments, plain=plain)


@infer.command("view")
@click.argument("inf_id", type=click.STRING, required=True)
def view_impl(inf_id: str):
    """
    Print information about a single inference deployment
    """

    console = Console()
    inf_dep = get_deployment(inf_id)

    markdown_content = (
        f"[bold][orange_red1]ID[/orange_red1] : [cyan]{inf_dep['id']}[/cyan]\n"
    )
    markdown_content += (
        f"[orange_red1]Name[/orange_red1] : [yellow]{inf_dep['name']}[/yellow]\n"
    )
    markdown_content += (
        f"[orange_red1]Status[/orange_red1] : [yellow]{inf_dep['status']}[/yellow]\n"
    )
    markdown_content += f"[orange_red1]Cost[/orange_red1] : [yellow]$ {round(inf_dep['current_price_per_hour'], 3)}[/yellow]\n"
    markdown_content += (
        f"[orange_red1]Model[/orange_red1] : [yellow]{inf_dep['model']}[/yellow]\n"
    )

    url = inf_dep.get("link", "")
    if url:
        if inf_dep["inf_type"] in ["llm", "tti", "vlm"]:
            url += "/inference"
        else:
            url += "inference/embed"
    markdown_content += (
        f"[orange_red1]Endpoint[/orange_red1] : [yellow]{url}[/yellow]\n"
    )
    markdown_content += f"[orange_red1]APIKey[/orange_red1] : [yellow]{get_garb('AUTH_ENDPOINT_KEY_' + inf_id)}[/yellow]\n\n"
    markdown_content += (
        f"[bold underline magenta]Autoscaling Configuration[/bold underline magenta]\n"
    )
    markdown_content += f"[orange_red1]Autoscaling strategy [/orange_red1] : [yellow]{inf_dep['autoscaling_config']['autoscaling_strategy']}[/yellow]\n"
    markdown_content += f"[orange_red1]Scale-up Time Window (sec)[/orange_red1] : [yellow]{inf_dep['autoscaling_config']['scale_up_time_window_sec']}[/yellow]\n"
    markdown_content += f"[orange_red1]Scale-down Time Window (sec)[/orange_red1] : [yellow]{inf_dep['autoscaling_config']['scale_down_time_window_sec']}[/yellow]\n"
    markdown_content += f"[orange_red1]Scale to zero (sec)[/orange_red1] : [yellow]{inf_dep['autoscaling_config']['scale_to_zero']}[/yellow]\n\n"
    markdown_content += (
        f"[bold underline magenta]Worker Configuration[/bold underline magenta]\n"
    )
    markdown_content += f"[orange_red1]Minimum workers[/orange_red1] : [yellow]{inf_dep['initial_worker_config']['min_workers']}[/yellow]\n"
    markdown_content += f"[orange_red1]Maximum price per hr[/orange_red1] : [yellow]{inf_dep['max_price_per_hour']}[/yellow]\n"
    markdown_content += f"[orange_red1]Allow spot instances[/orange_red1] : [yellow]{inf_dep['allow_spot_instances']}[/yellow]\n"
    console.print(Panel(markdown_content))
