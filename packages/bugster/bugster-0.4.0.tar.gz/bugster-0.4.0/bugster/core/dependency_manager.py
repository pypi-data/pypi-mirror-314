import pytest


class DependencyManager:
    """
    Simple dependency management:
    - Tests can be marked with @pytest.mark.depends(on=["test_a", "test_b"])
    - Before running a test, this manager checks if dependencies passed.
    """

    def __init__(self):
        self.results = {}

    def record_result(self, test_name: str, outcome: str):
        # outcome could be 'passed', 'failed', 'skipped'
        self.results[test_name] = outcome

    def check_dependencies(self, item):
        mark = item.get_closest_marker("depends")
        if mark:
            dependencies = mark.kwargs.get("on", [])
            for dep in dependencies:
                outcome = self.results.get(dep)
                if outcome is None:
                    pytest.skip(f"Dependency {dep} has not been run yet.")
                elif outcome != "passed":
                    pytest.skip(f"Dependency {dep} did not pass. Skipping this test.")
