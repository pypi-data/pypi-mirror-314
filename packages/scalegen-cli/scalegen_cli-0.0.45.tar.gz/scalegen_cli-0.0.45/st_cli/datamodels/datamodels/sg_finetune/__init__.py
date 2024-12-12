import os
from typing import Literal, Optional, Union, List

from pydantic import Field, BaseModel


class SGFinetuneParams(BaseModel):
    """
    Base class for all AutoTrain parameters.
    """

    model: str = Field(None, title="Model name")
    job_name: Optional[str] = Field("", title="ScaleGen job name")
    project_name: Optional[str] = Field("ScaleGen Project", title="Output directory")
    data_path: str = Field("data", title="Data path")
    push_to_hub: bool = Field(False, title="Push to hub")
    repo_id: Optional[str] = Field(None, title="Repo id")
    username: Optional[str] = Field(None, title="Hugging Face Username")
    hf_token: Optional[str] = Field(None, title="Huggingface token")
    wandb_key: Optional[str] = Field(None, title="Wandb key")
    comet_ml_key: Optional[str] = Field(
        None, title="Comet ML key for experiment tracking"
    )

    class Config:
        protected_namespaces = ()

    def save(self, output_dir):
        """
        Save parameters to a json file.
        """
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "training_params.json")
        # save formatted json
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4))

    def __str__(self):
        """
        String representation of the parameters.
        """
        data = self.model_dump()
        data["hf_token"] = "*****" if data.get("hf_token") else None
        data["wandb_key"] = "*****" if data.get("wandb_key") else None
        data["cometml_key"] = "*****" if data.get("cometml_key") else None
        return str(data)

    def __init__(self, quiet: bool = True, logger=None, **data):
        """
        Initialize the parameters, check for unused/extra parameters and warn the user.
        """
        super().__init__(**data)

        # Parameters not supplied by the user
        defaults = set(self.model_fields.keys())
        supplied = set(data.keys())
        not_supplied = defaults - supplied
        if not_supplied and not quiet and logger:
            logger.warning(
                f"Parameters not supplied by user and set to default: {', '.join(not_supplied)}"
            )

        # Parameters that were supplied but not used
        # This is a naive implementation. It might catch some internal Pydantic params.
        unused = supplied - set(self.model_fields)
        if unused and not quiet and logger:
            logger.warning(f"Parameters supplied but not used: {', '.join(unused)}")


