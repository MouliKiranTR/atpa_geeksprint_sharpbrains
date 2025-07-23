"""
ADO Wiki Search Service

A standalone service class for searching through locally stored wiki pages and returning
consolidated content based on keyword matching.

This service can be easily integrated into any application by copying this file
and importing the AdoWikiSearchService class.

Features:
- Full-text search across all markdown files in the wiki directory
- Case-insensitive pattern matching using regex
- Consolidated results with cleaned content
- Content cleaning (removes tables, URLs, GUIDs, special characters)
- Built using Python's built-in modules (os, re) for simplicity

Usage:
    from ado_wiki_search_service import AdoWikiSearchService

    service = AdoWikiSearchService("/path/to/wikis")
    result = service.search(["git", "conventions"])
"""

import logging
import os
import re
import time
from typing import Any, Dict, List
from urllib.parse import unquote


class WikiSearchService:
    """
    Standalone wiki content search service.

    This class provides all the functionality needed to search through wiki files
    and return consolidated, cleaned content. It can be easily integrated into any
    application without dependencies on Flask or other frameworks.
    """

    def __init__(self, wiki_base_path: str, max_content_length: int = 5000):
        """
        Initialize the wiki search service.

        Args:
            wiki_base_path: Root path to the wiki directory
            max_content_length: Maximum characters to return in consolidated content
        """
        self.wiki_base_path = wiki_base_path
        self.max_content_length = max_content_length
        self.supported_extensions = [".md", ".txt"]
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def _is_supported_file(self, file_path: str) -> bool:
        """Check if file has supported extension."""
        return any(file_path.lower().endswith(ext) for ext in self.supported_extensions)

    def _decode_filename(self, filename: str) -> str:
        """Decode URL-encoded characters in filenames."""
        try:
            return unquote(filename)
        except Exception:
            return filename

    def _read_file_contents(self, file_path: str) -> str:
        """
        Read the complete contents of a file.

        Args:
            file_path: Path to the file to read

        Returns:
            File contents as string, or empty string if error
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                return file.read()
        except Exception as e:
            self.logger.warning(f"Error reading file contents {file_path}: {str(e)}")
            return ""

    def _clean_content(self, content: str) -> str:
        """
        Clean and sanitize file content for API response.

        Removes:
        - Tabs and excessive whitespace
        - Multiple consecutive newlines
        - URLs and links (markdown and regular)
        - Special characters and symbols
        - Random GUIDs
        - Table formatting characters

        Args:
            content: Raw file content

        Returns:
            Cleaned content string
        """
        if not content:
            return ""

        # Remove tabs and replace with single space
        cleaned = content.replace("\t", " ")

        # Remove markdown links [text](url) and keep only the text
        cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)

        # Remove standalone URLs (http, https, ftp)
        cleaned = re.sub(r"https?://[^\s\)]+", "", cleaned)
        cleaned = re.sub(r"ftp://[^\s\)]+", "", cleaned)

        # Remove wiki-style links like /Projects-and-Functionalities/...
        cleaned = re.sub(r"/[A-Za-z0-9\-_%/]+", "", cleaned)

        # Remove GUIDs (pattern: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX)
        cleaned = re.sub(
            r"[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}",
            "",
            cleaned,
        )

        # Remove email-like patterns with @ symbols followed by GUIDs
        cleaned = re.sub(r"@<[A-Fa-f0-9\-]+>", "", cleaned)

        # Remove table formatting characters and markdown
        cleaned = re.sub(r"\|+", " ", cleaned)  # Remove table separators
        cleaned = re.sub(r"[-=]{3,}", "", cleaned)  # Remove table header separators
        cleaned = re.sub(
            r"\*{1,3}([^*]+)\*{1,3}", r"\1", cleaned
        )  # Remove bold/italic markdown
        cleaned = re.sub(
            r"`{1,3}([^`]+)`{1,3}", r"\1", cleaned
        )  # Remove code formatting
        cleaned = re.sub(r"#{1,6}\s*", "", cleaned)  # Remove markdown headers

        # Remove special characters and symbols (keep basic punctuation)
        cleaned = re.sub(r"[^\w\s\.\,\!\?\:\;\-\(\)]", " ", cleaned)

        # Remove multiple consecutive spaces
        cleaned = re.sub(r"\s{2,}", " ", cleaned)

        # Remove multiple consecutive newlines (keep max 2)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in cleaned.split("\n")]
        cleaned = "\n".join(lines)

        # Remove empty lines at start and end
        cleaned = cleaned.strip()

        # Limit content length to prevent excessive response size
        if len(cleaned) > self.max_content_length:
            cleaned = cleaned[: self.max_content_length] + "..."

        return cleaned

    def _extract_context(
        self, content: str, match_start: int, match_end: int, context_chars: int = 100
    ) -> str:
        """
        Extract context around a match for better readability.

        Args:
            content: Full file content
            match_start: Start position of match
            match_end: End position of match
            context_chars: Characters to include before and after match

        Returns:
            Context string with match highlighted
        """
        start = max(0, match_start - context_chars)
        end = min(len(content), match_end + context_chars)

        context = content[start:end]

        # Add ellipsis if truncated
        if start > 0:
            context = "..." + context
        if end < len(content):
            context = context + "..."

        return context.strip()

    def _search_in_file(
        self, file_path: str, patterns: List[re.Pattern]
    ) -> List[Dict[str, Any]]:
        """
        Search for patterns in a single file.

        Args:
            file_path: Path to the file to search
            patterns: List of compiled regex patterns

        Returns:
            List of match results with context
        """
        matches = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()

            for pattern in patterns:
                for match in pattern.finditer(content):
                    context = self._extract_context(content, match.start(), match.end())

                    matches.append(
                        {
                            "matched_text": match.group(),
                            "context": context,
                            "line_number": content[: match.start()].count("\n") + 1,
                            "position": match.start(),
                        }
                    )

        except Exception as e:
            self.logger.warning(f"Error reading file {file_path}: {str(e)}")

        return matches

    def _get_detailed_search_results(
        self, search_terms: List[str], case_sensitive: bool = False
    ) -> Dict[str, Any]:
        """
        Search for terms across all wiki files and return detailed results.

        Args:
            search_terms: List of search terms/keywords
            case_sensitive: Whether to perform case-sensitive search

        Returns:
            Dictionary containing detailed search results and metadata
        """
        start_time = time.time()

        # Compile regex patterns
        flags = 0 if case_sensitive else re.IGNORECASE
        patterns = []

        for term in search_terms:
            try:
                # Escape special regex characters but allow basic wildcards
                escaped_term = re.escape(term).replace(r"\*", ".*").replace(r"\?", ".")
                patterns.append(re.compile(escaped_term, flags))
            except re.error as e:
                self.logger.warning(f"Invalid regex pattern '{term}': {str(e)}")
                continue

        if not patterns:
            return {
                "results": [],
                "total_files_searched": 0,
                "total_matches": 0,
                "search_time_seconds": 0,
                "search_terms": search_terms,
            }

        results = []
        files_searched = 0
        total_matches = 0

        # Walk through wiki directory
        for root, dirs, files in os.walk(self.wiki_base_path):
            for file in files:
                if not self._is_supported_file(file):
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.wiki_base_path)

                # Decode URL-encoded path components
                display_path = "/".join(
                    self._decode_filename(part) for part in relative_path.split(os.sep)
                )

                matches = self._search_in_file(file_path, patterns)
                files_searched += 1

                if matches:
                    total_matches += len(matches)
                    # Read and clean file contents for the response
                    file_contents = self._read_file_contents(file_path)
                    cleaned_contents = self._clean_content(file_contents)

                    results.append(
                        {
                            "file_path": display_path,
                            "file_size_bytes": os.path.getsize(file_path),
                            "matches": matches,
                            "match_count": len(matches),
                            "contents": cleaned_contents,
                        }
                    )

        # Sort results by number of matches (descending)
        results.sort(key=lambda x: x["match_count"], reverse=True)

        search_time = time.time() - start_time

        return {
            "results": results,
            "total_files_searched": files_searched,
            "total_matches": total_matches,
            "search_time_seconds": round(search_time, 3),
            "search_terms": search_terms,
        }

    def search(self, search_terms: List[str]) -> Dict[str, Any]:
        """
        Main search method that returns consolidated search results.

        This is the primary method to use when integrating the service into other applications.

        Args:
            search_terms: List of search terms/keywords

        Returns:
            Dictionary containing consolidated search results in the format:
            {
                "query": "search terms",
                "total_matches": 412,
                "files_with_matches": 105,
                "search_time": 0.224,
                "contents": "consolidated cleaned content from all matching files"
            }
        """
        # Get detailed search results (always case-insensitive)
        search_results = self._get_detailed_search_results(
            search_terms, case_sensitive=False
        )

        # Consolidate contents from all matching files
        consolidated_contents = []
        for result in search_results["results"]:
            # Construct full file path to read contents
            file_path = os.path.join(
                self.wiki_base_path, result["file_path"].replace("/", os.sep)
            )
            file_contents = self._read_file_contents(file_path)
            cleaned_contents = self._clean_content(file_contents)

            # Add to consolidated contents if not empty
            if cleaned_contents.strip():
                consolidated_contents.append(cleaned_contents.strip())

        # Join all contents with separator
        all_contents = " ".join(consolidated_contents)

        # Apply final cleaning and length limit to consolidated content
        if len(all_contents) > self.max_content_length:
            all_contents = all_contents[: self.max_content_length] + "..."

        # Return unified response format
        return {
            "query": " ".join(search_terms),
            "total_matches": search_results["total_matches"],
            "files_with_matches": len(search_results["results"]),
            "search_time": search_results["search_time_seconds"],
            "contents": all_contents,
        }

    def health_check(self) -> Dict[str, Any]:
        """
        Check if the wiki directory exists and return health status.

        Returns:
            Dictionary containing health status information
        """
        return {
            "status": "healthy" if os.path.exists(self.wiki_base_path) else "unhealthy",
            "wiki_path": self.wiki_base_path,
            "wiki_exists": os.path.exists(self.wiki_base_path),
        }


# Example usage for integration into other applications:
if __name__ == "__main__":
    # Example of how to use the service in another application
    import json

    # Initialize the service
    # wiki_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wikis")
    wiki_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "resources", "wikis")
    service = WikiSearchService(wiki_path)

    # Perform a search
    result = service.search(["git", "conventions"])

    # Print formatted result
    print("Search Result:")
    print(json.dumps(result, indent=2))

    # Check health
    health = service.health_check()
    print("\nHealth Check:")
    print(json.dumps(health, indent=2))
