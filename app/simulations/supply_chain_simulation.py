import simpy
import random
import json
from app.data_models.supply_chain_models import SupplyChainStatus
from app.data_models.simulation_models import SimulationRequest, SimulationResults, SimulationStepResult

class SupplyChainSimulation:
    """A SimPy-based discrete-event simulation of the Beer Distribution Game."""

    def __init__(self, request: SimulationRequest):
        """
        Initializes the simulation environment.

        Args:
            request: A SimulationRequest object containing the initial state and parameters for the simulation.
        """
        self.env = simpy.Environment()
        self.request = request
        self.nodes = {}
        self.results = SimulationResults(total_cost=0, stockout_events=0, history=[])

    def run(self) -> SimulationResults:
        """
        Runs the full discrete-event simulation for the supply chain.

        Returns:
            A SimulationResults object containing the final costs, stockout events, and step-by-step history.
        """
        self._log_request()
        self.env.process(self.setup())
        self.env.run(until=self.request.steps)

        # Final cost calculation aggregates costs from all nodes
        self.results.total_cost = sum(n['cost'] for n in self.nodes.values())
        self._log_results()
        return self.results

    def setup(self):
        """
        Initializes the simulation environment, creating and linking all supply chain nodes.
        This is a generator function required by SimPy.
        """
        # Initialize nodes from the initial state provided in the request
        for name, node_status in self.request.initial_state.nodes.items():
            self.nodes[name] = {
                "name": name,
                "inventory": node_status.inventory.get('beer', 0),
                "incoming_orders": [],
                "cost": 0,
                "downstream_node": None  # Will be linked below
            }

        # Link nodes (currently hardcoded for the Beer Game topology)
        # TODO: Generalize this to support arbitrary supply chain topologies.
        self.nodes['brewery']['downstream_node'] = self.nodes['distributor']
        self.nodes['distributor']['downstream_node'] = self.nodes['wholesaler']
        self.nodes['wholesaler']['downstream_node'] = self.nodes['retailer']
        
        # Start a SimPy process for each node to run its logic concurrently.
        for name in self.nodes:
            self.env.process(self.node_process(self.nodes[name]))
        
        yield self.env.timeout(0)

    def node_process(self, node):
        """
        The main process governing the behavior of a single supply chain node in each simulation step.
        This is a generator function required by SimPy.

        Args:
            node: A dictionary representing the state of a supply chain node.
        """
        while True:
            # Step 1: Determine demand for the current time step.
            if node['name'] == 'retailer':
                # For the retailer, demand is stochastic (random) to simulate customer behavior.
                demand = random.randint(10, 30)
            else:
                # For upstream nodes, demand is the sum of incoming orders from the downstream node.
                demand = 0
                if node.get('incoming_orders'):
                    demand = sum(order['quantity'] for order in node['incoming_orders'])
                    node['incoming_orders'] = []  # Clear orders after they are processed.

            # Step 2: Fulfill demand based on available inventory.
            if node['inventory'] >= demand:
                # If there is enough inventory, fulfill the full demand.
                node['inventory'] -= demand
                if node['downstream_node']:
                    # Trigger the delivery process to the downstream node.
                    self.env.process(self.deliver(node['downstream_node'], demand))
            else:
                # If there is a stockout, fulfill with whatever inventory is available.
                self.results.stockout_events += 1
                if node['downstream_node']:
                    self.env.process(self.deliver(node['downstream_node'], node['inventory']))
                node['inventory'] = 0

            # Step 3: Apply inventory holding cost for any remaining stock.
            node['cost'] += node['inventory'] * 0.5

            # Step 4: Place a new replenishment order based on the agent's chosen policy.
            # The ordering policy is a callable function (e.g., a lambda) passed in the simulation request.
            order_quantity = self.request.get_ordering_policy()(
                node_name=node['name'],
                current_inventory=node['inventory'],
                demand=demand
            )
            
            if node['name'] != 'brewery':
                # All nodes except the brewery place an order with their upstream supplier.
                upstream_node = self._get_upstream_node(node['name'])
                if upstream_node:
                    upstream_node['incoming_orders'].append({'quantity': order_quantity})
            else:
                # The brewery "produces" its own order, simulating a production lead time.
                self.env.process(self.deliver(node, order_quantity))

            # Step 5: Record the state of all nodes at the end of the current time step.
            step_state = SimulationStepResult(
                step=self.env.now,
                nodes={name: {"inventory": data["inventory"], "cost": data["cost"]} for name, data in self.nodes.items()}
            )
            self.results.history.append(step_state)

            # Step 6: Wait for one time unit to pass before the next step.
            yield self.env.timeout(1)

    def deliver(self, target_node, quantity):
        """
        Simulates the lead time for a delivery between nodes.
        This is a generator function required by SimPy.

        Args:
            target_node: The destination node for the delivery.
            quantity: The number of units being delivered.
        """
        yield self.env.timeout(1)  # Represents a lead time of 1 simulation step.
        target_node['inventory'] += quantity

    def _get_upstream_node(self, node_name):
        """
        Retrieves the upstream node in the hardcoded Beer Game topology.
        
        Args:
            node_name: The name of the current node.

        Returns:
            A dictionary representing the upstream node, or None if not found.
        """
        # TODO: Generalize this to support arbitrary supply chain topologies.
        if node_name == 'retailer': return self.nodes['wholesaler']
        if node_name == 'wholesaler': return self.nodes['distributor']
        if node_name == 'distributor': return self.nodes['brewery']
        return None

    def _log_request(self):
        """Prints a formatted summary of the simulation request."""
        print("\n" + "╔" + "═" * 50 + "╗")
        print(f"║ {'Simulation Request':^48} ║")
        print("╠" + "═" * 50 + "╣")
        print(f"║ Scenario: {self.request.scenario_name:<38} ║")
        print(f"║ Steps: {self.request.steps:<41} ║")
        print(f"║ Policy: {self.request.ordering_policy_str:<40} ║")
        print("╚" + "═" * 50 + "╝")

    def _log_results(self):
        """Prints a formatted summary of the final simulation results."""
        print("\n" + "╔" + "═" * 50 + "╗")
        print(f"║ {'Simulation Results':^48} ║")
        print("╠" + "═" * 50 + "╣")
        print(f"║ Scenario: {self.request.scenario_name:<38} ║")
        print("╟" + "─" * 50 + "╢")
        print(f"║ Total Cost: {self.results.total_cost:<36.2f} ║")
        print(f"║ Stockout Events: {self.results.stockout_events:<31} ║")
        print("╟" + "─" * 50 + "╢")
        print(f"║ {'Final Inventory':^48} ║")
        print("╟" + "─" * 50 + "╢")

        if not self.results.history:
            print("║ No history recorded. {'':<30} ║")
        else:
            final_step = self.results.history[-1]
            for node_name, data in final_step.nodes.items():
                inv_str = f"{data['inventory']:.0f} units"
                print(f"║   - {node_name.capitalize()}: {inv_str:<37} ║")
        
        print("╚" + "═" * 50 + "╝" + "\n")