class LLMTrainingParams(SGFinetuneParams):
    train_split: str = Field("train", title="Train data config")
    train_subset: Optional[str] = Field(None, title="Train data subset config")
    valid_split: Optional[str] = Field(None, title="Validation data config")
    valid_subset: Optional[str] = Field(None, title="Validation data subset config")
    add_eos_token: bool = Field(True, title="Add EOS token")
    block_size: int = Field(-1, title="Block size")
    model_max_length: Optional[int] = Field(None, title="Model max length")
    padding: Optional[Literal["left", "right"]] = Field(None, title="Padding side")

    # trainer params
    trainer: Literal["default", "reward", "sft", "dpo", "orpo"] = Field(
        "default", title="Trainer type"
    )
    use_flash_attention_2: bool = Field(False, title="Use flash attention 2")
    log: Union[str, List[str]] = Field(
        "none", title="Logging using experiment tracking"
    )
    disable_gradient_checkpointing: bool = Field(False, title="Gradient checkpointing")
    logging_steps: int = Field(-1, title="Logging steps")
    eval_strategy: str = Field("epoch", title="Evaluation strategy")
    save_total_limit: int = Field(1, title="Save total limit")
    save_strategy: str = Field("steps", title="Save strategy")
    auto_find_batch_size: bool = Field(False, title="Auto find batch size")
    mixed_precision: Optional[Literal["fp16", "bf16"]] = Field(
        None, title="fp16, bf16, or None"
    )
    lr: float = Field(3e-5, title="Learning rate")
    epochs: int = Field(1, title="Number of training epochs")
    batch_size: int = Field(2, title="Training batch size")
    warmup_ratio: float = Field(0.1, title="Warmup proportion")
    gradient_accumulation_steps: int = Field(1, title="Gradient accumulation steps")
    optimizer: str = Field("adamw_torch", title="Optimizer")
    lr_scheduler_type: str = Field("linear", title="Scheduler")
    weight_decay: float = Field(0.0, title="Weight decay")
    max_grad_norm: float = Field(1.0, title="Max gradient norm")
    seed: int = Field(42, title="Seed")
    save_steps: int = Field(20, title="Save steps to use")
    eval_steps: Optional[int] = Field(None, title="Save steps to use")
    load_best_model_at_end: bool = Field(True, title="Load the best model at the end")
    resume_from_checkpoint: Optional[str] = Field(None, title="Checkpoint dir")
    user_checkpoint_dir: Optional[str] = Field(
        "", title="User checkpoint dir to resume from"
    )
    neftune_noise_alpha: Optional[float] = Field(
        None,
        title="If not None, this will activate NEFTune noise embeddings. This can drastically improve model performance for instruction fine-tuning.",
    )
    use_deepspeed: Optional[str] = Field(None, title="stage_2, stage_3, or None")
    apply_chat_template: Optional[Literal["zephyr", "chatml", "tokenizer"]] = Field(
        None, title="Apply chat template, one of: None, zephyr, chatml or tokenizer"
    )
    torch_dtype: Optional[Literal["auto", "bfloat16", "float16", "float32"]] = Field(
        None, title="Load the model under this dtype"
    )
    use_torch_compile: bool = Field(
        None, title="Use torch.compile to accelerate training"
    )

    # bitsandbytes
    quantization: Optional[Literal["nf4", "fp4", "int8"]] = Field(
        None, title="Quantization type to use"
    )
    double_quantization: bool = Field(
        False,
        title=" This flag is used for nested quantization where the quantization constants from the first quantization are quantized again.",
    )

    # peft
    use_peft: Optional[Literal["lora", "adalora", "ia3", "llama_adapter"]] = Field(
        "lora", title="Use PEFT"
    )
    lora_r: int = Field(16, title="LoRA rank")
    lora_alpha: int = Field(32, title="LoRA/AdaLoRA alpha")
    lora_dropout: float = Field(0.05, title="LoRA/AdaLoRA dropout")
    init_lora_weights: Optional[Literal["gaussian", "pissa", "olora"]] = Field(
        None, title="Initialize LoRA weights"
    )
    use_rslora: bool = Field(False, title="Use RSLoRA")
    adalora_init_r: int = Field(
        12, title="The initial rank for each incremental matrix"
    )
    adalora_target_r: int = Field(
        8, title="The target average rank of incremental matrix"
    )
    llama_adapter_len: int = Field(128, title="Number of adapter tokens to insert")
    llama_adapter_layers: int = Field(
        8, title="Number of adapter layers (from the top)"
    )
    target_modules: Optional[str] = Field(None, title="Target modules")
    merge_adapter: bool = Field(False, title="Merge adapter")

    # dpo
    model_ref: Optional[str] = Field(None, title="Reference, for DPO trainer")
    dpo_beta: float = Field(0.1, title="Beta for DPO trainer")

    # orpo + dpo
    max_prompt_length: int = Field(128, title="Prompt length")
    max_completion_length: Optional[int] = Field(None, title="Completion length")

    # column mappings
    prompt_text_column: Optional[str] = Field(None, title="Prompt text column")
    text_column: str = Field("text", title="Text column", strict=False)
    rejected_text_column: Optional[str] = Field(None, title="Rejected text column")

    # unsloth
    use_unsloth: bool = Field(False, title="Use unsloth")

    def __init__(self, **data):

        if not data.get("seed"):
            data["seed"] = 42

        super().__init__(**data)


