import os
import tomli
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigLoader:
    """Configuration loader for the project."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize config loader."""
        self.config_path = config_path or os.path.join(os.getcwd(), "ct.toml")
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from TOML file."""
        try:
            with open(self.config_path, "rb") as f:
                self._config = tomli.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        try:
            keys = key.split(".")
            value = self._config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    @property
    def raw_config(self) -> Dict[str, Any]:
        """Get raw configuration dictionary."""
        return self._config.copy()

def load_env_vars() -> None:
    """Load environment variables from .env file."""
    env_path = Path(os.getcwd()) / ".env"
    if not env_path.exists():
        return
    
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

# Initialize configuration
config = ConfigLoader()
load_env_vars()
