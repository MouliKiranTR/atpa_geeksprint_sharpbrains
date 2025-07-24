"""
Cache Management endpoints for Lucid diagram caching
"""

from fastapi import APIRouter, HTTPException

from app.services.cache_service import cache_service

router = APIRouter()


@router.get("/stats")
async def get_cache_stats():
    """
    Get cache statistics including size, file count, and configuration
    """
    try:
        stats = await cache_service.get_cache_stats()
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting cache stats: {str(e)}"
        )


@router.get("/list")
async def list_cached_documents():
    """
    List all cached documents with metadata
    """
    try:
        cached_docs = await cache_service.list_cached_documents()
        return {
            "success": True,
            "cached_documents": cached_docs,
            "count": len(cached_docs)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing cached documents: {str(e)}"
        )


@router.post("/cleanup")
async def cleanup_expired_cache():
    """
    Clean up expired cache entries
    """
    try:
        result = await cache_service.cleanup_expired_cache()
        return {
            "success": True,
            "cleanup_result": result,
            "message": f"Cleaned {result['cleaned']} expired entries"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error cleaning up cache: {str(e)}"
        )


@router.get("/check/{document_id}")
async def check_cached_document(
    document_id: str,
    format: str = "png",
    page_id: str = None,
    width: int = None,
    height: int = None
):
    """
    Check if a specific document is cached
    """
    try:
        cached_result = await cache_service.get_cached_export(
            document_id, format, page_id, width, height
        )
        
        if cached_result:
            return {
                "success": True,
                "cached": True,
                "cache_info": {
                    "cache_key": cached_result.get("cache_key"),
                    "file_path": cached_result.get("file_path"),
                    "metadata": cached_result.get("metadata", {})
                }
            }
        else:
            return {
                "success": True,
                "cached": False,
                "message": "Document not found in cache or expired"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking cache for document: {str(e)}"
        ) 