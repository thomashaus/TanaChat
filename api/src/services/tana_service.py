"""Tana file service for handling file operations and metadata."""

import hashlib
import json
import uuid
from datetime import datetime
from typing import Any

from ..models.metadata import SupertagInfo, TanaImportMetadata
from ..services.spaces_client import SpacesClient
from ..services.tana_validator import validate_tana_json


class TanaFileService:
    """Service for managing Tana files in S3 storage."""

    def __init__(self, spaces_client: SpacesClient):
        self.spaces_client = spaces_client

    def generate_file_id(self) -> str:
        """Generate a unique file ID."""
        return str(uuid.uuid4())

    def calculate_file_hash(self, content: bytes) -> str:
        """Calculate SHA-256 hash of file content."""
        return hashlib.sha256(content).hexdigest()

    def extract_supertags_from_nodes(self, nodes: list[dict[str, Any]]) -> list[SupertagInfo]:
        """Extract supertag information from nodes."""
        supertag_counts = {}

        def process_node(node):
            # Process supertags for this node
            supertags = node.get("supertags", [])
            for supertag in supertags:
                if isinstance(supertag, dict):
                    supertag_id = supertag.get("uid", "unknown")
                    supertag_name = supertag.get("name", supertag_id)
                else:
                    supertag_id = supertag
                    supertag_name = supertag

                if supertag_id not in supertag_counts:
                    supertag_counts[supertag_id] = {
                        "uid": supertag_id,
                        "name": supertag_name,
                        "count": 0,
                    }
                supertag_counts[supertag_id]["count"] += 1

            # Process children recursively
            children = node.get("children", [])
            if children:
                for child in children:
                    process_node(child)

        for node in nodes:
            process_node(node)

        return [SupertagInfo(**info) for info in supertag_counts.values()]

    def extract_date_range_from_nodes(
        self, nodes: list[dict[str, Any]]
    ) -> tuple[datetime | None, datetime | None]:
        """Extract the oldest and newest creation dates from nodes."""
        timestamps = []

        def process_node(node):
            created_at = node.get("createdAt")
            if created_at and isinstance(created_at, int):
                timestamps.append(datetime.fromtimestamp(created_at / 1000))

            children = node.get("children", [])
            if children:
                for child in children:
                    process_node(child)

        for node in nodes:
            process_node(node)

        if not timestamps:
            return None, None

        return min(timestamps), max(timestamps)

    def create_metadata(
        self,
        file_id: str,
        original_filename: str,
        username: str,
        content: bytes,
        tana_data: dict[str, Any],
    ) -> TanaImportMetadata:
        """Create metadata for a Tana file import."""

        # Extract basic statistics
        nodes = tana_data.get("nodes", [])
        summary = tana_data.get("summary", {})

        # Extract supertags
        supertags = self.extract_supertags_from_nodes(nodes)

        # Extract date range
        oldest_date, newest_date = self.extract_date_range_from_nodes(nodes)

        return TanaImportMetadata(
            file_id=file_id,
            original_filename=original_filename,
            username=username,
            import_timestamp=datetime.utcnow(),
            total_nodes=len(nodes),
            top_level_nodes=summary.get("topLevelNodes", len(nodes)),
            leaf_nodes=summary.get("leafNodes", 0),
            calendar_nodes=summary.get("calendarNodes", 0),
            fields_count=summary.get("fields", 0),
            supertags=supertags,
            oldest_node_date=oldest_date,
            newest_node_date=newest_date,
            file_size_bytes=len(content),
            spaces_path=f"tana/{username}/{file_id}.json",
        )

    async def upload_file(
        self,
        original_filename: str,
        username: str,
        content: bytes,
        content_type: str = "application/json",
    ) -> TanaImportMetadata:
        """Upload a Tana file to S3 storage."""

        # Validate the content
        validation = validate_tana_json(content)
        if not validation.valid:
            raise ValueError(f"Invalid Tana file: {validation.error}")

        # Parse the JSON content
        tana_data = json.loads(content.decode("utf-8"))

        # Generate metadata
        file_id = self.generate_file_id()
        metadata = self.create_metadata(
            file_id=file_id,
            original_filename=original_filename,
            username=username,
            content=content,
            tana_data=tana_data,
        )

        # Upload the file to S3
        spaces_key = metadata.spaces_path
        upload_result = self.spaces_client.upload_file(
            key=spaces_key, data=content, content_type=content_type
        )

        if not upload_result["success"]:
            raise RuntimeError(f"Failed to upload to S3: {upload_result['error']}")

        # Upload metadata as a separate file
        metadata_key = f"tana/{username}/{file_id}.meta.json"
        metadata_content = metadata.model_dump_json(indent=2).encode("utf-8")
        metadata_upload = self.spaces_client.upload_file(
            key=metadata_key, data=metadata_content, content_type="application/json"
        )

        if not metadata_upload["success"]:
            raise RuntimeError(f"Failed to upload metadata to S3: {metadata_upload['error']}")

        return metadata

    async def list_files(self, username: str) -> list[dict[str, Any]]:
        """List all Tana files for a user."""
        prefix = f"tana/{username}/"
        files = self.spaces_client.list_files(prefix=prefix)

        # Filter to only include .json files (not .meta.json)
        tana_files = []
        for file_info in files:
            key = file_info["key"]
            if key.endswith(".json") and not key.endswith(".meta.json"):
                # Extract file_id from key
                file_id = key.split("/")[-1].replace(".json", "")

                # Try to get metadata
                metadata_key = f"{prefix}{file_id}.meta.json"
                metadata_content = self.spaces_client.download_file(metadata_key)

                metadata = None
                if metadata_content:
                    try:
                        metadata_data = json.loads(metadata_content.decode("utf-8"))
                        metadata = TanaImportMetadata(**metadata_data)
                    except Exception:
                        pass

                file_info["file_id"] = file_id
                file_info["metadata"] = metadata
                tana_files.append(file_info)

        return tana_files

    async def get_file(self, username: str, file_id: str) -> bytes | None:
        """Download a specific Tana file."""
        file_key = f"tana/{username}/{file_id}.json"
        return self.spaces_client.download_file(file_key)

    async def get_metadata(self, username: str, file_id: str) -> TanaImportMetadata | None:
        """Get metadata for a specific Tana file."""
        metadata_key = f"tana/{username}/{file_id}.meta.json"
        content = self.spaces_client.download_file(metadata_key)

        if not content:
            return None

        try:
            metadata_data = json.loads(content.decode("utf-8"))
            return TanaImportMetadata(**metadata_data)
        except Exception:
            return None

    async def delete_file(self, username: str, file_id: str) -> bool:
        """Delete a Tana file and its metadata."""
        file_key = f"tana/{username}/{file_id}.json"
        metadata_key = f"tana/{username}/{file_id}.meta.json"

        file_deleted = self.spaces_client.delete_file(file_key)
        metadata_deleted = self.spaces_client.delete_file(metadata_key)

        return file_deleted and metadata_deleted
