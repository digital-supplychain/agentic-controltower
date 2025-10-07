# app/agents/customer_behavior_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Customer Behavior Agent
customer_behavior_agent = Agent(
    config=agents_config['customer_behavior_agent'],
    verbose=True,
    llm=llm,
    cache=False
)