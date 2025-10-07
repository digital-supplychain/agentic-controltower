# app/agents/logistics_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Logistics Agent
logistics_agent = Agent(
    config=agents_config['logistics_agent'],
    verbose=True,
    llm=llm,
    cache=False
)