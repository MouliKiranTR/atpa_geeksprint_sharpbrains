"""
Pydantic schemas for request/response models
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class DataSourceType(str, Enum):
    """Available data source types"""
    FILE_UPLOAD = "file_upload"
    CONFLUENCE = "confluence"
    SHAREPOINT = "sharepoint"
    SLACK = "slack"
    WEB_SCRAPING = "web_scraping"
    DATABASE = "database"


class QueryRequest(BaseModel):
    """Request model for asking questions"""
    question: str = Field(..., description="User's question")
    data_sources: Optional[List[DataSourceType]] = Field(
        default=None,
        description=("Specific data sources to query "
                     "(if None, uses all available)")
    )
    context_limit: Optional[int] = Field(
        default=5000,
        description="Maximum number of characters for context"
    )
    include_sources: bool = Field(
        default=True,
        description="Whether to include source references in response"
    )


class QueryResponse(BaseModel):
    """Response model for answers"""
    answer: str = Field(..., description="AI-generated answer")
    confidence: float = Field(..., description="Confidence score (0-1)")
    sources: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Source documents used for the answer"
    )
    processing_time: float = Field(
        ..., description="Time taken to process in seconds"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ProgramGenerationRequest(BaseModel):
    """Request model for program generation"""
    user_input: str = Field(
        ..., description="Description of the program to generate"
    )


class ProgramGenerationResponse(BaseModel):
    """Response model for program generation"""
    program: str = Field(..., description="Generated program code")
    cost: Optional[float] = Field(
        None, description="Estimated cost of the generation"
    )
    status: str = Field(..., description="Generation status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


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


# Figma API Schemas
class FigmaFile(BaseModel):
    """Model for a Figma file"""
    key: str = Field(..., description="Unique file key")
    name: str = Field(..., description="File name")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail")
    last_modified: Optional[str] = Field(None, description="Last modified")
    file_type: str = Field(default="design", description="File type")


class FigmaFilesResponse(BaseModel):
    """Response model for Figma files"""
    files: List[FigmaFile]
    total_count: int
    has_more: bool


# Figma MCP Schemas
class MCPListFilesRequest(BaseModel):
    """Request model for listing Figma files via MCP"""
    limit: Optional[int] = 50
    offset: Optional[int] = 0
    search_query: Optional[str] = None
    team_id: Optional[str] = None


class MCPListFilesResponse(BaseModel):
    """Response model for listing Figma files via MCP"""
    files: List[FigmaFile]
    total_count: int
    has_more: bool
    message: str


class FileUploadRequest(BaseModel):
    """Request model for file uploads"""
    file_name: str = Field(..., description="Name of the uploaded file")
    file_type: str = Field(..., description="Type/extension of the file")
    content: str = Field(..., description="Base64 encoded file content")
    description: Optional[str] = Field(
        None, description="Description of the file"
    )


class FileUploadResponse(BaseModel):
    """Response model for file uploads"""
    file_id: str = Field(
        ..., description="Unique identifier for the uploaded file"
    )
    status: str = Field(..., description="Upload status")
    message: str = Field(..., description="Status message")
    processed: bool = Field(
        ..., description="Whether file has been processed"
    )


class DataSourceConfig(BaseModel):
    """Configuration for external data sources"""
    source_type: DataSourceType
    name: str = Field(..., description="Human-readable name for the source")
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Source-specific configuration"
    )
    enabled: bool = Field(
        default=True, description="Whether source is enabled"
    )


class DataSourceResponse(BaseModel):
    """Response model for data source information"""
    source_id: str = Field(
        ..., description="Unique identifier for the source"
    )
    source_type: DataSourceType
    name: str
    status: str = Field(..., description="Connection status")
    last_sync: Optional[datetime] = Field(
        None, description="Last sync timestamp"
    )
    document_count: int = Field(
        default=0, description="Number of documents indexed"
    )


class SummaryRequest(BaseModel):
    """Request model for document summarization"""
    content: str = Field(..., description="Content to summarize")
    max_length: Optional[int] = Field(
        default=500,
        description="Maximum length of summary in words"
    )
    style: Optional[str] = Field(
        default="professional",
        description="Summary style (professional, casual, technical)"
    )


class SummaryResponse(BaseModel):
    """Response model for document summaries"""
    summary: str = Field(..., description="Generated summary")
    original_length: int = Field(
        ..., description="Original content length"
    )
    summary_length: int = Field(..., description="Summary length")
    compression_ratio: float = Field(..., description="Compression ratio")


class HealthResponse(BaseModel):
    """Response model for health checks"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(default="1.0.0", description="API version")
    uptime: Optional[str] = Field(None, description="Service uptime")
    dependencies: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of external dependencies"
    )


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(
        None, description="Detailed error information"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(
        None, description="Request identifier"
    ) 