class SentenceTransformersParams(SGFinetuneParams):
    # data params
    train_split: str = Field("train", title="Train data config")
    train_subset: Optional[str] = Field(None, title="Train data subset config")
    valid_split: Optional[str] = Field(None, title="Validation data config")
    valid_subset: Optional[str] = Field(None, title="Validation data subset config")

    # trainer params
    lr: float = Field(3e-5, title="Learning rate")
    epochs: int = Field(3, title="Number of training epochs")
    max_seq_length: int = Field(128, title="Max sequence length")
    batch_size: int = Field(8, title="Training batch size")
    warmup_ratio: float = Field(0.1, title="Warmup proportion")
    gradient_accumulation: int = Field(1, title="Gradient accumulation steps")
    optimizer: str = Field("adamw_torch", title="Optimizer")
    scheduler: str = Field("linear", title="Scheduler")
    weight_decay: float = Field(0.0, title="Weight decay")
    max_grad_norm: float = Field(1.0, title="Max gradient norm")
    seed: int = Field(42, title="Seed")
    logging_steps: int = Field(-1, title="Logging steps")
    auto_find_batch_size: bool = Field(False, title="Auto find batch size")
    mixed_precision: Optional[str] = Field(None, title="fp16, bf16, or None")
    save_total_limit: int = Field(1, title="Save total limit")
    eval_strategy: str = Field("epoch", title="Evaluation strategy")
    save_strategy: str = Field("epoch", title="Save strategy")
    save_steps: int = Field(20, title="Save steps to use")
    resume_from_checkpoint: Optional[str] = Field(None, title="Checkpoint dir")
    wandb_key: Optional[str] = Field(None, title="Wandb key for experiment tracking")
    comet_ml_key: Optional[str] = Field(
        None, title="Comet ML key for experiment tracking"
    )
    log: str = Field("none", title="Logging using experiment tracking")
    early_stopping_patience: int = Field(5, title="Early stopping patience")
    early_stopping_threshold: float = Field(0.01, title="Early stopping threshold")
    # trainers: pair, pair_class, pair_score, triplet, qa
    # pair: sentence1, sentence2
    # pair_class: sentence1, sentence2, target
    # pair_score: sentence1, sentence2, target
    # triplet: sentence1, sentence2, sentence3
    # qa: sentence1, sentence2
    trainer: str = Field("pair_score", title="Trainer name")

    # column mappings
    sentence1_column: str = Field("sentence1", title="Sentence 1 column")
    sentence2_column: str = Field("sentence2", title="Sentence 2 column")
    sentence3_column: Optional[str] = Field("sentence3", title="Sentence 3 column")
    target_column: Optional[str] = Field("target", title="Target column")


class Seq2SeqParams(SGFinetuneParams):
    # trainer params
    max_seq_length: int = Field(128, title="Max sequence length")
    max_target_length: int = Field(128, title="Max target sequence length")
    batch_size: int = Field(2, title="Training batch size")
    early_stopping_patience: int = Field(5, title="Early stopping patience")
    early_stopping_threshold: float = Field(0.01, title="Early stopping threshold")

    # bitsandbytes
    quantization: Optional[Literal["nf4", "fp4", "int8"]] = Field(
        None, title="int4, int8, or None"
    )
    double_quantization: bool = Field(
        False,
        title=" This flag is used for nested quantization where the quantization constants from the first quantization are quantized again.",
    )

    # peft
    use_peft: Optional[Literal["lora", "adalora", "ia3", "llama_adapter"]] = Field(
        None, title="Use PEFT"
    )
    lora_r: int = Field(16, title="LoRA rank")
    lora_alpha: int = Field(32, title="LoRA/AdaLoRA alpha")
    lora_dropout: float = Field(0.05, title="LoRA/AdaLoRA dropout")
    adalora_init_r: int = Field(
        12, title="The initial rank for each incremental matrix"
    )
    adalora_target_r: int = Field(
        8, title="The target average rank of incremental matrix"
    )
    llama_adapter_len: int = Field(128, title="Number of adapter tokens to insert")
    llama_adapter_layers: int = Field(
        8, title="Number of adapter layers (from the top)"
    )
    target_modules: str = Field("all-linear", title="Target modules for PEFT")
    merge_adapter: bool = Field(False, title="Merge adapter")

    # column mappings
    text_column: str = Field("text", title="Text column")
    target_column: str = Field("target", title="Target text column")


