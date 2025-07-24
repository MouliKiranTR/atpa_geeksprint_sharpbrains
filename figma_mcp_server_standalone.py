#!/usr/bin/env python3
"""
Standalone Figma MCP Server

This script runs a standalone MCP server that provides tools for listing 
and searching Figma files using the Figma REST API.

Usage:
    python figma_mcp_server_standalone.py

Environment Variables Required:
    FIGMA_API_TOKEN: Your Figma personal access token (required)
"""

import asyncio
import os
import sys
from pathlib import Path


def setup_imports():
    """Setup imports after path modification."""
    # Add the project root to Python path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Import the MCP server module
    from app.services.figma_mcp_server import run_figma_mcp_server
    return run_figma_mcp_server


def main():
    """Main function to run the Figma MCP server."""
    # Setup imports
    run_figma_mcp_server = setup_imports()
    
    # Check for required environment variables
    api_token = os.getenv("FIGMA_API_TOKEN")
    if not api_token:
        print("Error: FIGMA_API_TOKEN environment variable is required")
        print("\nTo get a Figma personal access token:")
        print("1. Go to https://www.figma.com/")
        print("2. Sign in to your account")
        print("3. Go to Settings → Security → Personal access tokens")
        print("4. Click 'Generate new token' and copy the value")
        print("\nExample:")
        print("export FIGMA_API_TOKEN=your_figma_token_here")
        print("python figma_mcp_server_standalone.py")
        sys.exit(1)
    
    print("🚀 Starting Figma MCP Server...")
    print(f"📡 API Token configured: {api_token[:8]}...")
    print("\nAvailable MCP Tools:")
    print("• list_figma_files - List all accessible Figma files")
    print("• search_figma_files - Search files by query")
    print("\n" + "="*50)
    print("MCP Server is ready for connections...")
    
    try:
        # Run the MCP server
        asyncio.run(run_figma_mcp_server())
    except KeyboardInterrupt:
        print("\n👋 Shutting down Figma MCP Server...")
    except Exception as e:
        print(f"❌ Error running MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 