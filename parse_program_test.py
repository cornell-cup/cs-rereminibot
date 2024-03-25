import os
import re
import socket
import sys
import time
import threading
import math

blockly_function_map = {
    "move_forward": "bot_script.sendKV(\"WHEELS\",\"forward\")",
    "move_backward": "bot_script.sendKV(\"WHEELS\",\"backward\")",
    "turn_clockwise": "bot_script.sendKV(\"WHEELS\",\"left\")",
    "turn_counter_clockwise": "bot_script.sendKV(\"WHEELS\",\"right\")",
    # "move_forward_distance": "fwd_dst",
    # "move_backward_distance": "back_dst",
    # "move_to": "move_to",
    "wait": "time.sleep",        
    "stop": "bot_script.sendKV(\"WHEELS\",\"stop\")"
    # "set_wheel_power": "ECE_wheel_pwr",
    # "turn_clockwise": "right",     
    # "turn_counter_clockwise": "left",
    # "turn_clockwise_angle": "right_angle",     
    # "turn_counter_clockwise_angle": "left_angle",
    # "turn_to": "turn_to",
    # "move_servo": "move_servo",    
    # "read_ultrasonic": "read_ultrasonic",
}

def parse_program(script: str) -> str:
    # Regex is for bot-specific functions (move forward, stop, etc)
    # 1st group is the whitespace (useful for def, for, etc),
    # 2nd group is for func name, 3rd group is for args,
    # 4th group is for anything else (additional whitespace,
    # ":" for end of if condition, etc)
    pattern = r"(.*)bot\.(\w+)\(([^)]*)\)(.*)"
    regex = re.compile(pattern)
    program_lines = script.split('\n')
    parsed_program = []
    for line in program_lines:
        match = regex.match(line)
        # match group 2: command, such as move_forward
        # match group 3: argument, such as power like 100
        while match:
            command = match.group(2)
            argument = str(match.group(3))
            if command in blockly_function_map:
                func = blockly_function_map[command]
            else:
                func = command

            if command == "wait":
                    func = func + "(" + argument + ")"
                    
            # elif func.startswith("bot_script.sendKV(\"WHEELS\","):
            #     if argument != '':
            #         float_power = float(argument) / 100
            #         func = func.replace("pow",str(float_power))   

            whitespace = match.group(1)
            if not whitespace:
                whitespace = ""
            parsed_line = whitespace
            parsed_line += func
            parsed_line += match.group(4)
            print("G1:", match.group(1))
            print("G2:", match.group(2))
            print("G3:", match.group(3))
            print("G4:", match.group(4))

            print("Parsed Line", parsed_line)
            
            line = parsed_line

            match = regex.match(line)

        parsed_program.append(line + '\n') 
    parsed_program_string = "".join(parsed_program)
    return parsed_program_string


prog = "bot.move_forward(50)\n"
prog += "(bot.move_backward(100), bot.wait(0.25))\n"
prog += "bot.turn_counter_clockwise(60)\n"
prog += "bot.turn_clockwise(40)\n"
prog += "bot.stop(), print(\"Hello\")"

print(prog)
print()
print(parse_program(prog))