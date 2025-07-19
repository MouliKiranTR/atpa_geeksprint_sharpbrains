# Lucid Diagrams MCP Integration

This integration provides access to your Lucid diagrams (Lucidchart and Lucidspark) through the Model Context Protocol (MCP). You can list and search your diagrams using either the standalone MCP server or the REST API endpoints.

## 🚀 Features

- **List All Diagrams**: Get all accessible Lucid diagrams with pagination support
- **Search Diagrams**: Search diagrams by title, content, or metadata
- **Product Filtering**: Filter results by Lucidchart or Lucidspark
- **MCP Tools**: Full MCP compatibility for AI assistants and tools
- **REST API**: Traditional HTTP endpoints for web applications

## 📋 Prerequisites

1. **Lucid API Key**: You need a Lucid API key to access your diagrams
2. **Python Dependencies**: The `mcp` library and `httpx` for API calls
3. **Environment Configuration**: Proper environment variables set up

## 🔧 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The key dependencies are:
- `mcp==1.0.0` - Model Context Protocol library
- `httpx==0.25.2` - HTTP client for Lucid API calls
- `fastapi==0.104.1` - For REST API endpoints

### 2. Get Your Lucid API Key

1. Go to [Lucid Developer Portal](https://developer.lucid.co/)
2. Create an application or use an existing one
3. Generate an API key
4. Copy the API key for configuration

### 3. Configure Environment Variables

Copy `env.example` to `.env` and update:

```bash
# Lucid API Configuration
LUCID_API_KEY=your_lucid_api_key_here
LUCID_API_BASE_URL=https://api.lucid.co
```

## 🖥️ Usage

### Option 1: Standalone MCP Server

Run the standalone MCP server that other applications can connect to:

```bash
# Set environment variable
export LUCID_API_KEY=your_api_key_here

# Run the MCP server
python mcp_server_standalone.py
```

The MCP server provides these tools:
- `list_lucid_diagrams` - List all accessible diagrams
- `search_lucid_diagrams` - Search diagrams by query

### Option 2: REST API Endpoints

Start the FastAPI application and use the HTTP endpoints:

```bash
# Start the API server
python run.py
```

Available endpoints:
- `POST /api/v1/lucid-mcp/list-diagrams` - List diagrams with filters
- `GET /api/v1/lucid-mcp/search/{query}` - Search diagrams
- `GET /api/v1/lucid-mcp/status` - Check integration status

### Option 3: Direct Python Integration

Use the Lucid service directly in your Python code:

```python
from app.services.lucid_service import lucid_service

# List all diagrams
response = await lucid_service.get_account_documents(limit=50)

# Search diagrams
response = await lucid_service.search_documents(
    query="project timeline",
    product_filter="lucidchart",
    limit=20
)

print(f"Found {len(response.documents)} diagrams")
for doc in response.documents:
    print(f"- {doc.title} ({doc.product}) [ID: {doc.id}]")
```

## 📖 API Reference

### MCP Tools

#### `list_lucid_diagrams`

Lists Lucid diagrams with optional filtering and pagination.

**Parameters:**
- `limit` (integer, optional): Maximum diagrams to return (1-100, default: 50)
- `offset` (integer, optional): Number of diagrams to skip (default: 0)
- `search_query` (string, optional): Filter diagrams by search query
- `product_filter` (string, optional): Filter by "lucidchart" or "lucidspark"

**Example:**
```json
{
  "limit": 25,
  "offset": 0,
  "search_query": "project",
  "product_filter": "lucidchart"
}
```

#### `search_lucid_diagrams`

Search for specific diagrams using a query string.

**Parameters:**
- `query` (string, required): Search query string
- `limit` (integer, optional): Maximum results to return (1-100, default: 20)
- `product_filter` (string, optional): Filter by "lucidchart" or "lucidspark"

**Example:**
```json
{
  "query": "workflow diagram",
  "limit": 10,
  "product_filter": "lucidspark"
}
```

### REST API Endpoints

#### `POST /api/v1/lucid-mcp/list-diagrams`

**Request Body:**
```json
{
  "limit": 50,
  "offset": 0,
  "search_query": "optional search term",
  "product_filter": "lucidchart"
}
```

**Response:**
```json
{
  "diagrams": [
    {
      "id": "diagram-id-123",
      "title": "Project Timeline",
      "created": "2024-01-15T10:30:00Z",
      "lastModified": "2024-01-20T14:45:00Z",
      "product": "lucidchart",
      "collaboratorCount": 3,
      "folderId": "folder-123",
      "folderName": "Project Diagrams"
    }
  ],
  "total_count": 25,
  "has_more": false,
  "message": "Found 25 Lucid diagrams"
}
```

#### `GET /api/v1/lucid-mcp/search/{query}`

**Parameters:**
- `query` (path): Search query string
- `limit` (query, optional): Maximum results (default: 20)
- `product_filter` (query, optional): "lucidchart" or "lucidspark"

**Example:**
```
GET /api/v1/lucid-mcp/search/project%20timeline?limit=10&product_filter=lucidchart
```

#### `GET /api/v1/lucid-mcp/status`

Check the status of the Lucid MCP integration.

**Response:**
```json
{
  "lucid_api_configured": true,
  "mcp_server_available": true,
  "supported_tools": [
    "list_lucid_diagrams",
    "search_lucid_diagrams"
  ],
  "message": "Lucid MCP integration is ready"
}
```

## 🔒 Authentication

The integration uses Lucid's REST API with API key authentication. The API key should be provided via the `LUCID_API_KEY` environment variable.

**Security Notes:**
- Keep your API key secure and don't commit it to version control
- Use environment variables or secure secret management
- The API key provides access to all diagrams in your Lucid account
- Consider using separate API keys for different environments

## 🐛 Troubleshooting

### Common Issues

1. **"Lucid API key is not configured"**
   - Ensure `LUCID_API_KEY` environment variable is set
   - Verify the API key is valid and active

2. **"Invalid Lucid API key or unauthorized access"**
   - Check that your API key is correct
   - Verify your Lucid account has API access enabled

3. **"Failed to connect to Lucid API"**
   - Check your internet connection
   - Verify the `LUCID_API_BASE_URL` is correct
   - Check if there are any firewall restrictions

4. **MCP Server Connection Issues**
   - Ensure the MCP server is running
   - Check that the client is using the correct transport
   - Verify environment variables are available to the server process

### Debug Mode

For detailed debugging, you can check the API status:

```bash
curl http://localhost:8000/api/v1/lucid-mcp/status
```

Or test the connection directly:

```python
from app.services.lucid_service import lucid_service

# Test the connection
try:
    response = await lucid_service.get_account_documents(limit=1)
    print("✅ Connection successful!")
    print(f"Found {response.totalCount} total diagrams")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

## 📚 Additional Resources

- [Lucid REST API Documentation](https://developer.lucid.co/reference/overview)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Lucid Developer Portal](https://developer.lucid.co/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This integration is part of the Onboarding Agent API project. See the main project license for details. 