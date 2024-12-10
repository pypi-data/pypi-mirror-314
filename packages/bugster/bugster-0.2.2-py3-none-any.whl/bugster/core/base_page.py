import time
from playwright.sync_api import Page
from bugster.core.custom_locator import BugsterLocator


class BugsterPage:
    """
    A custom page abstraction that:
    - Wraps Playwright's Page with extra functionality
    - Integrates BugsterLocator for stable element interactions
    - Could manage waits, screenshots, logging steps, etc.
    """

    def __init__(self, page: Page):
        self._page = page

    def goto(self, url: str, **kwargs):
        self._page.goto(url, **kwargs)
        self.wait_for_net()

    def wait_for_net(self, delay: float = 3.0):
        time.sleep(delay)

    def locator(self, selector: str, **kwargs) -> BugsterLocator:
        return BugsterLocator(self._page.locator(selector, **kwargs))

    def get_by_text(self, text: str, **kwargs) -> BugsterLocator:
        return BugsterLocator(self._page.get_by_text(text, **kwargs))

    def get_by_role(self, role: str, **kwargs) -> BugsterLocator:
        return BugsterLocator(self._page.get_by_role(role, **kwargs))

    def get_by_placeholder(self, placeholder: str, **kwargs) -> BugsterLocator:
        return BugsterLocator(self._page.get_by_placeholder(placeholder, **kwargs))

    def get_by_label(self, label: str, **kwargs) -> BugsterLocator:
        return BugsterLocator(self._page.get_by_label(label, **kwargs))

    def screenshot_step(self, name: str = "step"):
        """
        Capture a screenshot after a particular step. Integrate with highlighting if needed.
        """
        self._page.screenshot(path=f"{name}.png")

    def __getattr__(self, item):
        # Fallback to underlying page attributes if not defined here
        return getattr(self._page, item)
