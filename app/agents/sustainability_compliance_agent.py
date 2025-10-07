# app/agents/sustainability_compliance_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config
from app.tools.sustainability_tools import get_sustainability_tools

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Sustainability & Compliance Agent
sustainability_compliance_agent = Agent(
    config=agents_config['sustainability_compliance_agent'],
    verbose=True,
    llm=llm,
    tools=get_sustainability_tools(),  # Equip with tools to read sustainability guidelines
    cache=False
)