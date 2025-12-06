"""Tana Intermediate Format (TIF) models."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TanaIntermediateSupertag(BaseModel):
    """Supertag in Tana Intermediate Format."""

    uid: str
    name: str | None = None


class TanaIntermediateNode(BaseModel):
    """Node in Tana Intermediate Format."""

    uid: str
    name: str
    description: str | None = None
    created_at: int | None = Field(None, alias="createdAt")
    edited_at: int | None = Field(None, alias="editedAt")
    type: Literal["node", "date", "url", "codeblock", "field", "image"] | None = None
    media_url: str | None = Field(None, alias="mediaUrl")
    todo_state: Literal["todo", "done"] | None = Field(None, alias="todoState")
    refs: list[str] | None = None
    supertags: list[TanaIntermediateSupertag] | None = None
    children: list["TanaIntermediateNode"] | None = None

    class Config:
        populate_by_name = True


class TanaIntermediateSummary(BaseModel):
    """Summary statistics in Tana Intermediate Format."""

    leaf_nodes: int = Field(alias="leafNodes")
    top_level_nodes: int = Field(alias="topLevelNodes")
    total_nodes: int = Field(alias="totalNodes")
    calendar_nodes: int = Field(alias="calendarNodes")
    fields: int
    broken_refs: int = Field(alias="brokenRefs")

    class Config:
        populate_by_name = True


class TanaIntermediateFile(BaseModel):
    """Root structure of Tana Intermediate Format file."""

    version: Literal["TanaIntermediateFile V0.1"]
    summary: TanaIntermediateSummary | None = None
    nodes: list[TanaIntermediateNode]

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        if v != "TanaIntermediateFile V0.1":
            raise ValueError(f"Invalid Tana file version: {v}")
        return v


class TanaValidationResult(BaseModel):
    """Result of Tana file validation."""

    valid: bool
    error: str | None = None
    version: str | None = None
    node_count: int = 0
    supertag_count: int = 0
    supertags: list[str] = Field(default_factory=list)
