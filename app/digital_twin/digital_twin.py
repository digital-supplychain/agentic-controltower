from typing import List, Dict
from app.digital_twin.supply_chain_node import SupplyChainNode
from app.data_models.supply_chain_models import Order, Shipment, SupplyChainNodeStatus, SupplyChainStatus

class SingletonMeta(type):
    """A metaclass that implements the Singleton design pattern."""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DigitalTwin(metaclass=SingletonMeta):
    """
    Manages the state and logic of the entire Beer Distribution Game supply chain.
    
    This class is implemented as a Singleton to ensure that there is only one instance
    of the supply chain state accessible throughout the application. It is the single
    source of truth for the simulation.
    """

    def __init__(self):
        """Initializes the Digital Twin, setting up the supply chain nodes and initial state."""
        self.nodes: Dict[str, SupplyChainNode] = {}
        self.shipments_in_transit: List[Shipment] = []
        self.current_step: int = 0
        self._initialize_supply_chain()

    def _initialize_supply_chain(self):
        """
        Creates the individual nodes of the Beer Game supply chain and links them together.
        Sets the initial inventory for each node.
        """
        # Create nodes with initial inventory
        self.nodes['retailer'] = SupplyChainNode(name='retailer', node_type='Retailer', initial_inventory={'beer': 100})
        self.nodes['wholesaler'] = SupplyChainNode(name='wholesaler', node_type='Wholesaler', initial_inventory={'beer': 200})
        self.nodes['distributor'] = SupplyChainNode(name='distributor', node_type='Distributor', initial_inventory={'beer': 300})
        self.nodes['brewery'] = SupplyChainNode(name='brewery', node_type='Brewery', initial_inventory={'beer': 500})

        # Link the nodes
        self.nodes['retailer'].upstream_node = self.nodes['wholesaler']
        self.nodes['wholesaler'].downstream_node = self.nodes['retailer']
        self.nodes['wholesaler'].upstream_node = self.nodes['distributor']
        self.nodes['distributor'].downstream_node = self.nodes['wholesaler']
        self.nodes['distributor'].upstream_node = self.nodes['brewery']
        self.nodes['brewery'].downstream_node = self.nodes['distributor']
        
        print("INFO: Digital Twin initialized with the Beer Game supply chain.")

    def step(self):
        """
        Advances the simulation by one time step, processing all events for the period.
        This includes moving shipments, delivering goods, and fulfilling new orders.
        """
        self.current_step += 1
        print(f"\n--- Advancing simulation to step {self.current_step} ---")

        # Update the ETA for all shipments currently in transit.
        arrived_shipments = []
        for shipment in self.shipments_in_transit:
            shipment.eta -= 1
            if shipment.eta <= 0:
                arrived_shipments.append(shipment)

        # Process and deliver all shipments that have arrived at their destination.
        for shipment in arrived_shipments:
            destination_node = self.nodes.get(shipment.destination_node.lower())
            if destination_node:
                destination_node.receive_shipment(shipment)
            self.shipments_in_transit.remove(shipment)

        # Instruct each node to attempt to fulfill any pending incoming orders.
        for node in self.nodes.values():
            # Iterate over a copy of the list to allow for modification during iteration.
            for order in list(node.incoming_orders):
                if order.status == "PENDING":
                    new_shipment = node.fulfill_order(order)
                    if new_shipment:
                        self.shipments_in_transit.append(new_shipment)

    def get_node_state(self, node_name: str) -> SupplyChainNodeStatus:
        """
        Retrieves the current state of a specific node.

        Args:
            node_name: The name of the node to query.

        Returns:
            A SupplyChainNodeStatus object for the requested node, or None if not found.
        """
        node = self.nodes.get(node_name.lower())
        if not node:
            return None
        return SupplyChainNodeStatus(
            name=node.name,
            inventory=node.inventory,
            incoming_orders=node.incoming_orders,
            outgoing_orders=node.outgoing_orders,
        )

    def place_order(self, order: Order) -> SupplyChainNodeStatus:
        """
        Allows an agent to place an order on behalf of a downstream node.
        This is the primary mechanism for agents to interact with and control the supply chain.
        """
        node = self.nodes.get(order.destination_node.lower())
        if not node:
            return None
        
        node.place_order(order)
        return self.get_node_state(order.destination_node.lower())

    def get_full_state(self) -> SupplyChainStatus:
        """Returns a complete snapshot of the entire supply chain's current state."""
        return SupplyChainStatus(
            current_step=self.current_step,
            nodes={name: self.get_node_state(name) for name in self.nodes},
            shipments_in_transit=self.shipments_in_transit
        )