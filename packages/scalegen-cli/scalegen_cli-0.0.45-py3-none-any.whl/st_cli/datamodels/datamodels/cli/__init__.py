from pydantic import BaseModel
from typing import List, Optional

from ..common import ScaleTorchConfig, JobType, ProductType


class JobLaunchRequest(BaseModel):
    config: ScaleTorchConfig
    type: JobType
    productType: Optional[ProductType] = ProductType.SCALETORCH

    class Config:
        use_enum_values = True


class JobStopRequest(BaseModel):
    id: str
    trials: List[str]


class JobLaunchRespose(BaseModel):
    pass


class TrialLatestMetrics(BaseModel):
    acc: float
    loss: float
    val_loss: float
    val_acc: float


class Trial(BaseModel):
    trial_id: str
    status: str
    metrics: TrialLatestMetrics


class JobViewResponse(BaseModel):
    id: str
    type: JobType
    trials: List[Trial]
