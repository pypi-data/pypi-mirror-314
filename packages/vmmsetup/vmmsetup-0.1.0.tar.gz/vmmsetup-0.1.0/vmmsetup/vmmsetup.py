import os
import sys
from dotenv import load_dotenv

def get_env(env_name: str) -> str | None:
    """Loads the environment variable from a .env file."""
    load_dotenv()
    return os.environ.get(env_name)

sys.path[0] = get_env("PROJECT_ROOT")


