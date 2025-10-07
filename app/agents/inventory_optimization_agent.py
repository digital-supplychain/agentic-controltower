# app/agents/inventory_optimization_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config
from app.tools.simulation_tools import get_simulation_tools
from app.tools.digital_twin_tools import get_digital_twin_tools
from app.tools.optimization_tools import get_optimization_tools

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Inventory Optimization Agent
inventory_optimization_agent = Agent(
    config=agents_config['inventory_optimization_agent'],
    verbose=True,
    llm=llm,
    # Equip the agent with a comprehensive set of tools for simulation, optimization, and digital twin interaction
    tools=get_simulation_tools() + get_digital_twin_tools() + get_optimization_tools(),
    cache=False
)