from crewai import Task
from app.data_models.demand_forecast_models import DemandForecastOutput


def test_demand_forecast_workflow(erp_server):
    """Tests the full workflow of the Demand Forecast Agent."""
    # This test requires the ERP server to be running.
    # The `erp_server` fixture is passed as an argument to ensure it's active.
    
    # We import the crew here to ensure it's initialized *after* the server is running
    from app.control_tower.crew import control_tower_crew
    from app.agents.demand_forecast_agent import demand_forecast_agent

    print("--- Testing Demand Forecast Agent Workflow ---")

    # Define the task for the Demand Forecast Agent
    demand_forecast_task = Task(
        description="Forecast the demand for 'beer' for the next period.",
        expected_output="An object containing the demand forecast, historical data, and risk assessment.",
        agent=demand_forecast_agent,
        output_pydantic=DemandForecastOutput
    )

    control_tower_crew.tasks = [demand_forecast_task]
    result = control_tower_crew.kickoff()
    output: DemandForecastOutput = result.pydantic
    
    print("--- Final Output ---")
    print(output.model_dump_json(indent=2))

    assert len(output.historical_data) > 0
    assert output.risk_assessment is not None and len(output.risk_assessment) > 0
    assert output.demand_forecast.quantity > 0
    print("\n✅ Test Passed!")