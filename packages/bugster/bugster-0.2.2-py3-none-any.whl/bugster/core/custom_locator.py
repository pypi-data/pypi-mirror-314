from playwright.sync_api import Locator
import time


class BugsterLocator:
    """
    A wrapper around Playwright's Locator that:
    - Adds stable time delays (configurable)
    - Provides a unified logging mechanism
    - Potentially integrates with screenshot or highlighting steps
    """

    def __init__(self, locator: Locator, step_delay: float = 1.0):
        self._locator = locator
        self._step_delay = step_delay

    def __getattr__(self, name):
        return getattr(self._locator, name)

    def click(self, **kwargs):
        time.sleep(self._step_delay)
        self._locator.click(**kwargs)

    def fill(self, text: str, **kwargs):
        time.sleep(self._step_delay)
        self._locator.fill(text, **kwargs)

    def press(self, key: str, **kwargs):
        time.sleep(self._step_delay)
        self._locator.press(key, **kwargs)

    def check(self, **kwargs):
        time.sleep(self._step_delay)
        self._locator.check(**kwargs)

    def uncheck(self, **kwargs):
        time.sleep(self._step_delay)
        self._locator.uncheck(**kwargs)

    def get_by_role(self, role: str, **kwargs):
        """
        Chainable method to narrow down locator by role.
        """
        new_locator = self._locator.get_by_role(role, **kwargs)
        return BugsterLocator(new_locator, self._step_delay)

    def get_by_text(self, text: str, **kwargs):
        new_locator = self._locator.get_by_text(text, **kwargs)
        return BugsterLocator(new_locator, self._step_delay)

    def get_by_placeholder(self, placeholder: str, **kwargs):
        new_locator = self._locator.get_by_placeholder(placeholder, **kwargs)
        return BugsterLocator(new_locator, self._step_delay)

    def get_by_label(self, label: str, **kwargs):
        new_locator = self._locator.get_by_label(label, **kwargs)
        return BugsterLocator(new_locator, self._step_delay)

    def locator(self, selector: str, **kwargs):
        new_locator = self._locator.locator(selector, **kwargs)
        return BugsterLocator(new_locator, self._step_delay)

    def all(self):
        return self._locator.all()

    def is_visible(self, **kwargs):
        return self._locator.is_visible(**kwargs)
