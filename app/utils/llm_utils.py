import os
from dotenv import load_dotenv
from crewai import LLM
from crewai.utilities.paths import db_storage_path

load_dotenv()


def get_llm() -> LLM:
    """
    Initializes and returns the Language Model (LLM) configuration for the crew.
    It reads the model name and API key from environment variables.
    """
    return LLM(
        model=os.getenv("MODEL"),
        api_key=os.getenv("GEMINI_API_KEY")
    )

def get_embedder() -> dict:
    """
    Initializes and returns the configuration for the embedding model.
    This is used for semantic search and knowledge base retrieval.
    """
    return {
        "provider": "azure",
        "config": {
            "api_key": os.getenv("AZURE_API_KEY"),
            # "model": os.getenv("AZURE_API_EMBEDDING_MODEL"),
            "api_base": os.getenv("AZURE_API_BASE"),
            "api_version": os.getenv("AZURE_API_VERSION"),
            "deployment_id": os.getenv("AZURE_API_EMBEDDING_DEPLOYMENT_ID"),
            "dimensions": 3072,
        }
    }

def set_custom_storage_path(path: str):
    """
    Sets a custom storage path for CrewAI's internal database.

    Args:
        path: The directory path to use for storage.
    """
    os.environ["CREWAI_STORAGE_DIR"] = path

def print_storage_path():
    """
    Prints the location of the CrewAI knowledge base storage and lists its contents.
    This is a utility function for debugging and verification.
    """
    # Get the knowledge storage path
    knowledge_path = os.path.join(db_storage_path(), "knowledge")
    print(f"Knowledge storage location: {knowledge_path}")

    # List knowledge collections and files
    if os.path.exists(knowledge_path):
        print("\nKnowledge storage contents:")
        for item in os.listdir(knowledge_path):
            item_path = os.path.join(knowledge_path, item)
            if os.path.isdir(item_path):
                print(f"📁 Collection: {item}/")
                # Show collection contents
                try:
                    for subitem in os.listdir(item_path):
                        print(f"   └── {subitem}")
                except PermissionError:
                    print(f"   └── (permission denied)")
            else:
                print(f"📄 {item}")
        print("\r\n")
    else:
        print("No knowledge storage found yet.\r\n")

print_storage_path()

