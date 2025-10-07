from app.digital_twin import DigitalTwin
from app.data_models.supply_chain_models import Order


def test_digital_twin_simulation():
    """Tests the basic functionality of the Digital Twin."""
    print("--- Testing Digital Twin Simulation ---")

    # Initialize the Digital Twin
    dt = DigitalTwin()

    print("\n--- Initial State ---")
    print(dt.get_full_state().model_dump_json(indent=2))

    # --- Simulation ---
    # Step 1: Retailer places an order
    print("\n--- Retailer places an order for 20 units of beer ---")
    order = Order(product_id='beer', quantity=20, source_node='wholesaler', destination_node='retailer')
    dt.place_order(order)
    

    # Verify the order was placed correctly
    retailer_state = dt.get_node_state('retailer')
    wholesaler_state = dt.get_node_state('wholesaler')
    assert len(retailer_state.outgoing_orders) == 1
    assert retailer_state.outgoing_orders[-1].order_id == order.order_id
    assert len(wholesaler_state.incoming_orders) == 1
    assert wholesaler_state.incoming_orders[-1].order_id == order.order_id
    print("✅ Order placement verified.")

    # Step 2: Advance the simulation (Order is fulfilled, shipment is created)
    dt.step()
    print("\n--- State after Step 1 ---")
    state_step1 = dt.get_full_state()
    print(state_step1.model_dump_json(indent=2))

    # Verify shipment creation and inventory update
    assert len(state_step1.shipments_in_transit) == 1
    assert state_step1.shipments_in_transit[-1].order_id == order.order_id
    assert state_step1.nodes['wholesaler'].inventory['beer'] == 180  # 200 - 20
    assert state_step1.nodes['retailer'].inventory['beer'] == 100  # Unchanged
    print("✅ Step 1 verified: Shipment created, inventory updated.")

    # Step 3: Advance the simulation again (Shipment ETA decreases)
    dt.step()
    print("\n--- State after Step 2 ---")
    state_step2 = dt.get_full_state()
    print(state_step2.model_dump_json(indent=2))

    # Verify ETA update
    assert len(state_step2.shipments_in_transit) == 1
    assert state_step2.shipments_in_transit[-1].eta == 1
    print("✅ Step 2 verified: Shipment ETA updated.")

    # Step 4: Advance the simulation again (Shipment arrives)
    dt.step()
    print("\n--- State after Step 3 ---")
    state_step3 = dt.get_full_state()
    print(state_step3.model_dump_json(indent=2))

    # Verify shipment arrival and inventory update
    assert len(state_step3.shipments_in_transit) == 0
    assert state_step3.nodes['retailer'].inventory['beer'] == 120  # 100 + 20
    print("✅ Step 3 verified: Shipment arrived, inventory updated.")