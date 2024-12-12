from enum import Enum
import hashlib
import json
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class VMRole(str, Enum):
    CONTROLLER = "CONTROLLER"
    WORKER = "WORKER"
    DAPP_CPU_WORKER = "DAPP_CPU_WORKER"
    DAPP_TC = "DAPP_TC"
    DAPP_CONTROLLER = "DAPP_CONTROLLER"
    INFERENCE_CONTROLLER = "INFERENCE_CONTROLLER"
    INFERENCE_WORKER = "INFERENCE_WORKER"
    SINGLE_GPU_MACHINE = "SINGLE_GPU_MACHINE"

    # Retired
    NFS_SERVER = "NFS_SERVER"
    VIS_SERVER = "VIS_SERVER"
    TB_SERVER = "TB_SERVER"
    AIM_SERVER = "AIM_SERVER"
    WORKSTATION = "WORKSTATION"


class OnPremVMRole(str, Enum):
    ONPREM_CONTROLLER = "ONPREM_CONTROLLER"
    ONPREM_WORKER = "ONPREM_WORKER"


class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    DAPP_RUNNING = "DAPP_RUNNING"


class WorkstationStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    DELETED = "DELETED"
    DELETING = "DELETING"
    RESTARTING = "RESTARTING"
    FAILED = "FAILED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    SPOT_FAILURE = "SPOT_FAILURE"


class JobType(str, Enum):
    EXPERIMENT = "EXPERIMENT"
    HPTOPT = "HPTOPT"
    SIMPLE_JOB = "SIMPLE_JOB"
    FINETUNING = "FINETUNING"


class InferenceDeploymentType(str, Enum):
    llm = "llm"
    embedding = "embedding"
    tti = "tti"
    vlm = "vlm"


class InferenceDeploymentEngine(str, Enum):
    tei = "tei"
    vllm = "vllm"
    nim = "nim"
    lmdeploy = "lmdeploy"
    nos = "nos"
    friendli = "friendli"


class ProductType(str, Enum):
    SCALETORCH = "SCALETORCH"
    SCALEGEN = "SCALEGEN"


class ProviderEnum(str, Enum):
    DATACRUNCH = "DATACRUNCH"
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"
    RUNPOD = "RUNPOD"
    SCALETORCH = "SCALETORCH"
    ONPREM = "ONPREM"
    VASTAI = "VASTAI"
    SHADEFORM = "SHADEFORM"
    SCALEGENAI_OWN = "SCALEGENAI_OWN"
    SCALEGENAI_PARTNER = "SCALEGENAI_PARTNER"
    SCALEGENAI = "SCALEGENAI"

    # Not fully supported clouds
    EXOSCALE = "EXOSCALE"


class CodeCopyType(str, Enum):
    GITHUB_PRIVATE = "GITHUB_PRIVATE"
    GITHUB = "GITHUB"
    GITLAB_PRIVATE = "GITLAB_PRIVATE"
    GITLAB = "GITLAB"
    BITBUCKET_PRIVATE = "BITBUCKET_PRIVATE"
    BITBUCKET = "BITBUCKET"
    S3 = "S3"
    B2 = "B2"
    AZURE = "AZURE"
    GS = "GS"
    GDRIVE = "GDRIVE"
    DROPBOX = "DROPBOX"


code_credentials: Dict[CodeCopyType, List[str]] = {
    CodeCopyType.GITHUB_PRIVATE: ["GITHUB_PAT"],
    CodeCopyType.GITHUB: [],
    CodeCopyType.GITLAB_PRIVATE: ["GITLAB_PAT"],
    CodeCopyType.GITLAB: [],
    CodeCopyType.BITBUCKET_PRIVATE: ["BITBUCKET_APP_PASSWORD"],
    CodeCopyType.BITBUCKET: [],
    CodeCopyType.S3: ["AWS_ACCESS_KEY_ID", " AWS_SECRET_ACCESS_KEY"],
    CodeCopyType.AZURE: ["AZURE_ACCOUNT_NAME", "AZURE_ACCOUNT_KEY"],
    CodeCopyType.GS: ["GS_CREDS"],
    CodeCopyType.GDRIVE: ["GDRIVE_CREDS"],
    CodeCopyType.DROPBOX: ["DROPBOX_TOKEN"],
    CodeCopyType.B2: [],
}


