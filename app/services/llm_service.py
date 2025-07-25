"""
LLM Service for OpenAI integration
"""

import time
from typing import Any, Dict

import openai

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
        max_tokens: int = 1000,
        search_source: str = "wiki",
    ) -> Dict[str, Any]:
        """
        Generate an answer using OpenAI GPT model with enhanced prompts

        Args:
            question: User's question
            context: Relevant context from data sources
            max_tokens: Maximum tokens for response
            search_source: Type of source (wiki, general) for specialized prompts

        Returns:
            Dictionary containing answer and metadata
        """
        start_time = time.time()

        try:
            # Enhanced system prompt based on search source
            if search_source == "wiki":
                system_prompt = self._get_wiki_system_prompt()
            else:
                system_prompt = self._get_generic_system_prompt()

            # Enhanced user prompt with better context structuring
            user_prompt = self._create_enhanced_user_prompt(
                question, context, search_source
            )

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
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
                "tokens_used": response.usage.total_tokens,
            }

        except Exception as e:
            return {
                "answer": f"I apologize, but I encountered an error: {str(e)}",
                "confidence": 0.0,
                "processing_time": time.time() - start_time,
                "error": str(e),
            }

    async def summarize_content(
        self, content: str, max_length: int = 500, style: str = "professional"
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
                "technical": "Create a technical summary with specific details",
            }

            prompt = f"""
            {style_prompts.get(style, style_prompts["professional"])}.
            
            Please summarize the following content in approximately {max_length} words:
            
            {content}
            
            Summary:
            """

            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_length * 2,  # Rough estimate for tokens
                temperature=0.5,
            )

            summary = response.choices[0].message.content.strip()

            return {
                "summary": summary,
                "original_length": len(content.split()),
                "summary_length": len(summary.split()),
                "compression_ratio": len(summary) / len(content),
                "style": style,
            }

        except Exception as e:
            return {"summary": f"Error generating summary: {str(e)}", "error": str(e)}

    def _get_wiki_system_prompt(self) -> str:
        """Enhanced system prompt specifically for wiki/technical documentation analysis"""
        return """
        You are an expert technical documentation assistant specializing in enterprise knowledge management. 
        Your expertise includes software development, infrastructure, business processes, and organizational knowledge.

        CORE COMPETENCIES:
        - Technical documentation analysis and synthesis
        - Software architecture and implementation details
        - Business process workflows and dependencies
        - Team structures and organizational knowledge
        - Best practices and coding standards
        - Project management and development methodologies

        RESPONSE FRAMEWORK:
        1. **Executive Summary** (2-3 sentences for complex topics)
        2. **Detailed Analysis** with specific examples from context
        3. **Action Items** or next steps when applicable
        4. **Related Resources** mentioned in the documentation
        5. **Knowledge Gaps** if information is incomplete

        CITATION REQUIREMENTS:
        - Always reference specific wiki documents by name
        - Include section headers or page titles when available
        - Format citations as: [Source: Document_Name.md, Section: Header]
        - Quote exact text for critical information

        CONTEXT ANALYSIS GUIDELINES:
        - Prioritize official documentation over informal notes
        - Cross-reference multiple sources when available
        - Identify conflicting information and note discrepancies
        - Highlight recent updates or version-specific information
        - Connect related concepts across different wiki pages

        RESPONSE QUALITY INDICATORS:
        - Include specific file paths, URLs, or repository references
        - Mention team contacts or subject matter experts
        - Provide examples from actual code or configurations
        - Reference related projects or dependencies
        - Suggest documentation improvements when gaps are identified
        """

    def _get_generic_system_prompt(self) -> str:
        """Generic system prompt for non-wiki sources"""
        return """
        You are an intelligent assistant specializing in organizational knowledge and onboarding support.
        Provide clear, accurate, and actionable responses based on the provided context.
        
        Guidelines:
        - Be concise but comprehensive
        - Structure responses with clear headings
        - Provide specific examples when available
        - Always cite your sources
        - Indicate confidence level in your responses
        - Use a friendly but professional tone
        - If information is not in the context, say so clearly
        """

    def _create_enhanced_user_prompt(
        self, question: str, context: str, source_type: str
    ) -> str:
        """Create enhanced user prompt with better context structuring"""
        formatted_context = self._format_context_for_analysis(context, source_type)

        return f"""
        KNOWLEDGE BASE CONTEXT:
        {formatted_context}
        
        USER QUESTION: {question}
        
        ANALYSIS REQUEST:
        Please provide a comprehensive response that:
        1. Directly answers the user's question
        2. Provides relevant technical details and examples
        3. Identifies any prerequisites or dependencies
        4. Suggests follow-up actions or related topics
        5. Cites specific sources and sections
        
        If the question involves technical implementation, include:
        - Code examples or configuration snippets from the context
        - Architecture diagrams or flow descriptions mentioned
        - Integration points with other systems
        - Testing or validation approaches
        
        If the question involves processes or workflows, include:
        - Step-by-step procedures
        - Role responsibilities and handoffs
        - Tools and systems involved
        - Common issues and troubleshooting steps
        """

    def _format_context_for_analysis(self, context: str, source_type: str) -> str:
        """Format context with enhanced structure for better LLM understanding"""

        if source_type == "wiki":
            return f"""
            === TECHNICAL DOCUMENTATION SOURCES ===
            
            {context}
            
            === ANALYSIS INSTRUCTIONS ===
            - Extract actionable information from each source
            - Identify relationships between different documents
            - Note any code examples, configurations, or technical specifications
            - Flag any outdated information or broken references
            - Highlight critical dependencies or prerequisites
            """

        return f"""
        === INFORMATION SOURCES ===
        
        {context}
        
        === CONTEXT GUIDELINES ===
        - Focus on providing accurate, actionable information
        - Structure response clearly with appropriate sections
        - Cite sources appropriately
        """

    def _calculate_confidence(self, answer: str, context: str) -> float:
        """
        Enhanced confidence calculation based on answer characteristics

        Args:
            answer: Generated answer
            context: Source context

        Returns:
            Confidence score between 0 and 1
        """
        confidence = 0.5  # Base confidence

        # Increase confidence if answer is detailed and structured
        if len(answer) > 150:
            confidence += 0.15
        if any(marker in answer for marker in ["##", "**", "1.", "2.", "•", "-"]):
            confidence += 0.1  # Well-structured response

        # Increase confidence if answer contains specific technical information
        technical_indicators = [
            "code",
            "configuration",
            "repository",
            "file",
            "directory",
            "API",
            "endpoint",
            "function",
            "class",
            "method",
            "variable",
        ]
        if any(word in answer.lower() for word in technical_indicators):
            confidence += 0.15

        # Increase confidence if answer contains proper citations
        citation_patterns = ["[Source:", "Document:", "Section:", "See:", "Reference:"]
        if any(pattern in answer for pattern in citation_patterns):
            confidence += 0.1

        # Increase confidence if answer contains actionable information
        action_indicators = [
            "step",
            "procedure",
            "follow",
            "implement",
            "configure",
            "install",
        ]
        if any(word in answer.lower() for word in action_indicators):
            confidence += 0.1

        # Decrease confidence for uncertainty indicators
        uncertainty_phrases = [
            "not sure",
            "unclear",
            "might be",
            "possibly",
            "i don't know",
            "appears to",
            "seems like",
            "may be",
            "could be",
        ]
        uncertainty_count = sum(
            1 for phrase in uncertainty_phrases if phrase in answer.lower()
        )
        confidence -= uncertainty_count * 0.15

        # Decrease confidence if answer is too generic
        generic_phrases = ["it depends", "varies", "generally", "typically", "usually"]
        if sum(1 for phrase in generic_phrases if phrase in answer.lower()) > 2:
            confidence -= 0.1

        # Boost confidence if context overlap is high (basic keyword matching)
        context_words = set(context.lower().split())
        answer_words = set(answer.lower().split())
        overlap_ratio = len(context_words & answer_words) / max(len(answer_words), 1)
        if overlap_ratio > 0.3:
            confidence += 0.1

        # Ensure confidence is between 0 and 1
        return max(0.0, min(1.0, confidence))


# Create singleton instance
llm_service = LLMService()
