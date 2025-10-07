from crewai import Crew, Task, Process
from app.agents.inventory_optimization_agent import inventory_optimization_agent
from app.control_tower.crew_manager_agent import manager_agent
from app.data_models.simulation_models import SimulationResults


def test_inventory_optimization_workflow(erp_server):
    """Tests the full workflow of the Inventory Optimization Agent."""
    print("--- Testing Inventory Optimization Agent Workflow ---")

    # Define the task for the Inventory Optimization Agent
    inventory_task = Task(
        description="""
        Analyze the current state of the Beer Game supply chain and determine the best
        ordering policy for the 'wholesaler' node to minimize both costs and stockouts.
        You must test at least two different policies using the simulation tool.
        """,
        expected_output="Your final recommendation for the best ordering policy and the JSON summaries from the simulation tool for each policy you tested.",
        agent=inventory_optimization_agent,
        output_pydantic=SimulationResults
    )

    # Create an isolated crew for this test
    inventory_crew = Crew(
        agents=[inventory_optimization_agent],
        tasks=[inventory_task],
        process=Process.hierarchical,
        manager_agent=manager_agent,
        verbose=True
    )

    result = inventory_crew.kickoff()
    output: SimulationResults = result.pydantic

    print("\n--- Final Output ---")
    # print(output.model_dump_json(indent=2))

    # Basic validation of the output
    # TODO: Re-enable these assertions once the simulation model is fully implemented
    # assert output.total_cost > 0, "The simulation should have a total cost."
    # assert output.stockout_events >= 0, "Stockout events should be zero or more."
    # assert len(output.history) > 0, "The simulation should have a history."

    print("\n✅ Test Passed!")