class GPUType(str, Enum):
    A10G = "A10G"
    A30 = "A30"
    A40 = "A40"

    # A100 (40GB)
    # When just A100 is mentioned, it is assumed to be 40GB
    # We will also include SXM and NVLINK versions when only A100 is mentioned in API or JC
    # The same applies to H100_80GB and A100_80GB
    A100 = "A100"
    A100_PCIE = "A100_PCIE"  # PCIE
    A100_SXM = "A100_SXM"  # SXM
    A100_PCIE_NVLINK = "A100_PCIE_NVLINK"  # PCIE with NVLINK
    A100_SXM_NVLINK = "A100_SXM_NVLINK"  # SXM with NVLINK

    # A100_80GB
    A100_80GB = "A100_80GB"
    A100_80GB_PCIE = "A100_80GB_PCIE"  # PCIE
    A100_80GB_SXM = "A100_80GB_SXM"  # SXM
    A100_80GB_PCIE_NVLINK = "A100_80GB_PCIE_NVLINK"  # PCIE with NVLINK
    A100_80GB_SXM_NVLINK = "A100_80GB_SXM_NVLINK"  # SXM with NVLINK

    # H100_80GB
    H100_80GB = "H100_80GB"
    H100_80GB_PCIE = "H100_80GB_PCIE"  # PCIE
    H100_80GB_SXM = "H100_80GB_SXM"  # SXM
    H100_80GB_PCIE_NVLINK = "H100_80GB_PCIE_NVLINK"  # PCIE with NVLINK
    H100_80GB_SXM_NVLINK = "H100_80GB_SXM_NVLINK"  # SXM with NVLINK

    # H200
    H200 = "H200"
    H200_PCIE = "H200_PCIE"  # PCIE
    H200_SXM = "H200_SXM"  # SXM
    H200_PCIE_NVLINK = "H200_PCIE_NVLINK"  # PCIE with NVLINK
    H200_SXM_NVLINK = "H200_SXM_NVLINK"  # SXM with NVLINK

    GH201 = "GH201"
    K80 = "K80"
    L4 = "L4"
    L40 = "L40"
    L40S = "L40S"
    M60 = "M60"
    P40 = "P40"
    P100 = "P100"
    RTX_3070 = "RTX_3070"
    RTX_3080 = "RTX_3080"
    RTX_3080_TI = "RTX_3080_TI"
    RTX_3090 = "RTX_3090"
    RTX_3090_TI = "RTX_3090_TI"
    RTX_4000 = "RTX_4000"
    RTX_4070 = "RTX_4070"
    RTX_4070_TI = "RTX_4070_TI"
    RTX_4080 = "RTX_4080"
    RTX_4090 = "RTX_4090"
    RTX_6000_ADA = "RTX_6000_ADA"
    RTX_A2000 = "RTX_A2000"
    RTX_A4000 = "RTX_A4000"
    RTX_A4500 = "RTX_A4500"
    RTX_A5000 = "RTX_A5000"
    RTX_A6000 = "RTX_A6000"
    T4 = "T4"
    V100 = "V100"
    V520 = "V520"

    EMPTY = ""

    def expand_types(self) -> List["GPUType"]:
        if (
            self == GPUType.A100
            or self.value.startswith("A100_")
            and "80GB" not in self.value
        ):
            return [
                gpu_type
                for gpu_type in GPUType
                if gpu_type.value.startswith(max(self.value, "A100_"))
                and "80GB" not in gpu_type.value
            ]

        if any(map(self.value.startswith, ["A100_80GB", "H100_80GB"])):
            return [
                gpu_type
                for gpu_type in GPUType
                if gpu_type.value.startswith(self.value)
            ]

        else:
            return [self]


