"""
Upload endpoints for file and data source management
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List

from app.models.schemas import (
    FileUploadRequest,
    FileUploadResponse,
    DataSourceConfig,
    DataSourceResponse
)
from app.services.data_source_service import data_source_service

router = APIRouter()


@router.post("/file", response_model=FileUploadResponse)
async def upload_file(request: FileUploadRequest):
    """
    Upload and process a file for the knowledge base
    
    Accepts base64 encoded file content and extracts text for indexing.
    Supported file types: PDF, DOCX, TXT, XLSX, CSV
    """
    try:
        result = await data_source_service.process_file_upload(
            file_name=request.file_name,
            file_type=request.file_type,
            content=request.content,
            description=request.description
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return FileUploadResponse(
            file_id=result["file_id"],
            status="success",
            message=result["message"],
            processed=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file upload: {str(e)}"
        )


@router.post("/multipart-file")
async def upload_multipart_file(file: UploadFile = File(...)):
    """
    Upload a file using multipart form data
    
    Alternative endpoint for direct file uploads without base64 encoding
    """
    try:
        # Read file content
        content = await file.read()
        
        # Get file extension
        file_type = file.filename.split('.')[-1].lower()
        
        # Convert to base64 for processing
        import base64
        encoded_content = base64.b64encode(content).decode('utf-8')
        
        # Process the file
        result = await data_source_service.process_file_upload(
            file_name=file.filename,
            file_type=file_type,
            content=encoded_content,
            description=f"Uploaded via multipart: {file.filename}"
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )
        
        return FileUploadResponse(
            file_id=result["file_id"],
            status="success",
            message=result["message"],
            processed=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing multipart file upload: {str(e)}"
        )


@router.get("/status/{file_id}")
async def get_upload_status(file_id: str):
    """
    Get the status of an uploaded file
    
    Returns processing status and metadata for the specified file
    """
    try:
        document = data_source_service.get_document_by_id(file_id)
        
        if not document:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        
        return {
            "file_id": file_id,
            "status": "processed",
            "file_name": document["name"],
            "file_type": document["type"],
            "text_length": len(document["content"]),
            "metadata": document.get("metadata", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving upload status: {str(e)}"
        ) 