class TextClassificationParams(SGFinetuneParams):
    # data params
    train_split: str = Field("train", title="Train data config")
    train_subset: Optional[str] = Field(None, title="Train data subset config")
    valid_split: Optional[str] = Field(None, title="Validation data config")
    valid_subset: Optional[str] = Field(None, title="Validation data subset config")

    # trainer params
    lr: float = Field(5e-5, title="Learning rate")
    epochs: int = Field(3, title="Number of training epochs")
    max_seq_length: int = Field(128, title="Max sequence length")
    batch_size: int = Field(8, title="Training batch size")
    warmup_ratio: float = Field(0.1, title="Warmup proportion")
    gradient_accumulation: int = Field(1, title="Gradient accumulation steps")
    optimizer: str = Field("adamw_torch", title="Optimizer")
    scheduler: str = Field("linear", title="Scheduler")
    weight_decay: float = Field(0.0, title="Weight decay")
    max_grad_norm: float = Field(1.0, title="Max gradient norm")
    seed: int = Field(42, title="Seed")
    text_column: str = Field("text", title="Text column")
    target_column: str = Field("target", title="Target column")
    logging_steps: int = Field(-1, title="Logging steps")
    auto_find_batch_size: bool = Field(False, title="Auto find batch size")
    fp16: bool = Field(False, title="Enable fp16")
    save_total_limit: int = Field(1, title="Save total limit")
    save_strategy: str = Field("epoch", title="Save strategy")
    save_steps: int = Field(20, title="Save steps to use")
    resume_from_checkpoint: Optional[str] = Field(None, title="Checkpoint dir")
    wandb_key: Optional[str] = Field(None, title="Wandb key for experiment tracking")
    evaluation_strategy: str = Field("epoch", title="Evaluation strategy")
    log: str = Field("none", title="Logging using experiment tracking")


class TokenClassificationParams(SGFinetuneParams):
    # data params
    train_split: str = Field("train", title="Train data config")
    train_subset: Optional[str] = Field(None, title="Train data subset config")
    valid_split: Optional[str] = Field(None, title="Validation data config")
    valid_subset: Optional[str] = Field(None, title="Validation data subset config")

    # trainer params
    lr: float = Field(5e-5, title="Learning rate")
    epochs: int = Field(3, title="Number of training epochs")
    max_seq_length: int = Field(128, title="Max sequence length")
    batch_size: int = Field(8, title="Training batch size")
    warmup_ratio: float = Field(0.1, title="Warmup proportion")
    gradient_accumulation: int = Field(1, title="Gradient accumulation steps")
    optimizer: str = Field("adamw_torch", title="Optimizer")
    scheduler: str = Field("linear", title="Scheduler")
    weight_decay: float = Field(0.0, title="Weight decay")
    max_grad_norm: float = Field(1.0, title="Max gradient norm")
    seed: int = Field(42, title="Seed")
    logging_steps: int = Field(-1, title="Logging steps")
    auto_find_batch_size: bool = Field(False, title="Auto find batch size")
    mixed_precision: Optional[str] = Field(None, title="fp16, bf16, or None")
    save_total_limit: int = Field(1, title="Save total limit")
    eval_strategy: str = Field("epoch", title="Evaluation strategy")
    save_strategy: str = Field("epoch", title="Save strategy")
    save_steps: int = Field(20, title="Save steps to use")
    resume_from_checkpoint: Optional[str] = Field(None, title="Checkpoint dir")
    wandb_key: Optional[str] = Field(None, title="Wandb key for experiment tracking")
    log: str = Field("none", title="Logging using experiment tracking")
    early_stopping_patience: int = Field(5, title="Early stopping patience")
    early_stopping_threshold: float = Field(0.01, title="Early stopping threshold")

    # column mappings
    tokens_column: str = Field("tokens", title="Tokens column")
    tags_column: str = Field("tags", title="Tags column")
