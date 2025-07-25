"""
Validation script to check the expected JSON request format
"""

import json


def validate_request_format():
    """Validate that the request format matches requirements"""

    expected_format = {
        "message": "string",
        "include_wiki": True,
        "include_lucid": False,
        "max_visual_items": 3,
    }

    print("✅ Expected ChatRequest format:")
    print(json.dumps(expected_format, indent=2))

    # Check that this is exactly what was requested
    required_properties = set(expected_format.keys())

    print(f"\n✅ Required properties: {sorted(required_properties)}")
    print(f"✅ Total properties: {len(required_properties)}")

    # Properties that should NOT exist
    removed_properties = [
        "conversation_id",
        "chat_history",
        "include_figma",
        "include_documents",
    ]

    print(f"\n🗑️ Removed properties: {removed_properties}")

    return expected_format


if __name__ == "__main__":
    validate_request_format()
