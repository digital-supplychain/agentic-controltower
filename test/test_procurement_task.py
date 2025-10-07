from crewai import Task
from app.data_models.supply_chain_models import SupplyChainNodeStatus


def test_procurement_workflow(erp_server):
    """Tests the workflow of the Procurement Agent interacting with the Digital Twin."""
    # This test requires the ERP server to be running.
    # The `erp_server` fixture is passed as an argument to ensure it's active.
    
    # We import the crew here to ensure it's initialized *after* the server is running
    from app.control_tower.crew import control_tower_crew
    from app.agents.procurement_agent import procurement_agent

    print("--- Testing Procurement Agent Workflow ---")

    # --- Step 1: Get initial state via agent ---
    get_initial_state_task = Task(
        description="Get the current state of the 'retailer' node.",
        expected_output="The state of the retailer node.",
        agent=procurement_agent,
        output_pydantic=SupplyChainNodeStatus
    )
    control_tower_crew.tasks = [get_initial_state_task]
    initial_state_result = control_tower_crew.kickoff()
    initial_state: SupplyChainNodeStatus = initial_state_result.pydantic
    print("\n--- Initial State of Retailer ---")
    print(initial_state.model_dump_json(indent=2))

    # --- Step 2: Define and run the procurement task ---
    procurement_task = Task(
        description=f"The retailer's inventory of 'beer' is low. Place an order for 25 units from the retailer to the wholesaler.",
        expected_output="A confirmation that the order was placed successfully, including the order ID.",
        agent=procurement_agent,
        output_pydantic=SupplyChainNodeStatus
    )
    control_tower_crew.tasks = [procurement_task]
    result = control_tower_crew.kickoff()
    print("\n--- Agent Final Output ---")
    print(result)

    # --- Step 3: Get final state via agent and verify ---
    get_final_state_task = Task(
        description="Get the current state of the 'retailer' node.",
        expected_output="The state of the retailer node.",
        agent=procurement_agent,
        output_pydantic=SupplyChainNodeStatus
    )
    control_tower_crew.tasks = [get_final_state_task]
    final_state_result = control_tower_crew.kickoff()
    final_state: SupplyChainNodeStatus = final_state_result.pydantic
    print("\n--- Final State of Retailer ---")
    print(final_state.model_dump_json(indent=2))

    print("\n--- Verification ---")
    # Check if a new outgoing order was created
    assert len(final_state.outgoing_orders) > len(initial_state.outgoing_orders), "No new outgoing order was created."
    
    new_order = final_state.outgoing_orders[-1]
    print(f"✅ Verification successful: A new outgoing order ({new_order.order_id}) was created.")

    # Check if the quantity is correct
    assert new_order.quantity == 25, f"The new order has an incorrect quantity of {new_order.quantity}."
    print(f"✅ Verification successful: The new order has the correct quantity of 25.")