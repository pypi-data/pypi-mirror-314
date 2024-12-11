from abc import ABC, abstractmethod


class BaseLoginStrategy(ABC):
    """
    An abstract class that defines a standard interface for performing login steps.
    Implementations should define `run_login(page, credentials)`:
      - page: An instance of BugsterPage
      - credentials: dict with "email" and "password", base and auth urls
    """

    @abstractmethod
    def run_login(self, page, credentials: dict):
        """
        Executes login steps:
          1. Navigate to the login page
          2. Fill in credentials
          3. Submit and wait for logged-in state
        """
        pass
