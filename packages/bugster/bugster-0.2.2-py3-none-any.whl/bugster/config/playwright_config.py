import os
import json

class PlaywrightConfig:
    """
    Loads and exposes browser and viewport configurations for Playwright.
    """
    def __init__(self, config_path: str = None):
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)

    def get_browser(self, default="chromium"):
        return self.config.get("browser", default)

    def get_viewport(self):
        return self.config.get("viewport", {"width": 1920, "height": 1080})

    def get_base_url(self, default="https://www.bugster.app"):
        return self.config.get("base_url", default)
