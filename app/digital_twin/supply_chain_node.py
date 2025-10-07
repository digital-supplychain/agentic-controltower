from typing import List, Dict, Optional
import uuid
from app.data_models.supply_chain_models import Order, Shipment

class SupplyChainNode:
    """
    Represents a single, stateful entity in the supply chain, such as a retailer,
    wholesaler, distributor, or brewery. Each node manages its own inventory,
    orders, and shipments.
    """

    def __init__(self, name: str, node_type: str, initial_inventory: Dict[str, int] = None):
        """
        Initializes a new supply chain node.

        Args:
            name: The unique name of the node (e.g., 'retailer').
            node_type: The type of the node (e.g., 'Retailer').
            initial_inventory: A dictionary mapping product IDs to their starting inventory levels.
        """
        self.name = name.lower()
        self.node_type = node_type
        self.inventory: Dict[str, int] = initial_inventory or {}
        self.incoming_orders: List[Order] = []  # Orders received from the downstream node.
        self.outgoing_orders: List[Order] = []  # Orders placed with the upstream node.
        self.incoming_shipments: List[Shipment] = [] # Shipments arriving at this node.
        self.upstream_node: Optional['SupplyChainNode'] = None
        self.downstream_node: Optional['SupplyChainNode'] = None

    def place_order(self, order: Order):
        """
        Places a new order with this node's upstream supplier.
        The order is added to this node's outgoing orders and the upstream node's incoming orders.
        """
        if not self.upstream_node:
            print(f"ERROR: Node '{self.name}' has no upstream node to order from.")
            return
        
        if not order.order_id:
            order.order_id = str(uuid.uuid4())

        self.outgoing_orders.append(order)
        order.source_node = self.upstream_node.name.lower()
        self.upstream_node.receive_order(order)

    def receive_order(self, order: Order):
        """Receives an order from a downstream node and adds it to the incoming order queue."""
        self.incoming_orders.append(order)

    def fulfill_order(self, order: Order) -> Optional[Shipment]:
        """
        Attempts to fulfill a pending incoming order.
        If inventory is sufficient, it decrements the stock, marks the order as fulfilled,
        and creates a new shipment. Otherwise, it does nothing.

        Args:
            order: The Order object to be fulfilled.

        Returns:
            A new Shipment object if the order was fulfilled, otherwise None.
        """
        if order.status != "PENDING":
            return None

        product_id = order.product_id
        quantity_ordered = order.quantity
        
        if self.inventory.get(product_id, 0) >= quantity_ordered:
            self.inventory[product_id] -= quantity_ordered
            order.status = "FULFILLED"
            
            new_shipment = Shipment(
                order_id=order.order_id,
                product_id=product_id,
                quantity=quantity_ordered,
                source_node=self.name,
                destination_node=order.destination_node.lower(),
                eta=2  # Simulate a 2-step transit time
            )
            print(f"INFO: Node '{self.name}' fulfilled order {order.order_id} and created shipment {new_shipment.shipment_id}.")
            return new_shipment
        else:
            print(f"WARN: Node '{self.name}' has insufficient inventory to fulfill order {order.order_id}.")
            return None

    def receive_shipment(self, shipment: Shipment):
        """
        Receives an incoming shipment from an upstream node and adds the quantity to the inventory.
        """
        product_id = shipment.product_id
        self.inventory[product_id] = self.inventory.get(product_id, 0) + shipment.quantity
        self.incoming_shipments = [s for s in self.incoming_shipments if s.shipment_id != shipment.shipment_id]
        print(f"INFO: Node '{self.name}' received shipment {shipment.shipment_id} of {shipment.quantity} {product_id}.")

    def __repr__(self):
        return f"SupplyChainNode(name='{self.name}', type='{self.node_type}', inventory={self.inventory})"