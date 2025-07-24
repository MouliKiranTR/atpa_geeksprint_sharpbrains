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
        
        # Concise system context
        base_context = """
You are an expert Technical Analyst specializing in architecture, 
design, and system analysis. Analyze visual content and provide 
actionable insights.

CORE CAPABILITIES:
- System Architecture & Component Analysis
- Process Flow & Workflow Documentation  
- Technical Design & Integration Patterns
- Data Flow & Security Architecture
- Performance & Scalability Assessment

RESPONSE APPROACH:
- Executive summary with key findings
- Visual content analysis with specific references
- Technical insights and recommendations
- Clear, structured markdown formatting
- Actionable next steps
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
        
        # Concise analysis instructions
        type_instructions = {
            "design": (
                "🎨 DESIGN FOCUS: UI/UX patterns, visual hierarchy, "
                "accessibility, design recommendations"
            ),
            "workflow": (
                "⚡ WORKFLOW FOCUS: Process flows, bottlenecks, "
                "user journeys, optimization opportunities"
            ), 
            "integration": (
                "🔗 INTEGRATION FOCUS: System connections, "
                "API patterns, data flows, architecture relationships"
            ),
            "architecture": (
                "🏗️ ARCHITECTURE FOCUS: Component mapping, "
                "data flows, scalability, security, technical debt"
            ),
            "general": (
                "📊 GENERAL FOCUS: Comprehensive overview, "
                "key insights, actionable recommendations"
            )
        }
        
        analysis_instruction = type_instructions.get(
            analysis_type, type_instructions["general"]
        )
        
        # Construct final prompt with enhanced markdown instructions
        final_prompt = f"""
        {base_context}
        
        {analysis_instruction}
        
        {visual_context}
        
        USER QUESTION:
        {user_question}
        
        📝 MARKDOWN RESPONSE FORMAT:
        
        Structure: ## 📋 Executive Summary | ## 🔍 Visual Analysis | 
        ## 🏗️ Key Findings | ## 💡 Recommendations | ## 🔗 Next Steps
        
        Format: Use ## headers with emojis, **bold** for emphasis, 
        `code` for technical terms, - for bullets, > for insights
        
        🔍 ANALYZE VISUAL CONTENT: If base64 data provided above, 
        examine diagrams thoroughly and reference specific elements, 
        components, flows, and patterns you observe.
        
        Provide comprehensive markdown analysis addressing the user's question.
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
            
        visual_content_section = "\n\nVISUAL ATTACHMENTS FOR ANALYSIS:\n"
        visual_content_section += "="*60 + "\n"
        
        for i, item in enumerate(visual_data, 1):
            if not item.get("success"):
                continue
                
            # Add base64 image data if available
            base64_data = item.get("screenshot_base64")
            if base64_data:
                source = item.get('source', 'unknown').upper()
                title = (
                    item.get('diagram_title') or 
                    item.get('file_name') or 
                    f"{source} Content"
                )
                
                visual_content_section += (
                    f"\n📊 VISUAL ATTACHMENT {i}: {title}\n"
                )
                visual_content_section += f"Source: {source}\n"
                visual_content_section += "Data Type: Image/Diagram\n"
                visual_content_section += (
                    f"Size: {len(base64_data)} characters\n"
                )
                
                # Include optimized base64 data for AI analysis
                # Limit to ~15KB per image to stay within 32KB WebSocket limit
                max_base64_length = 15000
                if len(base64_data) > max_base64_length:
                    truncated_data = base64_data[:max_base64_length]
                    visual_content_section += (
                        "\nImage Data (Base64 - Truncated):\n"
                    )
                    visual_content_section += f"{truncated_data}\n"
                    visual_content_section += (
                        f"[TRUNCATED: Showing {max_base64_length} of "
                        f"{len(base64_data)} total characters]\n"
                    )
                else:
                    visual_content_section += "\nImage Data (Base64):\n"
                    visual_content_section += f"{base64_data}\n"
                visual_content_section += "-" * 40 + "\n"
        
        if visual_content_section.count("📊 VISUAL ATTACHMENT") > 0:
            visual_content_section += (
                "\n🔍 ANALYSIS INSTRUCTION: Please carefully examine all "
                "visual attachments above. The base64 encoded images contain "
                "important diagrams, screenshots, or visual content that "
                "should be analyzed in detail to answer the user's question.\n"
            )
        
        return visual_content_section
    
    def _optimize_prompt_size(
        self, 
        final_prompt: str, 
        visual_data: List[Dict[str, Any]]
    ) -> str:
        """
        Optimize prompt size if it exceeds WebSocket limits
        
        Args:
            final_prompt: The complete prompt
            visual_data: Original visual data for re-processing
            
        Returns:
            Optimized prompt that fits within size limits
        """
        max_size = 30000  # Leave 2KB buffer under 32KB limit
        
        if len(final_prompt.encode('utf-8')) <= max_size:
            return final_prompt
        
        print("🔧 Optimizing prompt size for WebSocket transmission...")
        
        # Try reducing base64 data size further
        if visual_data:
            # Reduce base64 size more aggressively
            smaller_visual_content = (
                self._prepare_minimal_visual_content(visual_data)
            )
            
            # Rebuild prompt with smaller visual content
            base_prompt_parts = final_prompt.split(
                "\n\nVISUAL ATTACHMENTS FOR ANALYSIS:"
            )
            if len(base_prompt_parts) > 1:
                optimized_prompt = (
                    base_prompt_parts[0] + smaller_visual_content
                )
                
                if len(optimized_prompt.encode('utf-8')) <= max_size:
                    print("✅ Prompt optimized successfully")
                    return optimized_prompt
        
        # If still too large, remove visual content and use metadata only
        metadata_only_prompt = final_prompt.split(
            "\n\nVISUAL ATTACHMENTS FOR ANALYSIS:"
        )[0]
        
        metadata_only_prompt += (
            "\n\n📋 VISUAL CONTENT SUMMARY:\n"
            "Visual attachments were too large for transmission. "
            "Analysis based on metadata only.\n"
        )
        
        print("⚠️ Using metadata-only analysis due to size constraints")
        return metadata_only_prompt
    
    def _prepare_minimal_visual_content(
        self, 
        visual_data: List[Dict[str, Any]]
    ) -> str:
        """
        Prepare minimal visual content for size-constrained scenarios
        """
        visual_content_section = "\n\nVISUAL ATTACHMENTS (MINIMAL):\n"
        visual_content_section += "="*40 + "\n"
        
        for i, item in enumerate(visual_data, 1):
            if not item.get("success"):
                continue
                
            base64_data = item.get("screenshot_base64")
            if base64_data:
                source = item.get('source', 'unknown').upper()
                title = (
                    item.get('diagram_title') or 
                    item.get('file_name') or 
                    f"{source} Content"
                )
                
                visual_content_section += f"📊 {i}: {title}\n"
                
                # Very small base64 sample (first 5KB only)
                mini_sample = base64_data[:5000]
                visual_content_section += f"Sample: {mini_sample}...\n"
                visual_content_section += (
                    f"[{len(base64_data)} chars total]\n\n"
                )
        
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
        
        # Monitor prompt size to avoid WebSocket frame limit (32KB)
        prompt_size = len(final_prompt.encode('utf-8'))
        prompt_size_kb = prompt_size / 1024
        
        print(f"📏 Prompt size: {prompt_size_kb:.1f}KB")
        
        if prompt_size > 30000:  # Warn if approaching 32KB limit
            print("⚠️ WARNING: Prompt size approaching WebSocket limit (32KB)")
        
        # Count visual attachments
        visual_count = final_prompt.count("📊 VISUAL ATTACHMENT")
        if visual_count > 0:
            print(f"📎 Sending {visual_count} visual attachments for analysis")
        
        ws = connect(url)
        ws.send(json.dumps(message))
        
        answer = ""
        cost_tracker = {}
        eof = False
        
        print("📨 Receiving analysis response...")
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
            initial_prompt = base_prompt + visual_content
            
            # Optimize prompt size for WebSocket transmission
            final_prompt = self._optimize_prompt_size(
                initial_prompt, visual_data
            )
            
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
        
        # Only add metadata if the AI didn't generate proper headers
        if (not markdown_content.startswith('##') and 
                not markdown_content.startswith('# ')):
            title = self._generate_title(analysis_type)
            metadata_section = f"""# {title}

**Query:** {user_question}
**Generated:** {self._get_current_timestamp()}

---

"""
            markdown_content = metadata_section + markdown_content
        
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