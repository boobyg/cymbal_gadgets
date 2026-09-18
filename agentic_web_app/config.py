import os
from pathlib import Path

def load_dotenv(filepath=".env"):
    """Simple .env loader without external dependencies."""
    env_path = Path(filepath)
    if not env_path.is_file():
        env_path = Path(__file__).resolve().parent / ".env"
    if env_path.is_file():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

load_dotenv()

LOOKER_BASE_URL = os.environ.get("LOOKER_BASE_URL", "https://ceworkshops.cloud.looker.com").rstrip("/")
LOOKER_CLIENT_ID = os.environ.get("LOOKER_CLIENT_ID", "specify your own user id / secret")
LOOKER_CLIENT_SECRET = os.environ.get("LOOKER_CLIENT_SECRET", "specify your own user id / secret")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "cymbal_gadgets_boris")
DEFAULT_EXPLORE = os.environ.get("DEFAULT_EXPLORE", "transactions")
PORT = int(os.environ.get("PORT", "8080"))
HOST = os.environ.get("HOST", "0.0.0.0")
