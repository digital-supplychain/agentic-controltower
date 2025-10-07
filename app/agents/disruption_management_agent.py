# app/agents/disruption_management_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config
from app.utils.tools_utils import get_weather_tools, get_news_tools

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Disruption Management Agent
disruption_management_agent = Agent(
    config=agents_config['disruption_management_agent'],
    verbose=True,
    llm=llm,
    tools=get_weather_tools() + get_news_tools(),  # Equip with tools to access weather and news data
    cache=False
)