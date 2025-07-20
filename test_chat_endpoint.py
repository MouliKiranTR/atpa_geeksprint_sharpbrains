"""
Simple test script for the chat endpoint
"""

import asyncio
import json
from app.api.v1.endpoints.chat import send_chat_message, ChatRequest


async def test_chat_endpoint():
    """Test the chat endpoint with a simple message"""
    
    # Test message
    test_request = ChatRequest(
        message="Hello, can you help me understand our system architecture?",
        conversation_id=None,
        chat_history=[],
        include_figma=True,
        include_lucid=True,
        include_documents=True,
        max_visual_items=2
    )
    
    try:
        print("🚀 Testing chat endpoint...")
        print(f"📝 Request: {test_request.message}")
        
        # Call the endpoint
        response = await send_chat_message(test_request)
        
        print("✅ Chat endpoint test successful!")
        print(f"💬 Response: {response.message[:200]}...")
        print(f"🆔 Conversation ID: {response.conversation_id}")
        print(f"📊 Visual query: {response.is_visual_query}")
        print(f"🔍 Analysis type: {response.analysis_type}")
        print(f"⏱️  Processing time: {response.processing_time:.2f}s")
        
        return response
        
    except Exception as e:
        print(f"❌ Chat endpoint test failed: {e}")
        return None


if __name__ == "__main__":
    # Run the test
    result = asyncio.run(test_chat_endpoint())
    
    if result:
        print("\n🎉 Chat endpoint is ready for frontend integration!")
        print("\n📖 Usage instructions:")
        print("POST /api/v1/chat/message")
        print("Content-Type: application/json")
        print("\nRequest body:")
        print(json.dumps({
            "message": "Your message here",
            "conversation_id": "optional-conversation-id",
            "chat_history": [],
            "include_figma": True,
            "include_lucid": True,
            "include_documents": True,
            "max_visual_items": 3
        }, indent=2))
    else:
        print("\n❌ Chat endpoint needs debugging before frontend integration") 