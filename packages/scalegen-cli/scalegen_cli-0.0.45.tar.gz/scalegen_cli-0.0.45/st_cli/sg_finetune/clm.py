# Standard modules
from typing import Any, Dict, List, Optional

# Third-party modules
import click
from rich import box
from rich.console import Console
from rich.table import Table

# Product modules
from st_cli.client import send_request
from st_cli.utils import (
    display_event_logs,
    CategorizedMutuallyExclusiveOption,
    PatchedCommand,
)
from st_cli.stop import stop
from st_cli.view import view
from st_cli.launch import launch
from st_cli.datamodels.datamodels import FinetuningIn, GPUType, FinetuningType
from st_cli.datamodels.datamodels.sg_finetune import LLMTrainingParams

DEFAULT_LLM_PARAMS = LLMTrainingParams()


def find_next_word_in_string(input_: str, target: str) -> Optional[str]:
    list_of_words = input_.split()
    try:
        next_word = list_of_words[list_of_words.index(target) + 1]
    except ValueError:
        next_word = None
    return next_word


@click.group(name="clm")
def clm():
    """
    Casual language modeling
    """
    pass


clm.add_command(stop, name="stop")
clm.add_command(view, name="view")
clm.add_command(launch, name="launch")


def create_ft_job(ft_req_data: FinetuningIn, quiet: bool = False):
    console = Console()
    with console.status("[bold green]Launching fine-tuning job...") as _:

        resp = send_request(
            "POST", "/finetune/create", data=ft_req_data.model_dump(mode="json")
        )

    if resp.status_code not in [500, 422]:
        resp_data = resp.json()
        if resp_data.get("warning") is not None:
            warnings_ = resp_data["warning"].split("\n")
            for w in warnings_:
                if w:
                    click.echo(click.style(f"Warning: {w}", fg="yellow"))
        if resp_data["info"] is not None:
            info_ = resp_data["info"].split("\n")
            for i in info_:
                if i:
                    click.echo(click.style(f"Info: {i}", fg="cyan"))
    else:
        resp_data = resp.content.decode("utf-8")

    if resp.status_code == 200:
        job_id = resp_data["message"]["job_id"]
        click.echo(click.style(f"\nLaunched job - Id: {job_id}", fg="green"))
    elif resp.status_code == 400:
        click.echo(
            click.style(f"Bad request: {resp_data['message']}", fg="red"), err=True
        )
        return
    elif resp.status_code == 500:
        click.echo(
            click.style(
                f"\nSomething went wrong: {resp_data}. Please try launch job later",
                fg="red",
            ),
            err=True,
        )
        return
    else:
        click.echo(
            click.style(f"\nCouldn't create workload: {resp_data}", fg="red"), err=True
        )
        return

    if not quiet:
        display_event_logs(job_id, ft_type="clm")


