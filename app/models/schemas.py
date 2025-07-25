"""
Pydantic schemas for request/response models
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DataSourceType(str, Enum):
    """Available data source types"""

    FILE_UPLOAD = "file_upload"
    CONFLUENCE = "confluence"
    SHAREPOINT = "sharepoint"
    SLACK = "slack"
    WEB_SCRAPING = "web_scraping"
    DATABASE = "database"


# Lucid Diagram Schemas
class LucidDocument(BaseModel):
    id: str
    title: str
    created: str
    lastModified: str
    product: str  # e.g., "lucidchart", "lucidspark"
    collaboratorCount: Optional[int] = None
    folderId: Optional[str] = None
    folderName: Optional[str] = None


class LucidDocumentsResponse(BaseModel):
    documents: List[LucidDocument]
    totalCount: int
    hasMore: bool


# MCP Server Schemas
class MCPListDiagramsRequest(BaseModel):
    limit: Optional[int] = 50
    offset: Optional[int] = 0
    search_query: Optional[str] = None
    product_filter: Optional[str] = None  # "lucidchart" or "lucidspark"


class MCPListDiagramsResponse(BaseModel):
    diagrams: List[LucidDocument]
    total_count: int
    has_more: bool
    message: str


class FileUploadRequest(BaseModel):
    """Request model for file uploads"""

    file_name: str = Field(..., description="Name of the uploaded file")
    file_type: str = Field(..., description="Type/extension of the file")
    content: str = Field(..., description="Base64 encoded file content")
    description: Optional[str] = Field(None, description="Description of the file")


class FileUploadResponse(BaseModel):
    """Response model for file uploads"""

    file_id: str = Field(..., description="Unique identifier for the uploaded file")
    status: str = Field(..., description="Upload status")
    message: str = Field(..., description="Status message")
    processed: bool = Field(..., description="Whether file has been processed")


class DataSourceConfig(BaseModel):
    """Configuration for external data sources"""

    source_type: DataSourceType
    name: str = Field(..., description="Human-readable name for the source")
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Source-specific configuration"
    )
    enabled: bool = Field(default=True, description="Whether source is enabled")


class DataSourceResponse(BaseModel):
    """Response model for data source information"""

    source_id: str = Field(..., description="Unique identifier for the source")
    source_type: DataSourceType
    name: str
    status: str = Field(..., description="Connection status")
    last_sync: Optional[datetime] = Field(None, description="Last sync timestamp")
    document_count: int = Field(default=0, description="Number of documents indexed")


class HealthResponse(BaseModel):
    """Response model for health checks"""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(default="1.0.0", description="API version")
    uptime: Optional[str] = Field(None, description="Service uptime")
    dependencies: Dict[str, str] = Field(
        default_factory=dict, description="Status of external dependencies"
    )


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(None, description="Request identifier")
