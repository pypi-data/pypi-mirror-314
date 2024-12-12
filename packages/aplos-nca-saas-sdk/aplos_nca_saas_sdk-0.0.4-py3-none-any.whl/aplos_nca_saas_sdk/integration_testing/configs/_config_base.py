from typing import Dict
from typing import Any


class ConfigBase:
    """Base Configuration Class"""

    def __init__(self, enabled: bool = True):
        self.enabled: bool = enabled

    def load(self, test_config: Dict[str, Any]):
        """Load the configuration from a dictionary"""
        self.enabled = test_config.get("enabled", True)
