import yaml

# Paths to your YAML configuration files
AGENTS_CONFIG_PATH = 'app/config/agents.yaml'
TASKS_CONFIG_PATH = 'app/config/tasks.yaml'
PROMPTS_CONFIG_PATH = 'app/config/prompts.yaml'

def _load_yaml_config(file_path: str) -> dict:
    """
    A helper function to load a YAML file from a given path.

    Args:
        file_path: The path to the YAML file.

    Returns:
        A dictionary containing the parsed YAML content.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_agents_config() -> dict:
    """Loads and returns the agent configurations from the YAML file."""
    return _load_yaml_config(AGENTS_CONFIG_PATH)

def get_tasks_config() -> dict:
    """Loads and returns the task configurations from the YAML file."""
    return _load_yaml_config(TASKS_CONFIG_PATH)

def get_prompts_config() -> dict:
    """Loads and returns the prompt configurations from the YAML file."""
    return _load_yaml_config(PROMPTS_CONFIG_PATH)