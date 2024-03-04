def init_emotional_system(program):
    program.append("er = {}\n")
    program.append("ae = {}\n")
    program.append("ce = None\n")

    program.append("des = {}\n")
    program.append("des[\"wheels\"] = True\n")
    program.append("des[\"display\"] = True\n")
    program.append("des[\"speaker\"] = True\n")

def create_action_steps_function(statements):
    def action_function():
        exec(statements)

    return action_function

class Emotion:
    """
    Represents an emotion that can be added to and run by an XRP bot.
    """

    def __init__(self, name : str, action_steps):
        self._name = name
        self.required_devices = []
        self.action_steps = create_action_steps_function(action_steps)

    def add_rd(self, device : str):
        self.required_devices.append(device)

    def pe(self):
        self.action_steps()

    def check_devices(self, device_statuses):
        for device in self.required_devices:
            if not device_statuses[device]:
                return False
        return True
