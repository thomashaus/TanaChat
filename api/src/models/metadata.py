"""Metadata models for Tana imports."""

from datetime import datetime

from pydantic import BaseModel, Field


class SupertagInfo(BaseModel):
    """Information about a supertag found in import."""

    uid: str
    name: str | None = None
    count: int = Field(description="Number of nodes using this supertag")


class TanaImportMetadata(BaseModel):
    """Metadata generated when a Tana file is imported."""

    file_id: str = Field(description="UUID for this import")
    original_filename: str
    username: str = Field(description="User who uploaded the file")
    import_timestamp: datetime

    # Stats from file
    total_nodes: int
    top_level_nodes: int
    leaf_nodes: int
    calendar_nodes: int
    fields_count: int

    # Supertags extracted
    supertags: list[SupertagInfo] = Field(default_factory=list)

    # Date range of nodes
    oldest_node_date: datetime | None = None
    newest_node_date: datetime | None = None

    # File info
    file_size_bytes: int
    spaces_path: str = Field(description="Path in S3")


class FileInfo(BaseModel):
    """Information about a stored Tana file."""

    file_id: str
    original_filename: str
    username: str
    file_size_bytes: int
    spaces_path: str
    upload_timestamp: datetime
    last_modified: str = Field(description="Last modified timestamp from S3")
    url: str = Field(description="URL to access the file in S3")
    metadata: TanaImportMetadata | None = None
