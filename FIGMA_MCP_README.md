# Figma MCP Integration

This integration provides access to your Figma files through the Model Context Protocol (MCP). You can list and search your Figma files using either the standalone MCP server or the REST API endpoints.

## 🚀 Features

- **List All Files**: Get all accessible Figma files with pagination support
- **Search Files**: Search files by name, key, or content
- **Team Support**: Access files from specific teams
- **MCP Tools**: Full MCP compatibility for AI assistants and tools
- **REST API**: Traditional HTTP endpoints for web applications

## 📋 Prerequisites

1. **Figma Personal Access Token**: You need a Figma personal access token to access your files
2. **Python Dependencies**: The `mcp` library and `httpx` for API calls
3. **Environment Configuration**: Proper environment variables set up

## 🔧 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The key dependencies are:
- `mcp==1.0.0` - Model Context Protocol library
- `httpx==0.25.2` - HTTP client for Figma API calls
- `fastapi==0.104.1` - For REST API endpoints

### 2. Get Your Figma Personal Access Token

1. Go to [Figma](https://www.figma.com/)
2. Sign in to your account
3. Go to **Settings** → **Security** → **Personal access tokens**
4. Click **Generate new token**
5. Enter a name for your token and press Enter
6. Copy the generated token immediately (you won't be able to see it again)

### 3. Configure Environment Variables

Copy `env.example` to `.env` and update:

```bash
# Figma API Configuration
FIGMA_API_TOKEN=your_figma_personal_access_token_here
```

## 🖥️ Usage

### Option 1: Standalone MCP Server

Run the standalone MCP server that other applications can connect to:

```bash
# Set environment variable
export FIGMA_API_TOKEN=your_token_here

# Run the MCP server
python figma_mcp_server_standalone.py
```

The MCP server provides these tools:
- `list_figma_files` - List all accessible files
- `search_figma_files` - Search files by query

### Option 2: REST API Endpoints

Start the FastAPI application and use the HTTP endpoints:

```bash
# Start the API server
python run.py
```

Available endpoints:
- `POST /api/v1/figma-mcp/list-files` - List files with filters
- `GET /api/v1/figma-mcp/search/{query}` - Search files
- `GET /api/v1/figma-mcp/status` - Check integration status

### Option 3: Direct Python Integration

Use the Figma service directly in your Python code:

```python
from app.services.figma_service import figma_service

# List user's files
response = await figma_service.get_user_files(limit=50)

# Search files
response = await figma_service.get_user_files(
    search_query="design system",
    limit=20
)

print(f"Found {len(response.files)} files")
for file in response.files:
    print(f"- {file.name} [Key: {file.key}]")
```

## 📖 API Reference

### MCP Tools

#### `list_figma_files`

Lists Figma files with optional filtering and pagination.

**Parameters:**
- `limit` (integer, optional): Maximum files to return (1-100, default: 50)
- `offset` (integer, optional): Number of files to skip (default: 0)
- `search_query` (string, optional): Filter files by search query
- `team_id` (string, optional): Filter files from specific team

**Example:**
```json
{
  "limit": 25,
  "offset": 0,
  "search_query": "design system",
  "team_id": "team_123"
}
```

#### `search_figma_files`

Search for specific files using a query string.

**Parameters:**
- `query` (string, required): Search query string
- `limit` (integer, optional): Maximum results to return (1-100, default: 20)
- `team_id` (string, optional): Filter files from specific team

**Example:**
```json
{
  "query": "mobile app design",
  "limit": 10,
  "team_id": "team_123"
}
```

### REST API Endpoints

#### `POST /api/v1/figma-mcp/list-files`

**Request Body:**
```json
{
  "limit": 50,
  "offset": 0,
  "search_query": "optional search term",
  "team_id": "optional_team_id"
}
```

**Response:**
```json
{
  "files": [
    {
      "key": "file_key_123",
      "name": "Design System",
      "thumbnail_url": "https://...",
      "last_modified": "2024-01-20T14:45:00Z",
      "file_type": "design"
    }
  ],
  "total_count": 25,
  "has_more": false,
  "message": "Found 25 Figma files"
}
```

#### `GET /api/v1/figma-mcp/search/{query}`

**Parameters:**
- `query` (path): Search query string
- `limit` (query, optional): Maximum results (default: 20)
- `team_id` (query, optional): Team ID to filter files from

**Example:**
```
GET /api/v1/figma-mcp/search/mobile%20design?limit=10&team_id=team_123
```

#### `GET /api/v1/figma-mcp/status`

Check the status of the Figma MCP integration.

**Response:**
```json
{
  "figma_api_configured": true,
  "mcp_server_available": true,
  "supported_tools": [
    "list_figma_files",
    "search_figma_files"
  ],
  "features": [
    "User files access",
    "Team files access",
    "Client-side search",
    "File filtering"
  ],
  "message": "Figma MCP integration is ready"
}
```

## 🔒 Authentication

The integration uses Figma's REST API with personal access token authentication. The token should be provided via the `FIGMA_API_TOKEN` environment variable.

**Security Notes:**
- Keep your token secure and don't commit it to version control
- Use environment variables or secure secret management
- The token provides access to all files in your Figma account
- Consider using separate tokens for different environments
- Personal access tokens cannot be scoped to specific files or teams

## 🐛 Troubleshooting

### Common Issues

1. **"Figma API token is not configured"**
   - Ensure `FIGMA_API_TOKEN` environment variable is set
   - Verify the token is valid and active

2. **"Invalid Figma API token or unauthorized access"**
   - Check that your token is correct
   - Verify you copied the complete token (they're quite long)
   - Ensure the token hasn't expired or been revoked

3. **"Failed to connect to Figma API"**
   - Check your internet connection
   - Verify there are no firewall restrictions
   - Check if Figma's API is experiencing issues

4. **MCP Server Connection Issues**
   - Ensure the MCP server is running
   - Check that the client is using the correct transport
   - Verify environment variables are available to the server process

### Debug Mode

For detailed debugging, you can check the API status:

```bash
curl http://localhost:8000/api/v1/figma-mcp/status
```

Or test the connection directly:

```python
from app.services.figma_service import figma_service

# Test the connection
try:
    response = await figma_service.get_user_files(limit=1)
    print("✅ Connection successful!")
    print(f"Found {response.total_count} total files")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## 📚 Additional Resources

- [Figma REST API Documentation](https://www.figma.com/developers/api)
- [Figma Personal Access Tokens Guide](https://help.figma.com/hc/en-us/articles/8085703771159-Manage-personal-access-tokens)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Figma Developer Documentation](https://www.figma.com/plugin-docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This integration is part of the Onboarding Agent API project. See the main project license for details. 