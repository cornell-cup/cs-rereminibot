"""
Base Station for the MiniBot.
"""
import os
import re
import socket
import time
import threading
import ctypes
import json
import queue
import random
import copy
from time import sleep
from typing import Tuple, Optional

from basestation.bot import Bot
from basestation import config

# database imports
from basestation.databases.user_database import User, Chatbot as ChatbotTable, Submission
from basestation.databases.user_database import db

# imports from basestation util
import basestation.piVision.pb_utils as pb_utils

from basestation.emotion_bs import *

from random import choice, randint
from string import digits, ascii_lowercase, ascii_uppercase
from typing import Any, Dict, List, Tuple, Optional
from copy import deepcopy
import subprocess
from basestation import ChatbotWrapper
 

MAX_VISION_LOG_LENGTH = 1000
VISION_UPDATE_FREQUENCY = 30
VISION_DATA_HOLD_THRESHOLD = 5


def make_thread_safe(func):
    """ Decorator which wraps the specified function with a lock.  This makes
    sure that there aren't concurrent calls to the basestation functions.  The
    reason we need this is because both SpeechRecognition and the regular
    movement buttons call basestation functions to make the Minibot move.  The
    SpeechRecognition function runs in its own background thread.  We
    do not want the SpeechRecognition function calling the basestation functions
    while the movement button requests are calling them.  Hence we protect
    the necessary basestation functions with a lock that is owned by the basestation
    Arguments:
         func: The function that will become thread safe
    """
    def decorated_func(*args, **kwargs):
        # args[0] is self for any basestation member function
        assert isinstance(args[0], BaseStation)
        lock = args[0].lock
        lock.acquire()
        val = func(*args, **kwargs)
        lock.release()
        return val
    return decorated_func


