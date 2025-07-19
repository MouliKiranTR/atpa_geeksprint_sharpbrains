# Lucid Document Export to Open Arena

This feature allows you to export Lucid documents as images and upload them directly to Open Arena for analysis.

## 🚀 Quick Start

### Prerequisites

1. Set up your Lucid API key:
   ```bash
   export LUCID_API_KEY=your_lucid_api_key_here
   ```

2. Ensure your Open Arena authentication is configured (TR_ACCESS_TOKEN)

### Using the API Endpoint

#### 1. List Available Documents

First, find the document you want to export:

```bash
curl -X POST "http://localhost:8000/api/v1/lucid-mcp/list-diagrams" \
     -H "Content-Type: application/json" \
     -d '{
       "limit": 10
     }'
```

#### 2. Export and Upload Document

Use the document ID from step 1:

```bash
curl -X POST "http://localhost:8000/api/v1/lucid-mcp/export-and-upload" \
     -H "Content-Type: application/json" \
     -d '{
       "document_id": "your-document-id-here",
       "format": "png",
       "width": 1920
     }'
```

### Using the Test Script

Run the included test script to see the functionality in action:

```bash
python test_lucid_export.py
```

## 📖 API Reference

### Export and Upload Endpoint

**POST** `/api/v1/lucid-mcp/export-and-upload`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `document_id` | string | ✅ | Lucid document ID to export |
| `page_id` | string | ❌ | Specific page to export |
| `format` | string | ❌ | Image format (png, jpg, pdf, svg) |
| `width` | integer | ❌ | Export width in pixels |
| `height` | integer | ❌ | Export height in pixels |

**Example Request:**
```json
{
  "document_id": "abc-123-def",
  "format": "png",
  "width": 1920
}
```

**Example Response:**
```json
{
  "success": true,
  "message": "Successfully exported and uploaded to Open Arena",
  "lucid_export": {
    "document_id": "abc-123-def",
    "page_id": null,
    "format": "png",
    "size": 245678
  },
  "openarena_upload": {
    "file_id": "file-uuid-456",
    "filename": "lucid_export_abc-123-def.png",
    "status": "uploaded"
  }
}
```

### Help Endpoint

**GET** `/api/v1/lucid-mcp/export-help`

Returns information about available endpoints and usage instructions.

## 🔧 How It Works

1. **Export**: Uses the Lucid REST API `GET /documents/{id}` endpoint with export parameters
2. **Upload**: Converts the exported image to base64 and uploads to Open Arena via the data source service
3. **Analysis**: The uploaded image is now available for analysis in Open Arena

## 📝 Supported Formats

- **PNG** (default) - Best for diagrams with transparency
- **JPG** - Smaller file size, good for photos
- **PDF** - Vector format, scalable
- **SVG** - Vector format, web-friendly

## 🚨 Error Handling

Common errors and solutions:

| Error | Solution |
|-------|----------|
| "Lucid API key is not configured" | Set the `LUCID_API_KEY` environment variable |
| "Document not found" | Verify the document ID exists and you have access |
| "Failed to upload to Open Arena" | Check TR_ACCESS_TOKEN configuration |

## 🧪 Testing

The `test_lucid_export.py` script demonstrates the complete workflow:

1. Searches for available Lucid documents
2. Exports the first document found
3. Uploads it to Open Arena
4. Shows the API endpoint usage

## 🔗 Integration with Existing Features

This functionality integrates with:

- **Enhanced Query Service**: Visual analysis of Lucid diagrams
- **Visual Capture Service**: Alternative screenshot methods
- **Data Source Service**: File upload and management
- **Open Arena Service**: AI-powered analysis

## 📚 Next Steps

After uploading, you can:

1. Use the enhanced query service to analyze the diagram
2. Ask questions about the visual content via Open Arena
3. Integrate with other visual analysis tools

## 🔧 Configuration

### Environment Variables

```bash
# Required for Lucid export
LUCID_API_KEY=your_lucid_api_key_here
LUCID_API_BASE_URL=https://api.lucid.co  # Default

# Required for Open Arena upload
TR_ACCESS_TOKEN=your_open_arena_token_here
```

### Optional Settings

- Default export width: 1920 pixels
- Default format: PNG
- Supported formats: png, jpg, pdf, svg
- Maximum file size: Determined by Open Arena limits

## 🤝 Contributing

To extend this functionality:

1. Add new export formats in `lucid_service.py`
2. Enhance error handling for specific use cases
3. Add batch export capabilities
4. Integrate with additional analysis services 