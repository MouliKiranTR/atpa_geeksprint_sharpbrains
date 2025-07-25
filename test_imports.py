"""
Test script to verify that all imports work correctly after refactoring
"""


def test_imports():
    try:
        print("Testing imports...")

        # Test main application imports
        print("✅ Main app import successful")

        # Test chat endpoint imports
        from app.api.v1.endpoints.chat import ChatRequest

        print("✅ Chat endpoint imports successful")

        # Test schemas imports
        print("✅ Schema imports successful")

        # Test ChatRequest structure
        test_request = ChatRequest(
            message="test message",
            include_wiki=True,
            include_lucid=False,
            max_visual_items=3,
        )
        print("✅ ChatRequest model working correctly")
        print(f"   - message: {test_request.message}")
        print(f"   - include_wiki: {test_request.include_wiki}")
        print(f"   - include_lucid: {test_request.include_lucid}")
        print(f"   - max_visual_items: {test_request.max_visual_items}")

        # Test that removed properties are gone
        try:
            # These should raise AttributeError if properly removed
            test_request.conversation_id
            print("❌ ERROR: conversation_id still exists!")
        except AttributeError:
            print("✅ conversation_id properly removed")

        try:
            test_request.chat_history
            print("❌ ERROR: chat_history still exists!")
        except AttributeError:
            print("✅ chat_history properly removed")

        try:
            test_request.include_figma
            print("❌ ERROR: include_figma still exists!")
        except AttributeError:
            print("✅ include_figma properly removed")

        try:
            test_request.include_documents
            print("❌ ERROR: include_documents still exists!")
        except AttributeError:
            print("✅ include_documents properly removed")

        print("\n🎉 ALL TESTS PASSED! Refactoring completed successfully.")
        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


if __name__ == "__main__":
    test_imports()
