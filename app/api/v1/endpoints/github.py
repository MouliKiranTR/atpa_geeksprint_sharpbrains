"""
GitHub API endpoints for repository and code search
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

from app.services.github_service import github_service

router = APIRouter()


class GitHubSearchRequest(BaseModel):
    """Request model for GitHub search"""
    query: str
    limit: int = 10
    language: Optional[str] = None
    sort: str = "best-match"


class GitHubCodeSearchRequest(BaseModel):
    """Request model for GitHub code search"""
    query: str
    repo: Optional[str] = None
    language: Optional[str] = None
    limit: int = 10


class GitHubIssueSearchRequest(BaseModel):
    """Request model for GitHub issue search"""
    query: str
    repo: Optional[str] = None
    state: str = "open"
    limit: int = 10


class GitHubAuthRequest(BaseModel):
    """Request model for GitHub authentication"""
    token: str


@router.get("/repositories/search")
async def search_repositories(
        query: str = Query(..., description="Search query for repositories"),
        limit: int = Query(10, description="Maximum number of results"),
        language: Optional[str] = Query(None, description="Programming language filter"),
        sort: str = Query("best-match", description="Sort order")
) -> Dict[str, Any]:
    """
    Search GitHub repositories

    Args:
        query: Search query
        limit: Maximum number of results (default: 10)
        language: Programming language filter (optional)
        sort: Sort order (best-match, stars, updated)

    Returns:
        Repository search results
    """
    try:
        result = await github_service.search_repositories(
            query=query,
            limit=limit,
            language=language,
            sort=sort
        )

        return {
            "success": True,
            "data": {
                "repositories": [
                    {
                        "full_name": repo.full_name,
                        "name": repo.name,
                        "description": repo.description,
                        "url": repo.url,
                        "language": repo.language,
                        "stars": repo.stars,
                        "updated_at": repo.updated_at,
                        "owner": repo.owner
                    }
                    for repo in result.repositories
                ],
                "total_count": result.total_count,
                "has_more": result.has_more,
                "search_query": result.search_query
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub search failed: {str(e)}")


@router.post("/repositories/search")
async def search_repositories_post(request: GitHubSearchRequest) -> Dict[str, Any]:
    """
    Search GitHub repositories (POST method)

    Args:
        request: GitHub search request

    Returns:
        Repository search results
    """
    try:
        result = await github_service.search_repositories(
            query=request.query,
            limit=request.limit,
            language=request.language,
            sort=request.sort
        )

        return {
            "success": True,
            "data": {
                "repositories": [
                    {
                        "full_name": repo.full_name,
                        "name": repo.name,
                        "description": repo.description,
                        "url": repo.url,
                        "language": repo.language,
                        "stars": repo.stars,
                        "updated_at": repo.updated_at,
                        "owner": repo.owner
                    }
                    for repo in result.repositories
                ],
                "total_count": result.total_count,
                "has_more": result.has_more,
                "search_query": result.search_query
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub search failed: {str(e)}")


@router.get("/code/search")
async def search_code(
        query: str = Query(..., description="Code search query"),
        repo: Optional[str] = Query(None, description="Specific repository to search"),
        language: Optional[str] = Query(None, description="Programming language filter"),
        limit: int = Query(10, description="Maximum number of results")
) -> Dict[str, Any]:
    """
    Search code in GitHub repositories

    Args:
        query: Code search query
        repo: Specific repository to search (optional)
        language: Programming language filter (optional)
        limit: Maximum number of results (default: 10)

    Returns:
        Code search results
    """
    try:
        result = await github_service.search_code(
            query=query,
            repo=repo,
            language=language,
            limit=limit
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub code search failed: {str(e)}")


@router.post("/code/search")
async def search_code_post(request: GitHubCodeSearchRequest) -> Dict[str, Any]:
    """
    Search code in GitHub repositories (POST method)

    Args:
        request: GitHub code search request

    Returns:
        Code search results
    """
    try:
        result = await github_service.search_code(
            query=request.query,
            repo=request.repo,
            language=request.language,
            limit=request.limit
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub code search failed: {str(e)}")


@router.get("/repositories/{owner}/{repo}")
async def get_repository_info(owner: str, repo: str) -> Dict[str, Any]:
    """
    Get detailed repository information

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        Repository information
    """
    try:
        repo_name = f"{owner}/{repo}"
        result = await github_service.get_repository_info(repo_name)

        if result.get("error"):
            raise HTTPException(status_code=404, detail=result["error"])

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get repository info: {str(e)}")


@router.get("/issues/search")
async def search_issues(
        query: str = Query(..., description="Issue search query"),
        repo: Optional[str] = Query(None, description="Specific repository to search"),
        state: str = Query("open", description="Issue state (open, closed, all)"),
        limit: int = Query(10, description="Maximum number of results")
) -> Dict[str, Any]:
    """
    Search GitHub issues

    Args:
        query: Issue search query
        repo: Specific repository to search (optional)
        state: Issue state (open, closed, all)
        limit: Maximum number of results (default: 10)

    Returns:
        Issue search results
    """
    try:
        result = await github_service.search_issues(
            query=query,
            repo=repo,
            state=state,
            limit=limit
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub issue search failed: {str(e)}")


@router.post("/issues/search")
async def search_issues_post(request: GitHubIssueSearchRequest) -> Dict[str, Any]:
    """
    Search GitHub issues (POST method)

    Args:
        request: GitHub issue search request

    Returns:
        Issue search results
    """
    try:
        result = await github_service.search_issues(
            query=request.query,
            repo=request.repo,
            state=request.state,
            limit=request.limit
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub issue search failed: {str(e)}")

@router.get("/health")
async def github_health_check() -> Dict[str, Any]:
    """
    Check if GitHub API is available and authenticated

    Returns:
        GitHub API status
    """
    try:
        print("=== GitHub Health Check Called ===")
        is_available = await github_service._check_github_api()
        print(f"=== Authentication result: {is_available} ===")
        
        return {
            "success": True,
            "github_api_available": is_available,
            "status": "authenticated" if is_available else "not available or not authenticated"
        }
        
    except Exception as e:
        return {
            "success": False,
            "github_api_available": False,
            "status": f"error: {str(e)}"
        }


@router.post("/auth/token")
async def authenticate_with_token(request: GitHubAuthRequest) -> Dict[str, Any]:
    """
    Authenticate GitHub API with a personal access token

    Args:
        request: GitHub authentication request with token
        
    Returns:
        Authentication status
    """
    try:
        success = await github_service.set_github_token(request.token)
        
        return {
            "success": success,
            "message": "GitHub token authenticated successfully" if success else "GitHub token authentication failed",
            "github_api_available": success
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Authentication error: {str(e)}",
            "github_api_available": False
        }
