from bugster.auth.base_login import BaseLoginStrategy


class UserInputLoginStrategy(BaseLoginStrategy):
    def __init__(self, instructions):
        """
        instructions: a list of dictionaries, each describing a step, e.g.:
        [
          {"action": "goto", "url": "/auth/sign-in"},
          {"action": "fill", "method": "placeholder", "value": "email", "text": "{email}"},
          ...
        ]

        The "{email}" or "{password}" can be template placeholders replaced at runtime.
        """
        self.instructions = instructions

    def run_login(self, page, credentials: dict, testmanagement: dict):
        for instr in self.instructions:
            self.execute_step(page, instr, credentials, testmanagement)
        page.wait_for_net()

    def execute_step(self, page, instr, credentials, testmanagement):
        action = instr["action"]
        environment = testmanagement.get("environment", None)
        auth = testmanagement.get("auth", None)
        if action == "goto":
            auth_url = environment.get("auth_url", None)
            if not auth_url:
                base_url = environment.get("base_url", None)
                page.goto(base_url + instr["url"])
            else:
                page.goto(auth_url)
        elif action == "fill":
            text = instr["text"]
            text = text.replace("{email}", credentials["email"]).replace(
                "{password}", credentials["password"]
            )
            locator = self.get_locator(page, instr)
            locator.click()
            locator.fill(text)
        elif action == "click":
            locator = self.get_locator(page, instr)
            locator.click()

    def get_locator(self, page, instr):
        # Dynamically choose the locator method based on instructions
        method = instr.get("method")
        value = instr.get("value")
        if method == "placeholder":
            return page.get_by_placeholder(value)
        elif method == "label":
            return page.get_by_label(value)
        elif method == "role":
            return page.get_by_role(value, **instr.get("kwargs", {}))
        elif method == "text":
            return page.get_by_text(value)
        else:
            return page.locator(value)  # fallback to raw selector
