import os
from datetime import datetime, timezone


def capture_screenshot(page, step_name="step", output_dir="screenshots"):
    """
    Captures a screenshot of the current page state.
    step_name: A descriptive name of the step being captured.
    output_dir: Directory where screenshots are saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S%f")
    filename = f"{step_name}_{timestamp}.png"
    path = os.path.join(output_dir, filename)
    page.screenshot(path=path)
    return path