on_prem_gpu_type_map = {
    GPUType.A10G: ["a10"],
    GPUType.A30: ["a30"],
    GPUType.A40: ["a40"],
    GPUType.A100: ["a100", "40gb"],
    GPUType.A100_80GB: ["a100", "80gb"],
    GPUType.GH201: ["****"],  # TODO
    GPUType.H100_80GB: ["h100"],
    GPUType.K80: ["k80"],
    GPUType.L4: ["l4"],
    GPUType.L40: ["l40"],
    GPUType.L40S: ["l40s"],
    GPUType.M60: ["m60"],
    GPUType.P40: ["p40"],
    GPUType.P100: ["p100"],
    GPUType.RTX_3070: ["3070", "rtx"],
    GPUType.RTX_3080: ["3080", "rtx"],
    GPUType.RTX_3080_TI: ["rtx", "3080", "ti"],
    GPUType.RTX_3090: ["3090", "rtx"],
    GPUType.RTX_3090_TI: ["rtx", "3090", "ti"],
    GPUType.RTX_4000: ["rtx", "4000"],
    GPUType.RTX_4070: ["rtx", "4070"],
    GPUType.RTX_4070_TI: ["rtx", "4070", "ti"],
    GPUType.RTX_4080: ["rtx", "4080"],
    GPUType.RTX_4090: ["rtx", "4090"],
    GPUType.RTX_6000_ADA: ["rtx", "6000", "ada"],
    GPUType.RTX_A2000: ["rtx", "a2000"],
    GPUType.RTX_A4000: ["rtx", "a4000"],
    GPUType.RTX_A4500: ["rtx", "a4500"],
    GPUType.RTX_A5000: ["rtx", "a5000"],
    GPUType.RTX_A6000: ["rtx", "a6000"],
    GPUType.T4: ["t4"],
    GPUType.V100: ["v100"],
    GPUType.V520: ["v520"],
}


class LLMAPIProviderEnum(str, Enum):
    ANYSCALE = "ANYSCALE"
    TOGETHER = "TOGETHER"
    DEEPINFRA = "DEEPINFRA"
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"


# Classes for Config
class SearchSpaceElement(BaseModel):
    type: str
    value: List[Any]


class Tuner(BaseModel):
    name: str
    optimizeMode: str


class Tuning(BaseModel):
    searchSpace: Dict[str, SearchSpaceElement]
    tuner: Optional[Tuner] = None


class Experiment(BaseModel):
    args: Dict[str, List[Any]]


class CloudProviderChoice(BaseModel):
    name: ProviderEnum
    regions: List[str] = []

    class Config:
        use_enum_values = False


class DockerCreds(BaseModel):
    registry: str
    username: str
    password: str


class DockerImageSelection(BaseModel):
    image: str
    credentials: Optional[DockerCreds] = None
    pythonPath: Optional[str] = None


class ArtifactsDestination(BaseModel):
    name: str
    filter: Optional[str] = None


class VirtualMount(BaseModel):
    name: str
    src: Optional[str] = None
    dest: Optional[str] = None
    filter: Optional[str] = None
    prefetch: Optional[bool] = None
    unravelArchives: Optional[bool] = None


class CommonRequirements(BaseModel):
    # General fields
    name: Optional[str] = None

    # Setup fields
    cuda: Optional[str] = None
    pythonVersion: Optional[str] = "3.8"
    customImage: Optional[DockerImageSelection] = None
    environment: Optional[Dict[str, Any]] = {}
    artifactsDestination: Optional[ArtifactsDestination] = None
    virtualMounts: Optional[List[VirtualMount]] = []
    from_template: Optional[str] = None

    # Infra fields
    useSpot: bool = False
    cloudProviders: Optional[List[CloudProviderChoice]] = []
    minvCPUs: int = -1
    minMemory: int = -1

    maxCPUWorkers: Optional[int] = 0
    instanceTypes: Optional[List[str]] = []
    gpuTypes: Optional[List[GPUType]] = []

    maxPricePerHour: Optional[int] = -1

    class Config:
        use_enum_values = False
        validate_assignment = True

    def __init__(self, **data: Any):
        if isinstance(data.get("cuda", None), float):
            data["cuda"] = str(data["cuda"])

        if data.get("instanceTypes") is None:
            if data.get("maxCPUWorkers") is None and data.get("gpuTypes") is None:
                raise TypeError(
                    "Please specify either maxCPUWorkers or [gpuTypes, gpusPerTrial] or instanceTypes"
                )

        # if data.get('maxCPUWorkers') and data.get('gpuTypes'):
        #     raise TypeError('Please specify only one of maxCPUWorkers and gpuTypes')

        super().__init__(**data)


