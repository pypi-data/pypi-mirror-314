import os
import json


class TestMetadata:
    """
    Reads and stores metadata about the current test run.
    For example:
    - Browser type (chromium, firefox, webkit)
    - Viewport size
    - Device emulation
    - Base URL
    - Credentials
    """

    def __init__(self, config_path: str = None):
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.config = json.load(f)

    def get_browser(self, default: str = "chromium") -> str:
        return self.config.get("environment", {}).get("browser", default)

    def get_viewport(self) -> dict:
        return self.config.get("environment", {}).get(
            "viewport", {"width": 1920, "height": 1080}
        )

    def get_credentials(self) -> dict:
        """
        Example: loads credentials from config or environment
        """
        creds = self.config.get("auth", {}).get("credentials", {})
        creds = {
            "email": creds.get("email", "test@example.com"),
            "password": creds.get("password", "secret"),
        }
        return creds

    def get_base_url(self) -> str:
        return self.config.get("environment", {}).get(
            "base_url", "https://www.example.com"
        )

    def get_auth_url(self) -> str:
        return self.config.get("environment", {}).get(
            "auth_url", "https://www.example.com"
        )

    def get_login_strategy(self):
        return self.config.get("auth", {}).get(
            "strategy", "default.path:BaseLoginStrategy"
        )

    def get_login_instructions(self):
        return self.config.get("auth", {}).get("instructions", {})
