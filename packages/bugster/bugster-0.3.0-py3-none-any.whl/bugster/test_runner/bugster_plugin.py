# conftest.py
import os
import json
import pytest
from playwright.sync_api import sync_playwright
from bugster.core.base_page import BugsterPage
from bugster.auth.streategies import UserInputLoginStrategy
from bugster.config.credentials import load_credentials
from bugster.core.test_metadata import TestMetadata
from bugster.core.dependency_manager import DependencyManager
from bugster.reporting.screenshots import capture_screenshot
from bugster.reporting.trace_viewer import start_trace, stop_and_save_trace


#############################
# Session-Level Fixtures
#############################


@pytest.fixture
def cred_key_param(request):
    try:
        return request.param
    except AttributeError:
        return None


@pytest.fixture(scope="session")
def test_metadata():
    """
    Loads and provides test metadata for the entire session.
    This could read a config path from ENV, or fallback to defaults.
    """
    config_path = "bugster.json"
    return TestMetadata(config_path=config_path)


@pytest.fixture(scope="session")
def credentials():
    """
    Loads credentials from environment or file.
    """
    return load_credentials()


@pytest.fixture(scope="session")
def login_strategy(test_metadata):
    """
    Dynamically loads a login strategy from an environment variable.
    """
    strategy_path = test_metadata.get_login_strategy()
    login_instructions = test_metadata.get_login_instructions()

    return UserInputLoginStrategy(login_instructions)


@pytest.fixture(scope="session")
def dependency_manager():
    """
    A session-level dependency manager to handle test dependencies.
    """
    return DependencyManager()


@pytest.fixture(scope="session", autouse=True)
def register_dependency_hooks(request, dependency_manager):
    """
    Hook into Pytest to run dependency checks before tests and record outcomes after tests.
    """
    # Store in pytest config for access in hooks
    request.config._dependency_manager = dependency_manager


#############################
# Browser and Context Setup
#############################


@pytest.fixture(scope="session")
def browser_type_launch_args(test_metadata):
    """
    Provides arguments to launch browser based on metadata.
    For simplicity, let's assume test_metadata can provide browser type and headless options.
    """
    browser_type = test_metadata.get_browser(default="chromium")
    # Extend with logic to determine headless or other flags
    return {"headless": False, "browser": browser_type}


@pytest.fixture(scope="session")
def browser_context_args(test_metadata):
    """
    Default browser context arguments from metadata.
    Override in per-test fixtures if needed.
    """
    return {
        "viewport": test_metadata.get_viewport(),
        "user_agent": "Chrome/69.0.3497.100 Safari/537.36",
    }


@pytest.fixture(scope="function")
def page(
    request,
    browser_type_launch_args,
    browser_context_args,
    credentials,
    login_strategy,
    cred_key_param,
):
    """
    The main page fixture:
    - Reads per-test markers (e.g. @pytest.mark.viewport)
    - Launches the browser with given arguments
    - Creates a new context and page
    - Runs login if required
    - Starts trace, captures screenshots
    - Teardown: captures final screenshot, stops trace, closes context
    """
    # Handle per-test viewport override
    viewport_marker = request.node.get_closest_marker("viewport")
    final_context_args = dict(browser_context_args)
    if viewport_marker:
        w = viewport_marker.kwargs.get("width", final_context_args["viewport"]["width"])
        h = viewport_marker.kwargs.get(
            "height", final_context_args["viewport"]["height"]
        )
        final_context_args["viewport"] = {"width": w, "height": h}
    # Launch the browser
    with sync_playwright() as p:
        browser_type = browser_type_launch_args.get("browser", "chromium")
        if browser_type == "chromium":
            bt = p.chromium
        elif browser_type == "firefox":
            bt = p.firefox
        else:
            bt = p.webkit

        launch_args = dict(browser_type_launch_args)
        launch_args.pop(
            "browser", None
        )  # remove browser key as it's not a valid arg for launch
        browser = bt.launch(**launch_args)

        # Create a new context with overridden args if any
        context = browser.new_context(**final_context_args)

        # Start tracing for debugging
        start_trace(context)

        pg = context.new_page()
        bugster_page = BugsterPage(pg)
        credentials_dict = credentials.get("auth", {}).get("credentials", {})
        if cred_key_param:
            # Multiple credentials scenario (or * scenario)
            selected_cred = credentials_dict.get(cred_key_param)
            if not selected_cred:
                raise ValueError(f"Credential '{cred_key_param}' not found.")
            login_strategy.run_login(bugster_page, selected_cred, credentials)
        else:
            # Check if there's a login marker with a single credential scenario
            login_marker = request.node.get_closest_marker("login")
            if login_marker:
                creds = login_marker.kwargs.get("credentials", None)
                if isinstance(creds, str) and creds != "*":
                    # Single credential scenario
                    selected_cred = credentials_dict.get(creds)
                    if not selected_cred:
                        raise ValueError(f"Credential '{creds}' not found.")
                    login_strategy.run_login(bugster_page, selected_cred, credentials)
                # If creds == "*" but we didn't parametrize, that's a logic error in pytest_generate_tests
                # or the scenario isn't handled. Ensure that's handled below.

        capture_screenshot(pg, step_name="start")

        yield bugster_page

        # On test finish, take a screenshot for the final state
        capture_screenshot(pg, step_name="end")

        # Stop and save trace
        test_name = request.node.name
        stop_and_save_trace(context, test_name=test_name)

        # Cleanup
        context.close()
        browser.close()


#############################
# Hooks for Dependencies
#############################
def pytest_generate_tests(metafunc):
    login_marker = metafunc.definition.get_closest_marker("login")
    print(metafunc)
    if login_marker:
        creds = login_marker.kwargs.get("credentials", None)
        print(creds)
        if creds == "*":
            c = load_credentials()
            all_creds = c.get("auth", {}).get("credentials", {})
            param_values = list(all_creds.keys())
            if param_values:
                print(param_values)
                metafunc.parametrize("cred_key_param", param_values, ids=param_values)
        elif isinstance(creds, list):
            if len(creds) > 1:
                metafunc.parametrize("cred_key_param", creds, ids=creds)
        elif isinstance(creds, str):
            pass
        else:
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """
    A hook to check dependencies before each test runs and record results after.
    """
    dm = item.session.config._dependency_manager
    dm.check_dependencies(item)
    outcome = yield
    # Record test result
    result = "passed" if outcome.excinfo is None else "failed"
    dm.record_result(item.name, result)
