"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    query, upload, health, program_generation, 
    lucid_mcp, figma_mcp, enhanced_query
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    query.router, 
    prefix="/query", 
    tags=["query"]
)
api_router.include_router(
    upload.router, 
    prefix="/upload", 
    tags=["upload"]
)
api_router.include_router(
    health.router, 
    prefix="/health", 
    tags=["health"]
) 
api_router.include_router(
    program_generation.router,
    prefix="/program",
    tags=["program-generation"]
)
api_router.include_router(
    lucid_mcp.router,
    prefix="/lucid-mcp",
    tags=["lucid-mcp"]
)
api_router.include_router(
    figma_mcp.router,
    prefix="/figma-mcp",
    tags=["figma-mcp"]
)
api_router.include_router(
    enhanced_query.router,
    prefix="/enhanced-query",
    tags=["enhanced-query"]
) 