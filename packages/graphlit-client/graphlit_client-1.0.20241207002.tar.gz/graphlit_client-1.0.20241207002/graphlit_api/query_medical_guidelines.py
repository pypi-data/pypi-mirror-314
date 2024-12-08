# Generated by ariadne-codegen
# Source: ./documents

from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel


class QueryMedicalGuidelines(BaseModel):
    medical_guidelines: Optional["QueryMedicalGuidelinesMedicalGuidelines"] = Field(
        alias="medicalGuidelines"
    )


class QueryMedicalGuidelinesMedicalGuidelines(BaseModel):
    results: Optional[List[Optional["QueryMedicalGuidelinesMedicalGuidelinesResults"]]]


class QueryMedicalGuidelinesMedicalGuidelinesResults(BaseModel):
    id: str
    name: str
    alternate_names: Optional[List[Optional[str]]] = Field(alias="alternateNames")
    creation_date: Any = Field(alias="creationDate")
    thing: Optional[str]
    relevance: Optional[float]


QueryMedicalGuidelines.model_rebuild()
QueryMedicalGuidelinesMedicalGuidelines.model_rebuild()
