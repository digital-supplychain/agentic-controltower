# Agentic Supply Chain Control Tower (SCCT)
**Harnessing Generative AI and Agentic AI for Autonomous & Resilient Supply Chain Management**

---

## Introduction: What is Agentic SCCT? Why Does It Matter?
Traditional supply chains struggle to react quickly to constant disruptions, creating a gap between seeing a problem and solving it. The Agentic Supply Chain Control Tower (SCCT) is a new paradigm where a team of autonomous AI agents actively manages the supply chain, enabling it to predict issues, make intelligent decisions, and act on them 24/7 to become more resilient and efficient.

## What is this Repository About?
This repository contains a hands-on, executable Proof-of-Concept (PoC) that brings the Agentic SCCT framework to life. It uses a simulation of the classic "Beer Distribution Game" to provide a testbed where you can run demonstrations and see how these AI agents collaborate to manage complex supply chain challenges.

## Agentic Workforce: The Team of AI Agents
This project uses a team of 10 specialized AI agents, orchestrated by a central manager agent. Each agent has a specific role and a curated set of tools, allowing them to collaborate effectively to solve complex tasks.

| Agent | Purpose |
| :--- | :--- |
| **📈 Demand Forecast Agent** | Forecasts short and long-term demand |
| **📦 Inventory Optimization Agent** | Optimizes safety stock and reorder points |
| **🛒 Procurement Agent** | Automates supplier selection and purchasing |
| **🧑‍⚖️ Supplier Evaluation Agent** | Assesses supplier performance and risk |
| **🏭 Production Scheduling Agent** | Allocates resources and sequences jobs |
| **🚚 Logistics Agent** | Plans and re-routes shipments |
| **👥 Customer Behavior Agent** | Analyzes customer data to predict churn |
| **⚠️ Disruption Management Agent** | Monitors risks and triggers contingency plans |
| **♻️ Sustainability & Compliance Agent** | Ensures alignment with ESG goals |
| **🧠 Feedback & Learning Agent** | Aggregates data and adjusts agent behavior |

## Technical Stack
*   **Core Language:** Python
*   **Agent Framework:** [CrewAI](https://github.com/joaomdmoura/crewAI) - A popular open-source framework for building and orchestrating autonomous AI agents.
*   **Simulation:** [SimPy](https://simpy.readthedocs.io/en/latest/) - A process-based, open-source framework for discrete-event simulation in Python.
*   **Optimization:** [PuLP](https://coin-or.github.io/pulp/) - An open-source Python library for creating and solving linear programming (LP) problems.
*   **Package & Environment Manager:** [uv](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver, used here to manage dependencies and run scripts.
*   **Demonstration & Testing Framework:** [pytest](https://docs.pytest.org/en/stable/) - A framework that makes it easy to write small, readable tests, and can scale to support complex functional testing.
*   **External System Integration:** [Model Context Protocol (MCP)](https://github.com/the-model-context-protocol/mcp) - A standardized protocol for AI models to interact with external tools and servers.

## Folder Structure
*   **/app**: Contains the core application logic.
    *   **/agents**: Defines the individual AI agents.
    *   **/config**: Contains YAML configuration files for agents, tasks, and prompts.
    *   **/control_tower**: Contains the core orchestration logic, including the crew and manager agent definitions.
    *   **/data_models**: Contains Pydantic models for structured data exchange.
    *   **/digital_twin**: Implements the Digital Twin of the Beer Game.
    *   **/flows**: Defines structured, multi-step `CrewAI Flow` workflows.
    *   **/mcp**: Contains the mock external server implementations (ERP, Weather, News).
    *   **/optimizations**: Contains the logic for dynamic optimization model generation.
    *   **/simulations**: Contains the `SimPy`-based simulation models.
    *   **/tools**: Defines the custom tools the agents use to interact with the system.
    *   **/utils**: Contains utility functions for configuration, LLM setup, etc.
*   **/instructions**: Contains detailed markdown files with project documentation.
*   **/knowledge**: Contains knowledge base files for the agents (e.g., sustainability guides).
*   **/test**: Contains the executable demonstration scripts for the PoC.

## How to Setup and Run the PoC Demonstrations
This project uses `pytest` to run the demonstration scripts located in the `/test` directory.

### 1. Configure your Environment
Before running the demonstrations, you need to set up your environment variables for the Large Language Model (LLM) and embedding models.

1.  Rename the `.env.example` file to `.env`.
2.  Open the `.env` file and enter your API keys and other required values.
3.  If you are using a different LLM provider, you may also need to modify the `get_llm()` and `get_embedder()` functions in the `app/utils/llm_utils.py` file.

### 2. Run the Demonstrations
To run a single demonstration and see its full output, use the `pytest` command with the `-v` (verbose) and `-s` (show prints) flags, followed by the path to the test file. For example:
```bash
uv run pytest -v -s test/test_demand_forecast_task.py
```

## Demonstration of Core Agentic Capabilities
This PoC provides tangible proof of the advanced capabilities enabled by the Agentic SCCT framework. The system's intelligence follows a logical "Sense, Act, and Optimize" workflow, with each capability demonstrated by an executable script.

| Capability Demonstrated | Command |
| :--- | :--- |
| **Digital Twin Integrity** | `uv run pytest -v -s test/test_digital_twin.py` |
| **External System Connectivity (MCP)** | `uv run pytest -v -s test/test_mcp_servers.py` |
| **Unified Sensing** | `uv run pytest -v -s test/test_demand_forecast_task.py` |
| **Autonomous Action** | `uv run pytest -v -s test/test_procurement_task.py` |
| **Governed Autonomy** | `uv run pytest -v -s test/test_sustainability_flow.py` |
| **Predictive Foresight (Simulation)** | `uv run pytest -v -s test/test_inventory_ordering_simulation_task.py` |
| **Dynamic Problem-Solving (Optimization)** | `uv run pytest -v -s test/test_inventory_optimization_task.py` |

## Contact and Inquiries
We welcome feedback, questions, and opportunities for collaboration. Please feel free to reach out for:
*   **General Feedback:** Share your thoughts on the framework and implementation.
*   **Research Inquiries:** Discuss the academic foundations and implications of this work.
*   **Collaboration:** Explore opportunities to apply or extend this research.
*   **Technical Support:** Report issues or ask questions about the codebase.

**Contact:** `mousavi@sophia.ac.jp`