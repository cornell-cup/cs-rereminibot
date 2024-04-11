import time

def init_emotional_system(program):
    program.append("added_emotions = {}\n")
    program.append("current_emotion = None\n")

    program.append("devices_emotional_status = {}\n")
    program.append("devices_emotional_status[\"wheels\"] = True\n")
    program.append("devices_emotional_status[\"display\"] = True\n")
    program.append("devices_emotional_status[\"speaker\"] = True\n")

def create_action_steps_function(statements, exec_dict):
    def action_function():
        exec(statements, exec_dict)

    return action_function

class Emotion:
    """
    Represents an emotion that can be added to and run by an XRP bot.
    """

    def __init__(self, name : str, action_steps, basestation, bot_script):
        self._name = name
        self.required_devices = []
        action_step_exec_dict = {
            "bot_script" : bot_script,
            "self" : basestation,
            "time" : time
        }
        self.action_steps = create_action_steps_function(action_steps, action_step_exec_dict)

    def add_required_device(self, device : str):
        self.required_devices.append(device)

    def process_emotion(self):
        self.action_steps()

    def check_devices(self, device_statuses):
        for device in self.required_devices:
            if not device_statuses[device]:
                return False
        return True
