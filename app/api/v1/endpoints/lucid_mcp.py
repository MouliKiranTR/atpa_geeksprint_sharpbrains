"""
Lucid MCP endpoints for accessing Lucid diagrams via MCP tools
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import base64

from app.models.schemas import (
    MCPListDiagramsRequest,
    MCPListDiagramsResponse
)
from app.services.lucid_service import lucid_service

router = APIRouter()


@router.post("/export-and-upload")
async def export_lucid_and_upload_to_openarena(
    document_id: str,
    page_id: Optional[str] = None,
    format: str = "png",
    width: Optional[int] = 1920,
    height: Optional[int] = None
):
    """
    Export a Lucid document as an image and upload it to Open Arena
    
    Args:
        document_id: Lucid document ID to export
        page_id: Optional specific page to export
        format: Image format (png, jpg, pdf, svg) - default: png
        width: Optional width for export - default: 1920
        height: Optional height for export
    """
    if not lucid_service:
        raise HTTPException(
            status_code=500,
            detail="Lucid API key is not configured."
        )
    
    try:
        # Export the document from Lucid
        print(f"Exporting Lucid document: {document_id}")
        export_result = await lucid_service.export_document_image(
            document_id=document_id,
            page_id=page_id,
            format=format,
            width=width,
            height=height
        )
        
        if not export_result.get("success"):
            error_msg = export_result.get('error', 'Unknown error')
            raise HTTPException(
                status_code=400,
                detail=f"Failed to export Lucid document: {error_msg}"
            )
        
        # Get image data and upload to Open Arena
        image_data = export_result["image_data"]
        
        # Import data source service
        from app.services.data_source_service import data_source_service
        
        # Convert image to base64 for upload
        encoded_content = base64.b64encode(image_data).decode('utf-8')
        
        # Create filename
        ext = f".{format.lower()}"
        filename = f"lucid_export_{document_id}"
        if page_id:
            filename += f"_page_{page_id}"
        filename += ext
        
        # Upload to Open Arena
        upload_result = await data_source_service.process_file_upload(
            file_name=filename,
            file_type=format.lower(),
            content=encoded_content,
            description=f"Exported from Lucid document {document_id}"
        )
        
        if not upload_result.get("success"):
            error_msg = upload_result.get('error', 'Unknown error')
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload to Open Arena: {error_msg}"
            )
        
        print(f"Successfully uploaded with file ID: {upload_result['file_id']}")
        
        return {
            "success": True,
            "message": "Successfully exported and uploaded to Open Arena",
            "lucid_export": {
                "document_id": document_id,
                "page_id": page_id,
                "format": format,
                "size": len(image_data)
            },
            "openarena_upload": {
                "file_id": upload_result["file_id"],
                "filename": filename,
                "status": "uploaded"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during export and upload: {str(e)}"
        )


@router.post("/list-diagrams", response_model=MCPListDiagramsResponse)
async def list_lucid_diagrams(request: MCPListDiagramsRequest):
    """
    List Lucid diagrams using the configured API key
    
    This endpoint provides the same functionality as the MCP server's 
    list_lucid_diagrams tool but via a REST API endpoint.
    """
    if not lucid_service:
        raise HTTPException(
            status_code=500,
            detail="Lucid API key is not configured. Please set LUCID_API_KEY."
        )
    
    try:
        if request.search_query:
            # First try API search
            print(f"DEBUG: Trying API search for: '{request.search_query}'")
            response = await lucid_service.search_documents(
                query=request.search_query,
                product_filter=request.product_filter,
                limit=request.limit,
                offset=request.offset,
                use_client_side_search=False
            )
            
            # If API search returns no results, try client-side search
            if len(response.documents) == 0:
                print("DEBUG: Trying client-side search")
                response = await lucid_service.search_documents(
                    query=request.search_query,
                    product_filter=request.product_filter,
                    limit=request.limit,
                    offset=request.offset,
                    use_client_side_search=True
                )
        else:
            # Use search API without query to list all documents
            # (since the /documents endpoint returns 404)
            response = await lucid_service.search_documents(
                query=None,
                product_filter=request.product_filter,
                limit=request.limit,
                offset=request.offset
            )
        
        message = f"Found {len(response.documents)} Lucid diagrams"
        if request.search_query:
            message += f" matching '{request.search_query}'"
        
        return MCPListDiagramsResponse(
            diagrams=response.documents,
            total_count=response.totalCount,
            has_more=response.hasMore,
            message=message
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Lucid API Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing Lucid API: {str(e)}"
        )


@router.get("/search/{query}")
async def search_lucid_diagrams(
    query: str,
    limit: Optional[int] = 20,
    product_filter: Optional[str] = None,
    use_client_side_search: Optional[bool] = False
):
    """
    Search Lucid diagrams by query string
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        product_filter: Filter by product type ("lucidchart" or "lucidspark")
        use_client_side_search: Use client-side search for flexible matching
    """
    if not lucid_service:
        raise HTTPException(
            status_code=500,
            detail="Lucid API key is not configured. Please set LUCID_API_KEY."
        )
    
    try:
        response = await lucid_service.search_documents(
            query=query,
            product_filter=product_filter,
            limit=limit,
            offset=0,
            use_client_side_search=use_client_side_search
        )
        
        search_type = "client-side" if use_client_side_search else "API"
        message = (
            f"Found {len(response.documents)} diagrams matching '{query}' "
            f"(using {search_type} search)"
        )
        
        return MCPListDiagramsResponse(
            diagrams=response.documents,
            total_count=response.totalCount,
            has_more=response.hasMore,
            message=message
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Lucid API Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching Lucid diagrams: {str(e)}"
        )


@router.get("/export-help")
async def get_export_help():
    """
    Get help information for using the export functionality
    """
    return {
        "message": "Lucid Export to Open Arena Help",
        "description": ("This service allows you to export Lucid documents "
                       "as images and upload them to Open Arena for analysis."),
        "endpoints": {
            "/export-and-upload": {
                "method": "POST",
                "description": "Export a Lucid document and upload to Open Arena",
                "required_params": ["document_id"],
                "optional_params": {
                    "page_id": "Specific page to export",
                    "format": "Image format (png, jpg, pdf, svg)",
                    "width": "Export width in pixels",
                    "height": "Export height in pixels"
                }
            },
            "/list-diagrams": {
                "method": "POST", 
                "description": "List available Lucid diagrams to get document IDs"
            }
        },
        "example_usage": {
            "step_1": "Use /list-diagrams to find document IDs",
            "step_2": "Use /export-and-upload with document_id to export and upload"
        },
        "supported_formats": ["png", "jpg", "pdf", "svg"]
    }


@router.get("/status")
async def get_mcp_status():
    """
    Get the status of the Lucid MCP integration
    """
    return {
        "lucid_api_configured": lucid_service is not None,
        "mcp_server_available": True,
        "supported_tools": [
            "list_lucid_diagrams",
            "search_lucid_diagrams"
        ],
        "features": [
            "API search",
            "Client-side search",
            "Typo-tolerant search",
            "Automatic fallback"
        ],
        "message": (
            "Lucid MCP integration is ready" if lucid_service
            else "Lucid API key not configured"
        )
    } 