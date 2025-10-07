# app/agents/production_scheduling_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Production Scheduling Agent
production_scheduling_agent = Agent(
    config=agents_config['production_scheduling_agent'],
    verbose=True,
    llm=llm,
    cache=False
)