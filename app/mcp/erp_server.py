from typing import List
from mcp.server.fastmcp import FastMCP
from app.data_models.erp_models import Product, Supplier, HistoricalData, StatusResponse
from app.data_models.supply_chain_models import SupplyChainStatus, SupplyChainNodeStatus, Order, Shipment

# This server simulates a basic ERP system.
mcp = FastMCP("ERP", port=8000, host="127.0.0.1")

class Database:
    """A simple in-memory database using Pydantic models."""
    def __init__(self):
        self.products = {
            "beer": Product(name="Premium Lager", cost=10, lead_time=7)
        }
        self.suppliers = {
            "beer": [
                Supplier(name="Brewery A", reliability_score=0.95, price=9.5),
                Supplier(name="Brewery B", reliability_score=0.88, price=8.9),
            ]
        }
        self.history = [
            HistoricalData(
                period=1,
                nodes={
                    "retailer": SupplyChainNodeStatus(name='retailer', inventory={'beer': 85}, incoming_orders=[], outgoing_orders=[Order(product_id='beer', quantity=15, source_node='wholesaler', destination_node='retailer')]),
                    "wholesaler": SupplyChainNodeStatus(name='wholesaler', inventory={'beer': 180}, incoming_orders=[Order(product_id='beer', quantity=15, source_node='wholesaler', destination_node='retailer')], outgoing_orders=[Order(product_id='beer', quantity=20, source_node='distributor', destination_node='wholesaler')]),
                    "distributor": SupplyChainNodeStatus(name='distributor', inventory={'beer': 280}, incoming_orders=[Order(product_id='beer', quantity=20, source_node='distributor', destination_node='wholesaler')], outgoing_orders=[Order(product_id='beer', quantity=20, source_node='brewery', destination_node='distributor')]),
                    "brewery": SupplyChainNodeStatus(name='brewery', inventory={'beer': 480}, incoming_orders=[Order(product_id='beer', quantity=20, source_node='brewery', destination_node='distributor')], outgoing_orders=[])
                },
                shipments_in_transit=[Shipment(order_id='dummy_order_id', product_id='beer', quantity=15, source_node='wholesaler', destination_node='retailer', eta=1)]
            ),
            HistoricalData(
                period=2,
                nodes={
                    "retailer": SupplyChainNodeStatus(name='retailer', inventory={'beer': 100}, incoming_orders=[], outgoing_orders=[Order(product_id='beer', quantity=25, source_node='wholesaler', destination_node='retailer')]),
                    "wholesaler": SupplyChainNodeStatus(name='wholesaler', inventory={'beer': 160}, incoming_orders=[Order(product_id='beer', quantity=25, source_node='wholesaler', destination_node='retailer')], outgoing_orders=[Order(product_id='beer', quantity=25, source_node='distributor', destination_node='wholesaler')]),
                    "distributor": SupplyChainNodeStatus(name='distributor', inventory={'beer': 260}, incoming_orders=[Order(product_id='beer', quantity=25, source_node='distributor', destination_node='wholesaler')], outgoing_orders=[Order(product_id='beer', quantity=25, source_node='brewery', destination_node='distributor')]),
                    "brewery": SupplyChainNodeStatus(name='brewery', inventory={'beer': 460}, incoming_orders=[Order(product_id='beer', quantity=25, source_node='brewery', destination_node='distributor')], outgoing_orders=[])
                },
                shipments_in_transit=[
                    Shipment(order_id='dummy_order_id_2', product_id='beer', quantity=20, source_node='wholesaler', destination_node='retailer', eta=1),
                    Shipment(order_id='dummy_order_id_3', product_id='beer', quantity=25, source_node='distributor', destination_node='wholesaler', eta=2)
                ]
            )
        ]

# Create a single instance of the database
DB = Database()

@mcp.tool()
def get_product_info(product_id: str) -> Product:
    """Returns information about a specific product."""
    return DB.products.get(product_id)

@mcp.tool()
def get_supplier_info(product_id: str) -> List[Supplier]:
    """Returns a list of suppliers for a specific product."""
    return DB.suppliers.get(product_id, [])

@mcp.tool()
def get_historical_data() -> List[HistoricalData]:
    """Returns historical order and inventory data."""
    return DB.history

@mcp.tool()
def record_period_data(period_data: SupplyChainStatus) -> StatusResponse:
    """Records the state of the Digital Twin for a given period."""
    try:
        # Convert the live status object to a historical record
        historical_entry = HistoricalData(
            period=period_data.current_step,
            nodes=period_data.nodes,
            shipments_in_transit=period_data.shipments_in_transit
        )
        DB.history.append(historical_entry)
        return StatusResponse(status="success", message=f"Data for period {period_data.current_step} recorded.")
    except Exception as e:
        return StatusResponse(status="error", message=str(e))

if __name__ == "__main__":
    mcp.run(transport="sse")