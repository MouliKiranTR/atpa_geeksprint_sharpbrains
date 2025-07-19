"""
Query endpoints for AI-powered question answering
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import time

from app.models.schemas import (
    QueryRequest, 
    QueryResponse, 
    SummaryRequest, 
    SummaryResponse
)
from app.services.llm_service import llm_service
from app.services.data_source_service import data_source_service

router = APIRouter()


@router.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Ask a question and get an AI-powered answer based on available data
    
    This endpoint:
    1. Searches through available documents for relevant content
    2. Creates context from relevant documents
    3. Uses LLM to generate an answer based on the context
    4. Returns the answer with confidence score and sources
    """
    try:
        start_time = time.time()
        
        # Search for relevant documents
        relevant_docs = await data_source_service.search_documents(
            query=request.question,
            source_types=request.data_sources,
            limit=10
        )
        
        if not relevant_docs:
            return QueryResponse(
                answer="I don't have any relevant information to answer your question. Please make sure you've uploaded the necessary documents or check if your question is related to available data sources.",
                confidence=0.0,
                sources=[],
                processing_time=time.time() - start_time
            )
        
        # Create context from relevant documents
        context = data_source_service.get_document_context(
            relevant_docs, 
            max_length=request.context_limit
        )
        
        # Generate answer using LLM
        llm_response = await llm_service.generate_answer(
            question=request.question,
            context=context
        )
        
        # Prepare sources if requested
        sources = []
        if request.include_sources:
            sources = [
                {
                    "document_id": doc["document"]["id"],
                    "document_name": doc["document"]["name"],
                    "source_type": doc["document"]["source_type"],
                    "relevance_score": doc["relevance_score"]
                }
                for doc in relevant_docs[:5]  # Limit to top 5 sources
            ]
        
        return QueryResponse(
            answer=llm_response["answer"],
            confidence=llm_response["confidence"],
            sources=sources,
            processing_time=time.time() - start_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_content(request: SummaryRequest):
    """
    Summarize provided content using AI
    
    This endpoint takes text content and returns an AI-generated summary
    with specified length and style preferences.
    """
    try:
        # Generate summary using LLM
        summary_result = await llm_service.summarize_content(
            content=request.content,
            max_length=request.max_length,
            style=request.style
        )
        
        if "error" in summary_result:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating summary: {summary_result['error']}"
            )
        
        return SummaryResponse(**summary_result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing summary request: {str(e)}"
        )


@router.get("/documents")
async def get_all_documents():
    """
    Get list of all available documents
    
    Returns metadata about all documents that can be queried
    """
    try:
        documents = data_source_service.get_all_documents()
        return {
            "total_documents": len(documents),
            "documents": [
                {
                    "id": doc["id"],
                    "name": doc["name"],
                    "type": doc["type"],
                    "source_type": doc["source_type"],
                    "description": doc.get("description"),
                    "text_length": len(doc["content"])
                }
                for doc in documents
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documents: {str(e)}"
        )


@router.get("/documents/{document_id}")
async def get_document(document_id: str):
    """
    Get specific document by ID
    
    Returns full document content and metadata
    """
    try:
        document = data_source_service.get_document_by_id(document_id)
        
        if not document:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        return document
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document: {str(e)}"
        )


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document by ID
    
    Removes the document from the system permanently
    """
    try:
        success = data_source_service.delete_document(document_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Document not found"
            )
        
        return {"message": f"Document {document_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting document: {str(e)}"
        ) 