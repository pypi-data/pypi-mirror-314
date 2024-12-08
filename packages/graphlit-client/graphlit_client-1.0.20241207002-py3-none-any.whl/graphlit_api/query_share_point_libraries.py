# Generated by ariadne-codegen
# Source: ./documents

from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class QuerySharePointLibraries(BaseModel):
    share_point_libraries: Optional["QuerySharePointLibrariesSharePointLibraries"] = (
        Field(alias="sharePointLibraries")
    )


class QuerySharePointLibrariesSharePointLibraries(BaseModel):
    account_name: Optional[str] = Field(alias="accountName")
    results: Optional[
        List[Optional["QuerySharePointLibrariesSharePointLibrariesResults"]]
    ]


class QuerySharePointLibrariesSharePointLibrariesResults(BaseModel):
    library_name: Optional[str] = Field(alias="libraryName")
    library_id: Optional[str] = Field(alias="libraryId")
    site_name: Optional[str] = Field(alias="siteName")
    site_id: Optional[str] = Field(alias="siteId")


QuerySharePointLibraries.model_rebuild()
QuerySharePointLibrariesSharePointLibraries.model_rebuild()
