"""
Program generation endpoints using OpenArena API
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ProgramGenerationRequest,
    ProgramGenerationResponse
)
from app.services.open_area_service import generate_program

router = APIRouter()


@router.post("/generate", response_model=ProgramGenerationResponse)
async def generate_program_endpoint(request: ProgramGenerationRequest):
    """
    Generate a program based on user input using OpenArena API
    
    This endpoint:
    1. Takes user input describing the desired program
    2. Calls OpenArena API to generate the program
    3. Returns the generated code with cost information
    """
    try:
        # Call the generate_program function from the service
        result = generate_program(request.user_input)
        
        if result["status"] == "error":
            raise HTTPException(
                status_code=500,
                detail=(f"Error generating program: "
                        f"{result.get('error', 'Unknown error')}")
            )
        
        return ProgramGenerationResponse(
            program=result["program"],
            cost=result["cost"],
            status=result["status"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating program: {str(e)}"
        ) 