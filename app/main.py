import pytest
import sys

def run_all_tests():
    """
    Runs all demonstration test cases sequentially using pytest.
    This serves as the main entry point for verifying the PoC's functionality.
    """
    print("--- Running All Agentic SCCT PoC Demonstrations ---")
    
    # Define the list of test files to run in a specific order
    test_files = [
        "test/test_digital_twin.py",
        "test/test_mcp_servers.py",
        "test/test_demand_forecast_task.py",
        "test/test_procurement_task.py",
        "test/test_sustainability_flow.py",
        "test/test_inventory_ordering_simulation_task.py",
        "test/test_inventory_optimization_task.py"
    ]
    
    # Execute pytest on the specified files
    # The '-v' flag is for verbose output, and '-s' is to show print statements.
    result_code = pytest.main(["-v", "-s"] + test_files)
    
    print("--- All Demonstrations Complete ---")
    
    # Exit with the appropriate code to indicate success or failure
    if result_code == 0:
        print("✅ All tests passed successfully!")
    else:
        print(f"❌ Some tests failed. (Exit code: {result_code})")
    sys.exit(result_code)

if __name__ == "__main__":
    run_all_tests()
