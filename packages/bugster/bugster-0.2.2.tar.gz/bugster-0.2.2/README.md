# Bugster Framework

Bugster is a powerful, flexible testing framework built on top of Playwright and pytest. It's designed to simplify the process of writing and managing end-to-end tests for web applications, with a focus on supporting multiple client configurations.

## Features

- Built on Playwright for robust, cross-browser testing
- Seamless integration with pytest
- Support for client-specific configurations and login strategies
- Custom `@login` decorator for easy test marking
- Flexible page object model with `BugsterPage`

## Installation

You can install Bugster using pip:

```bash
pip install bugster
```

This will install Bugster and its dependencies (including pytest and playwright).

After installation, you need to install the Playwright browsers:

```bash
playwright install
```

## Usage

### Basic Setup

1. Create a client configuration repository with the following structure:

```
customer-configs/
├── customer1/
│   ├── config.py
│   └── login_strategy.py
├── customer2/
│   ├── config.py
│   └── login_strategy.py
└── ...
```

2. In your test files, use the `@login` decorator to mark tests that require login:

```python
from bugster.decorators import login

@login
def test_requires_login(page):
    assert page.is_visible("text=Welcome")

def test_does_not_require_login(page):
    assert page.is_visible("text=Login")

@login
class TestLoggedInFeatures:
    def test_feature_1(self, page):
        assert page.is_visible("text=Feature 1")
```

### Running Tests

To run your tests, use pytest with the `--customer-id` option:

```bash
pytest --customer-id customer1 /path/to/your/tests
```

### Writing Client Configurations

In each client's `config.py`:

```python
from bugster.config.base_config import BaseConfig
from .login_strategy import CustomLoginStrategy

class CustomerConfig(BaseConfig):
    LOGIN_STRATEGY = CustomLoginStrategy
    CREDENTIALS = {
        "username": "customeruser",
        "password": "customerpass"
    }
    # Add any other customer-specific configuration here
```

In each client's `login_strategy.py`:

```python
from bugster.login.base_login_strategy import BaseLoginStrategy

class CustomLoginStrategy(BaseLoginStrategy):
    def login(self, page, credentials):
        page.goto("https://customer.example.com/login")
        page.fill("#username", credentials["username"])
        page.fill("#password", credentials["password"])
        page.click("#login-button")
        page.wait_for_selector("#welcome-message")
```

## Advanced Usage

Bugster provides a `BugsterPage` class that wraps Playwright's `Page` object, providing additional functionality. You can extend this class for custom page objects:

```python
from bugster.core.bugster_page import BugsterPage

class MyCustomPage(BugsterPage):
    def custom_action(self):
        # Implement custom action here
        pass
```

## Contributing

We welcome contributions to Bugster! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute.

## License

Bugster is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Changelog

See the [CHANGELOG.md](CHANGELOG.md) file for details on what has changed in each version of Bugster.

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub issue tracker](https://github.com/yourusername/bugster/issues).

## Acknowledgements

Bugster is built on top of the excellent [Playwright](https://playwright.dev/) and [pytest](https://docs.pytest.org/) projects. We're grateful to the maintainers and contributors of these projects for their fantastic work.