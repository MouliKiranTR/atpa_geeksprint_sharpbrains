"""
Chat endpoint for conversational interface with visual content analysis
"""

import time
from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.enhanced_query_service import enhanced_query_service

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat conversation"""

    message: str = Field(..., description="User's message", example="string")
    include_wiki: bool = Field(
        default=True, description="Whether to search wiki documents", example=True
    )
    include_lucid: bool = Field(
        default=False, description="Whether to search Lucid diagrams", example=False
    )
    max_visual_items: int = Field(
        default=3, description="Maximum visual items to process", ge=1, le=10, example=3
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "string",
                "include_wiki": True,
                "include_lucid": False,
                "max_visual_items": 3,
            }
        }
    }


class ChatResponse(BaseModel):
    """Response model for chat conversation"""

    message: str = Field(..., description="Assistant's response message")
    is_visual_query: bool = Field(
        default=False, description="Whether the query was detected as visual-related"
    )
    analysis_type: str = Field(
        default="general", description="Type of analysis performed"
    )
    search_summary: Dict[str, Any] = Field(
        default_factory=dict, description="Summary of search results"
    )
    visual_analysis_available: bool = Field(
        default=False, description="Whether visual analysis was performed"
    )
    processing_time: float = Field(default=0, description="Processing time in seconds")
    cost: Optional[float] = Field(None, description="Analysis cost if available")
    success: bool = Field(True, description="Whether the request succeeded")
    error: Optional[str] = Field(None, description="Error message if any")


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    """
    Send a chat message and get AI response with visual content analysis

    This endpoint provides a conversational interface that:
    1. Analyzes user messages for visual content needs
    2. Searches across Lucid and wiki sources
    3. Provides comprehensive responses with visual analysis
    4. Tracks performance and costs

    Features:
    - Automatic visual content detection
    - Multi-source search capabilities
    - Visual analysis and screenshot capture
    - Cost tracking and performance metrics
    """
    start_time = time.time()

    try:
        # Perform enhanced query analysis with simplified parameters
        results = await enhanced_query_service.chat_query(
            user_question=request.message,
            include_lucid=request.include_lucid,
            include_wiki=request.include_wiki,
            max_visual_items=request.max_visual_items,
        )

        # Check for errors
        if results.get("error"):
            error_message = f"I encountered an error: {results.get('error')}"
            return ChatResponse(
                message=error_message,
                is_visual_query=False,
                analysis_type="error",
                search_summary={"error": True},
                visual_analysis_available=False,
                processing_time=time.time() - start_time,
                success=False,
                error=results.get("error"),
            )

        # Extract information for response
        query_analysis = results.get("query_analysis", {})
        search_results = results.get("search_results", {})
        visual_analysis = results.get("visual_analysis", {})

        # Get assistant response
        assistant_response = results.get(
            "combined_response", "I couldn't generate a response to your message."
        )

        # Create search summary
        search_summary = {
            "figma_files_found": 0,  # Always 0 since figma removed
            "lucid_diagrams_found": len(search_results.get("lucid_diagrams", [])),
            "documents_found": 0,  # Always 0 since documents removed
            "total_sources_searched": sum(
                [1 if request.include_wiki else 0, 1 if request.include_lucid else 0]
            ),
            "visual_items_processed": (
                len(visual_analysis.get("visual_data", [])) if visual_analysis else 0
            ),
        }

        # Extract cost if available
        cost = None
        if visual_analysis and visual_analysis.get("cost"):
            cost = float(visual_analysis.get("cost", 0))

        return ChatResponse(
            message=assistant_response,
            is_visual_query=results.get("is_visual_query", False),
            analysis_type=query_analysis.get("analysis_type", "general"),
            search_summary=search_summary,
            visual_analysis_available=bool(
                visual_analysis and visual_analysis.get("success")
            ),
            processing_time=time.time() - start_time,
            cost=cost,
            success=True,
        )

    except Exception as e:
        error_message = f"I'm sorry, I encountered an error: {str(e)}"

        return ChatResponse(
            message=error_message,
            is_visual_query=False,
            analysis_type="error",
            search_summary={"error": True},
            visual_analysis_available=False,
            processing_time=time.time() - start_time,
            success=False,
            error=str(e),
        )


@router.get("/health")
async def chat_health_check():
    """Health check for chat service"""
    return {"status": "healthy", "service": "chat", "timestamp": time.time()}
