"""
Figma Service for communicating with Figma REST API
"""

import httpx
from typing import Optional, Dict, List
from app.core.config import settings
from app.models.schemas import FigmaFile, FigmaFilesResponse


class FigmaService:
    """Service for interacting with Figma REST API"""
    
    def __init__(self):
        self.api_token = settings.FIGMA_API_TOKEN
        self.base_url = "https://api.figma.com/v1"
        self.is_configured = bool(self.api_token)
    
    def _ensure_configured(self):
        """Ensure the service is properly configured"""
        if not self.is_configured:
            raise ValueError("FIGMA_API_TOKEN is not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Figma API requests"""
        return {
            "X-Figma-Token": self.api_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _filter_files_by_query(
        self, 
        files: List[FigmaFile], 
        query: str
    ) -> List[FigmaFile]:
        """
        Client-side filtering of files by query string.
        Searches in title and other relevant fields.
        
        Args:
            files: List of files to filter
            query: Search query string
            
        Returns:
            Filtered list of files
        """
        if not query:
            return files
        
        query_lower = query.lower()
        filtered_files = []
        
        for file in files:
            # Search in title (primary field)
            if query_lower in file.name.lower():
                filtered_files.append(file)
                continue
            
            # Search in key
            if query_lower in file.key.lower():
                filtered_files.append(file)
                continue
                
            # Search for partial matches (for typos)
            title_words = file.name.lower().split()
            query_words = query_lower.split()
            
            # Check if any query word is similar to any title word
            for query_word in query_words:
                for title_word in title_words:
                    # Simple similarity check for common typos
                    word_match = (
                        len(query_word) >= 4 and len(title_word) >= 4 and
                        (query_word in title_word or 
                         title_word in query_word or
                         self._similar_words(query_word, title_word))
                    )
                    if word_match:
                        filtered_files.append(file)
                        break
                else:
                    continue
                break
        
        return filtered_files
    
    def _similar_words(self, word1: str, word2: str) -> bool:
        """
        Simple similarity check for common typos.
        Returns True if words are similar enough.
        """
        if abs(len(word1) - len(word2)) > 2:
            return False
        
        # Check for common character swaps or missing letters
        min_len = min(len(word1), len(word2))
        if min_len < 4:
            return False
        
        matches = 0
        for i in range(min_len):
            if i < len(word1) and i < len(word2) and word1[i] == word2[i]:
                matches += 1
        
        # If 80% of characters match, consider it similar
        return matches / min_len >= 0.8

    async def get_user_files(
        self,
        limit: Optional[int] = None,
        offset: int = 0,
        search_query: Optional[str] = None
    ) -> FigmaFilesResponse:
        """
        Get user's files using Figma's REST API
        
        Args:
            limit: Maximum number of files to return (optional)
            offset: Number of files to skip for pagination
            search_query: Filter files by search query
            
        Returns:
            FigmaFilesResponse containing files and metadata
        """
        self._ensure_configured()
        url = f"{self.base_url}/me"
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                
                # Extract files from user data
                all_files = []
                
                # Process recent files
                recent_files = data.get("recent_files", [])
                for file_data in recent_files:
                    file_obj = FigmaFile(
                        key=file_data.get("key", ""),
                        name=file_data.get("name", "Untitled"),
                        thumbnail_url=file_data.get("thumbnail_url"),
                        last_modified=file_data.get("last_modified"),
                        file_type="design"
                    )
                    all_files.append(file_obj)
                
                # Filter files if search query provided
                if search_query:
                    all_files = self._filter_files_by_query(all_files, search_query)
                
                # Apply pagination
                start_idx = offset
                if limit:
                    end_idx = offset + limit
                    paginated_files = all_files[start_idx:end_idx]
                    has_more = end_idx < len(all_files)
                else:
                    paginated_files = all_files[start_idx:]
                    has_more = False
                
                return FigmaFilesResponse(
                    files=paginated_files,
                    total_count=len(all_files),
                    has_more=has_more
                )
                
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if e.response.status_code == 401:
                    raise ValueError(
                        "Invalid Figma API token or unauthorized access"
                    )
                elif e.response.status_code == 403:
                    raise ValueError("Forbidden: Check API token permissions")
                else:
                    error_msg = (
                        f"Figma API error: {e.response.status_code} "
                        f"- {e.response.text}"
                    )
                    raise ValueError(error_msg)
            except httpx.RequestError as e:
                raise ValueError(f"Failed to connect to Figma API: {str(e)}")
            except Exception as e:
                raise

    async def get_team_projects(
        self,
        team_id: str,
        limit: Optional[int] = None,
        offset: int = 0,
        search_query: Optional[str] = None
    ) -> FigmaFilesResponse:
        """
        Get files from a specific team using Figma's REST API
        
        Args:
            team_id: The team ID to get files from
            limit: Maximum number of files to return (optional)
            offset: Number of files to skip for pagination
            search_query: Filter files by search query
            
        Returns:
            FigmaFilesResponse containing files and metadata
        """
        self._ensure_configured()
        url = f"{self.base_url}/teams/{team_id}/projects"
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                projects = data.get("projects", [])
                
                all_files = []
                
                # Get files from each project
                for project in projects:
                    project_id = project.get("id")
                    if not project_id:
                        continue
                    
                    # Get files from this project
                    project_files_response = await self.get_project_files(project_id)
                    all_files.extend(project_files_response.files)
                
                # Filter files if search query provided
                if search_query:
                    all_files = self._filter_files_by_query(all_files, search_query)
                
                # Apply pagination
                start_idx = offset
                if limit:
                    end_idx = offset + limit
                    paginated_files = all_files[start_idx:end_idx]
                    has_more = end_idx < len(all_files)
                else:
                    paginated_files = all_files[start_idx:]
                    has_more = False
                
                return FigmaFilesResponse(
                    files=paginated_files,
                    total_count=len(all_files),
                    has_more=has_more
                )
                
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if e.response.status_code == 401:
                    raise ValueError(
                        "Invalid Figma API token or unauthorized access"
                    )
                elif e.response.status_code == 403:
                    raise ValueError("Forbidden: Check API token permissions")
                else:
                    error_msg = (
                        f"Figma API error: {e.response.status_code} "
                        f"- {e.response.text}"
                    )
                    raise ValueError(error_msg)
            except httpx.RequestError as e:
                raise ValueError(f"Failed to connect to Figma API: {str(e)}")

    async def get_project_files(
        self,
        project_id: str
    ) -> FigmaFilesResponse:
        """
        Get files from a specific project
        
        Args:
            project_id: The project ID to get files from
            
        Returns:
            FigmaFilesResponse containing files and metadata
        """
        self._ensure_configured()
        url = f"{self.base_url}/projects/{project_id}/files"
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                files_data = data.get("files", [])
                
                files = []
                for file_data in files_data:
                    file_obj = FigmaFile(
                        key=file_data.get("key", ""),
                        name=file_data.get("name", "Untitled"),
                        thumbnail_url=file_data.get("thumbnail_url"),
                        last_modified=file_data.get("last_modified"),
                        file_type="design"
                    )
                    files.append(file_obj)
                
                return FigmaFilesResponse(
                    files=files,
                    total_count=len(files),
                    has_more=False
                )
                
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if e.response.status_code == 401:
                    raise ValueError(
                        "Invalid Figma API token or unauthorized access"
                    )
                elif e.response.status_code == 403:
                    raise ValueError("Forbidden: Check API token permissions")
                else:
                    error_msg = (
                        f"Figma API error: {e.response.status_code} "
                        f"- {e.response.text}"
                    )
                    raise ValueError(error_msg)
            except httpx.RequestError as e:
                raise ValueError(f"Failed to connect to Figma API: {str(e)}")


# Global instance
figma_service = FigmaService() if settings.FIGMA_API_TOKEN else None 