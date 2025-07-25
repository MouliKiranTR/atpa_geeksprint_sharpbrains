#!/usr/bin/env python3
"""
Test script to validate all imports work correctly after figma_service removal
"""


def test_imports():
    """Test that all critical imports work without errors"""
    try:
        print("Testing enhanced_query_service import...")
        from app.services.enhanced_query_service import EnhancedQueryService

        print("✓ EnhancedQueryService imported successfully")

        print("Testing chat endpoint import...")
        from app.api.v1.endpoints.chat import router

        print("✓ Chat endpoint imported successfully")

        print("Testing main app import...")
        from app.main import app

        print("✓ Main app imported successfully")

        print("Testing enhanced_query_service instantiation...")
        service = EnhancedQueryService()
        print("✓ EnhancedQueryService instantiated successfully")

        print(
            "\n🎉 All imports successful! The figma_service cleanup was completed successfully."
        )
        return True

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False


if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
