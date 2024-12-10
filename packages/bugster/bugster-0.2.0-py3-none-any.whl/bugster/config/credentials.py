import os
import json


def load_credentials():
    """
    Load credentials from environment variables or a JSON file.
    Priority:
      1. BUGSTER_CREDENTIALS_FILE: Path to a JSON file with {"email": "...", "password": "..."}
      2. Environment variables: BUGSTER_EMAIL, BUGSTER_PASSWORD
      3. Defaults (for testing) if nothing else provided
    """
    creds_file = os.environ.get("BUGSTER_CONFIG_PATH", "./bugster.json")
    if not os.path.exists(creds_file):
        raise FileNotFoundError(
            f"Credentials file not found at {creds_file}. Please provide a valid credentials JSON file."
        )
    with open(creds_file, "r") as f:
        creds = json.load(f)

    # Validate that essential keys exist
    creds = {
        "email": creds.get("email", "test@example.com"),
        "password": creds.get("password", "secret"),
    }

    if "email" not in creds or "password" not in creds:
        raise ValueError("Credentials JSON must contain 'email' and 'password' fields.")

    return creds
