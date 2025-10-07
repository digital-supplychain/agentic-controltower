from pydantic import BaseModel, Field
from typing import Optional
import uuid

class Order(BaseModel):
    """
    Represents a purchase order between two nodes in the supply chain.
    Each order is given a unique ID upon creation.
    """
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the order.")
    product_id: str = Field(..., description="The unique identifier of the product being ordered.")
    quantity: int = Field(..., description="The number of units being ordered.")
    source_node: str = Field(..., description="The name of the node that will fulfill the order (e.g., 'wholesaler').")
    destination_node: str = Field(..., description="The name of the node that is placing the order (e.g., 'retailer').")
    status: str = Field(default="PENDING", description="The current status of the order (e.g., PENDING, FULFILLED).")

class Shipment(BaseModel):
    """
    Represents a physical shipment of goods in transit between two nodes.
    Each shipment is created to fulfill a specific order.
    """
    shipment_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for the shipment.")
    order_id: str = Field(..., description="The ID of the order that this shipment is fulfilling.")
    product_id: str = Field(..., description="The unique identifier of the product in the shipment.")
    quantity: int = Field(..., description="The number of units in the shipment.")
    source_node: str = Field(..., description="The name of the node from which the shipment originates.")
    destination_node: str = Field(..., description="The name of the node to which the shipment is being sent.")
    eta: int = Field(..., description="The estimated time of arrival in simulation steps.")

class SupplyChainNodeStatus(BaseModel):
    """
    Represents a snapshot of the current state of a single node in the supply chain.
    This includes its inventory and any pending orders.
    """
    name: str = Field(..., description="The unique name of the supply chain node (e.g., 'retailer').")
    inventory: dict[str, int] = Field(..., description="A dictionary mapping product IDs to their current inventory levels.")
    incoming_orders: list[Order] = Field(..., description="A list of orders placed by downstream nodes that this node needs to fulfill.")
    outgoing_orders: list[Order] = Field(..., description="A list of orders this node has placed with its upstream node.")

class SupplyChainStatus(BaseModel):
    """
    Represents a complete snapshot of the entire supply chain's state at a specific moment in time.
    This object is used as the initial state for simulations and for historical records.
    """
    current_step: int = Field(..., description="The simulation time step at which this status was recorded.")
    nodes: dict[str, SupplyChainNodeStatus] = Field(..., description="A dictionary of all nodes in the supply chain, keyed by their unique names.")
    shipments_in_transit: list[Shipment] = Field(..., description="A list of all shipments currently in transit between nodes.")