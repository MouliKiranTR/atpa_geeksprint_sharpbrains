"""
MCP Server for Figma Integration
Provides tools for listing and searching Figma files via MCP
"""

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from app.services.figma_service import figma_service


# Initialize MCP server
server = Server("figma-mcp")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    List available tools that this MCP server provides.
    
    Returns:
        list[Tool]: Available tools for Figma files
    """
    return [
        Tool(
            name="list_figma_files",
            description=(
                "List all Figma files accessible with the configured "
                "personal access token"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of files to return",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 100
                    },
                    "offset": {
                        "type": "integer",
                        "description": (
                            "Number of files to skip for pagination"
                        ),
                        "default": 0,
                        "minimum": 0
                    },
                    "search_query": {
                        "type": "string",
                        "description": (
                            "Optional search query to filter files"
                        )
                    },
                    "team_id": {
                        "type": "string",
                        "description": "Optional team ID to filter files from"
                    }
                }
            }
        ),
        Tool(
            name="search_figma_files",
            description="Search Figma files using a specific query",
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
                    "team_id": {
                        "type": "string",
                        "description": "Optional team ID to filter files from"
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
    if not figma_service:
        return [TextContent(
            type="text",
            text=(
                "Error: Figma API token is not configured. "
                "Please set FIGMA_API_TOKEN in your environment."
            )
        )]
    
    try:
        if name == "list_figma_files":
            return await _handle_list_files(arguments)
        elif name == "search_figma_files":
            return await _handle_search_files(arguments)
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


async def _handle_list_files(arguments: dict) -> list[TextContent]:
    """Handle list_figma_files tool call."""
    limit = arguments.get("limit", 50)
    offset = arguments.get("offset", 0)
    search_query = arguments.get("search_query")
    team_id = arguments.get("team_id")
    
    try:
        if team_id:
            # Get files from specific team
            response = await figma_service.get_team_projects(
                team_id=team_id,
                limit=limit,
                offset=offset,
                search_query=search_query
            )
        else:
            # Get user's files
            response = await figma_service.get_user_files(
                limit=limit,
                offset=offset,
                search_query=search_query
            )
        
        # Format response
        files_info = []
        for file in response.files:
            info = f"• {file.name}"
            if file.file_type:
                info += f" ({file.file_type})"
            if file.last_modified:
                info += f" - Last modified: {file.last_modified}"
            info += f" [Key: {file.key}]"
            if file.thumbnail_url:
                info += f" [Thumbnail: {file.thumbnail_url}]"
            files_info.append(info)
        
        if not files_info:
            message = "No Figma files found."
            if search_query:
                message += f" (searched for: '{search_query}')"
        else:
            message = f"Found {len(files_info)} Figma files"
            if search_query:
                message += f" matching '{search_query}'"
            if team_id:
                message += f" in team {team_id}"
            current_range = f"{offset + 1}-{offset + len(files_info)}"
            message += f" (showing {current_range}"
            if response.has_more:
                message += f" of {response.total_count}+ total)"
            else:
                message += f" of {response.total_count} total)"
            message += ":\n\n" + "\n".join(files_info)
        
        return [TextContent(type="text", text=message)]
        
    except ValueError as e:
        return [TextContent(
            type="text",
            text=f"Figma API Error: {str(e)}"
        )]


async def _handle_search_files(arguments: dict) -> list[TextContent]:
    """Handle search_figma_files tool call."""
    query = arguments["query"]
    limit = arguments.get("limit", 20)
    team_id = arguments.get("team_id")
    
    try:
        if team_id:
            # Search files from specific team
            response = await figma_service.get_team_projects(
                team_id=team_id,
                limit=limit,
                offset=0,
                search_query=query
            )
        else:
            # Search user's files
            response = await figma_service.get_user_files(
                limit=limit,
                offset=0,
                search_query=query
            )
        
        if not response.files:
            message = f"No Figma files found matching '{query}'"
            if team_id:
                message += f" in team {team_id}"
            return [TextContent(type="text", text=message)]
        
        # Format search results
        results = []
        for file in response.files:
            result = f"📄 **{file.name}**"
            if file.file_type:
                result += f" ({file.file_type})"
            result += f"\n   Key: {file.key}"
            if file.last_modified:
                result += f"\n   Last modified: {file.last_modified}"
            if file.thumbnail_url:
                result += f"\n   Thumbnail: {file.thumbnail_url}"
            results.append(result)
        
        message = (
            f"Found {len(results)} Figma files matching '{query}'"
        )
        if team_id:
            message += f" in team {team_id}"
        message += ":\n\n" + "\n\n".join(results)
        
        if response.has_more:
            total_info = f"{response.total_count}+"
            message += (
                f"\n\n(Showing first {limit} results of "
                f"{total_info} total)"
            )
        
        return [TextContent(type="text", text=message)]
        
    except ValueError as e:
        return [TextContent(
            type="text",
            text=f"Figma API Error: {str(e)}"
        )]


async def run_figma_mcp_server():
    """Run the Figma MCP server using stdio transport."""
    # Configure server options
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="figma-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        ) 