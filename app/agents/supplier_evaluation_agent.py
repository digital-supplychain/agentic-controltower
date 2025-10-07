# app/agents/supplier_evaluation_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Supplier Evaluation Agent
supplier_evaluation_agent = Agent(
    config=agents_config['supplier_evaluation_agent'],
    verbose=True,
    llm=llm,
    cache=False
)