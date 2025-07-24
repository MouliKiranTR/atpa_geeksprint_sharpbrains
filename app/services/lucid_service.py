"""
Lucid Service for communicating with Lucid REST API
"""

import httpx
from typing import Optional, Dict, List
from app.core.config import settings
from app.models.schemas import LucidDocument, LucidDocumentsResponse
from app.services.cache_service import cache_service


class LucidService:
    """Service for interacting with Lucid REST API"""
    
    def __init__(self):
        self.api_key = settings.LUCID_API_KEY
        self.base_url = settings.LUCID_API_BASE_URL
        self.is_configured = bool(self.api_key)
    
    def _ensure_configured(self):
        """Ensure the service is properly configured"""
        if not self.is_configured:
            raise ValueError("LUCID_API_KEY is not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Lucid API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Lucid-Api-Version": "1"
        }
    
    def _filter_documents_by_query(
        self, 
        documents: List[LucidDocument], 
        query: str
    ) -> List[LucidDocument]:
        """
        Client-side filtering of documents by query string.
        Searches in title and other relevant fields.
        
        Args:
            documents: List of documents to filter
            query: Search query string
            
        Returns:
            Filtered list of documents
        """
        if not query:
            return documents
        
        query_lower = query.lower()
        filtered_docs = []
        
        for doc in documents:
            # Search in title (primary field)
            if query_lower in doc.title.lower():
                filtered_docs.append(doc)
                continue
            
            # Search in product type
            if query_lower in doc.product.lower():
                filtered_docs.append(doc)
                continue
                
            # Search for partial matches (for typos like "Intergration")
            title_words = doc.title.lower().split()
            query_words = query_lower.split()
            
            # Check if any query word is similar to any title word
            for query_word in query_words:
                for title_word in title_words:
                    # Simple similarity check for common typos
                    word_match = (
                        len(query_word) >= 4 and len(title_word) >= 4 and
                        (query_word in title_word or title_word in query_word or
                         self._similar_words(query_word, title_word))
                    )
                    if word_match:
                        filtered_docs.append(doc)
                        break
                else:
                    continue
                break
        
        return filtered_docs
    
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

    async def search_documents(
        self, 
        query: Optional[str] = None,
        product_filter: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        use_client_side_search: bool = False
    ) -> LucidDocumentsResponse:
        """
        Search for documents using Lucid's REST API
        
        Args:
            query: Search query string
            product_filter: Filter by product ("lucidchart" or "lucidspark")
            limit: Maximum number of documents to return
            offset: Number of documents to skip
            use_client_side_search: If True, filter client-side
            
        Returns:
            LucidDocumentsResponse containing documents and metadata
        """
        self._ensure_configured()
        url = f"{self.base_url}/documents/search"
        
        # If using client-side search, get all documents first
        if use_client_side_search and query:
            print("DEBUG: Using client-side search")
            # Get all documents without query
            all_docs_response = await self.search_documents(
                query=None,
                product_filter=product_filter,
                limit=100,  # Get more documents for filtering
                offset=0,
                use_client_side_search=False
            )
            
            # Filter documents client-side
            filtered_docs = self._filter_documents_by_query(
                all_docs_response.documents, 
                query
            )
            
            # Apply pagination to filtered results
            start_idx = offset
            end_idx = offset + limit
            paginated_docs = filtered_docs[start_idx:end_idx]
            
            return LucidDocumentsResponse(
                documents=paginated_docs,
                totalCount=len(filtered_docs),
                hasMore=end_idx < len(filtered_docs)
            )
        
        # Build search payload for API search
        payload = {
            "limit": limit,
            "offset": offset
        }
        
        if query:
            payload["query"] = query
            print(f"DEBUG: Using API search with query: '{query}'")
            
        if product_filter:
            payload["productFilter"] = product_filter
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                
                data = response.json()
                # Handle case where API returns list directly instead of dict
                if isinstance(data, list):
                    # If data is a list, assume it's the documents list
                    documents_list = data
                    total_count = len(data)
                    has_more = False
                elif isinstance(data, dict):
                    # If data is a dict, extract documents from it
                    documents_list = data.get("documents", [])
                    total_count = data.get("totalCount", len(documents_list))
                    has_more = data.get("hasMore", False)
                else:
                    raise ValueError(
                        f"Unexpected API response format: {type(data)}"
                    )
                
                
                # Parse response and convert to our schema
                documents = []
                for i, doc_data in enumerate(documents_list):
                    # Ensure doc_data is a dictionary
                    if not isinstance(doc_data, dict):
                        print(f"DEBUG: Skip doc {i} - not dict")
                        continue  # Skip invalid entries
                    
                    # Check document ID (Lucid API uses 'documentId')
                    doc_id = doc_data.get("documentId")
                    
                    if not doc_id:
                        continue
                    
                    # Convert ID to string if it's not already
                    if not isinstance(doc_id, str):
                        doc_id = str(doc_id)
                    
                    # Handle parent folder ID (convert to string if needed)
                    parent_id = doc_data.get("parent")
                    folder_id = str(parent_id) if parent_id else None
                        
                    document = LucidDocument(
                        id=doc_id,
                        title=doc_data.get("title", "Untitled"),
                        created=doc_data.get("created", ""),
                        lastModified=doc_data.get("lastModified", ""),
                        product=doc_data.get("product", "unknown"),
                        collaboratorCount=None,  # Not available in search API
                        folderId=folder_id,  # Convert parent to string
                        folderName=None  # Not available in search API
                    )
                    documents.append(document)
                
                print(f"DEBUG: Successfully parsed {len(documents)} documents")
                
                return LucidDocumentsResponse(
                    documents=documents,
                    totalCount=total_count,
                    hasMore=has_more
                )
                
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                print(f"DEBUG: HTTPStatusError - Status: {status_code}")
                print(f"DEBUG: Response text: {e.response.text}")
                if e.response.status_code == 401:
                    raise ValueError(
                        "Invalid Lucid API key or unauthorized access"
                    )
                elif e.response.status_code == 403:
                    raise ValueError("Forbidden: Check API key permissions")
                else:
                    error_msg = (
                        f"Lucid API error: {e.response.status_code} "
                        f"- {e.response.text}"
                    )
                    raise ValueError(error_msg)
            except httpx.RequestError as e:
                print(f"DEBUG: RequestError: {str(e)}")
                raise ValueError(f"Failed to connect to Lucid API: {str(e)}")
            except Exception as e:
                print(f"DEBUG: Unexpected error: {str(e)}")
                raise
    
    async def get_account_documents(
        self,
        limit: int = 50,
        offset: int = 0
    ) -> LucidDocumentsResponse:
        """
        Get all documents in the account using the account documents endpoint
        
        Args:
            limit: Maximum number of documents to return
            offset: Number of documents to skip
            
        Returns:
            LucidDocumentsResponse containing documents and metadata
        """
        self._ensure_configured()
        url = f"{self.base_url}/documents"
        
        params = {
            "limit": limit,
            "offset": offset
        }
        
        print(f"DEBUG: Making request to {url} with params: {params}")
        print(f"DEBUG: Headers: {self._get_headers()}")
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(
                    url,
                    headers=self._get_headers(),
                    params=params,
                    timeout=30.0
                )
                
                print(f"DEBUG: Response status: {response.status_code}")
                print(f"DEBUG: Response headers: {dict(response.headers)}")
                
                if response.status_code != 200:
                    print(f"DEBUG: Response text: {response.text}")
                
                response.raise_for_status()
                
                data = response.json()
                print(f"DEBUG: Response data type: {type(data)}")
                print(f"DEBUG: Response data: {data}")
                
                # Handle case where API returns list directly instead of dict
                if isinstance(data, list):
                    # If data is a list, assume it's the documents list
                    documents_list = data
                    total_count = len(data)
                    has_more = False
                elif isinstance(data, dict):
                    # If data is a dict, extract documents from it
                    documents_list = data.get("documents", [])
                    total_count = data.get("totalCount", len(documents_list))
                    has_more = data.get("hasMore", False)
                else:
                    raise ValueError(
                        f"Unexpected API response format: {type(data)}"
                    )
                
                # Parse response and convert to our schema
                documents = []
                for doc_data in documents_list:
                    # Ensure doc_data is a dictionary
                    if not isinstance(doc_data, dict):
                        continue  # Skip invalid entries
                    
                    # Skip documents without valid IDs (uses 'documentId')
                    doc_id = doc_data.get("documentId")
                    if not doc_id or not isinstance(doc_id, str):
                        continue  # Skip documents with missing or invalid IDs
                    
                    # Handle parent folder ID (convert to string if needed)
                    parent_id = doc_data.get("parent")
                    folder_id = str(parent_id) if parent_id else None
                        
                    document = LucidDocument(
                        id=doc_id,
                        title=doc_data.get("title", "Untitled"),
                        created=doc_data.get("created", ""),
                        lastModified=doc_data.get("lastModified", ""),
                        product=doc_data.get("product", "unknown"),
                        collaboratorCount=None,  # Not available in search API
                        folderId=folder_id,  # Convert parent to string
                        folderName=None  # Not available in search API
                    )
                    documents.append(document)
                
                print(f"DEBUG: Successfully parsed {len(documents)} documents")
                
                return LucidDocumentsResponse(
                    documents=documents,
                    totalCount=total_count,
                    hasMore=has_more
                )
                
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                print(f"DEBUG: HTTPStatusError - Status: {status_code}")
                print(f"DEBUG: Response text: {e.response.text}")
                if e.response.status_code == 401:
                    raise ValueError(
                        "Invalid Lucid API key or unauthorized access"
                    )
                elif e.response.status_code == 403:
                    raise ValueError("Forbidden: Check API key permissions")
                else:
                    error_msg = (
                        f"Lucid API error: {e.response.status_code} "
                        f"- {e.response.text}"
                    )
                    raise ValueError(error_msg)
            except httpx.RequestError as e:
                print(f"DEBUG: RequestError: {str(e)}")
                raise ValueError(f"Failed to connect to Lucid API: {str(e)}")
            except Exception as e:
                print(f"DEBUG: Unexpected error: {str(e)}")
                raise

    async def export_document_image(
        self, 
        document_id: str,
        page_id: Optional[str] = None,
        format: str = "png",
        width: Optional[int] = None,
        height: Optional[int] = None,
        use_cache: bool = True
    ) -> Dict[str, any]:
        """
        Export a Lucid document as an image using Get/Export Document endpoint
        
        Args:
            document_id: The ID of the document to export
            page_id: Optional page ID to export specific page
            format: Image format (png, jpg, pdf, svg)
            width: Optional width for the image
            height: Optional height for the image
            use_cache: Whether to use caching (default: True)
            
        Returns:
            Dictionary containing success status, image data, and metadata
        """
        self._ensure_configured()
        
        # Check cache first if enabled
        if use_cache:
            cached_result = await cache_service.get_cached_export(
                document_id, format, page_id, width, height
            )
            if cached_result:
                return cached_result
        
        # Use the Get/Export Document endpoint
        url = f"{self.base_url}/documents/{document_id}"
        
        # Build query parameters for export
        params = {
            "exportFormat": format
        }
        
        if page_id:
            params["pageId"] = page_id
        
        if width:
            params["width"] = width
            
        if height:
            params["height"] = height
        
        # Use appropriate Accept header for image format
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Lucid-Api-Version": "1"
        }
        
        if format.lower() == "png":
            headers["Accept"] = "image/png"
        elif format.lower() == "jpg" or format.lower() == "jpeg":
            headers["Accept"] = "image/jpeg"
        elif format.lower() == "pdf":
            headers["Accept"] = "application/pdf"
        elif format.lower() == "svg":
            headers["Accept"] = "image/svg+xml"
        else:
            headers["Accept"] = "image/png"  # Default to PNG
        
        print(f"DEBUG: Exporting document {document_id} as {format}")
        print(f"DEBUG: URL: {url}")
        print(f"DEBUG: Params: {params}")
        print(f"DEBUG: Headers: {headers}")
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=60.0  # Longer timeout for image export
                )
                
                print(f"DEBUG: Export response status: {response.status_code}")
                print(f"DEBUG: Export response headers: {dict(response.headers)}")
                
                response.raise_for_status()
                
                # Check if response is binary (image) data
                content_type = response.headers.get("content-type", "")
                is_image = content_type.startswith("image/")
                is_pdf = content_type == "application/pdf"
                if is_image or is_pdf:
                    # Binary image data
                    image_data = response.content
                    
                    # Prepare metadata
                    metadata = {
                        "document_id": document_id,
                        "page_id": page_id,
                        "export_format": format,
                        "content_type": content_type
                    }
                    
                    # Cache the result if caching is enabled
                    cache_result = None
                    if use_cache:
                        cache_result = await cache_service.cache_export(
                            document_id, image_data, metadata, 
                            format, page_id, width, height
                        )
                    
                    result = {
                        "success": True,
                        "image_data": image_data,
                        "content_type": content_type,
                        "format": format,
                        "size": len(image_data),
                        "metadata": metadata,
                        "cached": False
                    }
                    
                    # Add cache information if available
                    if cache_result:
                        result["cache_info"] = cache_result
                        result["file_path"] = cache_result.get("file_path")
                    
                    return result
                else:
                    # Unexpected response type
                    error_msg = (f"Unexpected content type: {content_type}. "
                               f"Expected image data.")
                    return {
                        "success": False,
                        "error": error_msg,
                        "response_text": response.text[:500]
                    }
                    
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                print(f"DEBUG: HTTPStatusError - Status: {status_code}")
                print(f"DEBUG: Response text: {e.response.text}")
                
                error_msg = f"Lucid export failed: {status_code}"
                if status_code == 401:
                    error_msg = "Invalid Lucid API key or unauthorized access"
                elif status_code == 403:
                    error_msg = "Forbidden: Check API key permissions"
                elif status_code == 404:
                    error_msg = f"Document {document_id} not found"
                
                return {
                    "success": False,
                    "error": error_msg,
                    "status_code": status_code,
                    "response_text": e.response.text[:500]
                }
                
            except httpx.RequestError as e:
                print(f"DEBUG: RequestError: {str(e)}")
                return {
                    "success": False,
                    "error": f"Failed to connect to Lucid API: {str(e)}"
                }
            except Exception as e:
                print(f"DEBUG: Unexpected error: {str(e)}")
                return {
                    "success": False,
                    "error": f"Unexpected error during export: {str(e)}"
                }


# Global instance
lucid_service = LucidService() if settings.LUCID_API_KEY else None