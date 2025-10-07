# app/agents/procurement_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config
from app.tools.digital_twin_tools import get_digital_twin_tools

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Procurement Agent
procurement_agent = Agent(
    config=agents_config['procurement_agent'],
    verbose=True,
    llm=llm,
    tools=get_digital_twin_tools(),  # Equip with tools to interact with the Digital Twin (e.g., place orders)
    cache=False
)