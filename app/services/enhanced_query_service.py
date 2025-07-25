"""
Enhanced Query Service that integrates Lucid search with visual analysis
"""

import asyncio
import os
import time
from typing import Any, Dict, List

from app.services.data_source_service import data_source_service
from app.services.enhanced_openarena_service import enhanced_openarena_service
from app.services.lucid_service import LucidService
from app.services.prompt_service import PromptService
from app.services.visual_capture_service import visual_capture_service
from app.services.wiki_search_service import WikiSearchService


class EnhancedQueryService:
    """Enhanced query service with visual content analysis"""

    wiki_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "resources",
        "wikis",
    )

    def __init__(self):
        self.lucid_service = LucidService()
        self.wiki_service = WikiSearchService(self.wiki_path)
        self.prompt_service = PromptService()

    async def chat_query(
        self,
        user_question: str,
        include_lucid: bool = False,
        include_wiki: bool = False,
        max_visual_items: int = 3,
    ) -> Dict[str, Any]:
        """
        Analyze user query and provide comprehensive response with parallel
        source searching

        Args:
            user_question: User's question
            include_lucid: Whether to search Lucid diagrams
            include_wiki: Whether to search wiki documents
            max_visual_items: Maximum visual items to process

        Returns:
            Comprehensive analysis result
        """
        start_time = time.time()
        temp_files_to_cleanup = []
        final_prompt = (
            self.prompt_service.getBasePrompt()
            + "\n"
            + self.prompt_service.getPromptRules()
        )

        # Initialize results structure
        results = {"search_results": {}, "combined_response": "", "cost_tracker": None}

        try:
            # 🚀 PARALLEL SOURCE SEARCH - Search all enabled sources
            # Create search tasks for all enabled sources (parallel execution)
            search_tasks = []
            task_labels = []

            if include_lucid:
                search_tasks.append(self._search_lucid_content(user_question))
                task_labels.append("lucid")

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

            # Add Lucid diagrams to visual items
            visual_items = []

            lucid_condition = include_lucid and results["search_results"].get(
                "lucid_diagrams"
            )
            if lucid_condition:
                remaining_slots = max_visual_items - len(visual_items)
                lucid_diagrams = results["search_results"]["lucid_diagrams"][
                    :remaining_slots
                ]
                for diagram in lucid_diagrams:
                    visual_items.append(
                        {
                            "type": "lucid",
                            "id": diagram.id,
                            "name": diagram.title,
                            "source_info": {
                                "product": getattr(diagram, "product", "Unknown"),
                                "last_modified": getattr(
                                    diagram, "lastModified", "Unknown"
                                ),
                                "folder_id": getattr(diagram, "folderId", None),
                            },
                        }
                    )

            visual_data = []
            if visual_items:
                visual_data = await visual_capture_service.capture_multiple_screenshots(
                    visual_items, export_to_files=False
                )

                visual_content = (
                    enhanced_openarena_service._prepare_visual_content_for_prompt(
                        visual_data
                    )
                )
                final_prompt += self.prompt_service.getLucidPrompt(
                    visual_content, user_question
                )

            # Add wiki documents
            wiki_condition = include_wiki and results["search_results"].get(
                "wiki_documents"
            )
            if wiki_condition:
                wiki_documents = results["search_results"]["wiki_documents"]
                final_prompt += self.prompt_service.getWikiPrompt(
                    wiki_documents, user_question
                )

            # send request to openarena
            if include_lucid or include_wiki:
                answer, cost_tracker = enhanced_openarena_service.make_openarena_call(
                    final_prompt
                )
                results.update(
                    {"combined_response": answer, "cost_tracker": cost_tracker}
                )
            else:
                results.update(
                    {
                        "combined_response": ("Include at least one source to analyze"),
                        "cost_tracker": 0,
                    }
                )

            return results

        except Exception as e:
            return {
                "error": str(e),
                "is_visual_query": False,
                "analysis_approach": "error",
                "query_analysis": {
                    "original_question": user_question,
                    "processing_time": time.time() - start_time,
                },
                "search_results": {},
                "visual_analysis": None,
                "combined_response": f"Error analyzing query: {str(e)}",
            }
        finally:
            # Clean up temporary files
            if temp_files_to_cleanup:
                visual_capture_service.cleanup_temp_files(temp_files_to_cleanup)

    async def _search_lucid_content(self, query: str) -> Dict[str, Any]:
        """Search Lucid diagrams based on query"""
        try:
            response = await self.lucid_service.search_documents(
                query=query, limit=5, use_client_side_search=True
            )

            return {
                "lucid_diagrams": response.documents,
                "lucid_search_meta": {
                    "total_count": response.totalCount,
                    "has_more": response.hasMore,
                    "search_query": query,
                },
            }
        except Exception:
            return {}

    async def _search_wiki_content(self, query: str) -> Dict[str, Any]:
        """Enhanced wiki search with better query processing and relevance scoring"""
        print(f"🔍 Enhanced wiki search for: {query}")
        try:
            # Generate search query variations for better coverage
            enhanced_queries = self._generate_search_variations(query)

            all_results = []
            for search_query in enhanced_queries:
                search_terms = search_query.split()
                if search_terms:
                    result = self.wiki_service.search(search_terms)
                    if result and result.get("contents"):
                        all_results.append(
                            {
                                "query": search_query,
                                "result": result,
                                "relevance_score": self._calculate_wiki_relevance(
                                    query, result
                                ),
                            }
                        )

            # Combine and rank results by relevance
            combined_results = self._combine_wiki_search_results(all_results)

            if combined_results and combined_results.get("contents"):
                print(f"✅ Wiki search found meaningful content for: {query}")
                return {
                    "wiki_documents": [combined_results],
                    "wiki_search_meta": {
                        "original_query": query,
                        "enhanced_queries": enhanced_queries,
                        "total_sources": len(all_results),
                        "confidence": combined_results.get("confidence", 0.5),
                        "files_with_matches": combined_results.get(
                            "files_with_matches", 0
                        ),
                        "total_matches": combined_results.get("total_matches", 0),
                        "search_query": query,
                    },
                }

            print(f"❌ Wiki search found no meaningful content for: {query}")
            return {}

        except Exception as e:
            print(f"❌ Wiki search error for '{query}': {str(e)}")
            return {}

    def _generate_search_variations(self, query: str) -> List[str]:
        """Generate search query variations for better wiki coverage"""
        variations = [query]
        query_lower = query.lower()

        # Add technical variations
        if "git" in query_lower:
            variations.extend(
                [
                    query.replace("git", "version control"),
                    query + " workflow",
                    query + " best practices",
                    query + " repository",
                ]
            )

        # Add process variations
        if "convention" in query_lower or "standard" in query_lower:
            variations.extend(
                [
                    query.replace("convention", "guideline"),
                    query.replace("standard", "policy"),
                    query + " procedure",
                    query + " documentation",
                ]
            )

        # Add code-related variations
        if any(word in query_lower for word in ["code", "coding", "development"]):
            variations.extend(
                [
                    query + " best practices",
                    query + " guidelines",
                    query + " standards",
                    query.replace("code", "development"),
                ]
            )

        # Add architecture variations
        if any(word in query_lower for word in ["architecture", "design", "system"]):
            variations.extend(
                [
                    query + " diagram",
                    query + " implementation",
                    query + " components",
                    query.replace("architecture", "design"),
                ]
            )

        # Add deployment variations
        if any(
            word in query_lower for word in ["deploy", "deployment", "infrastructure"]
        ):
            variations.extend(
                [
                    query + " pipeline",
                    query + " automation",
                    query + " process",
                    query.replace("deploy", "release"),
                ]
            )

        return list(set(variations))  # Remove duplicates

    def _calculate_wiki_relevance(
        self, original_query: str, search_result: Dict[str, Any]
    ) -> float:
        """Calculate relevance score for wiki search results"""
        if not search_result or not search_result.get("contents"):
            return 0.0

        relevance = 0.0
        content = search_result.get("contents", "").lower()
        query_words = set(original_query.lower().split())

        # Content length factor (prefer substantial content)
        content_length = len(content)
        if content_length > 500:
            relevance += 0.3
        elif content_length > 200:
            relevance += 0.2
        elif content_length > 100:
            relevance += 0.1

        # Keyword match factor
        content_words = set(content.split())
        match_ratio = len(query_words & content_words) / max(len(query_words), 1)
        relevance += match_ratio * 0.4

        # Technical content indicators
        technical_terms = [
            "implementation",
            "configuration",
            "setup",
            "procedure",
            "workflow",
            "guideline",
            "standard",
            "policy",
            "best practice",
            "example",
        ]
        if any(term in content for term in technical_terms):
            relevance += 0.2

        # File metadata factors
        if search_result.get("files_with_matches", 0) > 1:
            relevance += 0.1  # Multiple relevant files

        return min(relevance, 1.0)

    def _combine_wiki_search_results(
        self, results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Combine and rank wiki search results by relevance"""
        if not results:
            return {}

        # Sort by relevance score
        sorted_results = sorted(
            results, key=lambda x: x.get("relevance_score", 0), reverse=True
        )

        # Take the best result as base
        best_result = sorted_results[0]["result"]

        # Combine contents from multiple sources if relevant
        combined_content = best_result.get("contents", "")
        files_with_matches = best_result.get("files_with_matches", 0)
        total_matches = best_result.get("total_matches", 0)

        # Add supplementary content from other highly relevant results
        for result_data in sorted_results[1:3]:  # Top 3 results max
            if result_data["relevance_score"] > 0.5:  # Only high-relevance results
                additional_content = result_data["result"].get("contents", "")
                if additional_content and additional_content not in combined_content:
                    combined_content += (
                        f"\n\n--- Additional Source ---\n{additional_content}"
                    )
                    files_with_matches += result_data["result"].get(
                        "files_with_matches", 0
                    )
                    total_matches += result_data["result"].get("total_matches", 0)

        return {
            "contents": combined_content,
            "files_with_matches": files_with_matches,
            "total_matches": total_matches,
            "confidence": sorted_results[0]["relevance_score"],
            "sources_combined": len(
                [r for r in sorted_results if r["relevance_score"] > 0.5]
            ),
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
            "performance",
            "scalability",
            "optimization",
            "implementation",
            "technology",
            "api",
            "database",
            "integration",
            "microservice",
            "deployment",
            "infrastructure",
            "code",
            "development",
        ]

        # Business focus keywords
        business_keywords = [
            "business",
            "value",
            "cost",
            "roi",
            "efficiency",
            "process",
            "workflow",
            "operational",
            "stakeholder",
            "capability",
            "strategy",
        ]

        # Security focus keywords
        security_keywords = [
            "security",
            "authentication",
            "authorization",
            "compliance",
            "privacy",
            "threat",
            "vulnerability",
            "access",
            "encryption",
            "firewall",
            "monitoring",
            "audit",
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
        self, documents: List[Dict[str, Any]]
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
            documents, max_length=3000
        )

        return {
            "context_preview": (
                doc_context[:500] + "..." if len(doc_context) > 500 else doc_context
            ),
            "full_context": doc_context,
            "document_count": len(documents),
            "total_length": len(doc_context),
        }

    async def _format_comprehensive_response(
        self,
        user_question: str,
        search_results: Dict[str, Any],
        visual_analysis: Dict[str, Any],
        analysis_approach: str,
        sources_searched: List[str],
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
        response_parts.append(f'**Query:** "{user_question}"')
        response_parts.append(f"**Analysis Approach:** {analysis_approach.title()}")
        response_parts.append(f"**Sources Searched:** {', '.join(sources_searched)}")

        # Add detailed search results
        search_summary = []

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
        error_sources = [key for key in search_results.keys() if key.endswith("_error")]
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
        self, user_question: str, sources_searched: List[str], errors: Dict[str, Any]
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
        response_parts.append(f'**Query:** "{user_question}"')
        response_parts.append(f"**Sources Searched:** {', '.join(sources_searched)}")

        # Check for errors
        error_sources = [key for key in errors.keys() if key.endswith("_error")]
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
            "Check if the relevant files/diagrams exist in your connected sources",
            "Verify your API connections are working properly",
            "Consider uploading relevant documents if available",
        ]

        for suggestion in suggestions:
            response_parts.append(f"- {suggestion}")

        return "\n\n".join(response_parts)


# Create service instance
enhanced_query_service = EnhancedQueryService()
