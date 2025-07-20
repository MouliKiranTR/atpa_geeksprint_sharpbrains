#!/usr/bin/env python3
"""
Cache Demo Script

This script demonstrates the new caching functionality for Lucid diagrams.
It shows how exported diagrams are cached locally and automatically uploaded
to OpenArena to avoid repeated downloads and improve performance.
"""

import asyncio
import os
import sys

# Add the app directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.lucid_service import lucid_service
from app.services.cache_service import cache_service


async def demo_caching():
    """Demo the caching functionality"""
    
    print("🚀 Lucid Diagram Caching Demo")
    print("=" * 50)
    
    if not lucid_service:
        print("❌ Lucid service not configured (missing LUCID_API_KEY)")
        return
    
    try:
        # Step 1: Show initial cache stats
        print("\n📊 Step 1: Initial Cache Statistics")
        stats = await cache_service.get_cache_stats()
        print(f"   📂 Cache enabled: {stats.get('enabled', False)}")
        print(f"   📁 Cache directory: {stats.get('cache_dir', 'N/A')}")
        print(f"   📈 Files in cache: {stats.get('total_files', 0)}")
        print(f"   💽 Cache size: {stats.get('total_size_mb', 0)} MB")
        
        # Step 2: Find a document to test with
        print("\n🔍 Step 2: Finding Lucid documents...")
        search_response = await lucid_service.search_documents(limit=3)
        
        if not search_response.documents:
            print("❌ No Lucid documents found")
            return
        
        test_doc = search_response.documents[0]
        document_id = test_doc.id
        print(f"   📋 Selected document: {test_doc.title}")
        print(f"   🆔 Document ID: {document_id}")
        
        # Step 3: First export (should cache the result)
        print(f"\n📤 Step 3: First export (will cache)")
        export_result1 = await lucid_service.export_document_image(
            document_id=document_id,
            format="png",
            width=1920
        )
        
        if not export_result1.get("success"):
            print(f"❌ Export failed: {export_result1.get('error')}")
            return
        
        print(f"   ✅ Export successful!")
        print(f"   📏 Image size: {len(export_result1['image_data'])} bytes")
        print(f"   💾 Cached: {export_result1.get('cached', False)}")
        
        if export_result1.get('file_path'):
            print(f"   📁 Cache file: {export_result1['file_path']}")
        
        cache_info = export_result1.get("cache_info", {})
        if cache_info.get("openarena_upload", {}).get("success"):
            upload_info = cache_info["openarena_upload"]
            print(f"   🚀 Auto-uploaded to OpenArena!")
            print(f"   📋 File ID: {upload_info['file_id']}")
        
        # Step 4: Second export (should use cached version)
        print(f"\n⚡ Step 4: Second export (should use cache)")
        export_result2 = await lucid_service.export_document_image(
            document_id=document_id,
            format="png",
            width=1920
        )
        
        if export_result2.get("success"):
            print(f"   ✅ Export successful!")
            print(f"   📏 Image size: {len(export_result2['image_data'])} bytes")
            print(f"   💾 From cache: {export_result2.get('cached', False)}")
            
            # Compare sizes to verify it's the same content
            same_size = len(export_result1['image_data']) == len(export_result2['image_data'])
            print(f"   🔄 Same content: {same_size}")
        
        # Step 5: Show updated cache stats
        print(f"\n📊 Step 5: Updated Cache Statistics")
        updated_stats = await cache_service.get_cache_stats()
        print(f"   📈 Files in cache: {updated_stats.get('total_files', 0)}")
        print(f"   💽 Cache size: {updated_stats.get('total_size_mb', 0)} MB")
        
        # Step 6: List cached documents
        print(f"\n📋 Step 6: Cached Documents")
        cached_docs = await cache_service.list_cached_documents()
        print(f"   📊 Total cached: {len(cached_docs)}")
        
        for i, doc in enumerate(cached_docs[:3], 1):  # Show first 3
            print(f"   {i}. Document ID: {doc.get('document_id', 'N/A')}")
            print(f"      Format: {doc.get('format', 'N/A')}")
            print(f"      Size: {doc.get('file_size', 0)} bytes")
            print(f"      Cached: {doc.get('cached_at', 'N/A')}")
            
        print(f"\n🎉 Cache Demo Completed Successfully!")
        print(f"\n💡 Key Benefits:")
        print(f"   • Faster subsequent access to same diagrams")
        print(f"   • Automatic upload to OpenArena")
        print(f"   • Reduced API calls to Lucid")
        print(f"   • Local file storage for offline access")
        
        print(f"\n🔧 API Endpoints Available:")
        print(f"   • GET /api/v1/cache/stats - View cache statistics")
        print(f"   • GET /api/v1/cache/list - List cached documents")
        print(f"   • POST /api/v1/cache/cleanup - Clean expired cache")
        print(f"   • GET /api/v1/cache/check/{{doc_id}} - Check specific cache")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main function"""
    print("This demo shows the new caching functionality for Lucid diagrams.")
    print("Make sure you have LUCID_API_KEY configured in your environment.")
    print()
    
    # Run the async demo
    asyncio.run(demo_caching())


if __name__ == "__main__":
    main() 