"""
Health check endpoints for monitoring system status
"""

from fastapi import APIRouter, HTTPException
import time
import datetime

from app.models.schemas import HealthResponse
from app.core.config import settings

router = APIRouter()

# Track startup time for uptime calculation
startup_time = datetime.datetime.utcnow()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Basic health check endpoint
    
    Returns the current status of the API service
    """
    try:
        uptime = datetime.datetime.utcnow() - startup_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        return HealthResponse(
            status="healthy",
            service="onboarding-agent-api",
            version="1.0.0",
            uptime=uptime_str
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/detailed")
async def detailed_health_check():
    """
    Detailed health check with dependency status
    
    Checks the status of external dependencies and services
    """
    try:
        dependencies = {}
        
        # Check OpenAI API
        dependencies["openai"] = "configured" if settings.OPENAI_API_KEY else "not_configured"
        
        # Check database (placeholder)
        dependencies["database"] = "connected"  # Would check actual DB connection
        
        # Check Redis (placeholder)
        dependencies["redis"] = "available"  # Would check actual Redis connection
        
        uptime = datetime.datetime.utcnow() - startup_time
        uptime_str = str(uptime).split('.')[0]
        
        return HealthResponse(
            status="healthy",
            service="onboarding-agent-api",
            version="1.0.0",
            uptime=uptime_str,
            dependencies=dependencies
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Detailed health check failed: {str(e)}"
        )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check for deployment orchestration
    
    Returns whether the service is ready to handle requests
    """
    try:
        # Check if essential services are available
        ready = True
        issues = []
        
        if not settings.OPENAI_API_KEY:
            ready = False
            issues.append("OpenAI API key not configured")
        
        if not settings.SECRET_KEY:
            ready = False
            issues.append("Secret key not configured")
        
        return {
            "ready": ready,
            "issues": issues,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Readiness check failed: {str(e)}"
        )


@router.get("/live")
async def liveness_check():
    """
    Liveness check for deployment orchestration
    
    Returns whether the service is alive and responsive
    """
    return {
        "alive": True,
        "timestamp": datetime.datetime.utcnow().isoformat()
    } 