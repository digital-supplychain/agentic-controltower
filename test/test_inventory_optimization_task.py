import pytest
from crewai import Task, Crew, Process
from app.agents.inventory_optimization_agent import inventory_optimization_agent
from app.control_tower.crew_manager_agent import manager_agent
from app.data_models.optimization_models import OptimizationResult
from app.utils.llm_utils import get_llm

def test_ai_generated_inventory_optimization():
    """
    Test case for the inventory optimization agent to dynamically formulate and solve an optimization problem.
    """
    task = Task(
        description="""
        The 'retailer' node needs to decide on an optimal replenishment order.
        First, you must formulate this situation into a detailed linear programming problem description.
        This description must include the decision variables, the objective function (to minimize total cost),
        and the inventory balance constraint.

        Use the following data for your formulation:
        - Current Inventory: 20 units
        - Demand Forecast: 50 units
        - Holding Cost: $0.5 per unit
        - Stockout Cost: $5.0 per unit
        - Unit Cost: $2.0 per unit

        After formulating the problem description, pass it to the 'Inventory Optimization Tool' within an 'OptimizationProblem' object under the 'problem' argument to solve it.
        """,
        expected_output="An OptimizationResult object containing the optimal value for the 'order_quantity' and the total expected cost.",
        output_pydantic=OptimizationResult,
        agent=inventory_optimization_agent
    )

    local_crew = Crew(
        agents=[inventory_optimization_agent],
        tasks=[task],
        process=Process.hierarchical,
        manager_llm=get_llm(),
        manager_agent=manager_agent,
        verbose=True
    )

    result = local_crew.kickoff()

    print("--- AI-Generated Inventory Optimization Test Result ---")
    print(result)
    print("-------------------------------------------------------")

    assert result.pydantic is not None, "The result should contain a Pydantic object."
    assert isinstance(result.pydantic, OptimizationResult), "The result should be an OptimizationResult object."
    assert "order_quantity" in result.pydantic.variable_values, "Result should contain the optimal order quantity."
    
    # The optimal order is to meet demand exactly, as stockout costs are high.
    order_quantity = result.pydantic.variable_values["order_quantity"]
    assert order_quantity == 30, f"Expected 30 but got {order_quantity}"