@clm.command(
    name="create",
    cls=PatchedCommand,
    context_settings=dict(max_content_width=150),
)
# ******************************* COMMON OPTIONS *******************************
@click.option(
    "--job_name", type=click.STRING, required=False, help="Fine-tuning job name to use."
)
@click.option("--model", required=True, type=click.STRING, help="Model to use.")
@click.option(
    "--base_model",
    required=False,
    type=click.STRING,
    help="Base model to use. Model must be compatible with base model. If base model is not specified, `--model` value will be used.",
)
@click.option(
    "--finetuning_type",
    type=click.Choice(["default", "reward", "sft", "dpo", "orpo"]),
    required=False,
    default="default",
    show_default=True,
    help="Fine-tuning method to use.",
)
@click.option(
    "--artifacts_storage",
    type=click.STRING,
    required=False,
    help="Artifacts storage (checkpoints store) to use.",
)
@click.option(
    "--wandb_key",
    required=False,
    type=click.STRING,
    help="Specify Weights & Biases key to track experiments.",
)
@click.option(
    "--comet_ml_key",
    required=False,
    type=click.STRING,
    help="Specify Comet ML key to track experiments.",
)
@click.option(
    "--hf_token", required=False, type=click.STRING, help="Hugging Face token to use."
)
@click.option(
    "--hf_username",
    required=False,
    type=click.STRING,
    help="Hugging Face username to use.",
)
@click.option(
    "--push_to_hub",
    required=False,
    is_flag=True,
    help="Push to hub True/False. In case you want to push the trained model to Hugging Face hub.",
)
@click.option(
    "--hf_repo_id",
    required=False,
    type=click.STRING,
    help="Repo id for Hugging Face hub. Format is username/repo_name.",
)
@click.option(
    "--hf_project_name",
    required=False,
    type=click.STRING,
    help="Project name in Hugging Face hub",
)
@click.option("-q", "--quiet", is_flag=True, help="Display status updates of workload.")
# ******************************* DATASET CONFIGURATION OPTIONS *******************************
@click.option(
    "--data_path",
    cls=CategorizedMutuallyExclusiveOption,
    required=True,
    type=click.STRING,
    help="Data path to use. Can be a hugging face dataset or name of a virtual mount (filename is set with `--user_dataset`).",
    category="Dataset configuration options",
)
@click.option(
    "--user_dataset",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    help="Filename of a dataset on virtual mount to use (`--data_path` must be set to a virtual mount name).",
    category="Dataset configuration options",
)
@click.option(
    "--train_subset",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    help="Training data subset to use.",
    category="Dataset configuration options",
)
@click.option(
    "--train_split",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    default="train",
    show_default=True,
    help="Train data split to use.",
    category="Dataset configuration options",
)
@click.option(
    "--valid_subset",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    help="Validation data subset to use.",
    category="Dataset configuration options",
)
@click.option(
    "--valid_split",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    help="Validation data split to use.",
    category="Dataset configuration options",
)
@click.option(
    "--add_eos_token",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Add EOS token to use.",
    category="Dataset configuration options",
)
@click.option(
    "--padding",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["left", "right"]),
    help="Padding side to use.",
    category="Dataset configuration options",
)
@click.option(
    "--apply_chat_template",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["zephyr", "chatml", "tokenizer"]),
    help="Apply chat template.",
    category="Dataset configuration options",
)
# ******************************* COLUMN MAPPING OPTIONS *******************************
@click.option(
    "--text_column",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    default="text",
    show_default=True,
    help="Text column to use.",
    category="Column mapping options",
)
@click.option(
    "--prompt_text_column",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    default="prompt",
    help="Prompt text column to use.",
    category="Column mapping options",
)
@click.option(
    "--rejected_text_column",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    default="text",
    show_default=True,
    help="Rejected text column to use.",
    category="Column mapping options",
)
# ******************************* CLOUD PROVIDER OPTIONS *******************************
@click.option(
    "--cloud_regions",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    multiple=True,
    help="Specify cloud region in following style <PROVIDER>:<region>. "
    + click.style("Example: AWS:us-east-1.", italic=True),
    category="Cloud provieder options",
)
@click.option(
    "--allow_spot_instances",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Allow spot instances.",
    category="Cloud provieder options",
)
# ******************************* OPTIMAL WORKER CONFIGURATION OPTIONS *******************************
@click.option(
    "--use_recipes",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Use Scalegen recipes for optimal workers configuration. All other worker specific options will be ignored.",
    category="Optimal worker configuration options",
    mutually_exclusive=["instance_types"],
)
@click.option(
    "--gpu_type",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    default=GPUType.A10G.value,
    help="Preferred GPU type to use.",
    category="Optimal worker configuration options",
    mutually_exclusive=["instance_types", "use_recipes"],
)
@click.option(
    "--gpu_num",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=1,
    help="Number of GPUs per worker to use.",
    category="Optimal worker configuration options",
    mutually_exclusive=["instance_types", "use_recipes"],
)
@click.option(
    "--instance_types",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    multiple=True,
    help="Provide space-separated list of instance types.",
    category="Optimal worker configuration options",
    mutually_exclusive=["gpu_type", "gpu_num", "use_recipes"],
)
# ******************************* TRAINING CONFIGURATION OPTIONS *******************************
@click.option(
    "--resume_from_checkpoint",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    help="Checkpoint path to use. Can be a hugging face model name or name of a virtual mount (directory is set with `--user_checkpoint`).",
    category="Training configuration options",
)
@click.option(
    "--user_checkpoint_dir",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    default=DEFAULT_LLM_PARAMS.user_checkpoint_dir,
    show_default=True,
    type=click.STRING,
    help="Dirname of a checkpoint in the specified virtual mount or HF model repository.",
    category="Training configuration options",
)
@click.option(
    "--epochs",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=1,
    show_default=True,
    help="Number of training epochs to use.",
    category="Training configuration options",
)
@click.option(
    "--lr",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.FLOAT,
    default=DEFAULT_LLM_PARAMS.lr,
    show_default=True,
    help="Learning rate to use.",
    category="Training configuration options",
)
@click.option(
    "--batch_size",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.batch_size,
    show_default=True,
    help="Training batch size to use.",
    category="Training configuration options",
)
@click.option(
    "--gradient_accumulation_steps",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.gradient_accumulation_steps,
    show_default=True,
    help="Number of updates steps to accumulate the gradients for, before performing a backward/update pass.",
    category="Training configuration options",
)
@click.option(
    "--model_max_length",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    help="The maximum length (in the number of tokens) for inputs up to the maximum size of the context of the base model. If not specified, will be set to the value stored in the associated model's config.",
    category="Training configuration options",
)
@click.option(
    "--block_size",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.block_size,
    show_default=True,
    help="Block size to use for chunking up the input into smaller blocks. If passed -1 or block_size > model_max_length, it will be set to model_max_length.",
    category="Training configuration options",
)
@click.option(
    "--seed",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.seed,
    show_default=True,
    help="Seed to use.",
    category="Training configuration options",
)
@click.option(
    "--optimizer",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    default=DEFAULT_LLM_PARAMS.optimizer,
    show_default=True,
    type=click.Choice(
        [
            "adamw_hf",
            "adamw_torch",
            "adamw_torch_fused",
            "adamw_apex_fused",
            "adamw_anyprecision",
            "adafactor",
        ]
    ),
    help="The optimizer to use.",
    category="Training configuration options",
)
@click.option(
    "--lr_scheduler_type",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(
        [
            "linear",
            "cosine",
            "cosine_with_restarts",
            "polynomial",
            "constant",
            "constant_with_warmup",
            "inverse_sqrt",
            "reduce_lr_on_plateau",
            "cosine_with_min_lr",
            "warmup_stable_decay",
        ]
    ),
    default=DEFAULT_LLM_PARAMS.lr_scheduler_type,
    show_default=True,
    help="Scheduler to use",
    category="Training configuration options",
)
@click.option(
    "--weight_decay",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.FLOAT,
    default=DEFAULT_LLM_PARAMS.weight_decay,
    show_default=True,
    help=" The weight decay to apply (if not zero) to all layers except all bias and LayerNorm weights.",
    category="Training configuration options",
)
@click.option(
    "--warmup_ratio",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.FLOAT,
    default=DEFAULT_LLM_PARAMS.warmup_ratio,
    show_default=True,
    help="Ratio of total training steps used for a linear warmup from 0 to learning_rate.",
    category="Training configuration options",
)
@click.option(
    "--max_grad_norm",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.FLOAT,
    default=DEFAULT_LLM_PARAMS.max_grad_norm,
    show_default=True,
    help="Maximum gradient norm (for gradient clipping).",
    category="Training configuration options",
)
@click.option(
    "--save_steps",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.save_steps,
    show_default=True,
    help="Number of updates steps before two checkpoint saves if save_strategy='step'. Should be an integer or a float in range [0,1). If smaller than 1, will be interpreted as ratio of total training steps.",
    category="Training configuration options",
)
@click.option(
    "--logging_steps",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.logging_steps,
    show_default=True,
    help="Number of update steps between two logs if logging_strategy='steps'. Should be an integer or a float in range [0,1). If smaller than 1, will be interpreted as ratio of total training steps.",
    category="Training configuration options",
)
@click.option(
    "--eval_strategy",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["epoch", "steps", "no"]),
    default=DEFAULT_LLM_PARAMS.eval_strategy,
    show_default=True,
    help="The evaluation strategy to adopt during training.",
    category="Training configuration options",
)
@click.option(
    "--eval_steps",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.eval_steps,
    show_default=True,
    help="Number of update steps between two evaluations if eval_strategy='steps'. Will default to the same value as logging_steps if not set. Should be an integer or a float in range [0,1). If smaller than 1, will be interpreted as ratio of total training steps.",
    category="Training configuration options",
)
@click.option(
    "--save_total_limit",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.save_total_limit,
    show_default=True,
    help="If a value is passed, will limit the total amount of checkpoints. Deletes the older checkpoints in output_dir. When load_best_model_at_end is enabled, the “best” checkpoint according to metric_for_best_model will always be retained in addition to the most recent ones. For example, for save_total_limit=5 and load_best_model_at_end, the four last checkpoints will always be retained alongside the best model. When save_total_limit=1 and load_best_model_at_end, it is possible that two checkpoints are saved: the last one and the best one (if they are different).",
    category="Training configuration options",
)
@click.option(
    "--load_best_model_at_end",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Whether or not to load the best model found during training at the end of training. When this option is enabled, the best checkpoint which recorded lower loss will always be saved (see save_total_limit for more), and the parameters save_strategy needs to be the same as eval_strategy, and in the case it is `steps`, save_steps must be a round multiple of eval_steps.",
    category="Training configuration options",
)
@click.option(
    "--save_strategy",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["epoch", "steps", "no"]),
    default=DEFAULT_LLM_PARAMS.save_strategy,
    show_default=True,
    help="The checkpoint save strategy to adopt during training",
    category="Training configuration options",
)
# ******************************* PEFT OPTIONS *******************************
@click.option(
    "--use_peft",
    cls=CategorizedMutuallyExclusiveOption,
    required=True,
    type=click.Choice(["lora", "adalora", "ia3", "llama_adapter"]),
    default=DEFAULT_LLM_PARAMS.use_peft,
    show_default=True,
    help="PEFT method to use.",
    category="PEFT options",
)
@click.option(
    "--lora_r",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.lora_r,
    show_default=True,
    help="Lora rank to use.",
    category="PEFT options",
)
@click.option(
    "--lora_alpha",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.lora_alpha,
    show_default=True,
    help="Lora alpha to use.",
    category="PEFT options",
)
@click.option(
    "--lora_dropout",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.FLOAT,
    default=DEFAULT_LLM_PARAMS.lora_dropout,
    show_default=True,
    help="Lora dropout to use.",
    category="PEFT options",
)
@click.option(
    "--init_lora_weights",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["gaussian", "pissa", "olora"]),
    help="How to initialize the weights of the adapter layers. Passing nothing (the default) results in the default initialization from the reference implementation from Microsoft. Passing ‘gaussian’ results in Gaussian initialization scaled by the LoRA rank for linear and layers. Pass 'olora' to use OLoRA initialization. Passing 'pissa' to use PiSSa initialization.",
    category="PEFT options",
)
@click.option(
    "--use_rslora",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="When set to True, uses Rank-Stabilized LoRA which sets the adapter scaling factor to lora_alpha/math.sqrt(r), since it was proven to work better. Otherwise, it will use the original default value of lora_alpha/r.",
    category="PEFT options",
)
@click.option(
    "--adalora_init_r",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.adalora_init_r,
    show_default=True,
    help="The initial rank for each incremental matri.",
    category="PEFT options",
)
@click.option(
    "--adalora_target_r",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.adalora_target_r,
    show_default=True,
    help="The target average rank of incremental matrix.",
    category="PEFT options",
)
@click.option(
    "--llama_adapter_len",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.llama_adapter_len,
    show_default=True,
    help="Number of adapter tokens to insert.",
    category="PEFT options",
)
@click.option(
    "--llama_adapter_layers",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.llama_adapter_layers,
    show_default=True,
    help="Number of adapter layers (from the top).",
    category="PEFT options",
)
@click.option(
    "--target_modules",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    default=DEFAULT_LLM_PARAMS.target_modules,
    help="Target modules to use",
    category="PEFT options",
)
@click.option(
    "--merge_adapter",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Use this flag to merge PEFT adapter with the model",
    category="PEFT options",
)
# ******************************* COMPUTE OPTIMIZATION CONFIGURATION OPTIONS *******************************
@click.option(
    "--use_deepspeed",  # FIXME: disable this option if any PEFT method is enable, or maybe we can even use them together?
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["stage_2", "stage_3"], case_sensitive=True),
    help="Use DeepSpeed for training.",
    category="Compute optimization configuration options",
)
@click.option(
    "--disable_gradient_checkpointing",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Disable gradient checkpointing. If not passed, will be used gradient checkpointing to save memory at the expense of slower backward pass.",
    category="Compute optimization configuration options",
)
@click.option(
    "--use_flash_attention_2",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Enable flash attention 2.",
    category="Compute optimization configuration options",
)
@click.option(
    "--mixed_precision",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["fp16", "bf16"], case_sensitive=True),
    help="Mixed precision type to use.",
    category="Compute optimization configuration options",
)
@click.option(
    "--quantization",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["nf4", "fp4", "int8"], case_sensitive=True),
    help="Quantization type to use.",
    category="Compute optimization configuration options",
)
@click.option(
    "--double_quantization",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="This flag is used for nested quantization where the quantization constants from the first quantization are quantized again.",
    category="Compute optimization configuration options",
)
@click.option(
    "--torch_dtype",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.Choice(["auto", "bfloat16", "float16", "float32"]),
    help="Load the model under specified dtype.",
    category="Compute optimization configuration options",
)
@click.option(
    "--auto_find_batch_size",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Whether to find a batch size that will fit into memory automatically through exponential decay, avoiding CUDA Out-of-Memory errors.",
    category="Compute optimization configuration options",
)
@click.option(
    "--neftune_noise_alpha",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.FLOAT,
    help="If not None, this will activate NEFTune noise embeddings. This can drastically improve model performance for instruction fine-tuning.",
    category="Compute optimization configuration options",
)
@click.option(
    "--use_unsloth",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Use Unsloth.",
    category="Compute optimization configuration options",
)
@click.option(
    "--use_torch_compile",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    is_flag=True,
    help="Use torch.compile to accelerate training.",
    category="Compute optimization configuration options",
)
# ******************************* DPO + ORPO OPTIONS*******************************
@click.option(
    "--model_ref",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.STRING,
    help="Reference model to use for DPO when not using PEFT.",
    category="DPO + ORPO options",
)
@click.option(
    "--dpo_beta",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.FLOAT,
    default=DEFAULT_LLM_PARAMS.dpo_beta,
    help="Beta for DPO trainer.",
    category="DPO + ORPO options",
)
@click.option(
    "--max_prompt_length",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    default=DEFAULT_LLM_PARAMS.max_prompt_length,
    help="Maximum prompt length to use.",
    category="DPO + ORPO options",
)
@click.option(
    "--max_completion_length",
    cls=CategorizedMutuallyExclusiveOption,
    required=False,
    type=click.INT,
    help="Maximum completion length to use.",
    category="DPO + ORPO options",
)
def create_impl(**finetune_kwargs: Any):
    """
    Function responsible for launching a scalegen finetune workload from the CLI
    """
    cloud_providers = []
    if finetune_kwargs["cloud_regions"]:
        cloud_providers_dict: Dict[str, List[str]] = {}
        for cloud_region in finetune_kwargs["cloud_regions"]:
            cloud, region = str(cloud_region).split(":")

            if cloud not in cloud_providers_dict:
                cloud_providers_dict[cloud] = [region]
            else:
                cloud_providers_dict[cloud].append(region)

        cloud_providers = [
            {"name": key, "regions": value}
            for key, value in cloud_providers_dict.items()
        ]

    data: Dict[str, Any] = {
        "ft_type": FinetuningType.CLM.value,
        "job_name": finetune_kwargs["job_name"],
        "model": finetune_kwargs["model"],
        "base_model": (
            finetune_kwargs["base_model"]
            if finetune_kwargs["base_model"]
            else finetune_kwargs["model"]
        ),
        "use_recipes": finetune_kwargs["use_recipes"],
        "artifacts_storage": finetune_kwargs["artifacts_storage"],
        "use_spot": finetune_kwargs["allow_spot_instances"],
        "data_path": finetune_kwargs["data_path"],
        "user_dataset": finetune_kwargs["user_dataset"],
        "gpu_type": finetune_kwargs["gpu_type"],
        "gpu_count": finetune_kwargs["gpu_num"],
        "cloud_providers": cloud_providers,
    }

    autotrain_params: Dict[str, Any] = {
        "model": finetune_kwargs["model"],
        "data_path": finetune_kwargs["data_path"],
        "wandb_key": finetune_kwargs["wandb_key"],
        "comet_ml_key": finetune_kwargs["comet_ml_key"],
        "hf_token": finetune_kwargs["hf_token"],
        "username": finetune_kwargs["hf_username"],
        "push_to_hub": finetune_kwargs["push_to_hub"],
        "repo_id": finetune_kwargs["hf_repo_id"],
        "project_name": finetune_kwargs["hf_project_name"],
        "trainer": finetune_kwargs["finetuning_type"],
        "train_split": finetune_kwargs["train_split"],
        "train_subset": finetune_kwargs["train_subset"],
        "valid_split": finetune_kwargs["valid_split"],
        "valid_subset": finetune_kwargs["valid_subset"],
        "add_eos_token": finetune_kwargs["add_eos_token"],
        "block_size": finetune_kwargs["block_size"],
        "model_max_length": finetune_kwargs["model_max_length"],
        "padding": finetune_kwargs["padding"],
        "use_flash_attention_2": finetune_kwargs["use_flash_attention_2"],
        "disable_gradient_checkpointing": finetune_kwargs[
            "disable_gradient_checkpointing"
        ],
        "logging_steps": finetune_kwargs["logging_steps"],
        "eval_strategy": finetune_kwargs["eval_strategy"],
        "save_total_limit": finetune_kwargs["save_total_limit"],
        "save_strategy": finetune_kwargs["save_strategy"],
        "auto_find_batch_size": finetune_kwargs["auto_find_batch_size"],
        "mixed_precision": finetune_kwargs["mixed_precision"],
        "lr": finetune_kwargs["lr"],
        "epochs": finetune_kwargs["epochs"],
        "batch_size": finetune_kwargs["batch_size"],
        "warmup_ratio": finetune_kwargs["warmup_ratio"],
        "gradient_accumulation_steps": finetune_kwargs["gradient_accumulation_steps"],
        "optimizer": finetune_kwargs["optimizer"],
        "lr_scheduler_type": finetune_kwargs["lr_scheduler_type"],
        "weight_decay": finetune_kwargs["weight_decay"],
        "max_grad_norm": finetune_kwargs["max_grad_norm"],
        "seed": finetune_kwargs["seed"],
        "save_steps": finetune_kwargs["save_steps"],
        "load_best_model_at_end": finetune_kwargs["load_best_model_at_end"],
        "neftune_noise_alpha": finetune_kwargs["neftune_noise_alpha"],
        "apply_chat_template": finetune_kwargs["apply_chat_template"],
        "torch_dtype": finetune_kwargs["torch_dtype"],
        "use_torch_compile": finetune_kwargs["use_torch_compile"],
        "quantization": finetune_kwargs["quantization"],
        "double_quantization": finetune_kwargs["double_quantization"],
        "use_peft": finetune_kwargs["use_peft"],
        "lora_r": finetune_kwargs["lora_r"],
        "lora_alpha": finetune_kwargs["lora_alpha"],
        "lora_dropout": finetune_kwargs["lora_dropout"],
        "adalora_init_r": finetune_kwargs["adalora_init_r"],
        "adalora_target_r": finetune_kwargs["adalora_target_r"],
        "llama_adapter_len": finetune_kwargs["llama_adapter_len"],
        "llama_adapter_layers": finetune_kwargs["llama_adapter_layers"],
        "target_modules": finetune_kwargs["target_modules"],
        "merge_adapter": finetune_kwargs["merge_adapter"],
        "model_ref": finetune_kwargs["model_ref"],
        "dpo_beta": finetune_kwargs["dpo_beta"],
        "max_prompt_length": finetune_kwargs["max_prompt_length"],
        "max_completion_length": finetune_kwargs["max_completion_length"],
        "prompt_text_column": finetune_kwargs["prompt_text_column"],
        "text_column": finetune_kwargs["text_column"],
        "rejected_text_column": finetune_kwargs["rejected_text_column"],
        "use_unsloth": finetune_kwargs["use_unsloth"],
        "resume_from_checkpoint": finetune_kwargs["resume_from_checkpoint"],
        "user_checkpoint_dir": finetune_kwargs["user_checkpoint_dir"],
        "use_rslora": finetune_kwargs["use_rslora"],
        "init_lora_weights": finetune_kwargs["init_lora_weights"],
    }
    ft_req_data = FinetuningIn(
        **data, autotrain_params=LLMTrainingParams(**autotrain_params)
    )

    # print(ft_req_data.model_dump(mode="json"))
    # exit()

    create_ft_job(ft_req_data, quiet=finetune_kwargs["quiet"])


