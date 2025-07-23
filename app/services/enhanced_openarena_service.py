"""
Enhanced OpenArena Service for visual content analysis
"""

import json
from typing import Dict, Any, List
from datetime import datetime
from websockets.sync.client import connect
from app.utils.openarena_authenticator import OpenArenaAuthenticator


class EnhancedOpenArenaService:
    """Enhanced service for visual content analysis using OpenArena"""
    
    def __init__(self):
        self.auth = OpenArenaAuthenticator()
        self.workflow_id = "592081d1-0a6e-4b5f-93b1-a08a674bf4bc"
        self.base_url = (
            "https://aiopenarena.gcs.int.thomsonreuters.com/v1/inference"
        )
    
    def _create_unified_analysis_prompt(
        self, 
        user_question: str,
        visual_data: List[Dict[str, Any]],
        analysis_type: str = "general"
    ) -> str:
        """
        Create a unified prompt for any type of visual content analysis
        
        Args:
            user_question: User's original question
            visual_data: List of visual content with metadata
            analysis_type: Type of analysis (general, design, workflow, 
                          architecture, etc.)
            
        Returns:
            Formatted prompt for OpenArena
        """
        
        # Base system context
        base_context = """
You are an expert Onboarding Knowledge Agent designed to help new team 
members, users, and stakeholders understand systems, processes, and 
organizational knowledge.

CORE CAPABILITIES:
- System Architecture Analysis: Understand and explain technical systems, 
  data flows, and integration points
- Process Documentation: Break down workflows, procedures, and business 
  processes
- Knowledge Synthesis: Connect information across different sources and 
  formats
- Contextual Guidance: Provide relevant, actionable advice based on 
  specific situations
- Progressive Learning: Adapt explanations to user expertise level

ONBOARDING FOCUS AREAS:
1. TECHNICAL SYSTEMS
   - Architecture overviews and component relationships
   - API documentation and integration patterns
   - Database schemas and data models
   - Security protocols and access patterns
   - Development workflows and deployment processes

2. BUSINESS PROCESSES
   - Operational workflows and decision trees
   - Approval processes and escalation paths
   - Communication protocols and stakeholder mapping
   - Quality assurance and compliance procedures
   - Project management methodologies

3. ORGANIZATIONAL KNOWLEDGE
   - Team structures and responsibilities
   - Cultural norms and best practices
   - Tool ecosystems and technology stack
   - Documentation standards and knowledge repositories
   - Training resources and learning paths

RESPONSE GUIDELINES:
- Start with a clear executive summary for complex topics
- Provide step-by-step breakdowns for processes
- Include relevant context and background information
- Offer multiple perspectives when applicable
- Suggest next steps and follow-up resources
- Use clear headings and structured formatting
- Include practical examples and use cases
- Identify knowledge gaps and recommend documentation improvements

ADAPTATION STRATEGIES:
- For technical queries: Focus on architecture, APIs, and implementation 
  details
- For process queries: Emphasize workflows, dependencies, and decision 
  points
- For general onboarding: Provide comprehensive overviews with learning 
  paths
- For specific problems: Offer targeted solutions with context

QUALITY STANDARDS:
- Accurate and up-to-date information
- Clear, jargon-free explanations with technical terms defined
- Actionable recommendations and next steps
- Structured presentation with visual aids when helpful
- Cross-references to related systems and processes
        """
        
        # Create context about the visual content
        visual_context = "\n\nVISUAL CONTENT ANALYSIS:\n"
        visual_context += "="*50 + "\n\n"
        
        for i, item in enumerate(visual_data, 1):
            if not item.get("success"):
                error_msg = item.get('error', 'Unknown error')
                visual_context += (
                    f"Item {i}: Failed to capture - {error_msg}\n\n"
                )
                continue
                
            source = item.get("source", "unknown")
            
            if source == "figma":
                visual_context += f"FIGMA FILE {i}:\n"
                file_name = item.get('file_name', 'Unknown')
                visual_context += f"- File Name: {file_name}\n"
                file_key = item.get('file_key', 'Unknown')
                visual_context += f"- File Key: {file_key}\n"
                
                metadata = item.get("metadata", {})
                if metadata:
                    doc_name = metadata.get('document_name', 'N/A')
                    visual_context += f"- Document Name: {doc_name}\n"
                    last_mod = metadata.get('last_modified', 'N/A')
                    visual_context += f"- Last Modified: {last_mod}\n"
                    version = metadata.get('version', 'N/A')
                    visual_context += f"- Version: {version}\n"
                    pages = metadata.get('pages', 'N/A')
                    visual_context += f"- Number of Pages: {pages}\n"
                    description = metadata.get('description', 'N/A')
                    visual_context += f"- Description: {description}\n"
                
                capture_method = item.get('capture_method', 'Unknown')
                visual_context += f"- Capture Method: {capture_method}\n"
                screenshot_available = (
                    'Yes' if item.get('screenshot_base64') else 'No'
                )
                visual_context += (
                    f"- Screenshot Available: {screenshot_available}\n"
                )
                
            elif source == "lucid":
                visual_context += f"LUCID DIAGRAM {i}:\n"
                diagram_title = item.get('diagram_title', 'Unknown')
                visual_context += f"- Diagram Title: {diagram_title}\n"
                diagram_id = item.get('diagram_id', 'Unknown')
                visual_context += f"- Diagram ID: {diagram_id}\n"
                
                metadata = item.get("metadata", {})
                if metadata:
                    export_id = metadata.get('export_id', 'N/A')
                    visual_context += f"- Export ID: {export_id}\n"
                    format_type = metadata.get('format', 'N/A')
                    visual_context += f"- Format: {format_type}\n"
                    scale = metadata.get('scale', 'N/A')
                    visual_context += f"- Scale: {scale}\n"
                
                capture_method = item.get('capture_method', 'Unknown')
                visual_context += f"- Capture Method: {capture_method}\n"
                screenshot_available = (
                    'Yes' if item.get('screenshot_base64') else 'No'
                )
                visual_context += (
                    f"- Screenshot Available: {screenshot_available}\n"
                )
            
            visual_context += "\n"
        
        # Analysis type specific instructions
        type_instructions = {
            "design": """
            DESIGN ANALYSIS FOCUS:
            - Evaluate visual hierarchy, typography, color schemes, and layout
            - Assess accessibility and usability principles
            - Identify design patterns and component usage
            - Analyze information architecture and content organization
            - Provide recommendations for design improvements
            - If no visual content available, suggest design approaches and 
              best practices
            """,
            
            "workflow": """
            WORKFLOW ANALYSIS FOCUS:
            - Map out process flows and decision points
            - Identify bottlenecks, inefficiencies, or gaps in the workflow
            - Analyze user journey and interaction patterns
            - Assess process complexity and potential simplifications
            - Suggest process improvements and optimizations
            - If no visual content available, recommend workflow 
              documentation strategies
            """,
            
            "integration": """
            INTEGRATION ANALYSIS FOCUS:
            - Identify data flows and system connections
            - Analyze integration points and dependencies
            - Assess API connections and data exchange patterns
            - Evaluate system architecture and technical relationships
            - Provide recommendations for better integration
            - If no visual content available, suggest architecture 
              documentation approaches
            """,

            "architecture": """
            ARCHITECTURE ANALYSIS FOCUS:
            - Complete component inventory and relationship mapping
            - End-to-end data flow and process analysis
            - Technology stack evaluation and optimization
            - Security architecture and compliance frameworks
            - Scalability, performance, and reliability analysis
            - Design decision rationale and trade-off analysis
            - Architectural debt and technical risk evaluation
            - Modernization and refactoring recommendations
            """,
            
            "general": """
            GENERAL ANALYSIS FOCUS:
            - Provide comprehensive overview of the visual content
            - Identify key elements, patterns, and relationships
            - Analyze purpose, functionality, and effectiveness
            - Highlight important insights and observations
            - Offer relevant recommendations and next steps
            - If no visual content available, provide guidance on content 
              creation
            """
        }
        
        analysis_instruction = type_instructions.get(
            analysis_type, type_instructions["general"]
        )
        
        # Construct final prompt
        final_prompt = f"""
        {base_context}
        
        {analysis_instruction}
        
        {visual_context}
        
        USER QUESTION:
        {user_question}
        
        ANALYSIS INSTRUCTIONS:
        1. Carefully analyze all provided visual content and metadata
        2. Focus on answering the user's specific question
        3. Provide detailed insights based on what you can observe
        4. Include specific examples and references to the visual elements
        5. Offer actionable recommendations when appropriate
        6. Structure your response clearly with headings and bullet points
        7. If visual content is not available, base your analysis on metadata
        
        Please provide a comprehensive analysis addressing the user's question.
        """
        
        return final_prompt.strip()
    
    def _prepare_visual_content_for_prompt(
        self, 
        visual_data: List[Dict[str, Any]]
    ) -> str:
        """
        Prepare visual content for inclusion in the prompt
        
        Args:
            visual_data: List of visual content data
            
        Returns:
            Formatted visual content section for prompt
        """
        if not visual_data:
            return ""
            
        visual_content_section = "\n\nVISUAL CONTENT:\n"
        
        for i, item in enumerate(visual_data, 1):
            if not item.get("success"):
                continue
                
            # Add base64 image data if available
            base64_data = item.get("screenshot_base64")
            if base64_data:
                filename = f"{item.get('source', 'unknown')}_{i}"
                visual_content_section += (
                    f"\n{filename}: [Image data: "
                    f"{len(base64_data)} characters]\n"
                )
                visual_content_section += f"Base64: {base64_data[:100]}...\n"
        
        return visual_content_section
    
    def _query_openarena_websocket(
        self, 
        final_prompt: str
    ) -> tuple[str, Dict[str, Any]]:
        """
        Query OpenArena using WebSocket connection
        
        Args:
            final_prompt: The complete prompt to send
            
        Returns:
            Tuple of (answer, cost_tracker)
        """
        token = self.auth.authenticate_and_get_token()
        url = (
            f"wss://wymocw0zke.execute-api.us-east-1.amazonaws.com/prod/"
            f"?Authorization={token}"
        )
        
        message = {
            "action": "SendMessage",
            "workflow_id": self.workflow_id,
            "query": final_prompt,
            "is_persistence_allowed": True
        }
        
        print("🔗 Connecting to OpenArena via WebSocket...")
        ws = connect(url)
        ws.send(json.dumps(message))
        
        answer = ""
        cost_tracker = {}
        eof = False
        
        while not eof:
            message = ws.recv()
            message_data = json.loads(message)
            
            for model, value in message_data.items():
                if "answer" in value:
                    answer += value["answer"]
                elif "cost_track" in value:
                    cost_tracker = value['cost_track']
                    eof = True
        
        ws.close()
        return answer, cost_tracker

    async def analyze_content(
        self,
        user_question: str,
        visual_data: List[Dict[str, Any]],
        analysis_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Unified method to analyze visual content using OpenArena
        
        Args:
            user_question: User's question about the visual content
            visual_data: List of captured visual content from all sources
            analysis_type: Type of analysis to perform
            
        Returns:
            Analysis result from OpenArena
        """
        try:
            # Get authentication token
            openarena_token = self.auth.authenticate_and_get_token()
            
            if not openarena_token:
                return {
                    "success": False,
                    "error": "Failed to authenticate with OpenArena"
                }
            
            # Create the unified analysis prompt
            base_prompt = self._create_unified_analysis_prompt(
                user_question, visual_data, analysis_type
            )
            
            # Add visual content to prompt if available
            visual_content = self._prepare_visual_content_for_prompt(
                visual_data
            )
            final_prompt = base_prompt + visual_content
            
            print(f"📊 Processing {len(visual_data)} visual items")
            print(f"🎯 Analysis type: {analysis_type}")
            
            # Make single call to OpenArena
            answer, cost_tracker = self._query_openarena_websocket(
                final_prompt
            )
            
            if answer:
                cost = cost_tracker.get('total_cost', None)
                
                print("✅ OpenArena Analysis Complete")
                print(f"💲 Estimated Cost: {cost}")
                
                # Format as proper markdown for frontend
                markdown_analysis = self._format_as_markdown(
                    answer, user_question, analysis_type
                )
                
                # Count processed items
                successful_items = len([
                    item for item in visual_data 
                    if item.get("success")
                ])
                
                return {
                    "success": True,
                    "analysis": markdown_analysis,
                    "content_type": "markdown",
                    "cost": cost,
                    "analysis_type": analysis_type,
                    "visual_items_processed": len(visual_data),
                    "successful_items": successful_items
                }
            else:
                return {
                    "success": False,
                    "error": "No response received from OpenArena"
                }
                
        except Exception as e:
            print(f"🚨 Failed to analyze content: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def determine_analysis_type(self, user_question: str) -> str:
        """
        Determine the appropriate analysis type based on user question
        
        Args:
            user_question: User's question
            
        Returns:
            Analysis type string
        """
        question_lower = user_question.lower()
        
        # Architecture-related keywords
        architecture_keywords = [
            "architecture", "system", "component", "integration", "data flow",
            "database", "service", "endpoint", "api", "technical", "design",
            "structure", "pattern"
        ]
        
        # Design-related keywords
        design_keywords = [
            "design", "ui", "ux", "interface", "layout", "color", "typography",
            "visual", "style", "component", "accessibility", "usability"
        ]
        
        # Workflow-related keywords
        workflow_keywords = [
            "workflow", "process", "flow", "step", "procedure", "journey",
            "path", "sequence", "order", "stages", "phases"
        ]
        
        # Check for keyword matches (architecture first as it's most specific)
        if any(
            keyword in question_lower for keyword in architecture_keywords
        ):
            return "architecture"
        elif any(keyword in question_lower for keyword in design_keywords):
            return "design"
        elif any(
            keyword in question_lower for keyword in workflow_keywords
        ):
            return "workflow"
        else:
            return "general"

    def _format_as_markdown(
        self, 
        content: str, 
        user_question: str, 
        analysis_type: str
    ) -> str:
        """
        Format the analysis content as proper markdown for frontend display
        
        Args:
            content: Raw analysis content
            user_question: Original user question
            analysis_type: Type of analysis performed
            
        Returns:
            Properly formatted markdown content
        """
        
        # Clean up and ensure proper markdown formatting
        markdown_content = content.strip()
        
        # Ensure proper spacing around headers
        import re
        
        # Fix header spacing
        markdown_content = re.sub(r'\n(#{1,6})', r'\n\n\1', markdown_content)
        markdown_content = re.sub(
            r'(#{1,6}[^\n]+)\n(?!\n)', 
            r'\1\n\n', 
            markdown_content
        )
        
        # Ensure proper list formatting
        markdown_content = re.sub(
            r'\n(-|\*|\d+\.)\s', 
            r'\n\n\1 ', 
            markdown_content
        )
        
        # Fix multiple consecutive newlines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        # Add metadata section at the top if not present
        if not markdown_content.startswith('# '):
            title = self._generate_title(analysis_type)
            metadata_section = f"""# {title}

**Analysis Type:** {analysis_type.title()}
**Query:** {user_question}
**Generated:** {self._get_current_timestamp()}

---

"""
            markdown_content = metadata_section + markdown_content
        
        # Add footer with helpful information
        footer = self._generate_markdown_footer(analysis_type)
        markdown_content += footer
        
        return markdown_content.strip()
    
    def _generate_title(self, analysis_type: str) -> str:
        """Generate an appropriate title for the analysis"""
        
        titles = {
            "architecture": "🏗️ Architecture Analysis",
            "design": "🎨 Design Analysis", 
            "workflow": "⚡ Workflow Analysis",
            "integration": "🔗 Integration Analysis",
            "general": "📊 Visual Content Analysis"
        }
        
        return titles.get(analysis_type, "📊 Content Analysis")
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in readable format"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    def _generate_markdown_footer(self, analysis_type: str) -> str:
        """Generate helpful footer information"""
        
        footer = f"""

---

## 🔗 Next Steps

Based on this {analysis_type} analysis, consider:

1. **Review** the key findings and recommendations above
2. **Implement** high-priority suggestions that align with your goals
3. **Document** any decisions or changes made based on this analysis
4. **Follow up** with specific technical questions if needed

> 💡 **Tip:** This analysis is most effective when combined with 
> hands-on implementation and iterative feedback.

---

*Analysis generated by Enhanced OpenArena Service | 
{self._get_current_timestamp()}*
"""
        
        return footer


# Create service instance
enhanced_openarena_service = EnhancedOpenArenaService() 