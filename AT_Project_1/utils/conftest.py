import pytest
import os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # We only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        driver = item.funcargs['setup']
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
        driver.save_screenshot(screenshot_path)
        item.add_report_section(
            "call", "screenshot", f"Screenshot saved to {screenshot_path}"
        )
