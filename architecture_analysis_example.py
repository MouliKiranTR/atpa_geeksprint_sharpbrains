"""
Example: Architecture Diagram Analysis using Lucid Charts

This example demonstrates how to analyze architecture diagrams from Lucid 
Charts
using the specialized reasoning prompt for structured architectural 
analysis.
"""

import asyncio
from app.services.enhanced_openarena_service import enhanced_openarena_service


async def analyze_lucid_architecture_example():
    """
    Example of analyzing Lucid architecture diagrams with reasoning focus
    """
    
    # Example user question about architecture
    user_question = """
    Please analyze the attached system architecture diagram from Lucid and provide:
    1. Component identification and relationships
    2. Data flow analysis  
    3. Potential bottlenecks or issues
    4. Recommendations for improvement
    5. Security considerations
    6. Scalability assessment
    """
    
    # Example Lucid visual data (focused on architecture diagrams)
    lucid_visual_data = [
        {
            "success": True,
            "source": "lucid",
            "diagram_title": "Microservices System Architecture",
            "diagram_id": "lucid_arch_001",
            "file_path": "/path/to/microservices_architecture.png",
            "capture_method": "lucid_export",
            "metadata": {
                "export_id": "exp_arch_001",
                "format": "PNG",
                "scale": "100%",
                "diagram_type": "system_architecture",
                "created_date": "2024-01-15",
                "last_modified": "2024-01-20"
            }
        },
        {
            "success": True,
            "source": "lucid",
            "diagram_title": "Data Flow and Integration Points",
            "diagram_id": "lucid_data_flow_002", 
            "file_path": "/path/to/data_flow_diagram.png",
            "capture_method": "lucid_export",
            "metadata": {
                "export_id": "exp_flow_002",
                "format": "PNG", 
                "scale": "100%",
                "diagram_type": "data_flow",
                "created_date": "2024-01-15",
                "last_modified": "2024-01-18"
            }
        },
        {
            "success": True,
            "source": "lucid",
            "diagram_title": "Network Topology and Security Zones",
            "diagram_id": "lucid_network_003",
            "file_path": "/path/to/network_topology.png", 
            "capture_method": "lucid_export",
            "metadata": {
                "export_id": "exp_network_003",
                "format": "PNG",
                "scale": "100%",
                "diagram_type": "network_topology",
                "created_date": "2024-01-10",
                "last_modified": "2024-01-16"
            }
        }
    ]
    
    print("🏗️ Starting Lucid Architecture Diagram Analysis...")
    print(f"📋 Question: {user_question}")
    print(f"📐 Lucid Diagrams to analyze: {len(lucid_visual_data)}")
    
    # Analyze with comprehensive reasoning focus
    result = await enhanced_openarena_service.analyze_content(
        user_question=user_question,
        visual_data=lucid_visual_data,
        analysis_type="architecture"
    )
    
    # Process results
    if result["success"]:
        print("✅ Lucid Architecture Analysis Successful!")
        print(f"💰 Cost: {result.get('cost', 'Unknown')}")
        print(f"🎯 Focus: {result['reasoning_focus']}")
        print(f"📊 Diagrams Processed: {result['diagrams_processed']}")
        print(f"📎 Diagrams Attached: {result['diagrams_attached']}")
        print("\n" + "="*60)
        print("📋 LUCID ARCHITECTURE ANALYSIS:")
        print("="*60)
        print(result["analysis"])
        
    else:
        print("❌ Lucid Architecture Analysis Failed!")
        print(f"Error: {result.get('error', 'Unknown error')}")


async def analyze_specific_lucid_diagram_types():
    """
    Demonstrate analysis of different Lucid diagram types with specific focuses
    """
    
    diagram_scenarios = [
        {
            "diagram_data": {
                "success": True,
                "source": "lucid",
                "diagram_title": "API Gateway and Microservices",
                "diagram_id": "lucid_api_gateway",
                "capture_method": "lucid_export",
                "metadata": {
                    "diagram_type": "api_architecture",
                    "description": "API gateway with backend microservices"
                }
            },
            "question": "How well does this API architecture support scalability?",
            "focus": "technical"
        },
        {
            "diagram_data": {
                "success": True,
                "source": "lucid", 
                "diagram_title": "Business Process Workflow",
                "diagram_id": "lucid_business_process",
                "capture_method": "lucid_export",
                "metadata": {
                    "diagram_type": "business_process",
                    "description": "End-to-end customer onboarding process"
                }
            },
            "question": "What are the business value and efficiency opportunities?",
            "focus": "business"
        },
        {
            "diagram_data": {
                "success": True,
                "source": "lucid",
                "diagram_title": "Security Architecture and Controls", 
                "diagram_id": "lucid_security_arch",
                "capture_method": "lucid_export",
                "metadata": {
                    "diagram_type": "security_architecture",
                    "description": "Security zones and access controls"
                }
            },
            "question": "Assess the security posture and identify vulnerabilities",
            "focus": "security"
        }
    ]
    
    for i, scenario in enumerate(diagram_scenarios, 1):
        print(f"\n🎯 Scenario {i}: {scenario['focus'].upper()} Analysis")
        print(f"📊 Diagram: {scenario['diagram_data']['diagram_title']}")
        
        result = await enhanced_openarena_service.analyze_content(
            user_question=scenario['question'],
            visual_data=[scenario['diagram_data']],
            analysis_type="architecture"
        )
        
        if result["success"]:
            print(f"✅ {scenario['focus'].title()} analysis completed")
            # Show preview of analysis
            analysis_preview = result["analysis"][:300] + "..."
            print(f"📝 Preview: {analysis_preview}")
        else:
            print(f"❌ Analysis failed: {result.get('error')}")


