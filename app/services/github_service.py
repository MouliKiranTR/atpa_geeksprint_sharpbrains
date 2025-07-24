"""
GitHub Service for repository and code search using GitHub REST API
"""

import asyncio
import json
import os
import httpx
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class GitHubRepository:
    """GitHub repository data structure"""
    full_name: str
    name: str
    description: str
    url: str
    language: str
    stars: int
    updated_at: str
    owner: str


@dataclass
class GitHubSearchResult:
    """GitHub search result data structure"""
    repositories: List[GitHubRepository]
    total_count: int
    has_more: bool
    search_query: str


class GitHubService:
    """GitHub service for repository and code search using REST API"""

    def __init__(self):
        """Initialize GitHub service"""
        print("=== GitHubService initialized ===")
        self._gh_available = None
        self._github_token = os.getenv("GITHUB_TOKEN")
        print(f"Token configured: {bool(self._github_token)}")
    
    async def _check_github_api(self) -> bool:
        """Check if GitHub API is accessible with token"""
        if self._gh_available is not None:
            return self._gh_available
        
        if not self._github_token:
            print("No GitHub token available")
            self._gh_available = False
            return False
        
        try:
            print(f"Testing GitHub authentication with token: {self._github_token[:20]}...")
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"token {self._github_token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "FastAPI-GitHub-Service"
                }
                
                print(f"Making request to GitHub API...")
                response = await client.get("https://api.github.com/user", headers=headers)
                print(f"GitHub auth response status: {response.status_code}")
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"GitHub API authenticated successfully as: {user_data.get('login', 'Unknown')}")
                    self._gh_available = True
                    return True
                else:
                    error_text = response.text
                    print(f"GitHub API authentication failed: {response.status_code}")
                    print(f"Error response: {error_text}")
                    try:
                        error_json = response.json()
                        print(f"Error details: {error_json}")
                    except:
                        pass
                    self._gh_available = False
                    return False
                        
        except Exception as e:
            print(f"GitHub API check failed: {str(e)}")
            self._gh_available = False
            return False
    
    async def set_github_token(self, token: str) -> bool:
        """Set GitHub token and test authentication"""
        self._github_token = token
        self._gh_available = None  # Reset cache
        return await self._check_github_api()

    async def search_repositories(
            self,
            query: str,
            limit: int = 10,
            language: Optional[str] = None,
            sort: str = "best-match"
    ) -> GitHubSearchResult:
        """
        Search GitHub repositories using REST API
        
        Args:
            query: Search query
            limit: Maximum number of results
            language: Programming language filter
            sort: Sort order (best-match, stars, updated)
            
        Returns:
            GitHubSearchResult with repository data
        """
        try:
            # Check if GitHub API is available
            if not await self._check_github_api():
                raise Exception("GitHub API is not available or not authenticated")
            
            # Build search query
            search_terms = [query]
            if language:
                search_terms.append(f"language:{language}")

            search_query = " ".join(search_terms)
            
            # Map sort parameter
            sort_param = "updated" if sort == "best-match" else sort
            
            # GitHub REST API search
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"token {self._github_token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "FastAPI-GitHub-Service"
                }
                
                params = {
                    "q": search_query,
                    "sort": sort_param,
                    "per_page": min(limit, 100)  # GitHub API max is 100
                }
                
                url = "https://api.github.com/search/repositories"
                response = await client.get(url, headers=headers, params=params)
                print(f"GitHub API request: {url} with params: {params}")
                print(f"GitHub API response status: {response.status_code}")
                
                if response.status_code != 200:
                    error_text = response.text
                    print(f"GitHub API search failed: {response.status_code} - {error_text}")
                    raise Exception(f"GitHub API error: {response.status_code} - {error_text}")
                
                data = response.json()
                print(f"GitHub API response: {json.dumps(data, indent=2)[:1000]}...")
                
                repositories = []
                for repo in data.get("items", []):
                    repositories.append(GitHubRepository(
                        full_name=repo.get("full_name", ""),
                        name=repo.get("name", ""),
                        description=repo.get("description", "") or "",
                        url=repo.get("html_url", ""),
                        language=repo.get("language", "") or "",
                        stars=repo.get("stargazers_count", 0),
                        updated_at=repo.get("updated_at", ""),
                        owner=repo.get("owner", {}).get("login", "") if repo.get("owner") else ""
                    ))

                return GitHubSearchResult(
                    repositories=repositories,
                    total_count=data.get("total_count", 0),
                    has_more=len(repositories) >= limit,
                    search_query=query
                )

        except Exception as e:
            # Log the actual error for debugging
            print(f"GitHub search error: {str(e)}")
            return GitHubSearchResult(
                repositories=[],
                total_count=0,
                has_more=False,
                search_query=query
            )

    async def search_code(
            self,
            query: str,
            repo: Optional[str] = None,
            language: Optional[str] = None,
            limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search code in GitHub repositories using REST API
        
        Args:
            query: Code search query
            repo: Specific repository to search in
            language: Programming language filter
            limit: Maximum number of results
            
        Returns:
            Dictionary with search results
        """
        try:
            # Check if GitHub API is available
            if not await self._check_github_api():
                raise Exception("GitHub API is not available or not authenticated")
            
            # Build search query
            search_terms = [query]
            if repo:
                search_terms.append(f"repo:{repo}")
            if language:
                search_terms.append(f"language:{language}")

            search_query = " ".join(search_terms)

            # GitHub REST API code search
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"token {self._github_token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "FastAPI-GitHub-Service"
                }
                
                params = {
                    "q": search_query,
                    "per_page": min(limit, 100)
                }
                
                url = "https://api.github.com/search/code"
                response = await client.get(url, headers=headers, params=params)
                if response.status_code != 200:
                    error_text = response.text
                    raise Exception(f"GitHub API error: {response.status_code} - {error_text}")
                
                data = response.json()
                
                return {
                    "code_results": data.get("items", []),
                    "total_count": data.get("total_count", 0),
                    "search_query": query
                }

        except Exception as e:
            # Log the actual error for debugging
            print(f"GitHub code search error: {str(e)}")
            return {
                "code_results": [],
                "total_count": 0,
                "search_query": query,
                "error": str(e)
            }

    async def get_repository_info(self, repo_name: str) -> Dict[str, Any]:
        """
        Get detailed repository information using REST API
        
        Args:
            repo_name: Repository name (owner/repo)
            
        Returns:
            Repository information dictionary
        """
        try:
            # Check if GitHub API is available
            if not await self._check_github_api():
                raise Exception("GitHub API is not available or not authenticated")
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"token {self._github_token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "FastAPI-GitHub-Service"
                }
                
                url = f"https://api.github.com/repos/{repo_name}"
                response = await client.get(url, headers=headers)
                if response.status_code != 200:
                    error_text = response.text
                    raise Exception(f"GitHub API error: {response.status_code} - {error_text}")
                
                return response.json()

        except Exception as e:
            # Log the actual error for debugging
            print(f"GitHub repo info error: {str(e)}")
            return {"error": str(e)}

    async def search_issues(
            self,
            query: str,
            repo: Optional[str] = None,
            state: str = "open",
            limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search GitHub issues using REST API
        
        Args:
            query: Issue search query
            repo: Specific repository to search in
            state: Issue state (open, closed, all)
            limit: Maximum number of results
            
        Returns:
            Dictionary with issue search results
        """
        try:
            # Check if GitHub API is available
            if not await self._check_github_api():
                raise Exception("GitHub API is not available or not authenticated")
            
            # Build search query
            search_terms = [query]
            if repo:
                search_terms.append(f"repo:{repo}")
            if state != "all":
                search_terms.append(f"state:{state}")

            search_query = " ".join(search_terms)

            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"token {self._github_token}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "FastAPI-GitHub-Service"
                }
                
                params = {
                    "q": search_query,
                    "per_page": min(limit, 100)
                }
                
                url = "https://api.github.com/search/issues"
                response = await client.get(url, headers=headers, params=params)
                if response.status_code != 200:
                    error_text = response.text
                    raise Exception(f"GitHub API error: {response.status_code} - {error_text}")
                
                data = response.json()
                
                return {
                    "issues": data.get("items", []),
                    "total_count": data.get("total_count", 0),
                    "search_query": query
                }

        except Exception as e:
            # Log the actual error for debugging
            print(f"GitHub issues search error: {str(e)}")
            return {
                "issues": [],
                "total_count": 0,
                "search_query": query,
                "error": str(e)
            }


# Create service instance
github_service = GitHubService()