@clm.command()
@click.option("-a", "--all", is_flag=True)
def list(all: bool = False):
    """
    List all your finetune workloads
    """
    """
    - Status of the Workload
    - Status of the trials:
        - Trial Name
        - Trial latest metrics
        - Trial Status
    """
    console = Console()

    with console.status("[bold green]Fetching fine-tuning jobs...") as status:

        resp = send_request("GET", f"/job")

        if resp.status_code == 204:
            click.echo(click.style(f"\nNo finetune jobs found", fg="red"))
            return
        elif resp.status_code != 200:
            err = (
                resp.json() if resp.status_code != 500 else resp.content.decode("utf-8")
            )
            click.echo(
                click.style(f"\nCouldn't list the finetune jobs: {err}", fg="red")
            )
            return

        resp_data = resp.json()

        table = Table(
            show_header=True,
            header_style="bold #2070b2",
            title="[bold] Jobs",
            box=box.DOUBLE_EDGE,
        )

        for col in ["ID", "Name", "Model", "Data", "Status"]:
            table.add_column(col, justify="left")

        for job in resp_data:
            if all or (
                not all and (job["status"] == "RUNNING" or job["status"] == "QUEUED")
            ):
                model = find_next_word_in_string(
                    job["spec"]["config"]["entrypoint"], "--model"
                )
                data = find_next_word_in_string(
                    job["spec"]["config"]["entrypoint"], "--data_path"
                )
                table.add_row(job["id"], job["name"], model, data, job["status"])

    if table.row_count <= 15:
        console.print(table, justify="left")
    else:
        with console.pager():
            console.print(table, justify="left")
