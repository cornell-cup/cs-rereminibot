def init_emotional_system(program):
    program.append("import emotion\n")

    program.append("emotion_repo = {}\n")
    program.append("added_emotions = {}\n")
    program.append("current_emotion = None\n")

    program.append("devices_emotional_status = {}\n")
    program.append("devices_emotional_status[\"wheels\"] = True\n")
    program.append("devices_emotional_status[\"display\"] = True\n")
    program.append("devices_emotional_status[\"speaker\"] = True\n")


def check_devices(emotion_name, emotion_repo, device_statuses):
    pass
    

class Emotion:
    """
    Represents an emotion that can be added to and run by an XRP bot.
    """

    def __init__(self, name : str, action_steps):
        self._name = name
        self.required_devices = []
        self.action_steps = action_steps

    def add_required_device(self, device : str):
        self.required_devices.append(device)

    def process_emotion(self):
        self.action_steps()
