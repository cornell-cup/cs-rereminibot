pythonCode = {
    "forward": "bot.move_forward(100)",
    "backward": "bot.move_backward(100)",
    "stop": "bot.stop()",
    "right": "bot.turn_clockwise(100)",
    "left": "bot.turn_counter_clockwise(100)",
    "repeat": "for i in range(n):",
    "end": "end",
    "custom block": "#custom block no.n"
}

commands = {
    "commands": {
        "turn left": ["110631159936"],
        "turn right": ["1107911474124"],
        "go forwards": ["1107815185135"],
        "go backwards": ["1107696200239"],
        "stop": ["110641412160"],
        #repeat, end, and custom block have dummy tags, same as dummy_ops2 and physical_blockly
        "repeat": ["000000000000"],
        "end": ["111111111111"],
        "custom block": ["222222222222"]
    },
    "tagRangeStart": 0,
    "tagRangeEnd": 23
}

def classify(command, commands):
    if command in commands["commands"]["turn left"]:
        return ["fake_bot", "left"]
    elif command in commands["commands"]["turn right"]:
        return ["fake_bot", "right"]
    elif command in commands["commands"]["go forwards"]:
        return ["fake_bot", "forward"]
    elif command in commands["commands"]["go backwards"]:
        return ["fake_bot", "backward"]
    elif command in commands["commands"]["repeat"]:
        return ["fake_bot", "repeat"]
    elif command in commands["commands"]["end"]:
        return ["fake_bot", "end"]
    elif command in commands["commands"]["custom block"]:
        return ["fake_bot", "custom block"]
    else:
        # do nothing if invalid command received
        return ["fake_bot", "stop"]