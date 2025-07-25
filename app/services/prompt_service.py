"""
Enhanced Prompt Service for optimized LLM interactions
"""

from typing import Any, Dict, List


class PromptService:
    def __init__(self):
        pass

    def getBasePrompt(self):
        """Enhanced base prompt for comprehensive analysis"""
        return """
        You are an expert enterprise knowledge assistant with specialized expertise in:
        - Technical documentation analysis and synthesis
        - Software architecture and development practices
        - Business process optimization and workflow analysis
        - Organizational knowledge management
        - Visual content interpretation and technical diagram analysis
        
        Your responses should be structured, actionable, and evidence-based.
        """

    def getLucidPrompt(self, context: str, question: str):
        """Enhanced prompt for Lucid diagram analysis"""
        return f"""
        VISUAL ANALYSIS CONTEXT:
        I'm analyzing Lucid diagrams that contain technical architecture, business processes, or system designs.
        
        DIAGRAM CONTEXT: {context}
        
        USER QUESTION: {question}
        
        ANALYSIS FRAMEWORK:
        Please provide a comprehensive analysis that includes:
        
        1. **Visual Content Summary**
           - Describe the diagram type (flowchart, architecture, process flow, etc.)
           - Identify key components, entities, and relationships
           - Note any text, labels, or annotations visible
        
        2. **Technical Analysis**
           - System architecture interpretation (if applicable)
           - Data flow and process sequence analysis
           - Integration points and dependencies
           - Technology stack or tool identification
        
        3. **Business Impact Assessment**
           - Process efficiency implications
           - Stakeholder roles and responsibilities
           - Workflow bottlenecks or optimization opportunities
           - Compliance or governance considerations
        
        4. **Actionable Recommendations**
           - Implementation suggestions
           - Best practices alignment
           - Risk mitigation strategies
           - Next steps for stakeholders
        
        Please structure your response clearly and reference specific elements from the diagram.
        """

    def getWikiPrompt(self, wiki_documents: List[Dict[str, Any]], question: str):
        """Enhanced prompt for wiki document analysis with multiple sources"""

        # Format wiki documents for better context
        formatted_context = self._format_wiki_context(wiki_documents)

        return f"""
        ENTERPRISE DOCUMENTATION ANALYSIS:
        
        KNOWLEDGE BASE SOURCES:
        {formatted_context}
        
        USER QUESTION: {question}
        
        ANALYSIS REQUIREMENTS:
        Please provide a comprehensive response that:
        
        1. **Executive Summary** (2-3 sentences)
           - Direct answer to the user's question
           - Key findings from the documentation
        
        2. **Detailed Analysis**
           - Specific information from the documentation
           - Step-by-step procedures when applicable
           - Technical specifications or requirements
           - Dependencies and prerequisites
        
        3. **Source Citations**
           - Reference specific documents by name
           - Quote exact text for critical information
           - Format: [Source: Document_Name, Section: Header]
        
        4. **Action Items**
           - Next steps for implementation
           - Required approvals or stakeholder involvement
           - Tools or systems that need to be accessed
           - Timeline considerations
        
        5. **Related Information**
           - Connected processes or procedures
           - Additional resources mentioned
           - Cross-references to other documentation
        
        6. **Knowledge Gaps**
           - Information not found in current documentation
           - Suggested documentation improvements
           - Areas requiring subject matter expert consultation
        
        QUALITY INDICATORS:
        - Include specific file paths, URLs, or repository references
        - Mention team contacts or process owners
        - Provide examples from actual configurations or code
        - Reference version information where applicable
        """

    def _format_wiki_context(self, wiki_documents: List[Dict[str, Any]]) -> str:
        """Format wiki documents for enhanced LLM understanding"""
        if not wiki_documents:
            return "No wiki documents available."

        formatted_sections = []
        for i, doc in enumerate(wiki_documents, 1):
            content = doc.get("contents", "")
            files_count = doc.get("files_with_matches", 0)
            matches_count = doc.get("total_matches", 0)

            section = f"""
            === DOCUMENTATION SOURCE {i} ===
            Content Summary: {files_count} files with {matches_count} relevant matches
            
            Documentation Content:
            {content}
            
            === END SOURCE {i} ===
            """
            formatted_sections.append(section)

        return "\n".join(formatted_sections)

    def getPromptRules(self):
        """Enhanced analysis rules for consistent high-quality responses"""
        return """
        # COMPREHENSIVE ANALYSIS RULES
        
        ## Content Standards
        - Base all answers strictly on provided documentation and visual content
        - If information is not available, explicitly state "Information not found in provided sources"
        - Provide specific, actionable information with clear next steps
        - Use professional but accessible language
        - Structure responses with clear headings and bullet points
        
        ## Citation Requirements
        - Always cite specific sources for all claims
        - Include document names, section headers, or visual element references
        - Quote exact text for critical procedures or specifications
        - Format citations consistently: [Source: Document_Name.md, Section: Header]
        
        ## Technical Accuracy
        - Preserve technical terminology and specifications exactly
        - Include version numbers, file paths, and system requirements
        - Note any prerequisites or dependencies clearly
        - Highlight potential compatibility or integration issues
        
        ## Response Format
        - Convert responses to structured HTML markdown format
        - Use semantic HTML tags appropriately:
          - <h1>, <h2>, <h3> for hierarchical headers
          - <b> for emphasis and key terms
          - <i> for technical terms or file names
          - <ul> and <li> for unordered lists
          - <ol> and <li> for sequential procedures
          - <code> for code snippets or commands
          - <pre> for multi-line code blocks
          - <a href=""> for links and references
          - <blockquote> for direct quotes from documentation
        
        ## Quality Assurance
        - Cross-reference information across multiple sources when available
        - Identify and note any conflicting information
        - Suggest documentation updates when gaps are identified
        - Include confidence indicators for recommendations
        - Provide context for decision-making criteria
        
        ## Error Prevention
        - Never fabricate information not present in sources
        - Avoid speculation beyond what's documented
        - Flag outdated information with timestamps when possible
        - Recommend verification steps for critical implementations
        """
