import os
from crewai import Agent
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai_tools import FileReadTool, FileWriterTool

from app.utils.llm_utils import get_llm
from app.utils.config import get_agents_config, get_prompts_config

# Get the LLM instance
llm = get_llm()

# Helper function to load markdown files
def load_markdown_files(directory: str) -> str:
    """
    A helper function to recursively load all markdown files from a directory into a single string.
    
    Args:
        directory: The path to the directory containing the markdown files.

    Returns:
        A string containing the concatenated content of all markdown files.
    """
    all_content = ""
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), "r", encoding='utf-8') as f:
                all_content += f.read() + "\n\n"
    return all_content

# --- Knowledge Base Setup ---
# The manager agent is equipped with a knowledge base containing project documentation.
# This allows it to provide context and guidance to other agents.
memory_bank_path = "memory_bank"
memory_bank_files = [os.path.join(memory_bank_path, f) for f in os.listdir(f"knowledge/{memory_bank_path}") if f.endswith('.md')]
# Only create a knowledge base if memory bank files are found.
knowledge_base = None
if memory_bank_files:
    source = TextFileKnowledgeSource(file_paths=memory_bank_files)
    # knowledge_base = KnowledgeBase(sources=[source]) # This line is commented out as it's not used

# --- Instructions and Prompts Setup ---
# Load custom instructions from markdown files to inject into the agent's system prompt.
custom_instructions = load_markdown_files("instructions")
# Load the system prompt template from the YAML configuration.
system_template = get_prompts_config()['crew_manager_agent']['system_template']

# --- Agent Definition ---
# Create the manager agent with its configuration, LLM, and enhanced system prompt.
agent_params = {
    "config": get_agents_config()['crew_manager_agent'],
    "llm": llm,
    "system_template": system_template.format(instructions=custom_instructions),
    "allow_delegation": True,
    "verbose": True,
    "inject_date": True,
    "cache": False,
}
# if knowledge_base:
#     agent_params["knowledge_base"] = knowledge_base

manager_agent = Agent(**agent_params)