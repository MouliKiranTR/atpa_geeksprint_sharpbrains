"""
Enhanced query endpoints for visual content analysis
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time

from app.services.enhanced_query_service import enhanced_query_service

router = APIRouter()


class EnhancedQueryRequest(BaseModel):
    """Request model for enhanced query with visual analysis"""
    question: str = Field(..., description="User's question")
    include_figma: bool = Field(
        default=True, 
        description="Whether to search Figma files"
    )
    include_lucid: bool = Field(
        default=True, 
        description="Whether to search Lucid diagrams"
    )
    include_documents: bool = Field(
        default=True, 
        description="Whether to search uploaded documents"
    )
    max_visual_items: int = Field(
        default=3, 
        description="Maximum visual items to process",
        ge=1,
        le=10
    )


class EnhancedQueryResponse(BaseModel):
    """Response model for enhanced query"""
    success: bool = Field(..., description="Whether the query was successful")
    is_visual_query: bool = Field(
        ..., 
        description="Whether the query was detected as visual-related"
    )
    answer: str = Field(..., description="Comprehensive formatted answer")
    analysis_type: str = Field(..., description="Type of analysis performed")
    search_summary: dict = Field(..., description="Summary of search results")
    visual_analysis_available: bool = Field(
        ..., 
        description="Whether visual analysis was performed"
    )
    processing_time: float = Field(..., description="Processing time in seconds")
    cost: Optional[float] = Field(
        None, description="Analysis cost if available"
    )
    error: Optional[str] = Field(None, description="Error message if any")


@router.post("/enhanced-ask", response_model=EnhancedQueryResponse)
async def enhanced_ask_question(request: EnhancedQueryRequest):
    """
    Enhanced question answering with visual content analysis
    
    This endpoint:
    1. Analyzes the user's question to determine if it's visual-related
    2. Searches Figma files and Lucid diagrams based on the query
    3. Captures screenshots of relevant visual content
    4. Uses OpenArena AI to analyze visual content with context
    5. Combines document search with visual analysis
    6. Returns a comprehensive, well-formatted response
    
    Features:
    - Automatic detection of visual queries
    - Parallel search across multiple sources
    - Screenshot capture and visual analysis
    - Intelligent analysis type determination
    - Structured response formatting
    """
    start_time = time.time()
    
    try:
        # Perform enhanced query analysis
        results = await enhanced_query_service.analyze_user_query(
            user_question=request.question,
            include_figma=request.include_figma,
            include_lucid=request.include_lucid,
            include_documents=request.include_documents,
            max_visual_items=request.max_visual_items
        )
        
        # Check for errors
        if results.get("error"):
            raise HTTPException(
                status_code=500,
                detail=f"Query analysis failed: {results.get('error')}"
            )
        
        # Extract information for response
        query_analysis = results.get("query_analysis", {})
        search_results = results.get("search_results", {})
        visual_analysis = results.get("visual_analysis", {})
        
        # Create search summary
        search_summary = {
            "figma_files_found": len(search_results.get("figma_files", [])),
            "lucid_diagrams_found": len(
                search_results.get("lucid_diagrams", [])
            ),
            "documents_found": len(search_results.get("documents", [])),
            "total_sources_searched": sum([
                1 if request.include_figma else 0,
                1 if request.include_lucid else 0,
                1 if request.include_documents else 0
            ])
        }
        
        # Extract cost if available
        cost = None
        if visual_analysis and visual_analysis.get("cost"):
            cost = float(visual_analysis.get("cost", 0))
        
        return EnhancedQueryResponse(
            success=True,
            is_visual_query=results.get("is_visual_query", False),
            answer=results.get("combined_response", "No response generated"),
            analysis_type=query_analysis.get("analysis_type", "general"),
            search_summary=search_summary,
            visual_analysis_available=bool(
                visual_analysis and visual_analysis.get("success")
            ),
            processing_time=time.time() - start_time,
            cost=cost
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhanced query: {str(e)}"
        )


@router.get("/analysis-types")
async def get_analysis_types():
    """
    Get available analysis types for visual content
    
    Returns the different types of analysis that can be performed
    on visual content, along with their descriptions.
    """
    return {
        "analysis_types": [
            {
                "type": "design",
                "name": "Design Analysis",
                "description": (
                    "Focuses on UI/UX, visual hierarchy, typography, "
                    "colors, and design patterns"
                ),
                "keywords": [
                    "design", "ui", "ux", "interface", "layout", 
                    "color", "typography"
                ]
            },
            {
                "type": "workflow", 
                "name": "Workflow Analysis",
                "description": (
                    "Analyzes process flows, decision points, "
                    "and user journeys"
                ),
                "keywords": [
                    "workflow", "process", "flow", "step", 
                    "procedure", "journey"
                ]
            },
            {
                "type": "integration",
                "name": "Integration Analysis", 
                "description": (
                    "Examines data flows, system connections, "
                    "and technical architecture"
                ),
                "keywords": [
                    "integration", "connect", "api", "data flow", 
                    "system", "architecture"
                ]
            },
            {
                "type": "general",
                "name": "General Analysis",
                "description": (
                    "Comprehensive overview and analysis of visual content"
                ),
                "keywords": [
                    "overview", "general", "explain", "describe", "analyze"
                ]
            }
        ]
    }


@router.get("/visual-keywords")
async def get_visual_keywords():
    """
    Get keywords that trigger visual content analysis
    
    Returns the list of keywords that the system uses to determine
    if a query should include visual content analysis.
    """
    return {
        "visual_keywords": [
            "figma", "lucid", "design", "diagram", "workflow", "process",
            "visual", "interface", "ui", "ux", "chart", "flow", "mockup",
            "wireframe", "prototype", "layout", "screen", "page",
            "architecture", "system", "structure", "blueprint", "schema",
            "checkpoint", "flowchart", "map", "model", "framework",
            "dashboard", "visualization", "graphic", "drawing", "sketch"
        ],
        "description": (
            "If a user query contains any of these keywords, the system "
            "will automatically search and analyze visual content from "
            "Figma and Lucid sources."
        )
    }


@router.post("/analyze-specific")
async def analyze_specific_visual_content(
    file_type: str,  # "figma" or "lucid"
    file_id: str,
    question: str,
    analysis_type: str = "general"
):
    """
    Analyze specific visual content by ID
    
    This endpoint allows direct analysis of a specific Figma file
    or Lucid diagram by providing its ID directly.
    
    Args:
        file_type: Type of file ("figma" or "lucid")
        file_id: ID/key of the file to analyze
        question: Question about the visual content
        analysis_type: Type of analysis to perform
    """
    try:
        if file_type not in ["figma", "lucid"]:
            raise HTTPException(
                status_code=400,
                detail="file_type must be either 'figma' or 'lucid'"
            )
        
        # Import services
        from app.services.visual_capture_service import visual_capture_service
        from app.services.enhanced_openarena_service import (
            enhanced_openarena_service
        )
        
        # Capture screenshot
        if file_type == "figma":
            visual_data = [
                await visual_capture_service.capture_figma_file_screenshot(
                    file_id, f"Figma File {file_id}"
                )
            ]
        else:  # lucid
            visual_data = [
                await visual_capture_service.capture_lucid_diagram_screenshot(
                    file_id, f"Lucid Diagram {file_id}"
                )
            ]
        
        # Analyze with OpenArena
        analysis_result = await enhanced_openarena_service.analyze_visual_content(
            user_question=question,
            visual_data=visual_data,
            analysis_type=analysis_type,
            include_screenshots=True
        )
        
        if not analysis_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {analysis_result.get('error', 'Unknown error')}"
            )
        
        return {
            "success": True,
            "file_type": file_type,
            "file_id": file_id,
            "analysis_type": analysis_type,
            "analysis": analysis_result.get("analysis", ""),
            "cost": analysis_result.get("cost"),
            "visual_data_captured": len([
                item for item in visual_data if item.get("success")
            ])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing specific content: {str(e)}"
        ) 