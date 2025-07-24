# 🗄️ Lucid Diagram Caching System

This system provides intelligent caching for Lucid diagram exports with automatic OpenArena integration to improve performance and reduce redundant API calls.

## 🚀 Features

### Core Functionality
- **Smart Caching**: Automatically caches exported Lucid diagrams locally
- **Auto-Upload**: Optionally uploads cached files to OpenArena 
- **Cache Management**: Built-in expiry, cleanup, and statistics
- **Multiple Formats**: Supports PNG, JPG, PDF, SVG exports
- **Configurable**: Flexible settings for cache behavior

### Performance Benefits
- ⚡ **Faster Access**: Subsequent requests use cached files
- 🔄 **Reduced API Calls**: Minimizes requests to Lucid API
- 📊 **Bandwidth Savings**: Avoids re-downloading large diagrams
- 🚀 **Auto-Upload**: Seamless OpenArena integration

## 📋 Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Cache Configuration
CACHE_ENABLED=true                    # Enable/disable caching
CACHE_DIR=./cache                     # Cache directory path
CACHE_EXPIRY_HOURS=24                 # Cache expiry time
AUTO_UPLOAD_TO_OPENARENA=true         # Auto-upload to OpenArena

# Required for functionality
LUCID_API_KEY=your_lucid_api_key      # Lucid API access
TR_ACCESS_TOKEN=your_openarena_token  # OpenArena access
```

### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `CACHE_ENABLED` | `true` | Enable/disable the caching system |
| `CACHE_DIR` | `./cache` | Directory to store cached files |
| `CACHE_EXPIRY_HOURS` | `24` | Hours before cache entries expire |
| `AUTO_UPLOAD_TO_OPENARENA` | `true` | Auto-upload cached files to OpenArena |

## 🔧 API Endpoints

### Cache Management

#### Get Cache Statistics
```http
GET /api/v1/cache/stats
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "enabled": true,
    "cache_dir": "./cache",
    "total_files": 6,
    "data_files": 3,
    "metadata_files": 3,
    "total_size_bytes": 2048576,
    "total_size_mb": 1.95,
    "expiry_hours": 24,
    "auto_upload": true
  }
}
```

#### List Cached Documents
```http
GET /api/v1/cache/list
```

**Response:**
```json
{
  "success": true,
  "cached_documents": [
    {
      "document_id": "abc-123-def",
      "cache_key": "a1b2c3d4e5f6",
      "format": "png",
      "page_id": null,
      "file_size": 245678,
      "cached_at": "2024-01-15T10:30:00",
      "expires_at": "2024-01-16T10:30:00",
      "is_expired": false,
      "file_path": "./cache/a1b2c3d4e5f6.png"
    }
  ],
  "count": 1
}
```

#### Clean Expired Cache
```http
POST /api/v1/cache/cleanup
```

**Response:**
```json
{
  "success": true,
  "cleanup_result": {
    "cleaned": 2,
    "errors": 0
  },
  "message": "Cleaned 2 expired entries"
}
```

#### Check Specific Document Cache
```http
GET /api/v1/cache/check/{document_id}?format=png&width=1920
```

**Response:**
```json
{
  "success": true,
  "cached": true,
  "cache_info": {
    "cache_key": "a1b2c3d4e5f6",
    "file_path": "./cache/a1b2c3d4e5f6.png",
    "metadata": {
      "document_id": "abc-123-def",
      "format": "png",
      "cached_at": 1642248600
    }
  }
}
```

### Enhanced Export Endpoints

The existing Lucid export endpoints now support caching:

#### Export with Caching
```http
POST /api/v1/lucid-mcp/export-and-upload
```

**Request:**
```json
{
  "document_id": "abc-123-def",
  "format": "png",
  "width": 1920,
  "use_cache": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully exported and uploaded to Open Arena",
  "lucid_export": {
    "document_id": "abc-123-def",
    "format": "png",
    "size": 245678,
    "cached": true,
    "file_path": "./cache/a1b2c3d4e5f6.png"
  },
  "openarena_upload": {
    "file_id": "file-uuid-456",
    "filename": "lucid_export_abc-123-def.png",
    "status": "uploaded"
  }
}
```

## 🔄 How It Works

### Cache Flow

1. **Request**: User requests Lucid diagram export
2. **Check Cache**: System checks if diagram is already cached
3. **Cache Hit**: If found and not expired, return cached file
4. **Cache Miss**: If not found, export from Lucid API
5. **Store & Upload**: Cache the file locally and optionally upload to OpenArena
6. **Return**: Provide file with cache metadata

### Cache Keys

Cache keys are generated using:
- Document ID
- Export format (png, jpg, pdf, svg)
- Page ID (if specified)
- Width/height parameters

Example: `document123_png_page1_w1920` → `a1b2c3d4e5f6`

### File Structure

```
cache/
├── a1b2c3d4e5f6.png      # Cached image data
├── a1b2c3d4e5f6.json     # Metadata
├── b2c3d4e5f6a1.pdf      # Another cached file
└── b2c3d4e5f6a1.json     # Its metadata
```

## 🧪 Testing & Demo

### Run Cache Demo
```bash
python cache_demo.py
```

This demonstrates:
- Initial export (creates cache)
- Second export (uses cache)
- Cache statistics
- OpenArena auto-upload

### Run Enhanced Export Test
```bash
python test_lucid_export.py
```

Shows the updated export flow with caching.

## 💡 Usage Examples

### Basic Usage

```python
from app.services.lucid_service import lucid_service