class CodeCopy(BaseModel):
    type: CodeCopyType
    repo: str
    ref: Optional[str] = None
    codeDir: Optional[str] = None
    credentials: Optional[Dict[str, str]] = None

    class Config:
        use_enum_values = False

    def __init__(self, **data: Any):

        GIT_TRANSFER_METHODS = [
            "GITHUB",
            "GITHUB_PRIVATE",
            "BITBUCKET",
            "BITBUCKET_PRIVATE",
            "GITLAB",
            "GITLAB_PRIVATE",
        ]
        type_ = data.get("type")
        # if type_ in GIT_TRANSFER_METHODS and not data.get('commit'):
        #     raise TypeError('The field "commit" must be provived for git based methods')

        credentials_needed = set(code_credentials[CodeCopyType(type_)])
        if type_ in GIT_TRANSFER_METHODS:
            if str(type_).endswith("PRIVATE"):
                if not data.get("credentials") or credentials_needed - set(dict(data.get("credentials")).keys()):  # type: ignore
                    raise TypeError(
                        f'Please provide the following fields in the credentials section: {code_credentials[CodeCopyType(data.get("type"))]}'
                    )

        # Consider only requried credentials
        data["credentials"] = {k: data["credentials"][k] for k in credentials_needed}

        super().__init__(**data)


class VisualisationType(str, Enum):
    TENSORBOARD = "TENSORBOARD"
    AIM = "AIM"
    WANDB = "WANDB"
    COMETML = "COMETML"


class VisualisationChoice(BaseModel):
    type: VisualisationType = VisualisationType.TENSORBOARD
    startWithJob: bool = False

    class Config:
        use_enum_values = False


class DAPPConfig(BaseModel):
    epochs: int = -1


def mutually_exclusive_check(data: Dict[str, Any], fields: List[str]):
    bools = [bool(data.get(field)) for field in fields]
    return bools.count(True) == 1


class ScaleTorchConfig(CommonRequirements):
    gpusPerTrial: int = 0
    maxGpus: int = 0
    numNodes: int = 1
    entrypoint: str
    requirements: Optional[str] = None  # Filename
    codeTransfer: Optional[CodeCopy] = None
    tuning: Optional[Tuning] = None
    experiment: Optional[Experiment] = None
    preJobCommands: Optional[List[str]] = []
    postJobCommands: Optional[List[str]] = []
    maxTime: Optional[str] = None
    maxCost: Optional[int] = -1
    visualisation: Optional[VisualisationChoice] = None
    maxTrials: Optional[int] = -1
    useDAPP: Optional[bool] = False
    dapp: Optional[DAPPConfig] = DAPPConfig()

    def __init__(self, **data: Any):
        if data.get("experiment") is None and data.get("tuning") is None:
            raise TypeError('Either "experiment" or "tuning" field should be present')

        if data.get("experiment") is not None and data.get("tuning") is not None:
            raise TypeError(
                'Only one of "experiment" or "tuning" field should be present'
            )

        # if data.get("tuning") is not None and data.get("maxTrials") is None:
        #     raise TypeError("Field maxTrials is mandatory for HPT Jobs")

        if not mutually_exclusive_check(data, ["maxCPUWorkers", "gpusPerTrial"]):
            raise TypeError(
                "Please specify either maxCPUWorkers or [gpuTypes, gpusPerTrial]"
            )

        if data.get("gpusPerTrial") and not data.get("maxGpus"):
            data["maxGpus"] = data.get("gpusPerTrial")

        if data.get("requirements") is None and data.get("customImage") is None:
            raise TypeError("Please specify requirements or use customImage")

        super().__init__(**data)


class WorkstationConfig(CommonRequirements):
    requirements: Optional[str] = None  # Contents of requirement file
    gpuCount: int = 0
    bareBone: Optional[bool] = False
    visualisation: Optional[VisualisationType] = None
    numWorkstations: int = 1
    setupCommands: Optional[List[str]] = []

    def __init__(self, **data: Any):

        numWorkstations = data.get("numWorkstations")
        if numWorkstations and numWorkstations <= 0:
            raise TypeError(f"numWorkstations cannot be {numWorkstations}")

        if (bool(data.get("gpuCount", 0)) or bool(data.get("gpuTypes"))) and bool(
            data.get("maxCPUWorkers")
        ):
            raise TypeError(
                "Please specify either maxCPUWorkers or [gpuCount, gpuTypes]"
            )

        if (
            not bool(data.get("gpuCount", 0)) or not bool(data.get("gpuTypes"))
        ) and not bool(data.get("maxCPUWorkers")):
            raise TypeError(
                "Please specify only one among maxCPUWorkers and [gpuCount, gpuTypes]"
            )

        super().__init__(**data)


