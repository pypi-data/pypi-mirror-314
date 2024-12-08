# Generated by ariadne-codegen
# Source: ./documents

from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class CountPersons(BaseModel):
    count_persons: Optional["CountPersonsCountPersons"] = Field(alias="countPersons")


class CountPersonsCountPersons(BaseModel):
    count: Optional[Any]


CountPersons.model_rebuild()
