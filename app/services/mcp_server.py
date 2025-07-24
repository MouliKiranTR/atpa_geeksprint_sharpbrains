"""
MCP Server for Lucid Diagrams Integration
Provides tools for listing and searching Lucid diagrams via MCP
"""

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from app.services.lucid_service import lucid_service


# Initialize MCP server
server = Server("lucid-diagrams-mcp")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools that this MCP server provides.
    
    Returns:
        list[Tool]: Available tools for Lucid diagrams
    """
    return [
        Tool(
            name="list_lucid_diagrams",
            description=(
                "List all Lucid diagrams (Lucidchart and Lucidspark) "
                "accessible with the configured API key"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of diagrams to return",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "offset": {
                        "type": "integer",
                        "description": (
                            "Number of diagrams to skip for pagination"
                        ),
                        "default": 0,
                        "minimum": 0
                    },
                    "search_query": {
                        "type": "string",
                        "description": (
                            "Optional search query to filter diagrams"
                        )
                    },
                    "product_filter": {
                        "type": "string",
                        "description": "Filter by product type",
                        "enum": ["lucidchart", "lucidspark"]
                    }
                }
            }
        ),
        Tool(
            name="search_lucid_diagrams",
            description="Search Lucid diagrams using a specific query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string",
                        "minLength": 1
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "product_filter": {
                        "type": "string",
                        "description": "Filter by product type",
                        "enum": ["lucidchart", "lucidspark"]
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls from the MCP client.
    
    Args:
        name: Name of the tool to call
        arguments: Arguments passed to the tool
        
    Returns:
        list[TextContent]: Response from the tool
    """
    if not lucid_service:
        return [TextContent(
            type="text",
            text=(
                "Error: Lucid API key is not configured. "
                "Please set LUCID_API_KEY in your environment."
            )
        )]
    
    try:
        if name == "list_lucid_diagrams":
            return await _handle_list_diagrams(arguments)
        elif name == "search_lucid_diagrams":
            return await _handle_search_diagrams(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error executing tool '{name}': {str(e)}"
        )]


async def _handle_list_diagrams(arguments: dict) -> list[TextContent]:
    """Handle list_lucid_diagrams tool call."""
    limit = arguments.get("limit", 50)
    offset = arguments.get("offset", 0)
    search_query = arguments.get("search_query")
    product_filter = arguments.get("product_filter")
    
    try:
        if search_query:
            # Use search API if query is provided
            response = await lucid_service.search_documents(
                query=search_query,
                product_filter=product_filter,
                limit=limit,
                offset=offset
            )
        else:
            # Use account documents API for listing all
            response = await lucid_service.get_account_documents(
                limit=limit,
                offset=offset
            )
        
        # Format response
        diagrams_info = []
        for doc in response.documents:
            info = f"• {doc.title}"
            if doc.product:
                info += f" ({doc.product})"
            if doc.folderId and doc.folderName:
                info += f" in folder '{doc.folderName}'"
            if doc.lastModified:
                info += f" - Last modified: {doc.lastModified}"
            if doc.collaboratorCount:
                info += f" - {doc.collaboratorCount} collaborators"
            info += f" [ID: {doc.id}]"
            diagrams_info.append(info)
        
        if not diagrams_info:
            message = "No Lucid diagrams found."
            if search_query:
                message += f" (searched for: '{search_query}')"
        else:
            message = f"Found {len(diagrams_info)} Lucid diagrams"
            if search_query:
                message += f" matching '{search_query}'"
            current_range = f"{offset + 1}-{offset + len(diagrams_info)}"
            message += f" (showing {current_range}"
            if response.hasMore:
                message += f" of {response.totalCount}+ total)"
            else:
                message += f" of {response.totalCount} total)"
            message += ":\n\n" + "\n".join(diagrams_info)
        
        return [TextContent(type="text", text=message)]
        
    except ValueError as e:
        return [TextContent(
            type="text",
            text=f"Lucid API Error: {str(e)}"
        )]


async def _handle_search_diagrams(arguments: dict) -> list[TextContent]:
    """Handle search_lucid_diagrams tool call."""
    query = arguments["query"]
    limit = arguments.get("limit", 20)
    product_filter = arguments.get("product_filter")
    
    try:
        response = await lucid_service.search_documents(
            query=query,
            product_filter=product_filter,
            limit=limit,
            offset=0
        )
        
        if not response.documents:
            return [TextContent(
                type="text",
                text=f"No Lucid diagrams found matching '{query}'"
            )]
        
        # Format search results
        results = []
        for doc in response.documents:
            result = f"📄 **{doc.title}**"
            if doc.product:
                result += f" ({doc.product})"
            result += f"\n   ID: {doc.id}"
            if doc.folderId and doc.folderName:
                result += f"\n   Folder: {doc.folderName}"
            if doc.lastModified:
                result += f"\n   Last modified: {doc.lastModified}"
            if doc.collaboratorCount:
                result += f"\n   Collaborators: {doc.collaboratorCount}"
            results.append(result)
        
        message = (
            f"Found {len(results)} Lucid diagrams matching '{query}':"
            f"\n\n" + "\n\n".join(results)
        )
        
        if response.hasMore:
            total_info = f"{response.totalCount}+"
            message += (
                f"\n\n(Showing first {limit} results of "
                f"{total_info} total)"
            )
        
        return [TextContent(type="text", text=message)]
        
    except ValueError as e:
        return [TextContent(
            type="text",
            text=f"Lucid API Error: {str(e)}"
        )]


async def run_mcp_server():
    """Run the MCP server using stdio transport."""
    # Configure server options
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="lucid-diagrams-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        ) 