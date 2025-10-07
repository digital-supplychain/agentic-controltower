# Agentic Supply Chain Control Tower (SCCT)

This project implements a multi-agent system for supply chain management, based on the concept of an Agentic Supply Chain Control Tower (SCCT). The system uses the CrewAI framework to create a team of specialized AI agents that collaborate to solve complex supply chain tasks, such as demand forecasting.

## Key Features

*   **Custom Manager Agent:** A manager agent orchestrates the workflow, delegating tasks to the appropriate agents.
*   **Knowledge Base:** The manager agent is equipped with a knowledge base that contains the project's "memory," allowing it to provide context and guidance to the other agents.
*   **External Configuration:** Agent and task definitions are managed in external YAML files, making the system modular and easy to extend.
*   **Hierarchical Process:** The crew uses a hierarchical process, which allows the manager agent to dynamically manage the workflow.
*   **AI-Driven Simulation & Optimization:** Agents can use predictive simulation (SimPy) to test heuristics and leverage LLMs to dynamically formulate and solve linear programming (PuLP) problems for optimal solutions.

## PoC Enhancements

This PoC has been enhanced with several key features to provide a comprehensive demonstration of the Agentic SCCT framework.

*   **Digital Twin:** A simulated Digital Twin of the Beer Distribution Game supply chain is implemented in `app/digital_twin/`.
*   **External Systems (MCPs):** Mock ERP, Weather, and News servers are implemented in `app/mcp/`.
    *   The **ERP server** runs as a persistent **SSE** server.
    *   The **Weather and News servers** run as on-demand **Stdio** servers.
*   **Testing:** A `/test` directory contains scripts to verify the functionality of the Digital Twin and MCP servers.

## Folder Structure

*   `/app`: Contains the core application logic.
    *   `/agents`: Defines the agents and the crew.
    *   `/config`: Contains the YAML configuration files for agents, tasks, and prompts.
    *   `/digital_twin`: Implements the Digital Twin of the Beer Game.
    *   `/data_models`: Contains Pydantic models for structured data.
    *   `/flows`: Defines structured, multi-step workflows for agents.
    *   `/mcp`: Contains the MCP server implementations.
    *   `/simulations`: Contains PySim simulation models.
    *   `/tools`: Defines custom tools for agents.
    *   `/utils`: Contains utility functions.
*   `/instructions`: Contains markdown files with project documentation.
*   `/knowledge`: Contains knowledge base files for the agents.
*   `/test`: Contains test scripts for the PoC.

## The Agents

This project uses a team of specialized AI agents to manage the supply chain. Each agent has a specific role and set of tools, allowing them to work together to solve complex tasks.

| Agent | Purpose | Functionality | Tools Used |
| :--- | :--- | :--- | :--- |
| **📈 Demand Forecast Agent** | Forecasts short and long-term demand | Uses AI models to generate accurate demand forecasts, adapting to seasonality, trends, and disruptions. | `MCPServerAdapter` (ERP) |
| **📦 Inventory Optimization Agent** | Optimizes safety stock and reorder points | Continuously optimizes inventory levels to balance service levels with holding costs. | `SupplyChainSimulationTool`, `InventoryOptimizationTool` |
| **🛒 Procurement Agent** | Automates supplier selection and purchasing | Automates the procurement process, from supplier selection to purchase order issuance. | `DigitalTwinTools` |
| **🧑‍⚖️ Supplier Evaluation Agent** | Assesses supplier performance and risk | Evaluates suppliers based on key performance indicators (KPIs) to identify high-performing and high-risk partners. | None |
| **🏭 Production Scheduling Agent** | Allocates resources and sequences jobs | Creates efficient and achievable production schedules based on constraints, priorities, and capacity. | None |
| **🚚 Logistics Agent** | Plans and re-routes shipments | Manages the efficient and timely movement of goods throughout the supply chain. | None |
| **👥 Customer Behavior Agent** | Analyzes customer data to predict churn | Analyzes customer data to improve satisfaction and retention. | None |
| **⚠️ Disruption Management Agent** | Monitors risks and triggers contingency plans | Ensures the resilience of the supply chain by monitoring for and responding to disruptions. | `MCPServerAdapter` (Weather, News) |
| **♻️ Sustainability & Compliance Agent** | Ensures alignment with ESG goals | Manages the ethical and sustainable operation of the supply chain. | `FileReadTool` |
| **🧠 Feedback & Learning Agent** | Aggregates data and adjusts agent behavior | Enables the entire system to learn and adapt over time by aggregating data, evaluating performance, and adjusting agent behavior. | `FileReadTool`, `FileWriterTool` |

## How to Run the PoC Demonstrations

This project uses `pytest` to run the demonstration scripts located in the `/test` directory.

### One-Time Setup

First, install the project in "editable" mode along with the testing dependencies. This only needs to be done once.

```bash
uv pip install -e .[test]
```

### Running a Specific Demonstration

To run a single demonstration and see its full output, use the `pytest` command with the `-v` (verbose) and `-s` (show prints) flags, followed by the path to the test file.

| Scenario | Command |
| :--- | :--- |
| **Demonstrate the Digital Twin** | `uv run pytest -v -s test/test_digital_twin.py` |
| **Demonstrate MCP Server Connectivity** | `uv run pytest -v -s test/test_mcp_servers.py` |
| **Demonstrate Demand Forecasting** | `uv run pytest -v -s test/test_demand_forecast_task.py` |
| **Demonstrate Procurement Workflow** | `uv run pytest -v -s test/test_procurement_task.py` |
| **Demonstrate Sustainability Flow** | `uv run pytest -v -s test/test_sustainability_flow.py` |
| **Demonstrate Simulation-Based Optimization** | `uv run pytest -v -s test/test_inventory_ordering_simulation_task.py` |
| **Demonstrate Optimization-Based Decision Making** | `uv run pytest -v -s test/test_inventory_optimization_task.py` |

### Running a Full System Check (Optional)

To run all demonstrations and verify that the entire system is working correctly after making changes, you can run `pytest` without specifying a file.

```bash
uv run pytest -v -s
```