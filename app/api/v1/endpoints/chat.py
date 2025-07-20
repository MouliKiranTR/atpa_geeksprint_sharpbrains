"""
Chat endpoint for conversational interface with visual content analysis
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import time
import uuid

from app.services.enhanced_query_service import enhanced_query_service

router = APIRouter()


class ChatMessage(BaseModel):
    """Individual chat message"""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[float] = Field(
        default=None, 
        description="Message timestamp"
    )


class ChatRequest(BaseModel):
    """Request model for chat conversation"""
    message: str = Field(..., description="User's message")
    conversation_id: Optional[str] = Field(
        default=None, 
        description="Conversation ID for context"
    )
    chat_history: Optional[List[ChatMessage]] = Field(
        default=[], 
        description="Previous chat messages for context"
    )
    include_figma: bool = Field(
        default=True, 
        description="Whether to search Figma files"
    )
    include_lucid: bool = Field(
        default=True, 
        description="Whether to search Lucid diagrams"
    )
    include_documents: bool = Field(
        default=True, 
        description="Whether to search uploaded documents"
    )
    max_visual_items: int = Field(
        default=3, 
        description="Maximum visual items to process",
        ge=1,
        le=10
    )


class ChatResponse(BaseModel):
    """Response model for chat conversation"""
    message: str = Field(..., description="Assistant's response message")
    conversation_id: str = Field(
        ..., 
        description="Conversation ID for tracking"
    )
    chat_history: List[ChatMessage] = Field(
        ..., 
        description="Updated chat history including new messages"
    )
    is_visual_query: bool = Field(
        ..., 
        description="Whether the query was detected as visual-related"
    )
    analysis_type: str = Field(
        ..., 
        description="Type of analysis performed"
    )
    search_summary: Dict[str, Any] = Field(
        ..., 
        description="Summary of search results"
    )
    visual_analysis_available: bool = Field(
        ..., 
        description="Whether visual analysis was performed"
    )
    processing_time: float = Field(
        ..., 
        description="Processing time in seconds"
    )
    cost: Optional[float] = Field(
        None, 
        description="Analysis cost if available"
    )
    success: bool = Field(True, description="Whether the request succeeded")
    error: Optional[str] = Field(None, description="Error message if any")


@router.post("/message", response_model=ChatResponse)
async def send_chat_message(request: ChatRequest):
    """
    Send a message in a chat conversation with visual content analysis
    
    This endpoint provides a conversational interface that:
    1. Maintains chat history and context
    2. Analyzes user messages for visual content needs
    3. Searches across Figma, Lucid, and document sources
    4. Provides comprehensive responses with visual analysis
    5. Tracks conversation state and costs
    
    Features:
    - Conversational context awareness
    - Automatic visual content detection
    - Multi-source search capabilities
    - Visual analysis and screenshot capture
    - Cost tracking and performance metrics
    - Conversation history management
    """
    start_time = time.time()
    
    try:
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Build current chat history
        current_history = (
            list(request.chat_history) if request.chat_history else []
        )
        
        # Add user message to history
        user_message = ChatMessage(
            role="user",
            content=request.message,
            timestamp=time.time()
        )
        current_history.append(user_message)
        
        # Perform enhanced query analysis
        results = await enhanced_query_service.analyze_user_query(
            user_question=request.message,
            include_figma=request.include_figma,
            include_lucid=request.include_lucid,
            include_documents=request.include_documents,
            max_visual_items=request.max_visual_items
        )
        
        # Check for errors
        if results.get("error"):
            error_message = f"I encountered an error: {results.get('error')}"
            
            # Add error response to history
            assistant_message = ChatMessage(
                role="assistant",
                content=error_message,
                timestamp=time.time()
            )
            current_history.append(assistant_message)
            
            return ChatResponse(
                message=error_message,
                conversation_id=conversation_id,
                chat_history=current_history,
                is_visual_query=False,
                analysis_type="error",
                search_summary={"error": True},
                visual_analysis_available=False,
                processing_time=time.time() - start_time,
                success=False,
                error=results.get("error")
            )
        
        # Extract information for response
        query_analysis = results.get("query_analysis", {})
        search_results = results.get("search_results", {})
        visual_analysis = results.get("visual_analysis", {})
        
        # Get assistant response
        assistant_response = results.get(
            "combined_response", 
            "I couldn't generate a response to your message."
        )
        
        # Create search summary
        search_summary = {
            "figma_files_found": len(search_results.get("figma_files", [])),
            "lucid_diagrams_found": len(
                search_results.get("lucid_diagrams", [])
            ),
            "documents_found": len(search_results.get("documents", [])),
            "total_sources_searched": sum([
                1 if request.include_figma else 0,
                1 if request.include_lucid else 0,
                1 if request.include_documents else 0
            ]),
            "visual_items_processed": (
                len(visual_analysis.get("visual_data", []))
                if visual_analysis else 0
            )
        }
        
        # Add assistant message to history
        assistant_message = ChatMessage(
            role="assistant",
            content=assistant_response,
            timestamp=time.time()
        )
        current_history.append(assistant_message)
        
        # Extract cost if available
        cost = None
        if visual_analysis and visual_analysis.get("cost"):
            cost = float(visual_analysis.get("cost", 0))
        
        return ChatResponse(
            message=assistant_response,
            conversation_id=conversation_id,
            chat_history=current_history,
            is_visual_query=results.get("is_visual_query", False),
            analysis_type=query_analysis.get("analysis_type", "general"),
            search_summary=search_summary,
            visual_analysis_available=bool(
                visual_analysis and visual_analysis.get("success")
            ),
            processing_time=time.time() - start_time,
            cost=cost,
            success=True
        )
        
    except Exception as e:
        error_message = f"I'm sorry, I encountered an error: {str(e)}"
        
        # Try to maintain conversation context even with errors
        try:
            conversation_id = request.conversation_id or str(uuid.uuid4())
            current_history = (
                list(request.chat_history) if request.chat_history else []
            )
            
            # Add user message
            current_history.append(ChatMessage(
                role="user",
                content=request.message,
                timestamp=time.time()
            ))
            
            # Add error response
            current_history.append(ChatMessage(
                role="assistant",
                content=error_message,
                timestamp=time.time()
            ))
            
            return ChatResponse(
                message=error_message,
                conversation_id=conversation_id,
                chat_history=current_history,
                is_visual_query=False,
                analysis_type="error",
                search_summary={"error": True},
                visual_analysis_available=False,
                processing_time=time.time() - start_time,
                success=False,
                error=str(e)
            )
        except Exception:
            # Fallback error response
            raise HTTPException(
                status_code=500,
                detail=f"Error processing chat message: {str(e)}"
            )


@router.get("/conversation/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Get conversation history by ID
    
    Note: This is a placeholder endpoint. In a production system,
    you would store and retrieve conversation history from a database.
    """
    return {
        "conversation_id": conversation_id,
        "message": "Conversation history retrieval not implemented yet",
        "chat_history": []
    }


@router.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    Clear a conversation history
    
    Note: This is a placeholder endpoint. In a production system,
    you would delete conversation history from a database.
    """
    return {
        "conversation_id": conversation_id,
        "message": "Conversation cleared",
        "success": True
    }


@router.get("/health")
async def chat_health_check():
    """Health check for chat service"""
    return {
        "status": "healthy",
        "service": "chat",
        "timestamp": time.time()
    } 