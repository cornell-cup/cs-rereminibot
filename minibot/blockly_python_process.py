# from ctypes import c_char_p
# from multiprocessing import Process, Manager, Value
# import os
# import importlib
# import sys

import _thread

class BlocklyPythonProcess:
    """ Stores the process which is executing the Blockly / Python script
    being executed by the user. """
    def __init__(self, BOT_LIB_FUNCS):
        # the currently executing process, None if nothing executing
        self.thread = None
        self.thread_alive = False
        self.thread_stop_flag = False
        # the result of the last executed process
        self.result = None 
        self.result_lock = _thread.allocate_lock()
        self.BOT_LIB_FUNCS = BOT_LIB_FUNCS
    
    def get_exec_result(self) -> str:
        """ Gets the execution result of the last blockly / python script """
        # Try to acquire lock (blocking=False, equivalent to waitflag=0)
        success = self.result_lock.acquire(waitflag=0)
        if success:
            if self.result:
                self.result_lock.release()
                return ""
            else:
                resultCopy = self.result
                self.result_lock.release()
                return resultCopy
        else:
            return ""
    
    def is_running(self) -> bool:
        """ Whether there is a currently executing blockly / python script """
        return self.thread is not None

    def kill_thread(self):
        # send kill signal to process
        # self.thread.terminate()
        # wait for the process to terminate completely
        # self.thread.join()
        self.thread_stop_flag = True
        self.thread = None
        self.result_lock.acquire(waitflag=1)
        self.result = "Killed by user"
        self.result_lock.release()
    
    def spawn_script(self, code: str):
        """ Starts the specified script in a new process so that the main
        minibot.py thread is not blocked.  For example, the user may want to 
        execute:
            while True:
                print("hi")
        and would not want the Minibot to become unresponsive.  Hence these 
        scripts must be spawned in new processes
    
        Arguments:
            code:  The code of the script that will be spawned
        """
        # script_name = "bot_script.py"
        program = self.process_string(code)

        # write the script to a file which we'll execute
        # file_dir is the path to folder this file is in
        # file_dir = os.path.dirname(os.path.realpath(__file__))
        # script_file = open(file_dir + "/scripts/" + script_name, 'w+')
        # script_file.write(program)
        # script_file.close()

        # create a shared variable of type "string" between the child
        # process and the current process

        # TODO: check if thread is alive
        if self.thread and self.thread_alive:
            self.kill_thread()
            self.result_lock.acquire(waitflag=1)
            self.result = "Another process is running....Killing the process now....." + "Press Run again"
            self.result_lock.release()
            return
        
        self.result_lock.acquire(waitflag=1)
        self.result = ""
        self.result_lock.release()
        
        # Run the Python program in a different process so that we
        # don't need to wait for it to terminate and we can kill it
        # whenever we want.
        # self.thread = _thread.start_new_thread(run_script, (script_name,))
        self.thread = _thread.start_new_thread(exec_script_str, (program,))

    def process_string(self, value: str) -> [str]:
        """
        Function from /minibot/main.py. Encases programs in a function
        called run(), which can later be ran when imported via the
        import library. Also adds imports necessary to run bot functions.
        Args:
            value (:obj:`str`): The program to format.
        """
        cmds = value.splitlines()
        program = []
        program.append("from scripts." + self.BOT_LIB_FUNCS + " import *\n")
        program.append("import time\n")
        # TODO: convert threading after replacing BOT_LIB_FUNCS files
        # program += "from threading import *\n"
        for i in range(len(cmds)):
            cmds[i] = cmds[i].replace(u'\xa0', u' ')
            program.append(cmds[i] + "\n")
        return program
    
    def exec_script_str(self, program: [str]):
        self.thread_alive = True
        self.result_lock.acquire(waitflag=0)
        try:
            line = 0
            while self.thread_stop_flag == False and line < len(program):
                exec(program[line])
                line = line + 1
            if self.thread_stop_flag:
                self.result = "Killed by user"
                self.result_lock.release()
                self.thread_alive = False
                return
            else:
                self.result = "Successful execution"
        except Exception as exception:
            str_exception = str(type(exception)) + ": " + str(exception)
            if self.thread_stop_flag:
                self.result = "Killed by user"
                self.result_lock.release()
                self.thread_alive = False
                return
            else:
                self.result = str_exception
            
        self.result_lock.release()
        self.thread_alive = False

    # def run_script(self, scriptname: str):
    #     """
    #     Loads a script and runs it.
    #     Args:
    #         scriptname: The name of the script to run.
    #     """
    #     # Cache invalidation and module refreshes are needed to ensure
    #     # the most recent script is executed

    #     try:
    #         index = scriptname.find(".")
    #         # new script is created under script folder with the script_names
    #         # invalidate_caches ensures that the new script file can be found later when importing the module
    #         importlib.invalidate_caches()
    #         script_name = "scripts." + scriptname[0: index]
    #         script = importlib.import_module(script_name)
    #         # re-compile and re-execute the script
    #         # reset the variables and object references
    #         importlib.reload(script)
    #         script.run()
    #         self.result = "Successful execution"
    #     except Exception as exception:
    #         str_exception = str(type(exception)) + ": " + str(exception)
    #         self.result = str_exception