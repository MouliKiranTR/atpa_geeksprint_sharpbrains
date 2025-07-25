# Chat Endpoint for Frontend Integration

## Overview

The chat endpoint provides a conversational interface that integrates with the enhanced query service, allowing frontend applications to communicate with the backend through a RESTful API. This endpoint supports visual content analysis and provides comprehensive responses.

## Endpoint Details

### Base URL
```
POST /api/v1/chat/message
```

### Request Model

```json
{
  "message": "string (required) - User's message",
  "include_wiki": "boolean (default: true) - Search wiki documents",
  "include_lucid": "boolean (default: false) - Search Lucid diagrams", 
  "max_visual_items": "integer (default: 3, min: 1, max: 10) - Max visual items to process"
}
```

### Response Model

```json
{
  "message": "string - Assistant's response",
  "is_visual_query": "boolean - Whether query was visual-related",
  "analysis_type": "string - Type of analysis performed",
  "search_summary": {
    "figma_files_found": "integer (always 0)",
    "lucid_diagrams_found": "integer", 
    "documents_found": "integer (always 0)",
    "total_sources_searched": "integer",
    "visual_items_processed": "integer"
  },
  "visual_analysis_available": "boolean - Whether visual analysis was performed",
  "processing_time": "number - Processing time in seconds",
  "cost": "number (optional) - Analysis cost if available",
  "success": "boolean - Whether request succeeded",
  "error": "string (optional) - Error message if any"
}
```

## Frontend Integration Examples

### JavaScript/TypeScript

```javascript
// Basic chat message
async function sendChatMessage(message) {
  const response = await fetch('/api/v1/chat/message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      include_wiki: true,
      include_lucid: true,
      max_visual_items: 3
    })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

// Usage example
try {
  const result = await sendChatMessage("Can you show me our system architecture?");
  console.log("Assistant:", result.message);
  console.log("Visual analysis available:", result.visual_analysis_available);
  
  // Send another message
  const followUp = await sendChatMessage(
    "Tell me more about the database connections"
    result.conversation_id,
    result.chat_history
  );
} catch (error) {
  console.error("Chat error:", error);
}
```

### React Hook Example

```jsx
import { useState, useCallback } from 'react';

function useChatAPI() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(async (message) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/v1/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          include_wiki: true,
          include_lucid: true,
          max_visual_items: 3
        })
      });

      if (!response.ok) {
        throw new Error(`Chat API error: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { sendMessage, isLoading, error };
}
```

## Key Features

### 1. Visual Content Analysis
- Automatic detection of visual queries
- Integration with Lucid services
- Screenshot capture and analysis
- Architecture-specific analysis for system diagrams

### 2. Multi-Source Search
- Lucid diagram search
- Wiki document search
- Configurable source inclusion

### 3. Performance Tracking
- Processing time metrics
- Cost tracking for AI analysis
- Search result summaries

### 4. Error Handling
- Graceful error responses
- Detailed error information

## Additional Endpoints

### Clear Conversation
```
### Health Check
```
GET /api/v1/chat/health
```

## Response Codes

- `200` - Success
- `422` - Validation Error (invalid request data)
- `500` - Internal Server Error

## Best Practices

### Frontend Implementation
1. **Handle Loading States**: Show loading indicators during API calls
2. **Error Handling**: Implement proper error handling and user feedback
3. **Rate Limiting**: Implement client-side rate limiting for better UX
4. **Message Formatting**: Parse and display markdown responses properly

### Performance Optimization
1. **Debouncing**: Debounce rapid message sends
2. **Progressive Loading**: Show partial responses as they arrive (if implementing streaming)

### Security Considerations
1. **Input Validation**: Validate user input before sending
2. **Authentication**: Implement proper authentication for production
3. **Rate Limiting**: Implement server-side rate limiting
4. **Data Sanitization**: Sanitize display of responses

## Testing

Run the test script to verify the endpoint:

```bash
python test_chat_endpoint.py
```

## Production Deployment Notes

For production deployment, consider implementing:

1. **Authentication**: Add user authentication and authorization
2. **Rate Limiting**: Implement API rate limiting
3. **Logging**: Add comprehensive logging
4. **Monitoring**: Add performance and error monitoring
5. **Caching**: Implement response caching where appropriate 