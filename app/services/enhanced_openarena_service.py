"""
Enhanced OpenArena Service for visual content analysis
"""

import requests
from typing import Dict, Any, List, Optional
from app.utils.openarena_authenticator import OpenArenaAuthenticator
import os


class EnhancedOpenArenaService:
    """Enhanced service for visual content analysis using OpenArena"""
    
    def __init__(self):
        self.auth = OpenArenaAuthenticator()
        self.workflow_id = "592081d1-0a6e-4b5f-93b1-a08a674bf4bc"
        self.base_url = (
            "https://aiopenarena.gcs.int.thomsonreuters.com/v1/inference"
        )
    
    def _create_visual_analysis_prompt(
        self, 
        user_question: str,
        visual_data: List[Dict[str, Any]],
        analysis_type: str = "general"
    ) -> str:
        """
        Create a specialized prompt for visual content analysis
        
        Args:
            user_question: User's original question
            visual_data: List of visual content with metadata
            analysis_type: Type of analysis (general, design, workflow, etc.)
            
        Returns:
            Formatted prompt for OpenArena
        """
        
        # Base system context
        base_context = """
You are an expert Onboarding Knowledge Agent designed to help new team members, 
users, and stakeholders understand systems, processes, and organizational 
knowledge.

CORE CAPABILITIES:
- System Architecture Analysis: Understand and explain technical systems, 
  data flows, and integration points
- Process Documentation: Break down workflows, procedures, and business 
  processes
- Knowledge Synthesis: Connect information across different sources and formats
- Contextual Guidance: Provide relevant, actionable advice based on specific 
  situations
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
- For process queries: Emphasize workflows, dependencies, and decision points
- For general onboarding: Provide comprehensive overviews with learning paths
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
                available_text = f"- Screenshot Available: {screenshot_available}\n"
                visual_context += available_text
                
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
                available_text = f"- Screenshot Available: {screenshot_available}\n"
                visual_context += available_text
            
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
    
    async def analyze_visual_content(
        self,
        user_question: str,
        visual_data: List[Dict[str, Any]],
        analysis_type: str = "general",
        include_screenshots: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze visual content using OpenArena with file attachments
        
        Args:
            user_question: User's question about the visual content
            visual_data: List of captured visual content (with file_path or base64)
            analysis_type: Type of analysis to perform
            include_screenshots: Whether to include screenshot data
            
        Returns:
            Analysis result from OpenArena
        """
        temp_files_to_cleanup = []
        
        try:
            # Get authentication token
            openarena_token = self.auth.authenticate_and_get_token()
            
            if not openarena_token:
                return {
                    "success": False,
                    "error": "Failed to authenticate with OpenArena"
                }
            
            # Create the analysis prompt with embedded visual data
            analysis_prompt = self._create_visual_analysis_prompt(
                user_question, visual_data, analysis_type
            )
            
            # Prepare headers for multipart request
            headers = {
                'Authorization': f'Bearer {openarena_token}',
                # Don't set Content-Type - let requests handle multipart
            }
            
            # Prepare files for attachment if available
            files_dict = {}
            if include_screenshots and visual_data:
                files_dict = self._prepare_attachment_files(
                    visual_data, temp_files_to_cleanup
                )
            
            # Make API request - OpenArena may not support multipart, so use base64 fallback
            if files_dict:
                print(f"📎 Processing {len(files_dict)} file attachments for OpenArena")
                
                # Convert files to base64 and embed in prompt
                enhanced_prompt = analysis_prompt + "\n\nVISUAL CONTENT:\n"
                
                for file_key, (filename, file_handle, content_type) in files_dict.items():
                    try:
                        # Read file content and encode as base64
                        file_handle.seek(0)  # Reset file pointer
                        file_content = file_handle.read()
                        import base64
                        encoded_content = base64.b64encode(file_content).decode('utf-8')
                        
                        enhanced_prompt += f"\n{filename}: [Image data: {len(file_content)} bytes]\n"
                        enhanced_prompt += f"Base64: {encoded_content[:100]}...\n"
                        
                        # Close file handle
                        file_handle.close()
                        
                    except Exception as e:
                        print(f"Error processing file {filename}: {e}")
                
                # Use JSON request with enhanced prompt
                headers['Content-Type'] = 'application/json'
                json_payload = {
                    "workflow_id": self.workflow_id,
                    "query": enhanced_prompt,
                    "is_persistence_allowed": True,
                    "modelparams": {
                        "anthropic_direct.claude-v4-sonnet": {
                            "temperature": "0.3",
                            "top_p": "0.9",
                            "max_tokens": "63999",
                            "top_k": "250",
                            "system_prompt": (
                                "You are an expert visual content analyst and "
                                "technical consultant. "
                                "Analyze the provided images (base64 encoded) and provide "
                                "detailed, structured analysis with clear "
                                "summaries, "
                                "actionable insights, and practical recommendations."
                                "Always include a brief executive summary at start."
                            ),
                            "enable_reasoning": "true",
                            "budget_tokens": "35425"
                        }
                    }
                }
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=json_payload,
                    timeout=120
                )
                
            else:
                # Fallback to JSON request without files
                headers['Content-Type'] = 'application/json'
                json_payload = {
                    "workflow_id": self.workflow_id,
                    "query": analysis_prompt,
                    "is_persistence_allowed": True,
                    "modelparams": {
                        "anthropic_direct.claude-v4-sonnet": {
                            "temperature": "0.3",
                            "top_p": "0.9",
                            "max_tokens": "63999",
                            "top_k": "250",
                            "system_prompt": (
                                "You are an expert visual content analyst and "
                                "technical consultant. "
                                "Provide detailed, structured analysis with clear "
                                "summaries, "
                                "actionable insights, and practical recommendations."
                                "Always include a brief executive summary at start."
                            ),
                            "enable_reasoning": "true",
                            "budget_tokens": "35425"
                        }
                    }
                }
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=json_payload,
                    timeout=120
                )
            
            status_code = response.status_code
            print(f"OpenArena Visual Analysis Response Status: {status_code}")
            
            if response.status_code == 200:
                ai_response = response.json()
                
                analysis_result = ai_response.get('result', {}).get(
                    'answer', {}
                ).get('anthropic_direct.claude-v4-sonnet', '')
                
                cost = ai_response.get('result', {}).get(
                    'cost_track', {}
                ).get('total_cost', None)
                
                print("💬 Visual Analysis Complete")
                print("💲 Estimated Analysis Cost:", cost)
                
                # Add executive summary if not present
                enhanced_analysis = self._enhance_analysis_with_summary(
                    analysis_result, user_question, analysis_type
                )
                
                # Count attached files vs screenshots
                files_attached = len(files_dict) if files_dict else 0
                screenshots_included = 0
                if include_screenshots:
                    screenshots_included = len([
                        item for item in visual_data 
                        if item.get("success") and (
                            item.get("file_path") or item.get("screenshot_base64")
                        )
                    ])
                
                return {
                    "success": True,
                    "analysis": enhanced_analysis,
                    "cost": cost,
                    "analysis_type": analysis_type,
                    "visual_items_processed": len(visual_data),
                    "files_attached": files_attached,
                    "screenshots_included": screenshots_included
                }
            else:
                error_text = response.text
                error_msg = f"OpenArena Error: {response.status_code}, {error_text}"
                print(f"⚠️ {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            print(f"🚨 Failed to analyze visual content: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            # Clean up any temporary files created from base64 data
            if temp_files_to_cleanup:
                self._cleanup_temp_files(temp_files_to_cleanup)
    
    def _create_visual_data_summary(
        self, visual_data: List[Dict[str, Any]]
    ) -> str:
        """Create a text summary of visual data for inclusion in prompt"""
        summary_parts = []
        
        for i, item in enumerate(visual_data, 1):
            if not item.get("success"):
                continue
                
            source = item.get("source", "unknown")
            summary_parts.append(f"Item {i} ({source.upper()}):")
            
            if source == "figma":
                file_name = item.get('file_name', 'Unknown')
                summary_parts.append(f"  - File: {file_name}")
                summary_parts.append(f"  - Key: {item.get('file_key', 'N/A')}")
                metadata = item.get("metadata", {})
                if metadata:
                    pages = metadata.get('pages', 'N/A')
                    summary_parts.append(f"  - Pages: {pages}")
                    last_modified = metadata.get('last_modified', 'N/A')
                    summary_parts.append(f"  - Last Modified: {last_modified}")
                    
            elif source == "lucid":
                diagram_title = item.get('diagram_title', 'Unknown')
                summary_parts.append(f"  - Diagram: {diagram_title}")
                diagram_id = item.get('diagram_id', 'N/A')
                summary_parts.append(f"  - ID: {diagram_id}")
                
            elif source == "documents":
                summary_parts.append("  - Document Context Available")
                metadata = item.get("metadata", {})
                if metadata.get("context_preview"):
                    preview = metadata['context_preview'][:200]
                    summary_parts.append(f"  - Preview: {preview}...")
                    
            elif source == "query_analysis":
                summary_parts.append("  - Analysis Context Available")
                metadata = item.get("metadata", {})
                query_type = metadata.get('query_type', 'N/A')
                summary_parts.append(f"  - Query Type: {query_type}")
                
            capture_method = item.get("capture_method", "unknown")
            summary_parts.append(f"  - Method: {capture_method}")
            summary_parts.append("")
        
        return "\n".join(summary_parts)
    
    def _enhance_analysis_with_summary(
        self, 
        analysis: str, 
        user_question: str, 
        analysis_type: str
    ) -> str:
        """Enhance analysis with executive summary if not present"""
        
        # Check if analysis already has a summary section
        lower_analysis = analysis.lower()
        has_summary = (
            "executive summary" in lower_analysis or 
            "## summary" in lower_analysis
        )
        if has_summary:
            return analysis
        
        # Create executive summary
        summary = f"""## 📋 Executive Summary

**Query**: {user_question}
**Analysis Type**: {analysis_type.title()} Analysis

**Key Findings**:
- Visual content search completed across Figma, Lucid, and document sources
- Analysis provided based on available metadata and contextual information
- Actionable recommendations generated for next steps

**Immediate Actions Recommended**:
1. Review the detailed analysis below
2. Consider creating visual documentation as suggested
3. Implement recommended architecture patterns
4. Follow up with specific technical questions as needed

---

"""
        
        # Prepend summary to existing analysis
        return summary + analysis

    def determine_analysis_type(self, user_question: str) -> str:
        """
        Determine the appropriate analysis type based on user question
        
        Args:
            user_question: User's question
            
        Returns:
            Analysis type string
        """
        question_lower = user_question.lower()
        
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
        
        # Integration-related keywords
        integration_keywords = [
            "integration", "connect", "api", "data flow", "system", 
            "architecture", "database", "service", "endpoint", "sync", 
            "communication"
        ]
        
        # Check for keyword matches
        if any(keyword in question_lower for keyword in design_keywords):
            return "design"
        elif any(keyword in question_lower for keyword in workflow_keywords):
            return "workflow"
        elif any(
            keyword in question_lower for keyword in integration_keywords
        ):
            return "integration"
        else:
            return "general"

    def _prepare_attachment_files(
        self, 
        visual_data: List[Dict[str, Any]], 
        temp_files_to_cleanup: List[str]
    ) -> Dict[str, Any]:
        """
        Prepare files for attachment to OpenArena request
        
        Args:
            visual_data: List of visual content data
            temp_files_to_cleanup: List to track temporary files for cleanup
            
        Returns:
            Dictionary of files for requests.post files parameter
        """
        files_dict = {}
        
        for i, item in enumerate(visual_data):
            if not item.get("success"):
                continue
            
            file_path = item.get("file_path")
            base64_data = item.get("screenshot_base64")
            source = item.get("source", "unknown")
            
            # Use file_path if available, otherwise create temp file from base64
            if file_path and os.path.exists(file_path):
                try:
                    file_handle = open(file_path, 'rb')
                    filename = os.path.basename(file_path)
                    files_dict[f'attachment_{i}_{source}'] = (
                        filename, file_handle, 'image/png'
                    )
                    print(f"📎 Attached file: {filename}")
                except Exception as e:
                    print(f"⚠️ Failed to attach file {file_path}: {e}")
                    
            elif base64_data:
                # Create temporary file from base64 data
                temp_file_path = self._create_temp_file_from_base64(
                    base64_data, i, source
                )
                if temp_file_path:
                    temp_files_to_cleanup.append(temp_file_path)
                    try:
                        file_handle = open(temp_file_path, 'rb')
                        filename = os.path.basename(temp_file_path)
                        files_dict[f'attachment_{i}_{source}'] = (
                            filename, file_handle, 'image/png'
                        )
                        print(f"📎 Attached temp file: {filename}")
                    except Exception as e:
                        print(f"⚠️ Failed to attach temp file {temp_file_path}: {e}")
        
        return files_dict
    
    def _create_temp_file_from_base64(
        self, 
        base64_data: str, 
        index: int, 
        source: str
    ) -> Optional[str]:
        """Create temporary file from base64 data"""
        try:
            import tempfile
            import base64
            
            # Decode base64 data
            image_data = base64.b64decode(base64_data)
            
            # Create temporary file
            temp_fd, temp_path = tempfile.mkstemp(
                suffix='.png', 
                prefix=f'{source}_{index}_'
            )
            
            # Write image data to temporary file
            with os.fdopen(temp_fd, 'wb') as temp_file:
                temp_file.write(image_data)
            
            return temp_path
            
        except Exception as e:
            print(f"⚠️ Failed to create temp file from base64: {e}")
            return None
    
    def _cleanup_temp_files(self, file_paths: List[str]) -> None:
        """Clean up temporary files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"🗑️ Cleaned up temp file: {file_path}")
            except Exception as e:
                print(f"⚠️ Failed to clean up {file_path}: {e}")


# Create service instance
enhanced_openarena_service = EnhancedOpenArenaService() 