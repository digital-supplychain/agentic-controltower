import json
from crewai.tools import BaseTool
from pydantic import BaseModel, ValidationError
from app.simulations.supply_chain_simulation import SupplyChainSimulation
from app.data_models.simulation_models import SimulationRequest, SimulationResults

class SupplyChainSimulationTool(BaseTool):
    name: str = "Predictive Supply Chain Simulation Tool"
    description: str = """
    Runs a 'what-if' discrete-event simulation of the supply chain to test different ordering policies.
    This tool is essential for comparing the potential outcomes of different heuristic strategies
    before applying one in the live Digital Twin. You must provide the 'initial_state',
    'ordering_policy_str', and a 'scenario_name' as arguments.
    """
    def _run(self, simulation_request: SimulationRequest) -> SimulationResults:
        """
        Executes the Beer Game simulation.

        Args:
            simulation_request: A SimulationRequest object containing all parameters for the simulation run.

        Returns:
            A SimulationResults object with the outcome of the simulation, or an error message if validation fails.
        """
        # Ensure the input is a Pydantic model, handling the case where it's passed as a dict.
        if isinstance(simulation_request, dict):
            try:
                simulation_request = SimulationRequest(**simulation_request)
            except ValidationError as e:
                return f"Error: Invalid simulation request provided. Details: {e}"

        # Initialize the simulation environment with the request and run it.
        simulation = SupplyChainSimulation(
            request=simulation_request
        )
        results = simulation.run()

        return results

def get_simulation_tools() -> list:
    """
    Factory function that returns a list of all available simulation tools.
    """
    return [SupplyChainSimulationTool()]