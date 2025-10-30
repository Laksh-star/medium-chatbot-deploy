"""Simple test of workflow imports without external dependencies."""

try:
    print("Testing workflow imports...")
    from app.workflows import DiscoveryWorkflow, TechExplorerWorkflow, AnalyticsWorkflow
    print("✅ Workflow imports successful")
    
    print("\nTesting workflow instantiation...")
    discovery = DiscoveryWorkflow()
    tech_explorer = TechExplorerWorkflow() 
    analytics = AnalyticsWorkflow()
    print("✅ Workflow instantiation successful")
    
    print("\nWorkflows ready for deployment!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()