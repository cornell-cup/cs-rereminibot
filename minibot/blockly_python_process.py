import _thread
from emotion import *

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

        # MAY NEED TO MOVE SOMEWHERE ELSE LATER
        self.current_emotion = None
    
    def get_exec_result(self) -> str:
        """ Gets the execution result of the last blockly / python script """
        # Try to acquire lock (blocking=False, equivalent to waitflag=0)
        success = self.result_lock.acquire()
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
        self.thread_stop_flag = True
        self.thread = None
        self.result_lock.acquire()
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
        program = self.process_string(code)
        program = ''.join(program)
        # create a shared variable of type "string" between the child
        # process and the current process

        # TODO: check if thread is alive
        if self.thread and self.thread_alive:
            self.kill_thread()
            self.result_lock.acquire()
            self.result = "Another process is running....Killing the process now....." + "Press Run again"
            self.result_lock.release()
            return
        
        self.result_lock.acquire()
        self.result = ""
        self.result_lock.release()
        
        # Run the Python program in a different process so that we
        # don't need to wait for it to terminate and we can kill it
        # whenever we want.
        self.exec_script_str(program)

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

        # Inject emotional code
        init_emotional_system(program)        

        # TODO: convert threading after replacing BOT_LIB_FUNCS files
        # program += "from threading import *\n"
        for i in range(len(cmds)):
            cmds[i] = cmds[i].replace(u'\xa0', u' ')
            program.append(cmds[i] + "\n")
        return program
    
    def exec_script_str(self, program: str):
        self.thread_alive = True
        self.result_lock.acquire()
        try:
            if self.thread_stop_flag == False:
                # try to execute the whole program
                print(program)
                exec(program)
            if self.thread_stop_flag:
                self.result = "Killed by user"
                self.result_lock.release()
                self.thread_alive = False
                return
            else:
                self.result = "Successful execution"
        except Exception as exception:
            str_exception = str(type(exception)) + ": " + str(exception)
            print(str_exception)
            if self.thread_stop_flag:
                self.result = "Killed by user"
                self.result_lock.release()
                self.thread_alive = False
                return
            else:
                self.result = str_exception
            
        self.result_lock.release()
        self.thread_alive = False