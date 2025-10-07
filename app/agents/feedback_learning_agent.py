# app/agents/feedback_learning_agent.py
from crewai import Agent
from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config
from crewai_tools import FileReadTool, FileWriterTool

# Initialize the LLM and load agent configurations
llm = get_llm()
agents_config = get_agents_config()

# Create the Feedback & Learning Agent
feedback_learning_agent = Agent(
    config=agents_config['feedback_learning_agent'],
    verbose=True,
    llm=llm,
    tools=[
        FileReadTool(),
        FileWriterTool(),
    ],
    cache=False
)