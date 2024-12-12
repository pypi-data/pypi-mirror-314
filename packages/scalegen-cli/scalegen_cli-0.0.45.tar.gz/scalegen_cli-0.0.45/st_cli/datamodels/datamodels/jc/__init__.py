from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel

from ..api import Job
from ..common import *


class CheckEnum(str, Enum):
    HEARTBEAT = "HEARTBEAT"
    COST_TIME = "COST_TIME"
    KEEP_ALIVE = "KEEP_ALIVE"
    SYNC_NNI = "SYNC_NNI"
    SYNC_DAPP_NNI = "SYNC_DAPP_NNI"


class NniTrialRespone(BaseModel):
    trialJobId: str
    status: str
    hyperParameters: List[str]
    sequenceId: int


class NniExperimentResponse(BaseModel):
    id: str
    status: str


##### Tasks #####


class TaskStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TaskType(str, Enum):
    CLEANUP = "CLEANUP"
    SETUP_JOB = "SETUP_JOB"
    DELETE_JOB = "DELETE_JOB"
    DELETE_DAPP_JOB = "DELETE_DAPP_JOB"
    REPROVISION_WORKER = "REPROVISION_WORKER"
    REPROVISION_DAPP_WORKER = "REPROVISION_DAPP_WORKER"
    VERIFY_ONPREM_NODE = "VERIFY_ONPREM_NODE"
    SETUP_INF_DEPLOYMENT = "SETUP_INF_DEPLOYMENT"
    DELETE_INF_DEPLOYMENT = "DELETE_INF_DEPLOYMENT"
    SCALE_INF_DEPLOYMENT = "SCALE_INF_DEPLOYMENT"
    SETUP_LLM_GATEWAY = "SETUP_LLM_GATEWAY"
    DELETE_LLM_GATEWAY = "DELETE_LLM_GATEWAY"
    SETUP_GPU_MACHINE = "SETUP_GPU_MACHINE"
    DELETE_GPU_MACHINE = "DELETE_GPU_MACHINE"

    # Retired tasks
    SETUP_WORKSTATION = "SETUP_WORKSTATION"
    DELETE_WORKSTATION = "DELETE_WORKSTATION"
    RESTART_WORKSTATION = "RESTART_WORKSTATION"
    STOP_WORKSTATION = "STOP_WORKSTATION"
    DELETE_TRIAL = "DELETE_TRIAL"
    START_TB = "START_TB"
    STOP_TB = "STOP_TB"
    START_AIM = "START_AIM"
    STOP_AIM = "STOP_AIM"
    STOP_VIS = "STOP_VIS"


class TaskPayloadBase(BaseModel):
    job_id: str
    ws_id: Optional[str] = None
    test_task: Optional[bool] = False


class SetupJobTaskPayload(TaskPayloadBase):
    test_job_doc: Optional[Job] = None

    # If test_job_doc doesn't fit the schema of type Job, set it to None
    def __init__(self, **kwargs):
        try:
            Job(**kwargs.get("test_job_doc", {}))
        except:
            kwargs["test_job_doc"] = None

        super().__init__(**kwargs)


class DeleteTrialTaskPayload(TaskPayloadBase):
    trial_id: str


class DeleteJobTaskPayload(TaskPayloadBase):
    has_failed: bool = False


class ReprovisionWorkerTaskPayload(SetupJobTaskPayload):
    worker_id: str


class VerifyOnPremNodeTaskPayload(TaskPayloadBase):
    on_prem_node_id: str


class ScaleType(str, Enum):
    UP = "up"
    DOWN = "down"
    ZERO = "zero"
    RELOAD = "reload"
    FAST_SCALE_UP_SETUP = "_fast_scale_up_setup"


class ScaleInferenceDeploymentTaskPayload(TaskPayloadBase):
    scale: ScaleType
    vm_num: int = 1
    target_throughput: Optional[float] = None
    use_initial_config: bool = False
    created_by: Optional[str] = None


class DeleteInferenceTaskPayload(TaskPayloadBase):
    failed: bool = False


task_to_payload_type = {
    TaskType.CLEANUP: TaskPayloadBase,
    TaskType.SETUP_JOB: SetupJobTaskPayload,
    TaskType.DELETE_JOB: DeleteJobTaskPayload,
    TaskType.DELETE_DAPP_JOB: TaskPayloadBase,
    TaskType.REPROVISION_WORKER: ReprovisionWorkerTaskPayload,
    TaskType.REPROVISION_DAPP_WORKER: ReprovisionWorkerTaskPayload,
    TaskType.VERIFY_ONPREM_NODE: VerifyOnPremNodeTaskPayload,
    TaskType.SETUP_INF_DEPLOYMENT: TaskPayloadBase,
    TaskType.SCALE_INF_DEPLOYMENT: ScaleInferenceDeploymentTaskPayload,
    TaskType.DELETE_INF_DEPLOYMENT: DeleteInferenceTaskPayload,
    TaskType.SETUP_LLM_GATEWAY: TaskPayloadBase,
    TaskType.DELETE_LLM_GATEWAY: TaskPayloadBase,
    TaskType.SETUP_GPU_MACHINE: TaskPayloadBase,
    TaskType.DELETE_GPU_MACHINE: TaskPayloadBase,
    # Retired tasks
    TaskType.SETUP_WORKSTATION: TaskPayloadBase,
    TaskType.DELETE_WORKSTATION: TaskPayloadBase,
    TaskType.RESTART_WORKSTATION: TaskPayloadBase,
    TaskType.STOP_WORKSTATION: TaskPayloadBase,
    TaskType.DELETE_TRIAL: DeleteTrialTaskPayload,
    TaskType.START_TB: TaskPayloadBase,
    TaskType.STOP_TB: TaskPayloadBase,
    TaskType.START_AIM: TaskPayloadBase,
    TaskType.STOP_AIM: TaskPayloadBase,
    TaskType.STOP_VIS: TaskPayloadBase,
}

if len(set(task_to_payload_type.keys())) != len(TaskType):
    raise ValueError("task_to_payload_type is missing some TaskType")


class Task(BaseModel):
    id: str
    status: TaskStatus
    type: TaskType
    payload: TaskPayloadBase
    timestamp: str
    user_id: str

    def __init__(self, *args, **kwargs):

        # For backwards compatibility or any dev tasks created with no job_id
        if kwargs["payload"].get("job_id", None) is None:
            kwargs["payload"]["job_id"] = "dummy_job_id"

        # Create the payload of right type
        if isinstance(kwargs["payload"], TaskPayloadBase):
            kwargs["payload"] = kwargs["payload"].model_dump(mode="json")

        kwargs["payload"] = task_to_payload_type[TaskType(kwargs["type"])](
            **kwargs["payload"]
        )

        # Call parent's __init__
        super().__init__(**kwargs)


#### Node ####


class NodeStatusCheck(BaseModel):
    id: str
    region: str
    status: NodeStatus
    ip: Optional[str] = None
    user_id: str
    job_id: str


##############


class JCSession(BaseModel):
    user_id: str
    timestamp: str
    cloud: str
    account_id: str
    status: str
    session_id: Optional[str] = None


### Inference ###

fast_scale_up_clouds = {ProviderEnum.AWS}
