# app/agents/demand_forecast_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config
from app.utils.tools_utils import get_erp_tools

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Demand Forecast Agent
demand_forecast_agent = Agent(
    config=agents_config['demand_forecast_agent'],
    verbose=True,
    allow_delegation=True,  # This agent can delegate tasks to other agents (e.g., Disruption Management)
    llm=llm,
    tools=get_erp_tools(),  # Equip the agent with tools to access ERP data
    cache=False
)