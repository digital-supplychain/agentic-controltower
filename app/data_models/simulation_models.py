from pydantic import BaseModel, Field
from typing import List, Dict, Callable
from .supply_chain_models import SupplyChainStatus

class SimulationRequest(BaseModel):
    """
    Defines the inputs for a predictive simulation run.
    This model structures the request sent to the SupplyChainSimulationTool.
    """
    initial_state: SupplyChainStatus = Field(..., description="The complete starting state of the supply chain for the simulation.")
    ordering_policy_str: str = Field(..., description="A string containing a Python lambda function that defines the ordering logic to be tested.")
    steps: int = Field(default=20, description="The number of time steps the simulation will run for.")
    scenario_name: str = Field(default="Default Scenario", description="A descriptive name for the simulation scenario.")

    def get_ordering_policy(self) -> Callable:
        """
        Dynamically evaluates the ordering_policy_str and returns it as a callable function.
        This allows agents to test arbitrary heuristic ordering policies.

        Warning:
            Using `eval` is a security risk in a production environment. It is used here for
            simplicity in this Proof-of-Concept. A production system would require a safer
            method for defining and executing policies.
        """
        try:
            return eval(self.ordering_policy_str)
        except Exception as e:
            raise ValueError(f"Invalid ordering policy lambda: {e}")

class SimulationStepResult(BaseModel):
    """Data model for the state of the simulation at a single time step."""
    step: int = Field(..., description="The time step number.")
    nodes: Dict[str, Dict[str, float]] = Field(..., description="A dictionary summarizing the state (e.g., inventory, cost) of each node at this step.")

class SimulationResults(BaseModel):
    """Data model for the final, aggregated results of a simulation run."""
    total_cost: float
    stockout_events: int
    history: List[SimulationStepResult]