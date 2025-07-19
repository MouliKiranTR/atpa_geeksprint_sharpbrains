"""
Lucid MCP endpoints for accessing Lucid diagrams via MCP tools
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.schemas import (
    MCPListDiagramsRequest,
    MCPListDiagramsResponse
)
from app.services.lucid_service import lucid_service

router = APIRouter()


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