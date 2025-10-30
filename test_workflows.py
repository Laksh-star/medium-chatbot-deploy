"""Test script for Medium Articles Chatbot workflows."""

import asyncio
import os
from app.workflows import discovery_workflow, tech_explorer_workflow, analytics_workflow

# Set test environment variables (use fake keys for testing)
os.environ["LLAMA_CLOUD_API_KEY"] = "llx-test-key"
os.environ["OPENAI_API_KEY"] = "sk-test-key"

async def test_discovery_workflow():
    """Test discovery workflow with sample query."""
    print("🔍 Testing Discovery Workflow...")
    try:
        result = await discovery_workflow.run(query="What Python articles do you have?")
        print(f"✅ Discovery Result: {result.result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Discovery Error: {e}")
        return False

async def test_tech_explorer_workflow():
    """Test tech explorer workflow with sample query."""
    print("\n🔬 Testing Tech Explorer Workflow...")
    try:
        result = await tech_explorer_workflow.run(query="What technologies does the author use?")
        print(f"✅ Tech Explorer Result: {result.result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Tech Explorer Error: {e}")
        return False

async def test_analytics_workflow():
    """Test analytics workflow with sample query."""
    print("\n📊 Testing Analytics Workflow...")
    try:
        result = await analytics_workflow.run(query="What content gaps should I address?")
        print(f"✅ Analytics Result: {result.result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Analytics Error: {e}")
        return False

async def main():
    """Run all workflow tests."""
    print("🧪 Starting Medium Articles Chatbot Workflow Tests\n")
    
    results = []
    results.append(await test_discovery_workflow())
    results.append(await test_tech_explorer_workflow()) 
    results.append(await test_analytics_workflow())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All workflows working correctly!")
    else:
        print("⚠️ Some workflows need attention")

if __name__ == "__main__":
    asyncio.run(main())