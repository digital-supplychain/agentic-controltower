from pydantic import BaseModel, Field
from typing import List, Dict
from .supply_chain_models import SupplyChainNodeStatus, Shipment

class Product(BaseModel):
    """Data model for a product, representing its master data in an ERP system."""
    name: str = Field(..., description="The official name of the product.")
    cost: float = Field(..., description="The standard cost per unit of the product.")
    lead_time: int = Field(..., description="The expected time, in simulation steps, to replenish the product.")

class Supplier(BaseModel):
    """Data model for a supplier, representing its master data in an ERP system."""
    name: str = Field(..., description="The name of the supplier.")
    reliability_score: float = Field(..., description="A score representing the supplier's reliability.")
    price: float = Field(..., description="The price per unit from this supplier.")

class HistoricalData(BaseModel):
    """
    Represents the historical state of the supply chain for a single recorded period.
    This is used for analysis and as input for forecasting models.
    """
    period: int = Field(..., description="The simulation period number for which this data was recorded.")
    nodes: Dict[str, SupplyChainNodeStatus] = Field(..., description="A dictionary containing the status of each node at the end of that period.")
    shipments_in_transit: List[Shipment] = Field(..., description="A list of all shipments that were in transit during that period.")

class StatusResponse(BaseModel):
    """A simple, generic status response model for operations that do not return complex data."""
    status: str = Field(..., description="The status of the operation (e.g., 'success', 'error').")
    message: str = Field(..., description="A message providing details about the operation.")