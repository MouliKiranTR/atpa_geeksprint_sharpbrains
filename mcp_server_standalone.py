#!/usr/bin/env python3
"""
Standalone Lucid Diagrams MCP Server

This script runs a standalone MCP server that provides tools for listing 
and searching Lucid diagrams using the Lucid REST API.

Usage:
    python mcp_server_standalone.py

Environment Variables Required:
    LUCID_API_KEY: Your Lucid API key (required)
    LUCID_API_BASE_URL: Lucid API base URL (optional, defaults to 
                        https://api.lucid.co)
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
    from app.services.mcp_server import run_mcp_server
    return run_mcp_server


def main():
    """Main function to run the MCP server."""
    # Setup imports
    run_mcp_server = setup_imports()
    
    # Check for required environment variables
    api_key = os.getenv("LUCID_API_KEY")
    if not api_key:
        print("Error: LUCID_API_KEY environment variable is required")
        print("\nTo get a Lucid API key:")
        print("1. Go to https://developer.lucid.co/")
        print("2. Create an application and generate an API key")
        print("3. Set the LUCID_API_KEY environment variable")
        print("\nExample:")
        print("export LUCID_API_KEY=your_api_key_here")
        print("python mcp_server_standalone.py")
        sys.exit(1)
    
    # Set default API URL if not provided
    if not os.getenv("LUCID_API_BASE_URL"):
        os.environ["LUCID_API_BASE_URL"] = "https://api.lucid.co"
    
    print("🚀 Starting Lucid Diagrams MCP Server...")
    print(f"📡 API Key configured: {api_key[:8]}...")
    print(f"🌐 API Base URL: {os.getenv('LUCID_API_BASE_URL')}")
    print("\nAvailable MCP Tools:")
    print("• list_lucid_diagrams - List all accessible Lucid diagrams")
    print("• search_lucid_diagrams - Search diagrams by query")
    print("\n" + "="*50)
    print("MCP Server is ready for connections...")
    
    try:
        # Run the MCP server
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        print("\n👋 Shutting down Lucid Diagrams MCP Server...")
    except Exception as e:
        print(f"❌ Error running MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 