class VirtualMachine(BaseModel):
    id: str
    ip: str
    cloud: ProviderEnum
    username: str
    metadata: Dict[str, Union[str, int, float]] = {}


class NodeStatus(str, Enum):
    PROVISIONING = "PROVISIONING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    DELETED = "DELETED"
    SPOT_FAILURE = "SPOT_FAILURE"
    UNKNOWN = "UNKNOWN"
    SPECTATING = "SPECTATING"
    HEALTHY = "HEALTHY"


class Node(VirtualMachine):
    role: VMRole
    instance_type: str
    status: str
    job_id: str
    user_id: Optional[str] = None
    gpu_count: int = 0
    gpu_type: GPUType = GPUType.EMPTY
    region: str
    timestamp: str = ""
    stop_time: Optional[str] = None
    restart_time: Optional[str] = None
    spot: bool
    to_be_persisted: bool = False
    auditor_status: Optional[NodeStatus] = NodeStatus.UNKNOWN
    ssh_key_id: Optional[str] = None
    excess: bool = False

    # If metadata is not present in the db, it will be set to {}
    def __init__(self, **data: Any):
        if data.get("metadata") is None:
            data["metadata"] = {}

        if data.get("gpu_type") is None:
            data["gpu_type"] = GPUType.EMPTY.value

        super().__init__(**data)


class OnPremNode(Node):
    vcpus: Optional[int] = 0
    memory: Optional[int] = 0
    verified: bool = False
    cpu_only: bool


######### Events #########


class EventType(str, Enum):
    CREATION = "CREATION"
    STATUS_CHANGE = "STATUS_CHANGE"
    JOB_UPDATE = "JOB_UPDATE"


class EntityType(str, Enum):
    NODE = "NODE"
    TASK = "TASK"
    JOB = "JOB"
    WORKSTATION = "WORKSTATION"
    TRIAL = "TRIAL"
    INFERENCE = "INFERENCE"
    GPU_MACHINE = "GPU_MACHINE"


class Event(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    event_type: EventType
    entity_type: EntityType
    entity_id: str
    message: str
    job_id: str
    metadata: Optional[Dict[str, Any]] = {}
    timestamp: Optional[str] = None

    class Config:
        use_enum_values = False


############ Recipes #########


class InferenceRecipe(BaseModel):
    model: str
    id: str
    gpu_reqs: Dict[GPUType, int]
    is_embeddings: Optional[bool] = False
    type: InferenceDeploymentType
    engine: InferenceDeploymentEngine


class InfPerformanceResult(BaseModel):
    id: str
    gpu_type: GPUType
    llmperf_results: Dict[str, Any]
    max_model_len: Optional[int] = None
    num_gpus: int
    results_mean_output_throughput_token_per_s: float


############# InstancePricing #############


class InstancePricingDB(BaseModel):
    id: str
    cloud: ProviderEnum
    gpu_count: int
    gpu_type: Optional[GPUType] = GPUType.EMPTY
    instance_type: str
    memory: float
    on_demand: float
    region: str
    spot: float
    vcpus: float
    metadata: Optional[Dict[str, Any]] = None


class HashableInstancePricingDB(InstancePricingDB):
    default_filters: set = {"instance_type", "gpu_type", "cloud", "region", "gpu_count"}
    _hash: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._hash = self.hash_machine()

    def hash_machine(self, filters: set = set()) -> str:
        if not filters:
            filters = self.default_filters

        # Compute the SHA-256 hash of the bytes-like object
        hash_object = hashlib.sha256()

        for f in filters:
            hash_object.update(json.dumps(getattr(self, f)).encode("utf-8"))

        # Convert the hash object to a hexadecimal string
        hash_hex = hash_object.hexdigest()

        return hash_hex

    def __eq__(self, other):
        if isinstance(other, HashableInstancePricingDB):
            if other._hash == self._hash:
                return True
        return False

    def __hash__(self):
        return int(self._hash, 16) % 10**8
