"""
Data Source Service for handling different data sources
"""

import base64
import io
import uuid
from typing import List, Dict, Any, Optional
from docx import Document
import PyPDF2
import pandas as pd

from app.core.config import settings
from app.models.schemas import DataSourceType


class DataSourceService:
    """Service for managing different data sources"""
    
    def __init__(self):
        self.supported_extensions = settings.ALLOWED_FILE_TYPES
        self.max_file_size = settings.MAX_FILE_SIZE
        self.documents = {}  # In-memory storage (use database in production)
    
    async def process_file_upload(
        self, 
        file_name: str, 
        file_type: str, 
        content: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process uploaded file and extract text content
        
        Args:
            file_name: Name of the file
            file_type: File extension/type
            content: Base64 encoded file content
            description: Optional description
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Validate file type
            if file_type.lower() not in self.supported_extensions:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_type}"
                }
            
            # Decode base64 content
            file_data = base64.b64decode(content)
            
            # Check file size
            if len(file_data) > self.max_file_size:
                return {
                    "success": False,
                    "error": f"File too large. Max size: {self.max_file_size} bytes"
                }
            
            # Extract text based on file type
            extracted_text = await self._extract_text_from_file(
                file_data, file_type.lower()
            )
            
            if not extracted_text:
                return {
                    "success": False,
                    "error": "Could not extract text from file"
                }
            
            # Store document
            doc_id = str(uuid.uuid4())
            self.documents[doc_id] = {
                "id": doc_id,
                "name": file_name,
                "type": file_type,
                "content": extracted_text,
                "description": description,
                "source_type": DataSourceType.FILE_UPLOAD,
                "metadata": {
                    "file_size": len(file_data),
                    "text_length": len(extracted_text)
                }
            }
            
            return {
                "success": True,
                "file_id": doc_id,
                "message": f"File {file_name} processed successfully",
                "text_length": len(extracted_text)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing file: {str(e)}"
            }
    
    async def _extract_text_from_file(
        self, file_data: bytes, file_type: str
    ) -> Optional[str]:
        """Extract text content from different file types"""
        try:
            if file_type == "pdf":
                return self._extract_text_from_pdf(file_data)
            elif file_type == "docx":
                return self._extract_text_from_docx(file_data)
            elif file_type == "txt":
                return file_data.decode('utf-8')
            elif file_type in ["xlsx", "csv"]:
                return self._extract_text_from_spreadsheet(file_data, file_type)
            else:
                return None
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None
    
    def _extract_text_from_pdf(self, file_data: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_data))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def _extract_text_from_docx(self, file_data: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(io.BytesIO(file_data))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
            return ""
    
    def _extract_text_from_spreadsheet(
        self, file_data: bytes, file_type: str
    ) -> str:
        """Extract text from spreadsheet files"""
        try:
            if file_type == "xlsx":
                df = pd.read_excel(io.BytesIO(file_data))
            else:  # csv
                df = pd.read_csv(io.BytesIO(file_data))
            
            # Convert DataFrame to text representation
            return df.to_string()
        except Exception as e:
            print(f"Error extracting spreadsheet text: {e}")
            return ""
    
    async def search_documents(
        self, 
        query: str, 
        source_types: Optional[List[DataSourceType]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search through available documents
        
        Args:
            query: Search query
            source_types: Limit search to specific source types
            limit: Maximum number of results
            
        Returns:
            List of relevant documents
        """
        results = []
        query_lower = query.lower()
        
        for doc_id, doc in self.documents.items():
            # Filter by source type if specified
            if source_types and doc["source_type"] not in source_types:
                continue
            
            # Simple text search (implement better search in production)
            content_lower = doc["content"].lower()
            if query_lower in content_lower or query_lower in doc["name"].lower():
                # Calculate simple relevance score
                score = content_lower.count(query_lower)
                results.append({
                    "document": doc,
                    "relevance_score": score
                })
        
        # Sort by relevance score and limit results
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]
    
    def get_document_context(
        self, 
        documents: List[Dict[str, Any]], 
        max_length: int = 5000
    ) -> str:
        """
        Combine document content into context for LLM
        
        Args:
            documents: List of documents
            max_length: Maximum context length
            
        Returns:
            Combined context string
        """
        context_parts = []
        current_length = 0
        
        for doc_info in documents:
            doc = doc_info["document"]
            doc_text = f"Document: {doc['name']}\n{doc['content']}\n\n"
            
            if current_length + len(doc_text) > max_length:
                # Truncate if needed
                remaining_space = max_length - current_length
                if remaining_space > 100:  # Only add if meaningful space left
                    doc_text = doc_text[:remaining_space] + "...\n\n"
                    context_parts.append(doc_text)
                break
            
            context_parts.append(doc_text)
            current_length += len(doc_text)
        
        return "".join(context_parts)
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all stored documents"""
        return list(self.documents.values())
    
    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get specific document by ID"""
        return self.documents.get(doc_id)
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete document by ID"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            return True
        return False


# Create singleton instance
data_source_service = DataSourceService() 