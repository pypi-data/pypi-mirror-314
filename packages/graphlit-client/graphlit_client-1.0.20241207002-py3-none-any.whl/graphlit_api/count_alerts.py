# Generated by ariadne-codegen
# Source: ./documents

from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class CountAlerts(BaseModel):
    count_alerts: Optional["CountAlertsCountAlerts"] = Field(alias="countAlerts")


class CountAlertsCountAlerts(BaseModel):
    count: Optional[Any]


CountAlerts.model_rebuild()
