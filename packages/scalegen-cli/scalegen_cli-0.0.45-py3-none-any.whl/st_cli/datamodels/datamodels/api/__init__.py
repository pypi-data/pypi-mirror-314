from decimal import Decimal

from typing import Union, Literal, List, Optional, Any, Set
from pydantic import Field, model_validator

from ..common import *
from ..sg_finetune import *


class ServicePlan(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    GROWTH = "GROWTH"


class Spec(BaseModel):
    config: ScaleTorchConfig
    type: JobType
    productType: Optional[ProductType] = ProductType.SCALETORCH

    class Config:
        use_enum_values = False


class Job(BaseModel):
    name: str
    spec: Spec
    id: str
    user_id: str
    status: JobStatus = JobStatus.QUEUED
    viz_page: str = ""
    stage: str = ""
    start_time: str
    end_time: Optional[str] = None
    cost: float = 0.0
    compute_used: Optional[Dict[str, Any]] = None
    last_cost_updated_time: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        use_enum_values = False


class Workstation(BaseModel):
    id: str
    user_id: str
    config: WorkstationConfig
    stage: str = ""
    status: str
    prev_status: str = ""
    start_time: str = ""
    cost: float = 0.0
    viz_page: Optional[str] = None
    nodes: Optional[List[Node]] = []
    last_cost_updated_time: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        populate_by_name = True
        use_enum_values = False


class WorkstationAction(str, Enum):
    RESTART = "RESTART"
    STOP = "STOP"


class CommonOut(BaseModel):
    success: bool
    message: Optional[Any] = None


class CreateJobOut(CommonOut):
    warning: Optional[Any] = None
    info: Optional[Any] = None


class CheckFtIn(BaseModel):
    status_code: int
    job_out: CreateJobOut


class gDriveOut(BaseModel):
    success: bool
    refresh_token: Optional[Any] = None
    access_token: Optional[Any] = None
    error: Optional[Any] = None


class Trial(BaseModel):
    trial_id: str
    status: str
    user_id: Optional[str] = None
    job_id: str
    hyperparameters: Dict[str, Any]
    host: Optional[str] = None
    is_dapp_trial: Optional[bool] = False
    gpu_indices: Optional[str] = None
    monitor_status: Optional[str] = None
    start_time: str = ""
    end_time: str = ""
    timestamp: Optional[str] = None


class JobOut(BaseModel):
    job_id: str


class UserMetadata(BaseModel):
    ns: str
    gt2: Dict[str, Any]
    dev_user: bool = False
    is_admin: bool = False
    plan: Optional[ServicePlan] = ServicePlan.GROWTH
    admin_user_id: Optional[str] = None
    client_ids: Optional[List[str]] = None
    launch_jc: Optional[bool] = True
    member_users: List[str] = []  # List of emails
    created_from_backend: Optional[bool] = True
    st_slack_webhook_url: Optional[str] = None
    sg_slack_webhook_url: Optional[str] = None
    stripe_customer_id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class User(BaseModel):
    email: str
    user_id: str
    email_verified: bool
    user_metadata: UserMetadata

    class Config:
        arbitrary_types_allowed = True


class OrderType(str, Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    OTP = "OTP"


class CreateSubscriptionInput(BaseModel):
    amount: int
    months: int
    payment_method_type: str
    use_test_customer: bool = False


class TopUpRegularBalanceInput(BaseModel):
    amount: int
    payment_method_type: str
    use_test_customer: bool = False


class UserSubscription(BaseModel):
    user_id: str
    active: bool
    discount_balance: Decimal
    regular_balance: Decimal
    refill_per_month: Decimal
    months_left: int
    last_refill: str


class GPUPrice(BaseModel):
    normal: float
    discount: float


class GPUPrices(BaseModel):
    on_demand: GPUPrice
    spot: GPUPrice


class DeploymentType(str, Enum):
    Job = "Job"
    InferenceDeployment = "InferenceDeployment"
    GPUMachine = "GPUMachine"


class GPUPricesIn(BaseModel):
    gpu: GPUType
    deployment_type: DeploymentType
    values: GPUPrices


class UserGPUPrices(BaseModel):
    user_id: str
    prices: Dict[str, Dict[GPUType, GPUPrices]]


class Transaction(BaseModel):
    amount: float
    order_type: OrderType
    status: str
    created_at: int


class SecretOut(BaseModel):
    secret: Dict[str, Any]
    success_status: bool


class SecretIn(BaseModel):
    secret_key: str
    secret_value: str
    typed: bool = False


class CloudDetails(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    cloud_provider: ProviderEnum
    bucket_name: Optional[str] = None
    primary: bool = False
    regions: List[str] = []

    class Config:
        use_enum_values = False


class CloudDetailsIn(CloudDetails):
    creds: Dict[str, str]


class UserRegisterIn(BaseModel):
    email: str
    productType: ProductType = ProductType.SCALETORCH
    send_welcome_email: Optional[bool] = True

    def __init__(self, **data: Any):
        email = data.get("email")
        if email:
            data["email"] = email.lower()

        super().__init__(**data)


class Checkpoint(BaseModel):
    id: str
    job_id: str
    trial_id: str
    filename: str
    user_id: str
    metadata: Dict[str, Any]
    timestamp: str
    copied_to_bucket: bool
    source: str
    timestamp: str

    class Config:
        populate_by_name = True


class Metrics(BaseModel):
    user_id: str
    job_id: str
    trial_id: str
    metrics: Dict[str, Any]
    epoch: int
    timestamp: Optional[str] = None


class Telemetry(BaseModel):
    source: str
    # filename: str
    # filesize: int
    data: int
    timestamp: Optional[str] = None
    job_id: str
    trial_id: str


class Credentials(BaseModel):
    client_id: str
    client_secret: str


class ArtifactsStorageIn(BaseModel):
    name: str
    path: str
    credentials: Dict[str, str] = {}


class ArtifactsStorage(ArtifactsStorageIn):
    id: Optional[str] = None
    user_id: Optional[str] = None


class VirtualMountIn(BaseModel):
    name: str
    src: str
    dest: Optional[str] = None
    filter: Optional[str] = None
    prefetch: Optional[bool] = False
    unravelArchives: Optional[bool] = False
    credentials: Dict[str, str] = {}


class VirtualMountDB(VirtualMountIn):
    id: Optional[str] = None
    user_id: Optional[str] = None


class Entity(str, Enum):
    ARTIFACTS_STORAGE = "ARTIFACTS_STORAGE"
    SECRET = "SECRET"
    CLOUD_PROVIDER = "CLOUD_PROVIDER"
    VIRTUAL_MOUNT = "VIRTUAL_MOUNT"
    GT2 = "GT2"


class UserAssignRevokeIn(BaseModel):
    member_email: str
    entity_type: Entity
    entity_ids: List[str]


class UserPermissionsOut(BaseModel):
    ARTIFACTS_STORAGE: List[str]
    SECRET: List[str]
    CLOUD_PROVIDER: List[str]
    VIRTUAL_MOUNT: List[str] = []
    GT2: List[str]


class UserPermissionsIn(UserPermissionsOut):
    member_email: str


class VisualisationDetails(BaseModel):
    type: VisualisationType
    key: str


class TemplateType(str, Enum):
    EXPERIMENT = "EXPERIMENT"
    HPTOPT = "HPTOPT"
    WORKSTATION = "WORKSTATION"
    SIMPLE_JOB = "SIMPLE_JOB"


class Template(BaseModel):
    id: Optional[str] = None
    name: str
    config: Union[ScaleTorchConfig, WorkstationConfig]
    type: TemplateType
    user_id: Optional[str] = None

    class Config:
        use_enum_values = False


class EventDB(Event):
    pass


class DiscountCondition(str, Enum):
    equal = "EQUAL"
    gt = "GT"
    gte = "GTE"
    lt = "LT"
    lte = "LTE"
    not_equal = "NOT_EQUAL"


class Discount(BaseModel):
    id: str
    condition: DiscountCondition
    field: str
    valid_until: str
    value: Union[str, int]
    discount: Decimal


class NodeUsage(BaseModel):
    id: str
    entity_id: str
    gpu_type: Optional[GPUType] = None
    gpu_count: Optional[int] = 0
    hours: Decimal
    cost: Decimal

    class Config:
        arbitrary_types_allowed = True


class JobUsage(BaseModel):
    id: str
    job_id: str
    job_type: JobType
    user_id: str
    timestamp: str
    nodes: List[NodeUsage]
    platform_cost: float
    last_status: str


class Invoice(BaseModel):
    id: str
    timestamp: str
    amount: float
    payment_status: str
    user_id: str


# OAuth Models


class Token(BaseModel):
    access_token: str
    expires_in: int


class OAuth2In(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    audience: str


class AccessKeyRecord(BaseModel):
    access_key_id: str
    access_key_secret_hashed: str
    user_id: str
    timestamp: str


# On-prem models


class OnPremNodeBase(BaseModel):
    ip: str
    name: Optional[str] = None
    role: OnPremVMRole
    username: str
    port: int
    private_ip: Optional[str] = None
    cpu_only: bool

    def __init__(self, **data: Any):
        # Patch for existing records in DB that have roles different from OnPremVMRoles
        if data.get("role", None) not in [role.name for role in OnPremVMRole]:
            if data.get("role", None) in [
                VMRole.CONTROLLER.name,
                VMRole.INFERENCE_CONTROLLER.name,
            ]:
                data["role"] = OnPremVMRole.ONPREM_CONTROLLER
            else:
                data["role"] = OnPremVMRole.ONPREM_WORKER

        super().__init__(**data)


class OnPremNodeIn(OnPremNodeBase):
    ssh_private_key: str


class OnPremNodeDB(OnPremNodeBase):
    id: str
    ssh_key_id: str
    vcpus: int
    memory: int
    verified: bool
    verification_message: str
    gpu_type: GPUType
    gpu_count: int
    user_id: str


class OnPremNodeCandidate(OnPremNodeDB):
    available_gpu_ids: List[str]


class OnPremJournalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class OnPremNodeJournal(BaseModel):
    id: str
    timestamp: str
    status: OnPremJournalStatus
    on_prem_node_id: str
    job_id: str
    used_gpu_ids: Set[str]


class OnPremNodeUpdateIn(BaseModel):
    ip: Optional[str] = None
    name: Optional[str] = None
    role: Optional[OnPremVMRole] = None
    username: Optional[str] = None
    ssh_private_key: Optional[str] = None
    port: Optional[int] = None
    private_ip: Optional[str] = None
    cpu_only: Optional[bool] = None


# Inference Models


class InferenceDeploymentInitialWorkersConfig(BaseModel):
    min_workers: int = 0
    initial_workers_gpu: Optional[GPUType] = None
    initial_workers_gpu_num: Optional[int] = None
    use_other_gpus: Optional[bool] = False
    instance_types: Optional[List[str]] = None
    use_on_prem: Optional[bool] = False
    use_cloudburst: Optional[bool] = False
    on_prem_node_ids: Optional[List[str]] = None
    expand_gpu_types: Optional[bool] = True
    max_workers: Optional[int] = 100


class InferenceDeploymentAutoscalingStrategy(str, Enum):
    ttft_latency_sec = "ttft_latency_sec"
    rps_per_worker = "rps_per_worker"
    e2e_latency_sec = "e2e_latency_sec"


class InferenceDeploymentAutoscalingConfig(BaseModel):
    scale_up_time_window_sec: Optional[int] = 5 * 60
    scale_down_time_window_sec: Optional[int] = 5 * 60
    scaling_up_timeout_sec: Optional[int] = 20 * 60
    scaling_down_timeout_sec: Optional[int] = 20 * 60
    scale_to_zero_timeout_sec: Optional[int] = 30 * 60
    enable_speedup_shared: Optional[bool] = False
    enable_fast_autoscaling: Optional[bool] = False
    scale_to_zero: Optional[bool] = False
    autoscaling_strategy: InferenceDeploymentAutoscalingStrategy = (
        InferenceDeploymentAutoscalingStrategy.ttft_latency_sec
    )
    upper_allowed_threshold: Optional[float] = 1
    lower_allowed_threshold: Optional[float] = 0.2

    # For backward compatibility. Should be deleted in the future
    upper_allowed_latency_sec: Optional[float] = 1
    lower_allowed_latency_sec: Optional[float] = 0.2


class InferenceDeploymentAPIGatewayData(BaseModel):
    provider: ProviderEnum
    region: Optional[str] = None
    api_id: Optional[str] = None
    hash_value: Optional[str] = None
    endpoint: Optional[str] = None


class InferenceControllerCloudConfig(BaseModel):
    public_url: bool = True
    use_ssl: bool = True
    use_api_gateway: bool = False
    vpc_id: Optional[str] = None
    cloud_provider: ProviderEnum
    region: str
    api_gateway_data: Optional[InferenceDeploymentAPIGatewayData] = None

    # def __init__(self, **data: Any):
    #     # Validate that use_api_gateway is True and vpc_id is valid only when cloud_provider is AWS
    #     if (data.get("use_api_gateway", False) or data.get("vpc_id", None)) and data.get("cloud_provider") != ProviderEnum.AWS:
    #         raise ValueError(f"vpc_id or use_api_gateway are only supported for cloud_provider: AWS, you provided {data.get('cloud_provider')}")

    #     super().__init__(**data)


class InferenceControllerOnPremConfig(BaseModel):
    use_ssl: bool = True
    on_prem_node_id: Optional[str] = (
        None  # if not provided, all cpu-only nodes are considered candidates
    )


class LLMLoraConfig(BaseModel):
    name: str
    hf_repo: str
    hf_token: Optional[str] = None


class InferenceDeploymentIn(BaseModel):
    name: str
    model: str
    base_model: Optional[str] = None
    inf_type: InferenceDeploymentType = InferenceDeploymentType.llm
    hf_token: Optional[str] = None
    engine: Optional[InferenceDeploymentEngine] = None
    custom_chat_template: Optional[str] = None
    allow_spot_instances: bool = False
    logs_store: Optional[str] = None
    cloud_providers: Optional[List[CloudProviderChoice]] = []
    initial_worker_config: Optional[InferenceDeploymentInitialWorkersConfig] = None
    autoscaling_config: Optional[InferenceDeploymentAutoscalingConfig] = (
        InferenceDeploymentAutoscalingConfig()
    )
    max_price_per_hour: Optional[float] = None
    min_throughput_rate: Optional[float] = None

    controller_cloud_config: Optional[InferenceControllerCloudConfig] = None
    controller_on_prem_config: Optional[InferenceControllerOnPremConfig] = None

    llm_loras: Optional[List[LLMLoraConfig]] = []

    # Only llm related args (vllm)
    max_model_len: Optional[int] = None
    throughput_optimized: Optional[bool] = False

    # Agentic related args
    agentic_deployment: Optional[bool] = False

    def __init__(self, **data: Any):
        # Validate that controller_cloud_config or controller_on_prem_config is provided
        if not data.get("controller_cloud_config", None) and not data.get(
            "controller_on_prem_config", None
        ):
            raise ValueError(
                "controller_cloud_config or controller_on_prem_config must be provided"
            )

        # Validate that only one of controller_cloud_config or controller_on_prem_config is provided
        if data.get("controller_cloud_config", None) and data.get(
            "controller_on_prem_config", None
        ):
            raise ValueError(
                "controller_cloud_config and controller_on_prem_config cannot be provided together"
            )

        super().__init__(**data)


class GpuTypeCount(BaseModel):
    type: GPUType
    count: int = Field(1, gt=0)


class InferenceDeploymentPriceEstimationIn(BaseModel):
    cloud: Optional[List[ProviderEnum]] = None
    gpu: Optional[List[GpuTypeCount]] = None
    region: Optional[List[str]] = None

    # number_of_workers: int = Field(1, gt=0)

    @model_validator(mode="after")
    def check_fields(self):
        fields = ["cloud", "gpu", "region"]
        if all(not getattr(self, field) for field in fields):
            raise ValueError("At least one of the fields must be provided.")
        return self


class SpotDemandDB(BaseModel):
    on_demand: float
    spot: float


class MinMaxPrice(BaseModel):
    min: float
    max: float


class EstimatedPrice(BaseModel):
    on_demand_price: MinMaxPrice
    spot_price: MinMaxPrice


class InferenceDeploymentUpdateIn(BaseModel):
    # Initial worker params
    initial_worker_config: Optional[InferenceDeploymentInitialWorkersConfig] = None

    # Auto scaling parameters
    autoscaling_config: Optional[InferenceDeploymentAutoscalingConfig] = None
    imidiate_scale_down: Optional[bool] = False

    max_price_per_hour: Optional[float] = None
    min_throughput_rate: Optional[float] = None
    allow_spot_instances: Optional[bool] = None

    llm_loras: Optional[List[LLMLoraConfig]] = []


class InferenceDeploymentGpuNodesIn(BaseModel):
    gpu_nodes_ids: List[str]


class InferenceDeploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PROVISIONING = "PROVISIONING"
    DELETED = "DELETED"
    FAILED = "FAILED"
    DELETING = "DELETING"


default_engine_strategy_map = {
    InferenceDeploymentType.vlm: [
        (
            InferenceDeploymentEngine.lmdeploy,
            InferenceDeploymentAutoscalingStrategy.rps_per_worker,
        ),
    ],
    InferenceDeploymentType.llm: [
        (
            InferenceDeploymentEngine.vllm,
            InferenceDeploymentAutoscalingStrategy.ttft_latency_sec,
        ),
        (
            InferenceDeploymentEngine.vllm,
            InferenceDeploymentAutoscalingStrategy.rps_per_worker,
        ),
        (
            InferenceDeploymentEngine.vllm,
            InferenceDeploymentAutoscalingStrategy.e2e_latency_sec,
        ),
        (
            InferenceDeploymentEngine.nim,
            InferenceDeploymentAutoscalingStrategy.ttft_latency_sec,
        ),
        (
            InferenceDeploymentEngine.nim,
            InferenceDeploymentAutoscalingStrategy.rps_per_worker,
        ),
        (
            InferenceDeploymentEngine.friendli,
            InferenceDeploymentAutoscalingStrategy.ttft_latency_sec,
        ),
        (
            InferenceDeploymentEngine.friendli,
            InferenceDeploymentAutoscalingStrategy.rps_per_worker,
        ),
    ],
    InferenceDeploymentType.embedding: [
        (
            InferenceDeploymentEngine.tei,
            InferenceDeploymentAutoscalingStrategy.rps_per_worker,
        ),
    ],
    InferenceDeploymentType.tti: [
        (
            InferenceDeploymentEngine.nos,
            InferenceDeploymentAutoscalingStrategy.rps_per_worker,
        )
    ],
}


class InferenceDeploymentDB(InferenceDeploymentIn):
    id: str
    user_id: str
    status: InferenceDeploymentStatus
    current_price_per_hour: float = 0
    cost: float = 0
    last_cost_updated_time: Optional[str] = None
    timestamp: str
    link: Optional[str] = None
    end_time: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

    # Making engine non-optional
    engine: InferenceDeploymentEngine  # type: ignore

    def __init__(self, **data: Any):
        # Patch for existing records in DB that do not have controller_cloud_config or controller_on_prem_config
        if not data.get("controller_cloud_config", None) and not data.get(
            "controller_on_prem_config", None
        ):
            data["controller_cloud_config"] = InferenceControllerCloudConfig(
                cloud_provider=ProviderEnum.AWS, region="us-east-1"
            ).model_dump(mode="json")

        if not data.get("engine", None):
            data["engine"] = default_engine_strategy_map[data["inf_type"]][0][0]

        super().__init__(**data)


class InferenceSupportedModelOut(BaseModel):
    model: str
    type: InferenceDeploymentType


class NodeIP(BaseModel):
    ip: str
    id: str
    tailscale_ip: Optional[str] = None


# FINETUNE DATAMODELS
class FinetuningType(str, Enum):
    CLM = "CLM"
    SENT_TRANSFORMERS = "SENT_TRANSFORMERS"
    SEQ2SEQ = "SEQ2SEQ"
    TEXT_CLASSIFICATION = "TEXT_CLASSIFICATION"
    TOKEN_CLASSIFICATION = "TOKEN_CLASSIFICATION"


class FinetuningIn(BaseModel):
    job_name: Optional[str] = None
    ft_type: FinetuningType = FinetuningType.CLM
    model: str
    base_model: Optional[str] = None
    use_recipes: Optional[bool] = False
    artifacts_storage: Optional[str] = None

    data_path: str
    user_dataset: Optional[str] = None

    use_spot: bool = False
    cloud_providers: Optional[List[CloudProviderChoice]] = []
    gpu_type: Optional[GPUType] = None
    gpu_count: Optional[int] = None

    autotrain_params: Optional[LLMTrainingParams] = None


class FinetuningJobDB(FinetuningIn):
    id: str
    user_id: str


class FinetuningRecipe(BaseModel):
    id: str
    model: str
    gpu_type: GPUType
    gpu_count: int
    autotrain_params: SGFinetuneParams


class CheckKeyIn(BaseModel):
    key_id: str
    key_secret: str


# Openai datamodels


class OpenaiFinetuningHyperparameters(BaseModel):
    batch_size: Optional[Union[str, int]] = "auto"
    learning_rate_multiplier: Optional[Union[str, float]] = "auto"
    n_epochs: Optional[Union[str, int]] = "auto"


class OpenaiScalegenIntegration(BaseModel):
    hf_token: Optional[str] = None
    push_to_hub: Optional[bool] = False
    username: Optional[str] = None
    repo_id: Optional[str] = Field(None, title="Repo id")

    use_spot: bool = False
    cloud_providers: Optional[List[CloudProviderChoice]] = []
    wandb_key: Optional[str] = None
    autotrain_params: Optional[SGFinetuneParams] = None


class OpenaiWandbIntegration(
    BaseModel
):  # Not used, implemented for completeness of openai api
    project: str
    name: Optional[str] = None
    entity: Optional[str] = None
    tags: List[str] = []


class OpenaiFinetuningIntegrationType(str, Enum):
    WANDB = "wandb"
    SCALEGEN = "scalegen"


class OpenaiIntegrations(BaseModel):
    type: OpenaiFinetuningIntegrationType
    scalegen: Optional[OpenaiScalegenIntegration] = None
    wandb: Optional[OpenaiWandbIntegration] = None  # Not used


class OpenaiFinetuningIn(BaseModel):
    model: str  # The name of the model to fine-tune
    training_file: str  # The ID of an uploaded file that contains training data.
    hyperparameters: Optional[OpenaiFinetuningHyperparameters] = (
        OpenaiFinetuningHyperparameters()
    )
    suffix: Optional[str] = (
        ""  # A string of up to 18 characters that will be added to your fine-tuned model name.
    )
    validation_file: Optional[Union[str, None]] = (
        None  # The ID of an uploaded file that contains validation data.
    )
    integrations: Optional[List[OpenaiIntegrations]] = []
    seed: Optional[int] = None


class OpenaiFinetuningJobError(BaseModel):
    code: str  # A machine-readable error code.
    message: str  # A human-readable error message.
    param: Union[str, None] = (
        None  # The parameter that was invalid, usually training_file or validation_file. This
    )
    # field will be null if the failure was not parameter-specific.


class OpenaiFinetuningJobStatus(str, Enum):
    VALIDATING_FILES = "validating_files"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OpenaiFinetuningJob(BaseModel):
    id: str  # The object identifier, which can be referenced in the API endpoints.
    created_at: (
        int  # The Unix timestamp (in seconds) for when the fine-tuning job was created.
    )
    error: Optional[Union[OpenaiFinetuningJobError, None]] = (
        None  # For fine-tuning jobs that have failed, this will
    )
    # contain more information on the cause of the failure.

    fine_tuned_model: Optional[Union[str, None]] = (
        None  # The name of the fine-tuned model that is being created.
    )
    # The value will be null if the fine-tuning job is still running.
    finished_at: Optional[Union[int, None]] = (
        None  # The Unix timestamp (in seconds) for when the fine-tuning job
    )
    # was finished. The value will be null if the fine-tuning job is still running.

    hyperparameters: OpenaiFinetuningHyperparameters  # The hyperparameters used for the fine-tuning job.
    model: str  # The base model that is being fine-tuned.
    object: str = (
        "fine_tuning.job"  # The object type, which is always "fine_tuning.job".
    )
    organization_id: str = (
        "scaletorch"  # The organization that owns the fine-tuning job.
    )

    result_files: List[str] = (
        []
    )  # The compiled results file ID(s) for the fine-tuning job. You can retrieve the
    # results with the Files API.

    status: OpenaiFinetuningJobStatus  # The current
    # status of the fine-tuning job, which can be either validating_files, queued, running, succeeded, failed, or
    # cancelled.

    trained_tokens: Optional[Union[int, None]] = (
        None  # The total number of billable tokens processed by this
    )
    # fine-tuning job. The value will be null if the fine-tuning job is still running.
    training_file: str  # The file ID used for training. You can retrieve the training data with the Files API.
    validation_file: Optional[Union[str, None]] = (
        None  # The file ID used for validation. You can retrieve the
    )
    # validation results with the Files API.


class OpenaiFinetuningJobDB(OpenaiFinetuningJob):
    user_id: str


class OpenaiFinetuningJobEvent(BaseModel):
    id: str
    created_at: int
    level: str
    message: str
    object: str = "fine_tuning.job.event"


class OpenaiFilePurposeEnum(str, Enum):
    fine_tune = "fine-tune"
    fine_tune_results = "fine-tune-results"
    assistants = "assistants"
    assistants_output = "assistants_output"


class OpenaiFile(BaseModel):
    id: str  # The file identifier, which can be referenced in the API endpoints.
    bytes: int  # The size of the file, in bytes.
    created_at: int  # The Unix timestamp (in seconds) for when the file was created.
    filename: str  # The name of the file.
    object: str = "file"  # The object type, which is always file.
    purpose: OpenaiFilePurposeEnum  # The intended purpose of
    # the file. Supported values are fine-tune, fine-tune-results, assistants, and assistants_output.


class OpenaiFileActualPath(BaseModel):
    filename: str
    storage_name: str


class OpenaiFileDB(OpenaiFile):
    actual_path: Optional[Union[None, OpenaiFileActualPath]] = None
    user_id: str


class OpenaiListFilesResponse(BaseModel):
    data: List[OpenaiFile]
    object: str = "list"


class OpenaiPaginatedResponse(BaseModel):
    object: str = "list"
    data: List[Union[OpenaiFinetuningJob, OpenaiFinetuningJobEvent]] = []
    has_more: bool = False


class OpenaiDeleteFileResponse(BaseModel):
    id: str
    object: str = "file"
    deleted: bool


class OpenaiFinishJobIn(BaseModel):
    result_model: Optional[Union[str, None]] = (
        None  # An openai file with resulting lora weights after finetuning
    )
    result_files: List[str] = []  # other resulting files, like logs
    trained_tokens: Optional[int] = 0  # Number of total consumed tokens (if possible)


class InferenceDeploymentGatewayCloudChoice(
    BaseModel
):  # TODO: Define this class properly
    pass


class LLMGatewayCreateIn(BaseModel):
    name: str
    gateway_cloud_config: InferenceDeploymentGatewayCloudChoice
    llm_apis: Set[LLMAPIProviderEnum]
    has_semantic_caching: bool = True
    has_pii_anon: bool = True
    has_prompt_inject_check: bool = True
    num_reties: int = 5


class LLMGatewayDB(LLMGatewayCreateIn):
    id: str
    user_id: str
    status: InferenceDeploymentStatus
    timestamp: str
    metadata: Optional[Dict[str, Any]] = {}


class LLMAPIProviderCreateIn(BaseModel):
    provider: LLMAPIProviderEnum
    api_key: str


class LLMAPIProviderDB(LLMAPIProviderCreateIn):
    id: str
    user_id: str


class GPUMachineAvailability(BaseModel):
    region: str
    sg_region: str
    available: bool


class AvailableGPUMachine(BaseModel):
    memory_in_gb: int
    vcpus: int

    num_gpus: int
    gpu_type: GPUType

    instance_type: str
    cloud: str
    provider_reference: str

    hourly_price: float
    reference_hourly_price: float
    availability: List[GPUMachineAvailability]


class GPUMachineDockerPortConfig(BaseModel):
    host_port: int
    container_port: int


class GPUMachineDockerConfig(BaseModel):
    image: str
    args: Optional[str] = None
    env_vars: Optional[Dict[str, str]] = None
    ports: Optional[List[GPUMachineDockerPortConfig]] = []


class GPUMachineCreateIn(BaseModel):
    machine_avail_id: str
    artifacts_store_name: Optional[str] = None
    docker_config: Optional[GPUMachineDockerConfig] = None


class GPUMachineStatus(str, Enum):
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    DELETING = "DELETING"
    DELETED = "DELETED"
    FAILED = "FAILED"


class GPUMachineDB(GPUMachineCreateIn):
    id: str
    user_id: str
    status: GPUMachineStatus
    timestamp: str
    instance_details: InstancePricingDB
    end_time: Optional[str] = None
    last_cost_updated_time: Optional[str] = None
    cost: float = 0


class DNSRecordIn(BaseModel):
    inf_id: str
    controller_ip: str


class DNSGetCertOut(BaseModel):
    cert_file: str
    key_file: str
    cert_chain_file: str


#### Fixed Templates ####


class FixedTemplateInferenceDB(BaseModel):
    id: str
    name: str
    config: InferenceDeploymentIn


class FixedTemplateFinetuneDB(BaseModel):
    id: str
    name: str
    config: FinetuningIn


class EditDevUserIn(BaseModel):
    user_status: Optional[str] = ""
    jc_status: Optional[str] = ""
