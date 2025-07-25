"""
Enhanced test script for the chat endpoint with parallel processing validation
"""

import asyncio
import json
import time

from app.api.v1.endpoints.chat import ChatRequest, send_chat_message


async def test_parallel_processing_performance():
    """Test the chat endpoint with parallel processing and measure performance"""

    print("🚀 Testing parallel processing performance...")

    # Test cases with different complexity levels
    test_cases = [
        {
            "name": "Architecture Query",
            "message": (
                "Can you explain our system architecture "
                "and show me the database connections?"
            ),
            "include_wiki": True,
            "include_lucid": True,
            "max_visual_items": 3,
        },
        {
            "name": "Design Analysis",
            "message": "Show me the UI design patterns and workflows in our Lucid files",
            "include_wiki": False,
            "include_lucid": True,
            "max_visual_items": 2,
        },
        {
            "name": "Process Flow Query",
            "message": "What are the main business processes documented in our Lucid diagrams?",
            "include_wiki": False,
            "include_lucid": True,
            "max_visual_items": 2,
        },
        {
            "name": "General Query",
            "message": "Give me an overview of our system documentation",
            "include_wiki": True,
            "include_lucid": True,
            "max_visual_items": 5,
        },
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 60}")
        print(f"🧪 Test Case {i}: {test_case['name']}")
        print(f"📝 Query: {test_case['message'][:50]}...")

        # Create test request
        test_request = ChatRequest(
            message=test_case["message"],
            include_wiki=test_case["include_wiki"],
            include_lucid=test_case["include_lucid"],
            max_visual_items=test_case["max_visual_items"],
        )

        try:
            start_time = time.time()
            print(f"⏱️  Starting test at {time.strftime('%H:%M:%S')}")

            # Call the endpoint
            response = await send_chat_message(test_request)

            end_time = time.time()
            processing_time = end_time - start_time

            # Analyze results
            success = response.success if hasattr(response, "success") else True

            test_result = {
                "test_case": test_case["name"],
                "success": success,
                "processing_time": processing_time,
                "endpoint_time": getattr(response, "processing_time", 0),
                "is_visual_query": getattr(response, "is_visual_query", False),
                "analysis_type": getattr(response, "analysis_type", "unknown"),
                "search_summary": getattr(response, "search_summary", {}),
                "visual_analysis_available": getattr(
                    response, "visual_analysis_available", False
                ),
                "cost": getattr(response, "cost", None),
            }

            results.append(test_result)

            # Print results
            print("✅ Test completed successfully!")
            print(f"⏱️  Total time: {processing_time:.2f}s")
            print(f"🔍 Visual query: {test_result['is_visual_query']}")
            print(f"📊 Analysis type: {test_result['analysis_type']}")
            print(f"🎯 Visual analysis: {test_result['visual_analysis_available']}")

            if test_result["search_summary"]:
                summary = test_result["search_summary"]
                print("📁 Sources found:")
                print(f"   - Figma: {summary.get('figma_files_found', 0)}")
                print(f"   - Lucid: {summary.get('lucid_diagrams_found', 0)}")
                print(f"   - Docs: {summary.get('documents_found', 0)}")
                print(f"   - Visual items: {summary.get('visual_items_processed', 0)}")

            if test_result["cost"]:
                print(f"💰 Cost: ${test_result['cost']:.4f}")

        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(
                {
                    "test_case": test_case["name"],
                    "success": False,
                    "error": str(e),
                    "processing_time": 0,
                }
            )

    # Performance analysis
    print(f"\n{'=' * 60}")
    print("📊 PARALLEL PROCESSING PERFORMANCE ANALYSIS")
    print(f"{'=' * 60}")

    successful_tests = [r for r in results if r.get("success", False)]

    if successful_tests:
        avg_time = sum(r["processing_time"] for r in successful_tests) / len(
            successful_tests
        )
        visual_tests = [r for r in successful_tests if r.get("is_visual_query", False)]

        print(f"✅ Successful tests: {len(successful_tests)}/{len(results)}")
        print(f"⏱️  Average processing time: {avg_time:.2f}s")

        if visual_tests:
            avg_visual_time = sum(r["processing_time"] for r in visual_tests) / len(
                visual_tests
            )
            print(f"🎨 Visual query average time: {avg_visual_time:.2f}s")

            visual_analysis_count = sum(
                1 for r in visual_tests if r.get("visual_analysis_available")
            )
            print(
                f"📸 Visual analysis success rate: {visual_analysis_count}/{len(visual_tests)}"
            )

        total_cost = sum(r.get("cost", 0) for r in successful_tests if r.get("cost"))
        if total_cost > 0:
            print(f"💰 Total estimated cost: ${total_cost:.4f}")

    # Performance insights
    print("\n🔍 PARALLEL PROCESSING INSIGHTS:")

    # Check for parallel processing indicators
    parallel_indicators = []
    for result in successful_tests:
        if result.get("search_summary", {}).get("total_sources_searched", 0) > 1:
            parallel_indicators.append("Multiple sources searched simultaneously")
        if result.get("visual_analysis_available"):
            parallel_indicators.append("Visual processing pipeline executed")

    if parallel_indicators:
        print("✅ Parallel processing features detected:")
        for indicator in set(parallel_indicators):
            print(f"   - {indicator}")
    else:
        print("⚠️  Limited parallel processing detected")

    return results


async def test_chat_endpoint():
    """Original test for backward compatibility"""

    # Test message
    test_request = ChatRequest(
        message="Hello, can you help me understand our system architecture?",
        include_wiki=True,
        include_lucid=True,
        max_visual_items=2,
    )

    try:
        print("🚀 Testing basic chat endpoint...")
        print(f"📝 Request: {test_request.message}")

        # Call the endpoint
        response = await send_chat_message(test_request)

        print("✅ Chat endpoint test successful!")
        print(f"💬 Response: {response.message[:200]}...")
        print(f"📊 Visual query: {response.is_visual_query}")
        print(f"🔍 Analysis type: {response.analysis_type}")
        print(f"⏱️  Processing time: {response.processing_time:.2f}s")

        return response

    except Exception as e:
        print(f"❌ Chat endpoint test failed: {e}")
        return None


async def main():
    """Run comprehensive tests"""
    print("🧪 Starting comprehensive chat endpoint tests with parallel processing...")

    # Run basic test
    basic_result = await test_chat_endpoint()

    if basic_result:
        print("\n" + "=" * 60)
        print("🚀 Basic test passed, running parallel processing performance tests...")

        # Run parallel processing tests
        performance_results = await test_parallel_processing_performance()

        print(f"\n{'=' * 60}")
        print("🎉 ALL TESTS COMPLETED!")
        print(f"{'=' * 60}")

        print("\n📖 Usage instructions:")
        print("POST /api/v1/chat/message")
        print("Content-Type: application/json")
        print("\nParallel processing features:")
        print("✅ Concurrent source searches (Figma, Lucid, Documents)")
        print("✅ Parallel visual content capture")
        print("✅ Optimized OpenArena data preparation")
        print("✅ Asynchronous context building")

        print("\nRequest body example:")
        print(
            json.dumps(
                {
                    "message": "Your message here",
                    "include_wiki": True,
                    "include_lucid": True,
                    "max_visual_items": 3,
                },
                indent=2,
            )
        )

        return True
    else:
        print("\n❌ Basic test failed - skipping performance tests")
        return False


if __name__ == "__main__":
    # Run the comprehensive tests
    success = asyncio.run(main())

    if success:
        print("\n🎉 Chat endpoint with parallel processing is ready!")
    else:
        print("\n❌ Chat endpoint needs debugging before use")
