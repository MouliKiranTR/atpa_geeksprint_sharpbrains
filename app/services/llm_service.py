"""
LLM Service for OpenAI integration
"""

import openai
import time
from typing import List, Dict, Any, Optional
from app.core.config import settings


class LLMService:
    """Service for interacting with Large Language Models"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
    
    async def generate_answer(
        self, 
        question: str, 
        context: str, 
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Generate an answer using OpenAI GPT model
        
        Args:
            question: User's question
            context: Relevant context from data sources
            max_tokens: Maximum tokens for response
            
        Returns:
            Dictionary containing answer and metadata
        """
        start_time = time.time()
        
        try:
            # Create system prompt for onboarding context
            system_prompt = """
            You are an intelligent onboarding assistant. Your role is to help new employees 
            understand company policies, procedures, and information by providing clear, 
            accurate, and helpful answers based on the provided context.
            
            Guidelines:
            - Base your answers strictly on the provided context
            - If information is not in the context, say so clearly
            - Provide specific, actionable information when possible
            - Use a friendly but professional tone
            - Structure your responses clearly with bullet points or sections when helpful
            - Always cite which documents or sources your information comes from
            """
            
            # Create user prompt with context and question
            user_prompt = f"""
            Context from company documents:
            {context}
            
            Question: {question}
            
            Please provide a comprehensive answer based on the context above.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            processing_time = time.time() - start_time
            
            # Calculate confidence based on response characteristics
            confidence = self._calculate_confidence(answer, context)
            
            return {
                "answer": answer,
                "confidence": confidence,
                "processing_time": processing_time,
                "model_used": self.model,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}",
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "error": str(e)
            }
    
    async def summarize_content(
        self, 
        content: str, 
        max_length: int = 500, 
        style: str = "professional"
    ) -> Dict[str, Any]:
        """
        Summarize content using OpenAI
        
        Args:
            content: Content to summarize
            max_length: Maximum length in words
            style: Summary style (professional, casual, technical)
            
        Returns:
            Dictionary containing summary and metadata
        """
        try:
            style_prompts = {
                "professional": "Create a professional, business-appropriate summary",
                "casual": "Create a casual, easy-to-understand summary",
                "technical": "Create a technical summary with specific details"
            }
            
            prompt = f"""
            {style_prompts.get(style, style_prompts['professional'])}.
            
            Please summarize the following content in approximately {max_length} words:
            
            {content}
            
            Summary:
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_length * 2,  # Rough estimate for tokens
                temperature=0.5
            )
            
            summary = response.choices[0].message.content.strip()
            
            return {
                "summary": summary,
                "original_length": len(content.split()),
                "summary_length": len(summary.split()),
                "compression_ratio": len(summary) / len(content),
                "style": style
            }
            
        except Exception as e:
            return {
                "summary": f"Error generating summary: {str(e)}",
                "error": str(e)
            }
    
    def _calculate_confidence(self, answer: str, context: str) -> float:
        """
        Calculate confidence score based on answer characteristics
        
        Args:
            answer: Generated answer
            context: Source context
            
        Returns:
            Confidence score between 0 and 1
        """
        # Simple heuristic for confidence calculation
        confidence = 0.5  # Base confidence
        
        # Increase confidence if answer is detailed
        if len(answer) > 100:
            confidence += 0.2
        
        # Increase confidence if answer contains specific information
        if any(word in answer.lower() for word in ['policy', 'procedure', 'document', 'section']):
            confidence += 0.1
        
        # Decrease confidence if answer indicates uncertainty
        uncertainty_phrases = ['not sure', 'unclear', 'might be', 'possibly', 'i don\'t know']
        if any(phrase in answer.lower() for phrase in uncertainty_phrases):
            confidence -= 0.3
        
        # Ensure confidence is between 0 and 1
        return max(0.0, min(1.0, confidence))


# Create singleton instance
llm_service = LLMService() 