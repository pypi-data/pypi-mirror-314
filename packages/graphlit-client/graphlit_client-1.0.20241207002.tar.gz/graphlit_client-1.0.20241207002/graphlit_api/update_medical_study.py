# Generated by ariadne-codegen
# Source: ./documents

from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class UpdateMedicalStudy(BaseModel):
    update_medical_study: Optional["UpdateMedicalStudyUpdateMedicalStudy"] = Field(
        alias="updateMedicalStudy"
    )


class UpdateMedicalStudyUpdateMedicalStudy(BaseModel):
    id: str
    name: str


UpdateMedicalStudy.model_rebuild()
