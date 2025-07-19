"""
Figma MCP endpoints for accessing Figma files via MCP tools
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from app.models.schemas import (
    MCPListFilesRequest,
    MCPListFilesResponse
)
from app.services.figma_service import figma_service

router = APIRouter()


@router.post("/list-files", response_model=MCPListFilesResponse)
async def list_figma_files(request: MCPListFilesRequest):
    """
    List Figma files using the configured personal access token
    
    This endpoint provides the same functionality as the MCP server's 
    list_figma_files tool but via a REST API endpoint.
    """
    if not figma_service:
        raise HTTPException(
            status_code=500,
            detail="Figma API token is not configured. Please set FIGMA_API_TOKEN."
        )
    
    try:
        if request.team_id:
            # Get files from specific team
            response = await figma_service.get_team_projects(
                team_id=request.team_id,
                limit=request.limit,
                offset=request.offset,
                search_query=request.search_query
            )
        else:
            # Get user's files
            response = await figma_service.get_user_files(
                limit=request.limit,
                offset=request.offset,
                search_query=request.search_query
            )
        
        message = f"Found {len(response.files)} Figma files"
        if request.search_query:
            message += f" matching '{request.search_query}'"
        if request.team_id:
            message += f" in team {request.team_id}"
        
        return MCPListFilesResponse(
            files=response.files,
            total_count=response.total_count,
            has_more=response.has_more,
            message=message
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Figma API Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error accessing Figma API: {str(e)}"
        )


@router.get("/search/{query}")
async def search_figma_files(
    query: str,
    limit: Optional[int] = 20,
    team_id: Optional[str] = None
):
    """
    Search Figma files by query string
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        team_id: Optional team ID to filter files from
    """
    if not figma_service:
        raise HTTPException(
            status_code=500,
            detail="Figma API token is not configured. Please set FIGMA_API_TOKEN."
        )
    
    try:
        if team_id:
            # Search files from specific team
            response = await figma_service.get_team_projects(
                team_id=team_id,
                limit=limit,
                offset=0,
                search_query=query
            )
        else:
            # Search user's files
            response = await figma_service.get_user_files(
                limit=limit,
                offset=0,
                search_query=query
            )
        
        message = f"Found {len(response.files)} files matching '{query}'"
        if team_id:
            message += f" in team {team_id}"
        
        return MCPListFilesResponse(
            files=response.files,
            total_count=response.total_count,
            has_more=response.has_more,
            message=message
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Figma API Error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching Figma files: {str(e)}"
        )


@router.get("/status")
async def get_figma_mcp_status():
    """
    Get the status of the Figma MCP integration
    """
    return {
        "figma_api_configured": figma_service is not None,
        "mcp_server_available": True,
        "supported_tools": [
            "list_figma_files",
            "search_figma_files"
        ],
        "features": [
            "User files access",
            "Team files access",
            "Client-side search",
            "File filtering"
        ],
        "message": (
            "Figma MCP integration is ready" if figma_service
            else "Figma API token not configured"
        )
    } 