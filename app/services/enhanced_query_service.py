"""
Enhanced Query Service that integrates Figma/Lucid search with visual analysis
"""

import asyncio
import time
from typing import Dict, Any
from app.services.figma_service import FigmaService
from app.services.lucid_service import LucidService
from app.services.enhanced_visual_capture_service import enhanced_visual_capture_service
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
            
            is_visual_query = any(
                keyword in user_question.lower() 
                for keyword in visual_keywords
            )
            
            results = {
                "is_visual_query": is_visual_query,
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
            
            # Capture and export visual content to files
            if visual_items and is_visual_query:
                print(f"📷 Capturing and exporting {len(visual_items)} items to files...")
                
                # Use enhanced visual capture service for file exports
                visual_data = await enhanced_visual_capture_service.capture_multiple_to_files(
                    visual_items
                )
                
                # Track files for cleanup
                for item in visual_data:
                    if item.get("success") and item.get("file_path"):
                        temp_files_to_cleanup.append(item["file_path"])
                
                # Analyze with OpenArena using file attachments
                visual_analysis = await enhanced_openarena_service.analyze_visual_content(
                    user_question=user_question,
                    visual_data=visual_data,
                    analysis_type=results["query_analysis"]["analysis_type"],
                    include_screenshots=True
                )
                
                results["visual_analysis"] = visual_analysis
                
            else:
                # No visual content found - provide analysis with metadata only
                print("📝 No visual content found, providing metadata-based analysis...")
                
                # Create mock visual data for analysis context
                mock_visual_data = []
                
                # Add Figma search metadata if available
                if results["search_results"].get("figma_search_meta"):
                    figma_meta = results["search_results"]["figma_search_meta"]
                    mock_visual_data.append({
                        "success": True,
                        "source": "figma",
                        "file_name": f"Figma Search Results (Query: {figma_meta.get('search_query', 'N/A')})",
                        "metadata": {
                            "search_performed": True,
                            "total_count": figma_meta.get("total_count", 0),
                            "has_more": figma_meta.get("has_more", False),
                            "search_query": figma_meta.get("search_query", "")
                        },
                        "capture_method": "metadata_only"
                    })
                
                # Add Lucid search metadata if available  
                if results["search_results"].get("lucid_search_meta"):
                    lucid_meta = results["search_results"]["lucid_search_meta"]
                    mock_visual_data.append({
                        "success": True,
                        "source": "lucid",
                        "diagram_title": f"Lucid Search Results (Query: {lucid_meta.get('search_query', 'N/A')})",
                        "metadata": {
                            "search_performed": True,
                            "total_count": lucid_meta.get("total_count", 0),
                            "has_more": lucid_meta.get("has_more", False),
                            "search_query": lucid_meta.get("search_query", "")
                        },
                        "capture_method": "metadata_only"
                    })
                
                # If we have document context, include it
                doc_context = ""
                if results["search_results"].get("documents"):
                    doc_context = data_source_service.get_document_context(
                        results["search_results"]["documents"],
                        max_length=2000
                    )
                    
                    mock_visual_data.append({
                        "success": True,
                        "source": "documents",
                        "file_name": f"Document Search Results ({len(results['search_results']['documents'])} found)",
                        "metadata": {
                            "document_count": len(results["search_results"]["documents"]),
                            "context_preview": doc_context[:300] + "..." if len(doc_context) > 300 else doc_context
                        },
                        "capture_method": "text_analysis"
                    })
                
                # Always provide at least basic analysis context
                if not mock_visual_data:
                    mock_visual_data.append({
                        "success": True,
                        "source": "query_analysis",
                        "file_name": f"Query Analysis: {user_question}",
                        "metadata": {
                            "query_type": results["query_analysis"]["analysis_type"],
                            "visual_keywords_detected": True,
                            "search_performed": True,
                            "sources_searched": ["figma", "lucid", "documents"] if include_figma and include_lucid and include_documents else []
                        },
                        "capture_method": "contextual_analysis"
                    })
                
                # Analyze with OpenArena using metadata and context
                visual_analysis = await enhanced_openarena_service.analyze_visual_content(
                    user_question=user_question,
                    visual_data=mock_visual_data,
                    analysis_type=results["query_analysis"]["analysis_type"],
                    include_screenshots=False  # No screenshots, just metadata analysis
                )
                
                results["visual_analysis"] = visual_analysis
            
            # Analyze document content if available
            if results["search_results"].get("documents"):
                doc_context = data_source_service.get_document_context(
                    results["search_results"]["documents"],
                    max_length=3000
                )
                
                # Create a simple document analysis
                results["document_analysis"] = {
                    "relevant_documents": len(results["search_results"]["documents"]),
                    "context_preview": doc_context[:500] + "..." if len(doc_context) > 500 else doc_context
                }
            
            # Create combined response
            combined_response = await self._create_combined_response(
                user_question,
                results
            )
            
            results["combined_response"] = combined_response
            results["query_analysis"]["processing_time"] = time.time() - start_time
            
            return results
            
        except Exception as e:
            return {
                "error": f"Failed to analyze query: {str(e)}",
                "processing_time": time.time() - start_time
            }
        finally:
            # Clean up temporary files
            if temp_files_to_cleanup:
                enhanced_visual_capture_service.cleanup_temp_files(temp_files_to_cleanup)
                print(f"🗑️ Cleaned up {len(temp_files_to_cleanup)} temporary files")
    
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
    
    async def _create_combined_response(
        self, 
        user_question: str, 
        results: Dict[str, Any]
    ) -> str:
        """Create a combined response from all analysis results"""
        
        response_parts = []
        
        # Add visual analysis if available
        if results.get("visual_analysis") and results["visual_analysis"].get("success"):
            analysis = results["visual_analysis"]["analysis"]
            response_parts.append(analysis)
        
        # Add document context if available and no visual analysis
        elif results.get("document_analysis"):
            doc_analysis = results["document_analysis"]
            response_parts.append(
                f"## 📄 Document Analysis\n\n"
                f"Found {doc_analysis['relevant_documents']} relevant documents.\n\n"
                f"**Context Preview:**\n{doc_analysis['context_preview']}"
            )
        
        # Fallback response if no analysis available
        if not response_parts:
            response_parts.append(
                f"## Analysis Results\n\n"
                f"I searched for content related to your question: \"{user_question}\"\n\n"
                f"**Search Summary:**\n"
                f"- Visual content search: {'✅' if results['is_visual_query'] else '❌'}\n"
                f"- Processing time: {results['query_analysis']['processing_time']:.2f}s\n\n"
                f"**Recommendations:**\n"
                f"1. Try more specific search terms\n"
                f"2. Check if the content exists in your Figma/Lucid accounts\n"
                f"3. Upload relevant documents if available"
            )
        
        return "\n\n".join(response_parts)


# Create service instance
enhanced_query_service = EnhancedQueryService() 