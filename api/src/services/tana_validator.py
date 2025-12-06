"""Tana file validation service"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

# Add parent directory to path to import shared lib
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from lib import TanaIO  # noqa: E402


class TanaNode(BaseModel):
    """Tana node structure"""

    uid: str
    name: str
    created: str
    edited: str
    type: str
    children: list["TanaNode"] = []
    fields: dict[str, Any] = {}
    inline_data: dict[str, Any] = {}


TanaNode.model_rebuild()


class TanaFile(BaseModel):
    """Tana Intermediate File structure"""

    version: str = "TanaIntermediateFile V0.1"
    nodes: list[TanaNode] = []
    meta: dict[str, Any] = {}


class TanaValidationError(Exception):
    """Custom Tana validation error"""

    pass


def validate_tana_file(content: str) -> dict[str, Any]:
    """
    Validate a Tana Intermediate File (TIF)

    Args:
        content: JSON content as string

    Returns:
        Validation result with status and details

    Example valid TIF:
    {
        "version": "TanaIntermediateFile V0.1",
        "nodes": [
            {
                "uid": "root",
                "name": "My Tana File",
                "created": "2024-01-01T00:00:00.000Z",
                "edited": "2024-01-01T00:00:00.000Z",
                "type": "node",
                "children": []
            }
        ],
        "meta": {
            "created": "2024-01-01T00:00:00.000Z",
            "format": "TanaIntermediateFile"
        }
    }
    """
    try:
        # Parse JSON first
        data = json.loads(content)

        # Validate against Pydantic model
        tana_file = TanaFile(**data)

        # Additional validations
        if tana_file.version != "TanaIntermediateFile V0.1":
            raise TanaValidationError(f"Unsupported version: {tana_file.version}")

        if not tana_file.nodes:
            raise TanaValidationError("TIF must contain at least one node")

        # Check for required fields in nodes
        node_uids = set()
        for node in tana_file.nodes:
            if not node.uid:
                raise TanaValidationError("All nodes must have a uid")
            if not node.name:
                raise TanaValidationError("All nodes must have a name")
            if node.uid in node_uids:
                raise TanaValidationError(f"Duplicate node uid: {node.uid}")
            node_uids.add(node.uid)

            # Validate required timestamps
            if not node.created:
                raise TanaValidationError(f"Node {node.uid} missing created timestamp")
            if not node.edited:
                raise TanaValidationError(f"Node {node.uid} missing edited timestamp")

        return {
            "valid": True,
            "version": tana_file.version,
            "node_count": len(tana_file.nodes),
            "meta": tana_file.meta,
            "nodes": [node.uid for node in tana_file.nodes],
        }

    except json.JSONDecodeError as e:
        return {"valid": False, "error": "Invalid JSON", "details": str(e)}
    except ValidationError as e:
        return {"valid": False, "error": "Validation error", "details": str(e)}
    except TanaValidationError as e:
        return {"valid": False, "error": "Tana validation error", "details": str(e)}
    except Exception as e:
        return {"valid": False, "error": "Unexpected error", "details": str(e)}


def extract_nodes_by_type(tana_file: dict[str, Any], node_type: str) -> list[dict[str, Any]]:
    """Extract nodes of a specific type from a Tana file"""
    nodes = []
    if not tana_file.get("valid"):
        return nodes

    # Parse and get all nodes
    try:
        data = json.loads(tana_file.get("content", "{}"))
        tana = TanaFile(**data)

        def extract_recursive(nodes_list: list[TanaNode], target_type: str) -> None:
            for node in nodes_list:
                if node.type == target_type:
                    nodes.append(
                        {
                            "uid": node.uid,
                            "name": node.name,
                            "created": node.created,
                            "edited": node.edited,
                            "fields": node.fields,
                            "inlineData": node.inlineData,
                            "children": [child.uid for child in node.children],
                        }
                    )
                extract_recursive(node.children, target_type)

        extract_recursive(tana.nodes, node_type)
    except Exception:
        pass

    return nodes


def validate_tana_json(content: bytes) -> dict[str, Any]:
    """
    Validate Tana JSON content using shared lib and detailed validation

    Args:
        content: JSON content as bytes

    Returns:
        Validation result with status and details
    """
    try:
        # Parse JSON
        data = json.loads(content.decode("utf-8"))

        # Use shared lib for basic structure validation
        tana_io = TanaIO()
        if not tana_io.validate_tana_structure(data):
            return {
                "valid": False,
                "error": "Invalid Tana file structure",
                "details": "File does not match expected Tana format (missing version/nodes/docs)",
            }

        # Use detailed validation for comprehensive checks
        return validate_tana_file(content.decode("utf-8"))

    except json.JSONDecodeError as e:
        return {"valid": False, "error": "Invalid JSON", "details": str(e)}
    except Exception as e:
        return {"valid": False, "error": "Unexpected error", "details": str(e)}


def validate_schema_compliance(content: str) -> dict[str, Any]:
    """
    Validate Tana file against additional schema requirements

    Returns detailed validation results
    """
    validation = validate_tana_file(content)

    if not validation["valid"]:
        return validation

    # Additional schema checks
    warnings = []

    try:
        data = json.loads(content)
        tana = TanaFile(**data)

        # Check for circular references
        visited = set()
        stack = []

        def check_circular(node_uid: str, path: list[str]) -> None:
            if node_uid in visited:
                cycle_path = " -> ".join(path + [node_uid])
                warnings.append(f"Circular reference detected: {cycle_path}")
                return

            visited.add(node_uid)
            stack.append(node_uid)

            # Check children in parsed structure
            for node in tana.nodes:
                if node.uid == node_uid:
                    for child_uid in [c.uid for c in node.children]:
                        check_circular(child_uid, path + [node_uid])

            stack.pop()

        for node_uid in validation["nodes"]:
            check_circular(node_uid, [])

        # Validate node structure
        for node in tana.nodes:
            # Check for empty names
            if not node.name.strip():
                warnings.append(f"Node {node.uid} has empty name")

            # Check timestamps format
            try:
                datetime.fromisoformat(node.created.replace("Z", "+00:00"))
                datetime.fromisoformat(node.edited.replace("Z", "+00:00"))
            except ValueError:
                warnings.append(f"Node {node.uid} has invalid timestamp format")

        return {"valid": True, "warnings": warnings, **validation}

    except Exception as e:
        return {"valid": False, "error": "Schema compliance check failed", "details": str(e)}