async def lucid_metadata_only_analysis():
    """
    Demonstrate analysis using only Lucid metadata (no image files)
    """
    
    user_question = """
    Based on the diagram metadata provided, what can you tell me about 
    the architectural complexity and suggest what additional documentation 
    or diagrams would be helpful?
    """
    
    # Metadata-only Lucid data (no actual image files)
    metadata_only_data = [
        {
            "success": True,
            "source": "lucid",
            "diagram_title": "Enterprise Architecture Overview",
            "diagram_id": "lucid_enterprise_overview",
            "capture_method": "metadata_only",
            "metadata": {
                "export_id": "exp_enterprise_001",
                "diagram_type": "enterprise_architecture",
                "created_date": "2024-01-01",
                "last_modified": "2024-01-25",
                "description": "High-level enterprise architecture showing all systems",
                "page_count": 3,
                "complexity_level": "high",
                "stakeholders": ["CTO", "Solution Architects", "DevOps Team"]
            }
        },
        {
            "success": True, 
            "source": "lucid",
            "diagram_title": "Database Entity Relationships",
            "diagram_id": "lucid_db_erd",
            "capture_method": "metadata_only",
            "metadata": {
                "export_id": "exp_db_001",
                "diagram_type": "database_schema",
                "created_date": "2024-01-10",
                "last_modified": "2024-01-22",
                "description": "Complete database schema with relationships",
                "table_count": 25,
                "complexity_level": "medium"
            }
        }
    ]
    
    print("\n🏗️ Lucid Metadata-Only Analysis...")
    
    result = await enhanced_openarena_service.analyze_content(
        user_question=user_question,
        visual_data=metadata_only_data,
        analysis_type="architecture"
    )
    
    if result["success"]:
        print("✅ Metadata Analysis Successful!")
        print("📋 Analysis Result:")
        print(result["analysis"])
    else:
        print(f"❌ Analysis Failed: {result.get('error')}")


if __name__ == "__main__":
    print("🚀 Lucid Architecture Diagram Analysis Examples")
    print("="*55)
    
    try:
        # Example 1: Full Lucid architecture analysis
        print("🔍 Example 1: Complete Lucid Architecture Analysis")
        asyncio.run(analyze_lucid_architecture_example())
        
        print("\n" + "="*55)
        print("🎯 Example 2: Different Diagram Types & Reasoning Focuses")
        asyncio.run(analyze_specific_lucid_diagram_types())
        
        print("\n" + "="*55)
        print("📊 Example 3: Metadata-Only Analysis")
        asyncio.run(lucid_metadata_only_analysis())
        
    except Exception as e:
        print(f"❌ Example failed: {e}")
        print("Note: This example requires proper authentication")


"""
LUCID-FOCUSED ARCHITECTURE ANALYSIS:

🎯 KEY FEATURES FOR LUCID DIAGRAMS:
- Specialized handling of Lucid diagram metadata
- Support for different Lucid diagram types:
  * System Architecture diagrams
  * Data Flow diagrams  
  * Network Topology diagrams
  * Business Process workflows
  * Database Entity Relationships
  * API Architecture diagrams
  * Security Architecture diagrams

📊 REASONING FOCUS OPTIONS:
- comprehensive: Full architectural analysis
- technical: Deep technical implementation focus
- business: Business process and value analysis  
- security: Security architecture assessment

🔍 ANALYSIS CAPABILITIES:
- Component relationship mapping
- Data flow analysis
- Bottleneck identification
- Security assessment
- Scalability evaluation
- Best practice recommendations

💡 USAGE SCENARIOS:
1. With actual Lucid diagram exports (PNG/JPG files)
2. Metadata-only analysis for high-level insights
3. Focused analysis by diagram type and reasoning focus
4. Multi-diagram analysis for comprehensive system understanding

The prompt automatically adapts to Lucid-specific metadata and provides
structured architectural insights based on visual content and context.
""" 