"""
Checkpoint Wiki Search API

A fast GET API that searches through locally stored wiki pages and returns
consolidated content based on keyword matching.

This Flask application provides a REST API wrapper around the AdoWikiSearchService.
The service class can be extracted and used in other applications independently.

Features:
- RESTful API endpoints for wiki search functionality
- Health check and file listing endpoints
- Error handling and logging
- Built on top of the standalone AdoWikiSearchService
"""

import logging
import os

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

from services.wiki_search_service import WikiSearchService

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration - Updated to point to resources/wikis
WIKI_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "wikis")

# Initialize the wiki search service
wiki_search_service = WikiSearchService(WIKI_BASE_PATH)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify(wiki_search_service.health_check())


@app.route("/search", methods=["GET"])
def search_wiki():
    """
    Search wiki content for specified keywords.

    Query Parameters:
        q (str): Search query (required)
        terms (str): Comma-separated search terms (alternative to q)

    Returns:
        JSON response with consolidated search results and metadata
    """
    try:
        # Get search parameters
        query = request.args.get("q", "").strip()
        terms_param = request.args.get("terms", "").strip()

        # Determine search terms
        search_terms = []
        if query:
            # Split query into terms (simple whitespace splitting)
            search_terms = [term.strip() for term in query.split() if term.strip()]
        elif terms_param:
            # Split comma-separated terms
            search_terms = [
                term.strip() for term in terms_param.split(",") if term.strip()
            ]

        if not search_terms:
            raise BadRequest("Search terms are required. Use 'q' or 'terms' parameter.")

        logger.info(f"Searching for terms: {search_terms}")

        # Use the service to perform search
        result = wiki_search_service.search(search_terms)
        return jsonify(result)

    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify(
        {
            "error": "Endpoint not found",
            "available_endpoints": ["/search", "/health"],
        }
    ), 404


if __name__ == "__main__":
    # Verify wiki directory exists
    if not os.path.exists(WIKI_BASE_PATH):
        logger.warning(f"Wiki directory not found: {WIKI_BASE_PATH}")
    else:
        logger.info(f"Wiki search API starting. Base path: {WIKI_BASE_PATH}")

    # Run the application
    app.run(host="127.0.0.1", port=5000, debug=True)