# Export with caching (default)
result = await lucid_service.export_document_image(
    document_id="abc-123",
    format="png",
    width=1920
)

# Skip cache for fresh export
result = await lucid_service.export_document_image(
    document_id="abc-123",
    format="png",
    width=1920,
    use_cache=False
)
```

### Cache Management

```python
from app.services.cache_service import cache_service

# Get cache statistics
stats = await cache_service.get_cache_stats()
print(f"Cache size: {stats['total_size_mb']} MB")

# List cached documents
docs = await cache_service.list_cached_documents()
print(f"Cached documents: {len(docs)}")

# Clean expired entries
result = await cache_service.cleanup_expired_cache()
print(f"Cleaned {result['cleaned']} entries")
```

### Visual Capture with Caching

```python
from app.services.visual_capture_service import visual_capture_service

# Capture with caching enabled
result = await visual_capture_service.capture_lucid_diagram_screenshot(
    diagram_id="abc-123",
    diagram_title="My Diagram",
    use_cache=True,
    format="png"
)
```

## 🚨 Error Handling

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| "Cache disabled" | `CACHE_ENABLED=false` | Set to `true` in config |
| "Cache directory not writable" | Permission issue | Check directory permissions |
| "Failed to upload to OpenArena" | Missing token | Configure `TR_ACCESS_TOKEN` |
| "Cache expired" | Old cached file | Normal behavior, will re-export |

### Cache Troubleshooting

```bash
# Check cache directory
ls -la ./cache/

# Verify permissions
chmod 755 ./cache

# Clear cache manually
rm -rf ./cache/*

# Check configuration
python -c "from app.core.config import settings; print(settings.CACHE_ENABLED)"
```

## 🔧 Maintenance

### Regular Cleanup

The system automatically cleans expired cache entries, but you can also:

```bash
# Manual cleanup via API
curl -X POST "http://localhost:8000/api/v1/cache/cleanup"

# Or via Python
python -c "import asyncio; from app.services.cache_service import cache_service; asyncio.run(cache_service.cleanup_expired_cache())"
```

### Monitoring

Monitor cache performance:

```bash
# Check cache stats
curl "http://localhost:8000/api/v1/cache/stats"

# List cached files
curl "http://localhost:8000/api/v1/cache/list"
```

## 🔗 Integration

### With Visual Analysis

Cached diagrams integrate seamlessly with:
- Enhanced Query Service
- Visual Capture Service  
- OpenArena Analysis
- Architecture Analysis

### With Existing Workflows

The caching system is backward compatible:
- Existing API calls work unchanged
- Optional cache parameter available
- Auto-upload can be disabled
- Cache can be completely disabled

## 📈 Performance Impact

### Before Caching
- 🐌 5-15 seconds per export
- 🔄 Repeated API calls for same diagram
- 📊 High bandwidth usage
- 💸 API rate limit concerns

### After Caching
- ⚡ <1 second for cached diagrams
- 🎯 Single API call per unique export
- 💾 Local file access
- 🚀 Auto-upload to OpenArena

## 🔮 Future Enhancements

Planned improvements:
- **Smart Invalidation**: Detect diagram changes
- **Compression**: Optimize cache storage
- **Cloud Cache**: Shared cache across instances
- **Batch Operations**: Bulk cache management
- **Analytics**: Cache hit/miss metrics

## 🤝 Contributing

To extend the caching system:

1. **Add New Formats**: Update `CacheService._get_cache_paths()`
2. **Custom Storage**: Implement new storage backends
3. **Cache Strategies**: Add TTL variations
4. **Monitoring**: Enhance statistics collection

## 📚 Related Documentation

- [LUCID_EXPORT_README.md](LUCID_EXPORT_README.md) - Basic export functionality
- [VISUAL_ANALYSIS_README.md](VISUAL_ANALYSIS_README.md) - Visual analysis features
- [LUCID_MCP_README.md](LUCID_MCP_README.md) - MCP integration
- [README.md](README.md) - Main project documentation 