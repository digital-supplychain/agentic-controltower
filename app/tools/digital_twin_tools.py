import json
from crewai.tools import BaseTool, tool
from app.digital_twin import DigitalTwin
from app.data_models.supply_chain_models import Order, SupplyChainNodeStatus, SupplyChainStatus

# Create a singleton instance of the DigitalTwin to be used by all tools.
# This ensures that all agents interact with the same, consistent state.
digital_twin = DigitalTwin()

@tool("Get Node State Tool")
def get_node_state(node_name: str) -> SupplyChainNodeStatus:
    """
    Returns the current state of a specific supply chain node from the Digital Twin.
    This includes inventory levels, incoming orders, and outgoing orders.
    """
    return digital_twin.get_node_state(node_name)

@tool("Get Full Supply Chain State Tool")
def get_supply_chain_state() -> SupplyChainStatus:
    """
    Returns the complete current state of the entire supply chain from the Digital Twin.
    This includes the state of all nodes and any shipments currently in transit.
    """
    return digital_twin.get_full_state()

@tool("Place Order Tool")
def place_order_in_digital_twin(order: Order) -> SupplyChainNodeStatus:
    """
    Places a new order in the Digital Twin. This is the primary way agents act upon the supply chain.
    The tool automatically handles the conversion from a dictionary to an Order object if needed.
    """
    if isinstance(order, dict):
        order = Order(**order)
    return digital_twin.place_order(order)

@tool("Advance Simulation Tool")
def advance_digital_twin_simulation() -> None:
    """
    Advances the Digital Twin simulation by one time step.
    This processes shipments, fulfills orders, and updates the state of the entire supply chain.
    """
    digital_twin.step()

def get_digital_twin_tools() -> list:
    """
    Factory function that returns a list of all available Digital Twin tools.
    This allows agents to be easily equipped with all necessary tools to interact with the simulation.
    """
    return [
        get_node_state,
        get_supply_chain_state,
        place_order_in_digital_twin,
        advance_digital_twin_simulation
    ]