class BaseStation:
    # THESE SHOULD BE CONSISTENT ACROSS THE BASESTATION AND ROBOT
    START_CMD_TOKEN = "<<<<"
    END_CMD_TOKEN = ">>>>"
    SOCKET_BUFFER_SIZE = 1024
    SOCKET_BUFFER_PADDING = 32

    def __init__(self, app_debug=False, reuseport = config.reuseport):
        self.active_bots = {}
        self.reuseport = reuseport
        self.chatbot = ChatbotWrapper.ChatbotWrapper()

        self.blockly_function_map = {
            "move_forward": "bot_script.sendKV(\"WHEELS\",\"(pow,pow)\")",
            "move_backward": "bot_script.sendKV(\"WHEELS\",\"(-pow,-pow)\")",
            "turn_clockwise": "bot_script.sendKV(\"WHEELS\",\"(pow,0)\")",
            "turn_counter_clockwise": "bot_script.sendKV(\"WHEELS\",\"(0,pow)\")",
            "wait": "time.sleep",        
            "stop": "bot_script.sendKV(\"WHEELS\",\"(0,0)\")",

            "set_expression": "bot_script.sendKV(\"SPR\",ARG)",
            "clear_expression": "bot_script.sendKV(\"SPR\",ARG)",
            "set_expression_playback_speed": "bot_script.sendKV(\"PBS\",ARG)",

            "start_accelerometer_streaming": "bot_script.sendKV(\"ACCEL\", 0)\nx = bot_script.readKV()\nprint(x)",
            "get_accelerometer_values": "bot_script.sendKV(\"IMU\", 0);bot_script.readKV();print(bot_script.accelerometer_values)",
            "get_accel_x": "get_imu("", True)[0]",
            "get_accel_y": "get_imu("", True)[1]",
            "get_accel_z": "get_imu("", True)[2]",
        }

        self.wheel_directions_multiplier_map = {
            "forward": [1, 1],
            "backward": [-1, -1],
            "left": [1, 0],
            "right": [0, 1],
            "stop": [0, 0]
        }

        self.wheel_directions = ["forward", "backward", "left", "right", "stop"]

        self.py_commands = queue.Queue()
        self.pb_map = {}
        self.pb_stopped = True

        # This socket is used to listen for new incoming Minibot broadcasts
        # The Minibot broadcast will allow us to learn the Minibot's ipaddress
        # so that we can connect to the Minibot
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.reuseport:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        else:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                

        # an arbitrarily small time
        self.sock.settimeout(0.01)

        # empty string means 0.0.0.0, which is all IP addresses on the local
        # machine, because some machines can have multiple Network Interface
        # Cards, and therefore will have multiple ip_addresses
        server_address = ("0.0.0.0", 5001)
        
        # checks if vision can see april tag by checking lenth of vision_log
        # self.connections = BaseConnection()

        # only bind in debug mode if you are the debug server, if you are the
        # monitoring program which restarts the debug server, do not bind,
        # otherwise the debug server won't be able to bind
        try:
            if app_debug and os.environ and os.environ["WERKZEUG_RUN_MAIN"] == "true":
                self.sock.bind(server_address)
            else:
                # since we are running in debug mode, always bind
                self.sock.bind(server_address)
        except:
            pass

        self._login_email = None
        self.speech_recog_thread = None
        self.lock = threading.Lock()
        self.commands = {
            "forward": "Minibot moves forward",
            "backward": "Minibot moves backwards",
            "left": "Minibot moves left",
            "right": "Minibot moves right",
            "stop": "Minibot stops",
        }

        self.script_thread = None
        # Keep track of any built-in scripts that are running / should run next
        self.builtin_script_state = {
            "procs": dict(),
            "next_req_id": 0
        }

        # Emotional System Variables (Possibly Upgrade to Handle Multiple Bots)
        self.emotion_repo = {}
        self.current_expression = None
        self.current_expression_playback_speed = 30
        

    # ==================== BOTS ====================

    def get_bot(self, bot_name: str) -> Bot:
        """ Returns bot object corresponding to bot name """
        if bot_name in self.active_bots:
            return self.active_bots[bot_name]
        return None

    def get_bot_names(self):
        """ Returns a list of the Bot Names. """
        return list(self.active_bots.keys())

    def listen_for_minibot_broadcast(self):
        """ Listens for the Minibot to broadcast a message to figure out the
        Minibot's ip address. Code taken from link below:
            https://github.com/jholtmann/ip_discovery
        """

        response = "i_am_the_base_station"
        # a minibot should send this message in order to receive the ip_address
        request_password = "i_am_a_minibot"

        buffer_size = 4096

        # Continuously read from the socket, collecting every single broadcast
        # message sent by every Minibot
        address_data_map = {}
        try:
            data, address = self.sock.recvfrom(buffer_size)
            while data:
                data = str(data.decode('UTF-8'))
                address_data_map[address] = data
                data, address = self.sock.recvfrom(buffer_size)
        # nothing to read
        except socket.timeout:
            pass

        # create a new Minibot object to represent each Minibot that sent a
        # broadcast to the basestation
        for address in address_data_map:
            # data should consist of "password port_number"
            data_lst = address_data_map[address].split(" ")
            if data_lst[0] == request_password:
                # Tell the minibot that you are the base station
                self.sock.sendto(response.encode(), address)
                self.add_bot(ip_address=address[0], port=data_lst[1])

    def add_bot(self, port: int, ip_address: str, bot_name: str = None):
        """ Adds a bot to the list of active bots """
        print("added bot")
        if not bot_name:
            # bot name is "minibot" + <last three digits of ip_address> + "_" +
            # <port number>
            bot_name = f"minibot{ip_address[-3:].replace('.', '')}_{port}"
        self.active_bots[bot_name] = Bot(bot_name, ip_address, port)

    def get_active_bots(self):
        """ Get the names of all the Minibots that are currently connected to
        Basestation
        """
        for bot_name in self.get_bot_names():
            status = self.get_bot_status(bot_name)
            # if the bot is inactive, remove it from the active bots list
            if status == "INACTIVE":
                self.remove_bot(bot_name)
        return self.get_bot_names()

    def get_bot_status(self, bot_name: str) -> str:
        """ Gets whether the Minibot is currently connected or has been
        disconnected.
        1. Send Minibot BOTSTATUS
        2. read from Minibot whatever Minibot has sent us.
        3. check when was the last time Minibot sent us "I'm alive"
        4. Return if Minibot is connected or not
        Arguments:
            bot_name: The name of the minibot
        """
        bot = self.get_bot(bot_name)
        # ask the bot to reply whether its ACTIVE
        bot.sendKV("BOTSTATUS", "")
        # read the newest message from the bot
        bot.readKV()
        if bot.is_connected():
            status = "ACTIVE"
        else:
            status = "INACTIVE"
        return status

    def remove_bot(self, bot_name: str):
        """Removes the specified bot from list of active bots."""
        self.active_bots.pop(bot_name)

    @make_thread_safe
    def move_bot_wheels(self, bot_name: str, direction: str, power: str):
        """ Gives wheels power based on user input """
        # stop currently running script (if any)
        self.stop_bot_script(bot_name)
        bot = self.get_bot(bot_name)
        direction = direction.lower()
        wheel_arg_str = "(0,0)"
        if direction in self.wheel_directions_multiplier_map.keys():
            wheel_arg = copy.deepcopy(self.wheel_directions_multiplier_map[direction])
            power = self.parse_power(power)
            wheel_arg[0] *= power
            wheel_arg[1] *= power
            wheel_arg_str = "(" + str(wheel_arg[0]) + "," + str(wheel_arg[1]) + ")"
        bot.sendKV("WHEELS", wheel_arg_str)

    def get_imu(self, bot_name: str, script: bool):
        if script == True:
            bot_script.sendKV("IMU", "")
            bot_script.readKV()
            return bot_script.accelerometer_values
        else:
            bot = self.get_bot(bot_name)
            bot.sendKV("IMU", "")
            bot.readKV()
            return bot.accelerometer_values


    def send_bot_script(self, bot_name: str, script: str):
        """Sends a python program to the specific bot"""
        parsed_program_string = self.parse_program(script)

        bot = self.get_bot(bot_name)
        self.stop_bot_script(bot_name)
        
        # reset the previous script_exec_result
        bot.script_exec_result_var.set_with_lock(False, "Waiting for execution completion")

        # Run the script in a separate thread
        self.script_thread = threading.Thread(target=self.run_bot_script, args=[bot_name, parsed_program_string])
        self.script_thread.start()

    def run_bot_script(self, bot_name: str, program_string: str):
        """ Executes a python program on the specific bot """
        bot_script = self.get_bot(bot_name)
        bot_script.script_alive_var.set_with_lock(True, True, timeout=-1)
        try:
            print("Current Expression:", self.current_expression)
            print("Parsed Program:")
            print(program_string)
            print("Executing Program...")
            exec_globals = {
                'bot_script': bot_script,
                'Emotion' : Emotion,
                'self' : self,
                }
            exec(program_string, exec_globals)  # Pass bot_script to exec()
            print("Finished Executing Program!")
            bot_script.script_exec_result_var.set_with_lock(True, "Successful execution", timeout=5)
        except Exception as exception:
            str_exception = str(type(exception)) + ": " + str(exception)
            bot_script.script_exec_result_var.set_with_lock(True, str_exception, timeout=5)
            print("exception encountered in running the program")
            print(str_exception)
        bot_script.script_alive_var.set_with_lock(True, False, timeout=-1)

    def stop_bot_script(self, bot_name: str):
        """ Stops any currently executing python program on the specific bot """
        bot = self.get_bot(bot_name)
        if bot == None:
            print("no bot available for stoppping bot script")
            return
        
        script_alive = bot.script_alive_var.get_with_lock(True, timeout=-1)
        if script_alive and self.script_thread != None:
            # stop current running script and send stop command to the bot
            bot.script_exec_result_var.set_with_lock(True, "Stop current program in execution", timeout=1)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.script_thread.ident), ctypes.py_object(SystemExit))
            print("interrupting the thread executing the script, result: " + str(res))
            bot.sendKV("WHEELS", "stop")

    # def get_virtual_program_execution_data(self, query_params: Dict[str, Any]) -> Dict[str, List[Dict]]:
    #     script = query_params['script_code']
    #     virtual_room_id = query_params['virtual_room_id']
    #     minibot_id = query_params['minibot_id']  
    #     world_width = query_params['world_width']
    #     world_height = query_params['world_height']
    #     cell_size = query_params['cell_size']
    #     query_params['id'] = query_params['minibot_id']  
    #     parsed_program_string = self.parse_program(script)
    #     worlds = self.get_worlds(virtual_room_id, world_width, world_height, cell_size, [minibot_id])
    #     minibot_location = self.get_vision_data_by_id(query_params)
    #     start = (minibot_location['x'],minibot_location['y'])
    #     return run_program_string_for_gui_data(parsed_program_string, start, worlds)

    def parse_program(self, script: str) -> str:
        """ Parses python program into commands that can be sent to the bot """
        # Regex is for bot-specific functions (move forward, stop, etc)
        # 1st group is the whitespace (useful for def, for, etc),
        # 2nd group is for func name, 3rd group is for args,
        # 4th group is for anything else (additional whitespace,
        # ":" for end of if condition, etc)
        pattern = r"(.*)bot\.(\w+)\(([^)]*)\)(.*)"
        regex = re.compile(pattern)
        program_lines = script.split('\n')
        parsed_program = []

        parsed_program.append("import time\n")

        init_emotional_system(parsed_program)

        for line in program_lines:
            match = regex.match(line)
            # match group 2: command, such as move_forward
            # match group 3: argument, such as power like 100
            while match:
                command = match.group(2)
                argument = str(match.group(3))

                if command in self.blockly_function_map:
                    func = self.blockly_function_map[command]
                else:
                    func = command

                if command == "wait":
                    func = func + "(" + argument + ")"

                # TODO Improve/rework blockly function map so this doesn't need to happen
                if command == "set_expression":
                    func = func.replace("ARG", argument)

                if command == "set_expression_playback_speed":
                    func = func.replace("ARG", argument)

                if command == "clear_expression":
                    func = func.replace("ARG", "\"\"")


                # TODO: implement custom power  
                # elif func.startswith("bot_script.sendKV(\"WHEELS\","):
                #     if argument != '':
                #         float_power = float(argument) / 100
                #         func = func.replace("pow",str(float_power))   
                if func.startswith("bot_script.sendKV(\"WHEELS\","):
                    if argument != '':
                        power = self.parse_power(argument)
                        func = func.replace("pow", str(power))   
                    else:
                        func = func.replace("-pow", "0").replace("pow", "0")
                

                whitespace = match.group(1)
                if not whitespace:
                    whitespace = ""
                parsed_line = whitespace
                # adding ; for multiline execution in exec
                parsed_line += func
                parsed_line += match.group(4)

                line = parsed_line
                match = regex.match(line)
            
            parsed_program.append(line + '\n') 

        parsed_program.append("time.sleep(1)\n") #TODO Possibly Remove
        parsed_program_string = "".join(parsed_program)
        return parsed_program_string

    def set_bot_ports(self, bot_name: str, ports: str):
        """Sets motor port(s) of the specific bot"""
        bot = self.get_bot(bot_name)
        ports_str = " ".join([str(l) for l in ports])
        bot.sendKV("PORTS", ports_str)

    def get_bot_script_exec_result(self, bot_name: str) -> str:
        """ Retrieve the last script's execution result from the specified bot.
        """
        bot = self.get_bot(bot_name)
        return bot.script_exec_result_var.get_with_lock(False)

    def parse_power(self, power: str) -> float:
        """ Convert power string (with max of 100) to a float with max of 1.
        """
        try:
            power = int(power)
            if power < 0:
                power = 0
            elif power > 100:
                power = 100
        except:
            power = 0
        power /= 100
        return power

    def get_current_expression(self):
        return self.current_expression
    
    def get_current_expression_playback_speed(self):
        return self.current_expression_playback_speed

    # ==================== DATABASE ====================
    def login(self, email: str, password: str) -> Tuple[int, Optional[str]]:
        """Logs in the user if the email and password are valid"""
        print("email:" + email)
        print("password" + password)
        if not email:
            return -1, None
        if not password:
            return 0, None

        user = User.query.filter(User.email == email).first()
        # email does not exist
        if not user:
            return -1, None
        if not user.verify_password(password):
            return 0, None
        self.login_email = email
        return 1, user.custom_function

    def register(self, email: str, password: str) -> int:
        """Registers a new user if the email and password are not null and
        there is no account associated wth the email yet"""
        print("registering new account")
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not email or not re.fullmatch(regex, email):
            return -1
        if not password:
            return 0

        user = User.query.filter(User.email == email).first()
        # user should not exist if we want to register a new account
        if user:
            return -2
        user = User(email=email, password=password)
        context = ChatbotTable(
            user_id=user.id,
            context=''
        )
        db.session.add(context)
        db.session.add(user)
        db.session.commit()
        self.login(email, password)
        return 1

    def get_user_id_by_email(self, email: str) -> int:
        user = User.query.filter(User.email == email).first()
        return user.id

    def clear_databases(self) -> None:
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print ('Clear table %s' % table)
            db.session.execute(table.delete())
        db.session.commit()

    def update_custom_function(self, custom_function: str) -> bool:
        """Adds custom function(s) for the logged in user if there is a user
        logged in
        """
        if not self.login_email:
            return False

        user = User.query.filter(User.email == self.login_email).first()
        user.custom_function = custom_function
        db.session.commit()
        return True

    def get_custom_function(self):
        print(self.login_email)
        if not self.login_email:
            return False, ""

        user = User.query.filter(User.email == self.login_email).first()
        return True, user.custom_function
    
    # ==================== PHYSICAL BLOCKLY ==================================
    def get_next_py_command(self):
        """ Gets the next python command for the physical blockly process """
        if self.py_commands.qsize() == 0:
            return ""
        val = self.py_commands.get(False)
        return val

    def get_rfid(self, bot_name: str):
        """ Gets the RFID tag from the specific bot """
        bot = self.get_bot(bot_name)
        bot.sendKV("RFID", 4)
        bot.readKV()
        print("rfid tag: " + bot.rfid_tags, flush=True)
        return bot.rfid_tags

    @make_thread_safe
    def set_bot_mode(self, bot_name: str, mode: str, pb_map: json, power: str):
        """ Set the bot to different physical blockly modes """
        bot = self.get_bot(bot_name)
        pb_map = str(pb_map)
        if mode == "physical-blockly" or mode == "physical-blockly-2":
            self.pb_stopped = False
            if mode == 'physical-blockly':
                self.physical_blockly(bot_name, 0, pb_map, power)
            else:
                self.physical_blockly(bot_name, 1, pb_map, power)
        # elif mode == "object_detection":
        #     self.bot_vision_server = subprocess.Popen(
        #         ['python', './basestation/piVision/server.py', '-p MobileNetSSD_deploy.prototxt',
        #          '-m', 'MobileNetSSD_deploy.caffemodel', '-mW', '2', '-mH', '2', '-v', '1'])
        # elif mode == "color_detection":
        #     self.bot_vision_server = subprocess.Popen(
        #         ['python', './basestation/piVision/server.py', '-p MobileNetSSD_deploy.prototxt',
        #          '-m', 'MobileNetSSD_deploy.caffemodel', '-mW', '2', '-mH', '2', '-v', '2'])
        # else:
        #     if self.bot_vision_server:
        #         self.bot_vision_server.kill()
        bot.sendKV("MODE", mode)
    
    def physical_blockly(self, bot_name: str, mode: int, pb_map: json, power: str):
        """ Runs the physical blockly process on the specific bot, with
        custom mapping of blocks and custom power option """
        rfid_tags = queue.Queue()
        pb_map = json.loads(pb_map)
        
        def tag_producer():
            while not self.pb_stopped:
                tag = self.get_rfid(bot_name)
                rfid_tags.put(tag)
                sleep(1.0)
            
        def tag_consumer():
            while not self.pb_stopped:
                try:
                    tag = rfid_tags.get(block=False).strip()
                    if tag in pb_map.keys():
                        tag = pb_map[tag]
                        task = pb_utils.classify(tag, pb_utils.commands)
                        py_code = pb_utils.pythonCode[task[1]]

                        if mode == 1:
                            if py_code[0:3] == "bot" and task[1] in self.wheel_directions:
                                self.move_bot_wheels(bot_name, task[1], power)
                        self.py_commands.put("pb:" + py_code)
                except:
                    pass
                sleep(1.0)
                
        threading.Thread(target=tag_consumer).start()
        threading.Thread(target=tag_producer).start()
    
    def end_physical_blockly(self, bot_name: str):
        """ Ends the physical blockly process """
        self.pb_stopped = True
        self.py_commands = queue.Queue()
        self.move_bot_wheels(bot_name, "STOP", "100")
        print("ending physical blockly thread")

    # ==================== NEW SPEECH RECOGNITION ============================
    def send_command(self, bot_name, command):
        if command in self.commands:
            self.move_bot_wheels(bot_name, command, 100)
            return self.commands[command] + " command sent"
        else:
            return "invalid commands"

    # ==================== CHATBOT ==========================================

    def chatbot_compute_answer(self, question: str) -> str:
        """ Computes answer for [question].
        Returns: <answer> : string
        """
        return self.chatbot.compute_answer(question)

    def update_chatbot_context(self, context: str) -> None:
        """ Update user's context to the Chatbot object
        """
        self.chatbot.update_context(context)

    def replace_context_stack(self, context_stack) -> None:
        """ Replace chatbot obj contextStack with <context_stack>.
        """
        self.chatbot.replace_context_stack(context_stack)

    def update_chatbot_all_context(self, context: str) -> None:
        """ Replaces all context in the Chatbot object
        with the input context.

        Usage: called when user logs in, replaces context with context fetched
        from database.
        """
        self.chatbot.reset_context()
        self.chatbot.update_context(context)

    def get_chatbot_obj_context(self) -> str:
        """ Returns all context currently stored in the chatbot object. 
        """
        return self.chatbot.get_all_context()

    def update_chatbot_context_db(self, user_email = '') -> int:
        """ Update user's context if user exists upon exiting the session.
        (closing the GUI tab)
        """
        user_email =  user_email if user_email else self.login_email
        curr_context_stack = self.chatbot.get_all_context()
        if curr_context_stack and user_email:
            print("user email", user_email)
            print("commit context stack to db", curr_context_stack)
            # get user_id from user_email
            user_id = self.get_user_id_by_email(user_email)
            user = ChatbotTable.query.filter_by(id=user_id)
            # get current context from chatbot_wrapper
            new_context = ''.join(curr_context_stack)
            # commit it to the db
            user.update({'context': new_context})
            db.session.commit()
            return 1
        return -1

    def chatbot_get_context(self):
        """Gets the stored context for the chatbot based on user_id.
         If user_id is nonexistent or empty, returns an empty
         json object. Otherwise, returns a json object with the context and its
         corresponding user_id """

        user_email = self.login_email

        if user_email is not None and user_email != "":
            user_id = self.get_user_id_by_email(user_email)
            user = ChatbotTable.query.filter_by(id=user_id).first()
            if user is None:
                return {'context': '', 'user_id': ''}
            else:
                print("user's context: " + user.context)
                self.chatbot.context_stack = [user.context]
                data = {'context': user.context, 'user_id': user_id}
                return data
        else:
            return {'context': '', 'user_id': ''}

    def chatbot_clear_context(self) -> None:
        """ Resets all context stored in the Chatbot object. 
        """
        print("reset context stack")
        self.chatbot.reset_context()

    def chatbot_delete_context_idx(self, idx) -> None:
        """ Deletes the local context at a given index. 
        """
        return self.chatbot.delete_context_by_id(idx)

    def chatbot_edit_context_idx(self, idx, context) -> None:
        """ Edits the local context based on input.
        """
        return self.chatbot.edit_context_by_id(idx, context)

    # ==================== GETTERS and SETTERS ====================
    @property
    def login_email(self) -> str:
        """Retrieves the login email property"""
        return self._login_email

    @login_email.setter
    def login_email(self, email: str):
        """Sets the login email property"""
        self._login_email = email

    # data analytics

    def get_user(self, email: str) -> User:
        user = User.query.filter_by(email=email).first()
        return user

    def save_submission(self, code: str, email: str) -> Submission:
        submission = Submission(
            code=code,
            time=time.strftime("%Y/%b/%d %H:%M:%S", time.localtime()),
            duration=-1,
            user_id=self.get_user(email).id
        )
        db.session.add(submission)
        db.session.commit()
        return submission

    def update_result(self, result: str, submission_id: int):
        if submission_id is None:
            return
        submission = Submission.query.filter_by(id=submission_id).first()
        submission.result = result
        db.session.commit()

    def get_all_submissions(self, user: User):
        submissions = []
        submissions = Submission.query.filter_by(user_id=User.id)
        return submissions

    
