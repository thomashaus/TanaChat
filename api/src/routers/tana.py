"""Tana file validation, upload, and management endpoints."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import Response

from ..dependencies import get_current_user
from ..models.metadata import TanaImportMetadata
from ..models.tana import TanaValidationResult
from ..services.spaces_client import get_spaces_client
from ..services.tana_service import TanaFileService
from ..services.tana_validator import validate_tana_json

router = APIRouter()


def get_tana_service() -> TanaFileService:
    """Initialize TanaFileService with S3 client."""
    spaces_client = get_spaces_client()
    if not spaces_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="S3 not configured",
        )
    return TanaFileService(spaces_client)


@router.post("/validate", response_model=TanaValidationResult, summary="Validate Tana JSON file")
async def validate_tana_file(file: UploadFile = File(...)):
    """
    Validate Tana JSON export format without storing the file.

    Supports Tana Intermediate Format (TIF) and Tagr Export Format.
    No authentication required for validation.

    Args:
        file: Tana JSON export file to validate

    Returns:
        Validation result with format type, node count, and any errors

    Raises:
        422: File is not a valid JSON file
        413: File size exceeds 100MB limit
    """
    if not file.filename or not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File must be a .json file",
        )

    content = await file.read()
    if len(content) > 100 * 1024 * 1024:  # 100MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 100MB limit",
        )

    result = validate_tana_json(content)
    return result


@router.post("/upload", response_model=TanaImportMetadata, summary="Upload Tana file")
async def upload_tana_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    tana_service: TanaFileService = Depends(get_tana_service),
):
    """
    Validate and upload Tana JSON export file to secure storage.

    Files are stored with user-scoped access control and rich metadata
    including node counts, supertag analysis, and creation timestamps.

    Args:
        file: Tana JSON export file to upload
        current_user: Authenticated user context
        tana_service: Tana file management service

    Returns:
        Import metadata with file ID, analysis results, and storage details

    Raises:
        422: Invalid file format or Tana validation errors
        503: Storage service unavailable
        500: Internal server error during upload
    """
    if not file.filename or not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File must be a .json file",
        )

    content = await file.read()
    if len(content) > 100 * 1024 * 1024:  # 100MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 100MB limit",
        )

    try:
        metadata = await tana_service.upload_file(
            original_filename=file.filename,
            username=current_user["username"],
            content=content,
            content_type="application/json",
        )
        return metadata
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/files", summary="List user's Tana files")
async def list_tana_files(
    current_user: dict = Depends(get_current_user),
    tana_service: TanaFileService = Depends(get_tana_service),
):
    """
    List all Tana files uploaded by the authenticated user.

    Returns metadata for each file including upload date, node counts,
    and validation status.

    Returns:
        List of user's Tana files with metadata

    Raises:
        500: Failed to retrieve file list
    """
    try:
        files = await tana_service.list_files(current_user["username"])
        return {"files": files, "count": len(files)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list files: {str(e)}",
        )


@router.get("/files/{file_id}", summary="Download Tana file")
async def get_tana_file(
    file_id: str,
    current_user: dict = Depends(get_current_user),
    tana_service: TanaFileService = Depends(get_tana_service),
):
    """
    Download a specific Tana file by ID.

    Only allows access to files owned by the authenticated user.

    Args:
        file_id: Unique identifier for the Tana file
        current_user: Authenticated user context

    Returns:
        Tana JSON file content

    Raises:
        404: File not found or access denied
        500: Failed to retrieve file
    """
    try:
        content = await tana_service.get_file(current_user["username"], file_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found",
            )
        return Response(content=content, media_type="application/json")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve file: {str(e)}",
        )


@router.get("/files/{file_id}/meta", response_model=TanaImportMetadata, summary="Get file metadata")
async def get_tana_metadata(
    file_id: str,
    current_user: dict = Depends(get_current_user),
    tana_service: TanaFileService = Depends(get_tana_service),
):
    """
    Get metadata for a specific Tana file without downloading the content.

    Returns analysis results, validation status, and file statistics.

    Args:
        file_id: Unique identifier for the Tana file
        current_user: Authenticated user context

    Returns:
        File import metadata and analysis results

    Raises:
        404: File metadata not found
        500: Failed to retrieve metadata
    """
    try:
        metadata = await tana_service.get_metadata(current_user["username"], file_id)
        if not metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Metadata not found",
            )
        return metadata
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metadata: {str(e)}",
        )


@router.delete("/files/{file_id}", summary="Delete Tana file")
async def delete_tana_file(
    file_id: str,
    current_user: dict = Depends(get_current_user),
    tana_service: TanaFileService = Depends(get_tana_service),
):
    """
    Delete a Tana file and its associated metadata.

    Permanently removes the file from storage and all related metadata.

    Args:
        file_id: Unique identifier for the Tana file
        current_user: Authenticated user context

    Returns:
        Deletion confirmation

    Raises:
        404: File not found or access denied
        500: Failed to delete file
    """
    try:
        success = await tana_service.delete_file(current_user["username"], file_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found or could not be deleted",
            )
        return {"message": "File deleted successfully", "file_id": file_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {str(e)}",
        )
