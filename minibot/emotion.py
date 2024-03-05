from scripts.ece_dummy_ops import * # REMOVE THIS LINE FOR ACTUAL ROBOT USE

def init_emotional_system(program):
    program.append("emotion_repo = {}\n")
    program.append("added_emotions = {}\n")
    program.append("current_emotion = None\n")

    program.append("devices_emotional_status = {}\n")
    program.append("devices_emotional_status[\"wheels\"] = True\n")
    program.append("devices_emotional_status[\"display\"] = True\n")
    program.append("devices_emotional_status[\"speaker\"] = True\n")

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

    def add_required_device(self, device : str):
        self.required_devices.append(device)

    def process_emotion(self):
        self.action_steps()

    def check_devices(self, device_statuses):
        for device in self.required_devices:
            if not device_statuses[device]:
                return False
        return True
