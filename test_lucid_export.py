#!/usr/bin/env python3
"""
Test script for Lucid document export and upload to Open Arena

This script demonstrates how to:
1. Search for Lucid documents
2. Export a document as an image
3. Upload the image to Open Arena

Usage:
    python test_lucid_export.py
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))


async def test_lucid_export():
    """Test the Lucid export and upload functionality"""
    
    # Import services
    from app.services.lucid_service import lucid_service
    from app.services.data_source_service import data_source_service
    import base64
    
    print("🚀 Testing Lucid Export and Upload to Open Arena")
    print("=" * 50)
    
    # Check if Lucid service is configured
    if not lucid_service or not lucid_service.is_configured:
        print("❌ Error: Lucid API key is not configured")
        print("Please set LUCID_API_KEY in your environment variables")
        return
    
    try:
        # Step 1: Search for available documents
        print("📋 Step 1: Searching for Lucid documents...")
        search_response = await lucid_service.search_documents(limit=5)
        
        if not search_response.documents:
            print("❌ No Lucid documents found")
            return
        
        print(f"✅ Found {len(search_response.documents)} documents:")
        for i, doc in enumerate(search_response.documents):
            print(f"  {i+1}. {doc.title} (ID: {doc.id})")
        
        # Use the first document for testing
        test_document = search_response.documents[0]
        document_id = test_document.id
        
        print(f"\n🎯 Step 2: Exporting document '{test_document.title}'...")
        print(f"   Document ID: {document_id}")
        
        # Step 2: Export the document
        export_result = await lucid_service.export_document_image(
            document_id=document_id,
            format="png",
            width=1920
        )
        
        if not export_result.get("success"):
            print(f"❌ Export failed: {export_result.get('error')}")
            return
        
        image_data = export_result["image_data"]
        print(f"✅ Export successful! Image size: {len(image_data)} bytes")
        
        # Step 3: Upload to Open Arena
        print("\n📤 Step 3: Uploading to Open Arena...")
        
        # Convert to base64
        encoded_content = base64.b64encode(image_data).decode('utf-8')
        
        # Create filename
        filename = f"lucid_export_{document_id}.png"
        
        upload_result = await data_source_service.process_file_upload(
            file_name=filename,
            file_type="png",
            content=encoded_content,
            description=f"Exported from Lucid document: {test_document.title}"
        )
        
        if not upload_result.get("success"):
            print(f"❌ Upload failed: {upload_result.get('error')}")
            return
        
        file_id = upload_result["file_id"]
        print(f"✅ Upload successful! File ID: {file_id}")
        
        print("\n🎉 SUCCESS! Document exported and uploaded successfully")
        print(f"   • Document: {test_document.title}")
        print(f"   • Export size: {len(image_data)} bytes")
        print(f"   • Open Arena File ID: {file_id}")
        
        # Step 4: Show API endpoint usage
        print("\n📡 API Endpoint Usage:")
        print("You can also use the REST API endpoint:")
        print("POST /api/v1/lucid-mcp/export-and-upload")
        print("Body: {")
        print(f"  \"document_id\": \"{document_id}\",")
        print("  \"format\": \"png\",")
        print("  \"width\": 1920")
        print("}")
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main function"""
    print("Lucid Export Test Script")
    print("This script tests exporting Lucid documents and "
          "uploading to Open Arena")
    
    # Run the async test
    asyncio.run(test_lucid_export())


if __name__ == "__main__":
    main() 