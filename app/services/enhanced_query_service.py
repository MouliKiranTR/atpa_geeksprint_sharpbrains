"""
Enhanced Query Service that integrates Figma/Lucid search with visual analysis
"""

import asyncio
import time
from typing import Dict, Any, List
from app.services.figma_service import FigmaService
from app.services.lucid_service import LucidService
from app.services.visual_capture_service import visual_capture_service
from app.services.enhanced_openarena_service import enhanced_openarena_service
from app.services.data_source_service import data_source_service


class EnhancedQueryService:
    """Enhanced query service with visual content analysis"""
    
    def __init__(self):
        self.figma_service = FigmaService()
        self.lucid_service = LucidService()
    
    async def analyze_user_query(
        self,
        user_question: str,
        include_figma: bool = True,
        include_lucid: bool = True,
        include_documents: bool = True,
        max_visual_items: int = 3
    ) -> Dict[str, Any]:
        """
        Analyze user query and provide comprehensive response
        
        Args:
            user_question: User's question
            include_figma: Whether to search Figma files
            include_lucid: Whether to search Lucid diagrams
            include_documents: Whether to search uploaded documents
            max_visual_items: Maximum visual items to process
            
        Returns:
            Comprehensive analysis result
        """
        start_time = time.time()
        temp_files_to_cleanup = []
        
        try:
            # Determine if query is visual-related (expanded keyword list)
            visual_keywords = [
                "figma", "lucid", "design", "diagram", "workflow", "process",
                "visual", "interface", "ui", "ux", "chart", "flow", "mockup",
                "wireframe", "prototype", "layout", "screen", "page",
                "architecture", "system", "structure", "blueprint", "schema",
                "checkpoint", "flowchart", "map", "model", "framework",
                "dashboard", "visualization", "graphic", "drawing", "sketch"
            ]
            
            # Architecture-specific keywords for specialized analysis
            architecture_keywords = [
                "architecture", "system", "checkpoint", "component", "integration",
                "microservice", "api", "database", "network", "security", 
                "deployment", "infrastructure", "topology", "schema", 
                "pattern", "framework", "service", "endpoint", "data flow",
                "communication", "scalability", "performance", "design pattern"
            ]
            
            is_visual_query = any(
                keyword in user_question.lower() 
                for keyword in visual_keywords
            )
            
            # Check if this is specifically an architecture question
            is_architecture_query = any(
                keyword in user_question.lower() 
                for keyword in architecture_keywords
            )
            
            # Determine analysis approach
            analysis_approach = "architecture" if is_architecture_query else "general"
            
            results = {
                "is_visual_query": is_visual_query,
                "is_architecture_query": is_architecture_query,
                "analysis_approach": analysis_approach,
                "query_analysis": {
                    "original_question": user_question,
                    "analysis_type": (
                        enhanced_openarena_service.determine_analysis_type(
                            user_question
                        )
                    ),
                    "processing_time": 0
                },
                "search_results": {},
                "visual_analysis": None,
                "document_analysis": None,
                "combined_response": ""
            }
            
            # Search for relevant content
            search_tasks = []
            
            if include_figma and is_visual_query:
                search_tasks.append(self._search_figma_content(user_question))
            
            if include_lucid and is_visual_query:
                search_tasks.append(self._search_lucid_content(user_question))
            
            if include_documents:
                search_tasks.append(self._search_document_content(user_question))
            
            # Execute searches concurrently
            if search_tasks:
                search_results_list = await asyncio.gather(*search_tasks)
                
                # Process search results
                for result in search_results_list:
                    if result:
                        results["search_results"].update(result)
            
            # Process visual content if found
            visual_items = []
            if results["search_results"].get("figma_files"):
                for file in results["search_results"]["figma_files"][:max_visual_items]:
                    visual_items.append({
                        "type": "figma",
                        "id": file.key,
                        "name": file.name
                    })
            
            if results["search_results"].get("lucid_diagrams"):
                remaining_slots = max_visual_items - len(visual_items)
                for diagram in results["search_results"]["lucid_diagrams"][:remaining_slots]:
                    visual_items.append({
                        "type": "lucid", 
                        "id": diagram.id,
                        "name": diagram.title
                    })
            
            # Capture and analyze visual content
            if visual_items and is_visual_query:
                print(f"📷 Capturing and exporting {len(visual_items)} items to files...")
                
                # Use consolidated visual capture service for file exports
                visual_data = await visual_capture_service.capture_multiple_screenshots(
                    visual_items, export_to_files=True
                )
                
                # Track files for cleanup
                for item in visual_data:
                    if item.get("success") and item.get("file_path"):
                        temp_files_to_cleanup.append(item["file_path"])
                
                # Choose analysis method based on query type
                if is_architecture_query:
                    print("🏗️ Using specialized architecture analysis...")
                    
                    # Determine reasoning focus for architecture analysis
                    reasoning_focus = self._determine_architecture_reasoning_focus(
                        user_question
                    )
                    
                    visual_analysis = await enhanced_openarena_service.analyze_architecture_diagrams(
                        user_question=user_question,
                        visual_data=visual_data,
                        reasoning_focus=reasoning_focus,
                        include_screenshots=True
                    )
                else:
                    print("🔍 Using general visual analysis...")
                    # Use general visual analysis
                    visual_analysis = await enhanced_openarena_service.analyze_visual_content(
                        user_question=user_question,
                        visual_data=visual_data,
                        analysis_type=results["query_analysis"]["analysis_type"],
                        include_screenshots=True
                    )
                    print(f"🔍 DEBUG: Visual analysis result: {visual_analysis.get('success', 'No success key')}")
                    if not visual_analysis.get('success'):
                        print(f"🔍 DEBUG: Visual analysis error: {visual_analysis.get('error', 'No error info')}")
                
                results["visual_analysis"] = visual_analysis
                
                # Format combined response with visual analysis
                results["combined_response"] = await self._format_response_with_visual_analysis(
                    user_question=user_question,
                    search_results=results["search_results"],
                    visual_analysis=visual_analysis,
                    analysis_approach=analysis_approach
                )
                
            else:
                print("📝 No visual content found, or non-visual query...")
                
                # Create mock visual data with metadata for analysis
                mock_visual_data = []
                if results["search_results"].get("figma_files"):
                    for file in results["search_results"]["figma_files"][:max_visual_items]:
                        mock_visual_data.append({
                            "success": True,
                            "file_key": file.key,
                            "file_name": file.name,
                            "metadata": {
                                "name": file.name,
                                "last_modified": getattr(file, 'last_modified', 'Unknown'),
                                "thumbnail_url": getattr(file, 'thumbnail_url', ''),
                                "description": "Figma design file - no screenshot captured"
                            },
                            "source": "figma",
                            "capture_method": "metadata_only"
                        })
                
                if results["search_results"].get("lucid_diagrams"):
                    remaining_slots = max_visual_items - len(mock_visual_data)
                    for diagram in results["search_results"]["lucid_diagrams"][:remaining_slots]:
                        mock_visual_data.append({
                            "success": True,
                            "diagram_id": diagram.id,
                            "diagram_title": diagram.title,
                            "metadata": {
                                "title": diagram.title,
                                "product": getattr(diagram, 'product', 'Unknown'),
                                "url": getattr(diagram, 'url', ''),
                                "description": "Lucid diagram - no screenshot captured"
                            },
                            "source": "lucid",
                            "capture_method": "metadata_only"
                        })
                
                # Choose analysis method for metadata-only analysis
                if is_architecture_query:
                    print("🏗️ Using architecture analysis for metadata...")
                    
                    reasoning_focus = self._determine_architecture_reasoning_focus(
                        user_question
                    )
                    
                    visual_analysis = await enhanced_openarena_service.analyze_architecture_diagrams(
                        user_question=user_question,
                        visual_data=mock_visual_data,
                        reasoning_focus=reasoning_focus,
                        include_screenshots=False
                    )
                    print(f"🔍 DEBUG: Metadata architecture analysis result: {visual_analysis.get('success', 'No success key')}")
                    if not visual_analysis.get('success'):
                        print(f"🔍 DEBUG: Metadata architecture analysis error: {visual_analysis.get('error', 'No error info')}")
                else:
                    print("🔍 Using general visual analysis for metadata...")
                    # Use general visual analysis for metadata
                    visual_analysis = await enhanced_openarena_service.analyze_visual_content(
                        user_question=user_question,
                        visual_data=mock_visual_data,
                        analysis_type=results["query_analysis"]["analysis_type"],
                        include_screenshots=False
                    )
                    print(f"🔍 DEBUG: Metadata visual analysis result: {visual_analysis.get('success', 'No success key')}")
                    if not visual_analysis.get('success'):
                        print(f"🔍 DEBUG: Metadata visual analysis error: {visual_analysis.get('error', 'No error info')}")
                
                results["visual_analysis"] = visual_analysis
                
                # Format response with metadata analysis
                results["combined_response"] = await self._format_response_with_metadata_analysis(
                    user_question=user_question,
                    search_results=results["search_results"],
                    visual_analysis=visual_analysis,
                    analysis_approach=analysis_approach
                )
            
            # Process document content if available (but visual content not found)
            if results["search_results"].get("documents") and not results.get("visual_analysis"):
                results["document_analysis"] = await self._analyze_document_content(
                    user_question, results["search_results"]["documents"]
                )
                
                # Create response based on document analysis
                if not results["combined_response"]:
                    results["combined_response"] = await self._format_document_response(
                        user_question, results["document_analysis"]
                    )
            
            # Set processing time
            results["query_analysis"]["processing_time"] = time.time() - start_time
            
            return results
            
        except Exception as e:
            print(f"🚨 Enhanced query analysis error: {e}")
            return {
                "error": str(e),
                "is_visual_query": False,
                "analysis_approach": "error",
                "query_analysis": {
                    "original_question": user_question,
                    "processing_time": time.time() - start_time
                },
                "search_results": {},
                "visual_analysis": None,
                "combined_response": f"Error analyzing query: {str(e)}"
            }
        finally:
            # Clean up temporary files
            if temp_files_to_cleanup:
                visual_capture_service.cleanup_temp_files(temp_files_to_cleanup)

    async def _search_figma_content(self, query: str) -> Dict[str, Any]:
        """Search Figma files based on query"""
        try:
            response = await self.figma_service.get_user_files(
                search_query=query,
                limit=5
            )
            
            return {
                "figma_files": response.files,
                "figma_search_meta": {
                    "total_count": response.total_count,
                    "has_more": response.has_more,
                    "search_query": query
                }
            }
        except Exception as e:
            print(f"Error searching Figma: {e}")
            return {}
    
    async def _search_lucid_content(self, query: str) -> Dict[str, Any]:
        """Search Lucid diagrams based on query"""
        try:
            response = await self.lucid_service.search_documents(
                query=query,
                limit=5,
                use_client_side_search=True
            )
            
            return {
                "lucid_diagrams": response.documents,
                "lucid_search_meta": {
                    "total_count": response.totalCount,
                    "has_more": response.hasMore,
                    "search_query": query
                }
            }
        except Exception as e:
            print(f"Error searching Lucid: {e}")
            return {}
    
    async def _search_document_content(self, query: str) -> Dict[str, Any]:
        """Search uploaded documents based on query"""
        try:
            documents = await data_source_service.search_documents(query)
            
            return {
                "documents": documents
            }
        except Exception as e:
            print(f"Error searching documents: {e}")
            return {}
    
    async def _format_response_with_visual_analysis(
        self, 
        user_question: str, 
        search_results: Dict[str, Any], 
        visual_analysis: Dict[str, Any], 
        analysis_approach: str
    ) -> str:
        """Formats a response using the visual analysis result."""
        response_parts = []
        
        # Add visual analysis result
        if visual_analysis and visual_analysis.get("success"):
            analysis = visual_analysis["analysis"]
            print(f"✅ DEBUG: Using visual analysis result (length: {len(analysis)})")
            response_parts.append(analysis)
        else:
            print(f"❌ DEBUG: Visual analysis failed or not available.")
            if visual_analysis and visual_analysis.get("error"):
                response_parts.append(f"## ⚠️ Visual Analysis Error\n\n{visual_analysis['error']}")
            else:
                response_parts.append("## 📝 No visual analysis result available.")
        
        # Add search results summary
        response_parts.append(f"## 🔍 Search Results for \"{user_question}\"")
        response_parts.append(f"- Figma files: {'✅' if search_results.get('figma_files') else '❌'}")
        response_parts.append(f"- Lucid diagrams: {'✅' if search_results.get('lucid_diagrams') else '❌'}")
        response_parts.append(f"- Documents: {'✅' if search_results.get('documents') else '❌'}")
        
        return "\n\n".join(response_parts)

    async def _format_response_with_metadata_analysis(
        self, 
        user_question: str, 
        search_results: Dict[str, Any], 
        visual_analysis: Dict[str, Any], 
        analysis_approach: str
    ) -> str:
        """Formats a response using the visual analysis result."""
        response_parts = []
        
        # Add visual analysis result
        if visual_analysis and visual_analysis.get("success"):
            analysis = visual_analysis["analysis"]
            print(f"✅ DEBUG: Using visual analysis result (length: {len(analysis)})")
            response_parts.append(analysis)
        else:
            print(f"❌ DEBUG: Visual analysis failed or not available.")
            if visual_analysis and visual_analysis.get("error"):
                response_parts.append(f"## ⚠️ Visual Analysis Error\n\n{visual_analysis['error']}")
            else:
                response_parts.append("## 📝 No visual analysis result available.")
        
        # Add search results summary
        response_parts.append(f"## 🔍 Search Results for \"{user_question}\"")
        response_parts.append(f"- Figma files: {'✅' if search_results.get('figma_files') else '❌'}")
        response_parts.append(f"- Lucid diagrams: {'✅' if search_results.get('lucid_diagrams') else '❌'}")
        response_parts.append(f"- Documents: {'✅' if search_results.get('documents') else '❌'}")
        
        return "\n\n".join(response_parts)

    async def _format_document_response(
        self, 
        user_question: str, 
        document_analysis: Dict[str, Any]
    ) -> str:
        """Formats a response based on document analysis."""
        response_parts = []
        
        response_parts.append(f"## 📄 Document Analysis")
        response_parts.append(f"Found {document_analysis['relevant_documents']} relevant documents.")
        response_parts.append(f"**Context Preview:**\n{document_analysis['context_preview']}")
        
        return "\n\n".join(response_parts)

    async def _analyze_document_content(
        self, 
        user_question: str, 
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyzes uploaded documents based on query."""
        doc_context = data_source_service.get_document_context(
            documents,
            max_length=3000
        )
        
        return {
            "relevant_documents": len(documents),
            "context_preview": doc_context[:500] + "..." if len(doc_context) > 500 else doc_context
        }

    def _determine_architecture_reasoning_focus(self, user_question: str) -> str:
        """
        Determine the appropriate reasoning focus for architecture analysis
        
        Args:
            user_question: User's question
            
        Returns:
            Reasoning focus (comprehensive, technical, business, security)
        """
        question_lower = user_question.lower()
        
        # Technical focus keywords
        technical_keywords = [
            "performance", "scalability", "optimization", "implementation",
            "technology", "api", "database", "integration", "microservice",
            "deployment", "infrastructure", "code", "development"
        ]
        
        # Business focus keywords
        business_keywords = [
            "business", "value", "cost", "roi", "efficiency", "process",
            "workflow", "operational", "stakeholder", "capability", "strategy"
        ]
        
        # Security focus keywords
        security_keywords = [
            "security", "authentication", "authorization", "compliance",
            "privacy", "threat", "vulnerability", "access", "encryption",
            "firewall", "monitoring", "audit"
        ]
        
        # Determine focus based on keywords
        if any(keyword in question_lower for keyword in security_keywords):
            return "security"
        elif any(keyword in question_lower for keyword in business_keywords):
            return "business"
        elif any(keyword in question_lower for keyword in technical_keywords):
            return "technical"
        else:
            return "comprehensive"


# Create service instance
enhanced_query_service = EnhancedQueryService() 