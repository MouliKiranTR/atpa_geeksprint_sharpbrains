"""
API endpoint for Lucid architecture diagram analysis
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from app.services.enhanced_openarena_service import enhanced_openarena_service
from app.services.lucid_service import lucid_service
from pydantic import BaseModel

router = APIRouter()


class LucidArchitectureRequest(BaseModel):
    user_question: str
    diagram_ids: List[str]
    reasoning_focus: Optional[str] = "comprehensive"
    include_screenshots: Optional[bool] = True


class LucidArchitectureResponse(BaseModel):
    success: bool
    analysis: Optional[str] = None
    cost: Optional[str] = None
    reasoning_focus: Optional[str] = None
    diagrams_processed: Optional[int] = None
    diagrams_attached: Optional[int] = None
    error: Optional[str] = None


@router.post("/analyze", response_model=LucidArchitectureResponse)
async def analyze_lucid_architecture_diagrams(request: LucidArchitectureRequest):
    """
    Analyze Lucid architecture diagrams with specialized reasoning
    
    This endpoint:
    1. Fetches Lucid diagrams by their IDs
    2. Uses the architecture-specific analysis prompt
    3. Provides structured reasoning about the architecture
    4. Returns actionable insights and recommendations
    
    Args:
        request: Contains user question, diagram IDs, and analysis options
        
    Returns:
        Structured architecture analysis with reasoning
    """
    
    try:
        # Validate reasoning focus
        valid_focuses = ["comprehensive", "technical", "business", "security"]
        if request.reasoning_focus not in valid_focuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid reasoning_focus. Must be one of: {valid_focuses}"
            )
        
        # Fetch Lucid diagrams
        print(f"📐 Fetching {len(request.diagram_ids)} Lucid diagrams...")
        
        visual_data = []
        for diagram_id in request.diagram_ids:
            try:
                # Fetch diagram from Lucid
                diagram_result = await lucid_service.export_diagram(
                    diagram_id=diagram_id,
                    format="PNG",
                    scale="100%"
                )
                
                if diagram_result.get("success"):
                    visual_data.append({
                        "success": True,
                        "source": "lucid",
                        "diagram_title": diagram_result.get("diagram_title", "Unknown"),
                        "diagram_id": diagram_id,
                        "file_path": diagram_result.get("file_path"),
                        "screenshot_base64": diagram_result.get("screenshot_base64"),
                        "capture_method": "lucid_export",
                        "metadata": {
                            "export_id": diagram_result.get("export_id"),
                            "format": "PNG",
                            "scale": "100%",
                            "diagram_type": "architecture",
                            "export_timestamp": diagram_result.get("timestamp")
                        }
                    })
                    print(f"✅ Successfully fetched: {diagram_result.get('diagram_title')}")
                else:
                    # Add failed diagram info
                    visual_data.append({
                        "success": False,
                        "source": "lucid",
                        "diagram_id": diagram_id,
                        "error": diagram_result.get("error", "Failed to fetch diagram")
                    })
                    print(f"❌ Failed to fetch diagram {diagram_id}: {diagram_result.get('error')}")
                    
            except Exception as e:
                print(f"❌ Error fetching diagram {diagram_id}: {e}")
                visual_data.append({
                    "success": False,
                    "source": "lucid", 
                    "diagram_id": diagram_id,
                    "error": str(e)
                })
        
        # Check if we have any successful diagrams
        successful_diagrams = [d for d in visual_data if d.get("success")]
        if not successful_diagrams:
            return LucidArchitectureResponse(
                success=False,
                error="No diagrams could be fetched successfully"
            )
        
        print(f"📊 Analyzing {len(successful_diagrams)} diagrams with {request.reasoning_focus} focus...")
        
        # Perform architecture analysis
        analysis_result = await enhanced_openarena_service.analyze_architecture_diagrams(
            user_question=request.user_question,
            visual_data=visual_data,
            reasoning_focus=request.reasoning_focus,
            include_screenshots=request.include_screenshots
        )
        
        if analysis_result["success"]:
            return LucidArchitectureResponse(
                success=True,
                analysis=analysis_result["analysis"],
                cost=analysis_result.get("cost"),
                reasoning_focus=analysis_result["reasoning_focus"],
                diagrams_processed=analysis_result["diagrams_processed"],
                diagrams_attached=analysis_result["diagrams_attached"]
            )
        else:
            return LucidArchitectureResponse(
                success=False,
                error=analysis_result.get("error", "Analysis failed")
            )
            
    except Exception as e:
        print(f"🚨 Lucid architecture analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-metadata-only")
async def analyze_lucid_metadata_only(request: LucidArchitectureRequest):
    """
    Analyze Lucid diagrams using only metadata (no image downloads)
    
    Useful for:
    - Quick architectural insights
    - High-level system understanding
    - Recommendations for additional documentation
    """
    
    try:
        print(f"📊 Analyzing {len(request.diagram_ids)} diagrams (metadata only)...")
        
        visual_data = []
        for diagram_id in request.diagram_ids:
            try:
                # Get diagram metadata only
                metadata_result = await lucid_service.get_diagram_metadata(diagram_id)
                
                if metadata_result.get("success"):
                    visual_data.append({
                        "success": True,
                        "source": "lucid",
                        "diagram_title": metadata_result.get("title", "Unknown"),
                        "diagram_id": diagram_id,
                        "capture_method": "metadata_only",
                        "metadata": {
                            "created_date": metadata_result.get("created_date"),
                            "last_modified": metadata_result.get("last_modified"),
                            "description": metadata_result.get("description"),
                            "page_count": metadata_result.get("page_count"),
                            "complexity_level": metadata_result.get("complexity_level")
                        }
                    })
                else:
                    visual_data.append({
                        "success": False,
                        "source": "lucid",
                        "diagram_id": diagram_id,
                        "error": metadata_result.get("error", "Failed to fetch metadata")
                    })
                    
            except Exception as e:
                visual_data.append({
                    "success": False,
                    "source": "lucid",
                    "diagram_id": diagram_id, 
                    "error": str(e)
                })
        
        # Perform metadata-only analysis
        analysis_result = await enhanced_openarena_service.analyze_architecture_diagrams(
            user_question=request.user_question,
            visual_data=visual_data,
            reasoning_focus=request.reasoning_focus,
            include_screenshots=False  # No screenshots for metadata-only
        )
        
        if analysis_result["success"]:
            return LucidArchitectureResponse(
                success=True,
                analysis=analysis_result["analysis"],
                cost=analysis_result.get("cost"),
                reasoning_focus=analysis_result["reasoning_focus"],
                diagrams_processed=analysis_result["diagrams_processed"],
                diagrams_attached=0  # No attachments for metadata-only
            )
        else:
            return LucidArchitectureResponse(
                success=False,
                error=analysis_result.get("error", "Metadata analysis failed")
            )
            
    except Exception as e:
        print(f"🚨 Lucid metadata analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reasoning-focuses")
async def get_available_reasoning_focuses():
    """
    Get available reasoning focus options for architecture analysis
    """
    return {
        "reasoning_focuses": [
            {
                "name": "comprehensive",
                "description": "Full analysis covering all architectural aspects",
                "use_cases": [
                    "Complete system understanding",
                    "Onboarding new team members", 
                    "Architecture reviews"
                ]
            },
            {
                "name": "technical", 
                "description": "Deep technical implementation focus",
                "use_cases": [
                    "Technology stack evaluation",
                    "Performance optimization",
                    "Technical debt assessment"
                ]
            },
            {
                "name": "business",
                "description": "Business value and operational perspective", 
                "use_cases": [
                    "Business capability mapping",
                    "ROI analysis",
                    "Process optimization"
                ]
            },
            {
                "name": "security",
                "description": "Security architecture and compliance focus",
                "use_cases": [
                    "Security assessments",
                    "Compliance reviews",
                    "Threat modeling"
                ]
            }
        ]
    } 