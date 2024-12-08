# Generated by ariadne-codegen
# Source: ./documents

from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import AlertTypes, EntityState


class UpdateAlert(BaseModel):
    update_alert: Optional["UpdateAlertUpdateAlert"] = Field(alias="updateAlert")


class UpdateAlertUpdateAlert(BaseModel):
    id: str
    name: str
    state: EntityState
    type: AlertTypes


UpdateAlert.model_rebuild()
