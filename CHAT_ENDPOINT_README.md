# Chat Endpoint for Frontend Integration

## Overview

The chat endpoint provides a conversational interface that integrates with the enhanced query service, allowing frontend applications to communicate with the backend through a RESTful API. This endpoint supports visual content analysis, maintains conversation history, and provides comprehensive responses.

## Endpoint Details

### Base URL
```
POST /api/v1/chat/message
```

### Request Model

```json
{
  "message": "string (required) - User's message",
  "conversation_id": "string (optional) - Conversation ID for context",
  "chat_history": [
    {
      "role": "user|assistant",
      "content": "string - Message content",
      "timestamp": "number (optional) - Unix timestamp"
    }
  ],
  "include_figma": "boolean (default: true) - Search Figma files",
  "include_lucid": "boolean (default: true) - Search Lucid diagrams", 
  "include_documents": "boolean (default: true) - Search uploaded documents",
  "max_visual_items": "integer (default: 3, min: 1, max: 10) - Max visual items to process"
}
```

### Response Model

```json
{
  "message": "string - Assistant's response",
  "conversation_id": "string - Conversation ID for tracking",
  "chat_history": [
    {
      "role": "user|assistant",
      "content": "string - Message content", 
      "timestamp": "number - Unix timestamp"
    }
  ],
  "is_visual_query": "boolean - Whether query was visual-related",
  "analysis_type": "string - Type of analysis performed",
  "search_summary": {
    "figma_files_found": "integer",
    "lucid_diagrams_found": "integer", 
    "documents_found": "integer",
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
async function sendChatMessage(message, conversationId = null, chatHistory = []) {
  const response = await fetch('/api/v1/chat/message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      conversation_id: conversationId,
      chat_history: chatHistory,
      include_figma: true,
      include_lucid: true,
      include_documents: true,
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
  console.log("Conversation ID:", result.conversation_id);
  
  // Continue conversation with history
  const followUp = await sendChatMessage(
    "Tell me more about the database connections",
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

  const sendMessage = useCallback(async (message, conversationId, chatHistory) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/v1/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          conversation_id: conversationId,
          chat_history: chatHistory,
          include_figma: true,
          include_lucid: true,
          include_documents: true,
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

### 1. Conversation Management
- Automatic conversation ID generation
- Chat history tracking
- Context-aware responses

### 2. Visual Content Analysis
- Automatic detection of visual queries
- Integration with Figma and Lucid services
- Screenshot capture and analysis
- Architecture-specific analysis for system diagrams

### 3. Multi-Source Search
- Figma file search
- Lucid diagram search
- Document database search
- Configurable source inclusion

### 4. Performance Tracking
- Processing time metrics
- Cost tracking for AI analysis
- Search result summaries

### 5. Error Handling
- Graceful error responses
- Conversation context preservation during errors
- Detailed error information

## Additional Endpoints

### Get Conversation History
```
GET /api/v1/chat/conversation/{conversation_id}
```
*Note: Currently a placeholder - implement database storage for production use*

### Clear Conversation
```
DELETE /api/v1/chat/conversation/{conversation_id}
```
*Note: Currently a placeholder - implement database storage for production use*

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
3. **Conversation Persistence**: Store conversation history in frontend state
4. **Rate Limiting**: Implement client-side rate limiting for better UX
5. **Message Formatting**: Parse and display markdown responses properly

### Performance Optimization
1. **Debouncing**: Debounce rapid message sends
2. **Caching**: Cache conversation history locally
3. **Progressive Loading**: Show partial responses as they arrive (if implementing streaming)

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

1. **Database Storage**: Store conversation history in a database
2. **Authentication**: Add user authentication and authorization
3. **Rate Limiting**: Implement API rate limiting
4. **Logging**: Add comprehensive logging
5. **Monitoring**: Add performance and error monitoring
6. **Caching**: Implement response caching where appropriate 