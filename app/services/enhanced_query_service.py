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
from app.services.wiki_search_service import WikiSearchService


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
        include_wiki: bool = True,
        max_visual_items: int = 3
    ) -> Dict[str, Any]:
        """
        Analyze user query and provide comprehensive response with parallel 
        source searching
        
        Args:
            user_question: User's question
            include_figma: Whether to search Figma files
            include_lucid: Whether to search Lucid diagrams
            include_documents: Whether to search uploaded documents
            include_wiki: Whether to search wiki documents
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
            analysis_approach = (
                "architecture" if is_architecture_query else "general"
            )
            
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
            
            # 🚀 PARALLEL SOURCE SEARCH - Search all enabled sources
            # Create search tasks for all enabled sources (parallel execution)
            search_tasks = []
            task_labels = []
            
            if include_figma:
                search_tasks.append(self._search_figma_content(user_question))
                task_labels.append("figma")
            
            if include_lucid:
                search_tasks.append(self._search_lucid_content(user_question))
                task_labels.append("lucid")
            
            if include_documents:
                search_tasks.append(
                    self._search_document_content(user_question)
                )
                task_labels.append("documents")
            
            if include_wiki:
                search_tasks.append(self._search_wiki_content(user_question))
                task_labels.append("wiki")
            
            # Execute all searches in parallel
            if search_tasks:
                search_results_list = await asyncio.gather(
                    *search_tasks, return_exceptions=True
                )
                
                # Process search results and handle any exceptions
                for i, (result, label) in enumerate(
                    zip(search_results_list, task_labels)
                ):
                    if isinstance(result, Exception):
                        # Add empty result for failed searches
                        error_key = f"{label}_error"
                        results["search_results"][error_key] = str(result)
                    elif result:
                        results["search_results"].update(result)
            
            # 📊 CONSOLIDATE SEARCH RESULTS for OpenArena
            
            # Collect visual items from search results
            visual_items = []
            
            # Add Figma files to visual items
            if results["search_results"].get("figma_files"):
                figma_list = results["search_results"]["figma_files"]
                figma_files = figma_list[:max_visual_items]
                for file in figma_files:
                    visual_items.append({
                        "type": "figma",
                        "id": file.key,
                        "name": file.name,
                        "source_info": {
                            "last_modified": getattr(
                                file, 'last_modified', 'Unknown'
                            ),
                            "thumbnail_url": getattr(
                                file, 'thumbnail_url', ''
                            ),
                            "file_type": getattr(
                                file, 'file_type', 'design'
                            )
                        }
                    })
            
            # Add Lucid diagrams to visual items
            if results["search_results"].get("lucid_diagrams"):
                remaining_slots = max_visual_items - len(visual_items)
                lucid_diagrams = results["search_results"][
                    "lucid_diagrams"
                ][:remaining_slots]
                for diagram in lucid_diagrams:
                    visual_items.append({
                        "type": "lucid", 
                        "id": diagram.id,
                        "name": diagram.title,
                        "source_info": {
                            "product": getattr(diagram, 'product', 'Unknown'),
                            "last_modified": getattr(
                                diagram, 'lastModified', 'Unknown'
                            ),
                            "folder_id": getattr(diagram, 'folderId', None)
                        }
                    })
            
            # 🎯 OPENARENA ANALYSIS - Pass consolidated results to OpenArena
            if visual_items or results["search_results"]:
                
                # Capture visual content if visual items found
                visual_data = []
                if visual_items:
                    
                    # Use consolidated visual capture service for file exports
                    visual_data = await (
                        visual_capture_service.capture_multiple_screenshots(
                            visual_items, export_to_files=True
                        )
                    )
                    
                    # Track files for cleanup
                    for item in visual_data:
                        if item.get("success") and item.get("file_path"):
                            temp_files_to_cleanup.append(item["file_path"])
                
                # Add document context to visual data if available
                if results["search_results"].get("documents"):
                    document_context = self._prepare_document_context(
                        results["search_results"]["documents"]
                    )
                    visual_data.append({
                        "success": True,
                        "source": "documents",
                        "metadata": document_context,
                        "capture_method": "context_extraction"
                    })
                
                # Add search metadata to visual data
                search_metadata = {
                    "sources_searched": task_labels,
                    "total_figma_files": len(
                        results["search_results"].get("figma_files", [])
                    ),
                    "total_lucid_diagrams": len(
                        results["search_results"].get("lucid_diagrams", [])
                    ),
                    "total_documents": len(
                        results["search_results"].get("documents", [])
                    ),
                    "total_wiki_documents": len(
                        results["search_results"].get("wiki_documents", [])
                    ),
                    "query_type": results["query_analysis"]["analysis_type"]
                }
                
                visual_data.append({
                    "success": True,
                    "source": "query_analysis",
                    "metadata": search_metadata,
                    "capture_method": "search_aggregation"
                })
                
                # 🏗️ Choose appropriate OpenArena analysis method
                if is_architecture_query:
                    
                    # Use unified analysis method for architecture analysis
                    visual_analysis = await (
                        enhanced_openarena_service.analyze_content(
                            user_question=user_question,
                            visual_data=visual_data,
                            analysis_type="architecture"
                        )
                    )
                else:
                    
                    visual_analysis = await (
                        enhanced_openarena_service.analyze_visual_content(
                            user_question=user_question,
                            visual_data=visual_data,
                            analysis_type=results["query_analysis"][
                                "analysis_type"
                            ],
                            include_screenshots=bool(visual_items)
                        )
                    )
                
                # Store analysis results
                results["visual_analysis"] = visual_analysis
                
                # Format comprehensive response
                results["combined_response"] = await (
                    self._format_comprehensive_response(
                        user_question=user_question,
                        search_results=results["search_results"],
                        visual_analysis=visual_analysis,
                        analysis_approach=analysis_approach,
                        sources_searched=task_labels
                    )
                )
                
            else:
                
                # Create fallback response when no sources return results
                results["combined_response"] = await (
                    self._format_no_results_response(
                        user_question=user_question,
                        sources_searched=task_labels,
                        errors=results["search_results"]
                    )
                )
            
            # Set processing time
            results["query_analysis"]["processing_time"] = (
                time.time() - start_time
            )
            
            return results
            
        except Exception as e:
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
                visual_capture_service.cleanup_temp_files(
                    temp_files_to_cleanup
                )

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
        except Exception:
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
        except Exception:
            return {}
    
    async def _search_document_content(self, query: str) -> Dict[str, Any]:
        """Search uploaded documents based on query"""
        try:
            documents = await data_source_service.search_documents(query)
            
            return {
                "documents": documents
            }
        except Exception:
            return {}

    async def _search_wiki_content(self, query: str) -> Dict[str, Any]:
        """Search wiki documents based on query"""
        try:
            wiki_results = await WikiSearchService.search(query)
            
            return {
                "wiki_documents": wiki_results,
                "wiki_search_meta": {
                    "total_count": len(wiki_results) if wiki_results else 0,
                    "search_query": query
                }
            }
        except Exception:
            return {}

    def _determine_architecture_reasoning_focus(
        self, user_question: str
    ) -> str:
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

    def _prepare_document_context(
        self, 
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Prepare document context for OpenArena analysis
        
        Args:
            documents: List of document search results
            
        Returns:
            Document context metadata
        """
        if not documents:
            return {"context_preview": "No documents found", "count": 0}
        
        # Get document context from data source service
        doc_context = data_source_service.get_document_context(
            documents,
            max_length=3000
        )
        
        return {
            "context_preview": (
                doc_context[:500] + "..." 
                if len(doc_context) > 500 
                else doc_context
            ),
            "full_context": doc_context,
            "document_count": len(documents),
            "total_length": len(doc_context)
        }

    async def _format_comprehensive_response(
        self, 
        user_question: str, 
        search_results: Dict[str, Any], 
        visual_analysis: Dict[str, Any], 
        analysis_approach: str,
        sources_searched: List[str]
    ) -> str:
        """
        Format a comprehensive response using OpenArena analysis and 
        search results
        
        Args:
            user_question: Original user question
            search_results: All search results from different sources
            visual_analysis: OpenArena analysis results
            analysis_approach: Type of analysis performed
            sources_searched: List of sources that were searched
            
        Returns:
            Formatted comprehensive response
        """
        response_parts = []
        
        # Add visual analysis result from OpenArena
        if visual_analysis and visual_analysis.get("success"):
            analysis = visual_analysis["analysis"]
            response_parts.append(analysis)
            
            # Add metadata about the analysis
            cost = visual_analysis.get("cost")
            if cost:
                response_parts.append(f"\n💲 **Analysis Cost:** ${cost}")
        else:
            if visual_analysis and visual_analysis.get("error"):
                response_parts.append(
                    f"## ⚠️ Analysis Error\n\n{visual_analysis['error']}"
                )
            else:
                response_parts.append("## 📝 No analysis result available.")
        
        # Add search results summary
        response_parts.append("\n## 🔍 Search Summary")
        response_parts.append(f"**Query:** \"{user_question}\"")
        response_parts.append(
            f"**Analysis Approach:** {analysis_approach.title()}"
        )
        response_parts.append(
            f"**Sources Searched:** {', '.join(sources_searched)}"
        )
        
        # Add detailed search results
        search_summary = []
        if search_results.get("figma_files"):
            count = len(search_results["figma_files"])
            search_summary.append(f"- **Figma Files:** {count} found")
        
        if search_results.get("lucid_diagrams"):
            count = len(search_results["lucid_diagrams"])
            search_summary.append(f"- **Lucid Diagrams:** {count} found")
        
        if search_results.get("documents"):
            count = len(search_results["documents"])
            search_summary.append(f"- **Documents:** {count} found")
        
        if search_results.get("wiki_documents"):
            count = len(search_results["wiki_documents"])
            search_summary.append(f"- **Wiki Documents:** {count} found")
        
        # Add error information if any searches failed
        error_sources = [
            key for key in search_results.keys() 
            if key.endswith("_error")
        ]
        if error_sources:
            search_summary.append(
                f"- **Errors:** {len(error_sources)} source(s) failed"
            )
        
        if search_summary:
            response_parts.append("\n".join(search_summary))
        else:
            response_parts.append("- No results found in any source")
        
        return "\n\n".join(response_parts)

    async def _format_no_results_response(
        self, 
        user_question: str, 
        sources_searched: List[str],
        errors: Dict[str, Any]
    ) -> str:
        """
        Format a response when no results are found from any source
        
        Args:
            user_question: Original user question
            sources_searched: List of sources that were searched
            errors: Any errors that occurred during searching
            
        Returns:
            Formatted no-results response
        """
        response_parts = []
        
        response_parts.append("## 📭 No Results Found")
        response_parts.append(f"**Query:** \"{user_question}\"")
        response_parts.append(
            f"**Sources Searched:** {', '.join(sources_searched)}"
        )
        
        # Check for errors
        error_sources = [
            key for key in errors.keys() if key.endswith("_error")
        ]
        if error_sources:
            response_parts.append("\n## ⚠️ Search Errors")
            for error_key in error_sources:
                source = error_key.replace("_error", "").title()
                error_msg = errors[error_key]
                response_parts.append(f"- **{source}:** {error_msg}")
        
        # Provide suggestions
        response_parts.append("\n## 💡 Suggestions")
        suggestions = [
            "Try using different keywords in your search",
            "Check if the relevant files/diagrams exist in your connected "
            "sources",
            "Verify your API connections are working properly",
            "Consider uploading relevant documents if available"
        ]
        
        for suggestion in suggestions:
            response_parts.append(f"- {suggestion}")
        
        return "\n\n".join(response_parts)


# Create service instance
enhanced_query_service = EnhancedQueryService() 