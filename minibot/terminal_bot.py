from blockly_python_process import BlocklyPythonProcess
from bs_repr import BS_Repr

from collections import deque
from select import select

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from socket import SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

# Micropython imports
import time
from builtins import dict, set
import _thread
import sys
import argparse

# NOTE: "flush=True" was removed from all print statements as a temporary
# solution to how flush is not present in MicroPython. Additional configs
# will possibly be added to ensure that print can be used for testing.

class Minibot:
    """ Represents a minibot.  Handles all communication with the basestation
    as well as executing commands sent by the basestation.

    Note: sock stands for socket throughout this file.  A socket is one endpoint
        of a communication channel. 
    """
    # address refers to ip_address and port
    # 255.255.255.255 to indicate that we are broadcasting to all addresses
    # on port 5001.  The Basestation has been hard-coded to listen on port 5001
    # for incoming Minibot broadcasts
    BROADCAST_ADDRESS = ('255.255.255.255', 5001)
    MINIBOT_MESSAGE = "i_am_a_minibot"
    BASESTATION_MESSAGE = "i_am_the_basestation"
    # 1024 bytes
    SOCKET_BUFFER_SIZE = 1024
    START_CMD_TOKEN = "<<<<"
    END_CMD_TOKEN = ">>>>"

    def __init__(self, port_number: int):
        # Set up WiFi connection

        # Create a UDP socket.  We want to establish a TCP (reliable) connection
        # between the basestation and the
        self.broadcast_sock = socket(AF_INET, SOCK_DGRAM)
        # can immediately rebind if the program is killed and then restarted
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # can broadcast messages to all
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.broadcast_sock.setblocking(False)

        # listens for a TCP connection from the basestation
        self.listener_sock = None
        self.port_number = port_number

        # Note:  The same socket can be in the readable_socks, writeable_socks
        # and errorable_socks i.e. the intersection of these lists does not need
        # to be (and will almost never be) the empty set

        # contains sockets which we are expecting to receive some data on
        self.readable_socks = []
        # contains sockets which we want to send some data on
        self.writable_socks = []
        # contains sockets that throw errors that we care about and want to
        # react to
        self.errorable_socks = []
        # TODO: All message queues should have a max limit of messages that they
        # store, implement custom class at some point
        # self.writable_sock_message_queue_map = dict()
        # replace map with key and value lists, as sockets are not hashable
        # map key to value using the same index in both lists
        self.writable_sock_message_queue_key = []
        self.writable_sock_message_queue_value = []
        self.bs_repr = None
        self.sock_lists = [self.readable_socks, self.writable_socks, self.errorable_socks]

        self.long_script_str = ""

        self.blockly_python_proc = BlocklyPythonProcess(BOT_LIB_FUNCS)
        
    def main(self):
        """ Implements the main activity loop for the Minibot.  This activity 
        loop continuously listens for commands from the basestation, and 
        connects/reconnects to the basestation if there is no connection.
        """

        # Couldn't find an equivalent for sock.fileno()
        # select would not cause an error if there is an inactive socket
        # so there is no need to remove closed socket through this operation
        # def remove_closed_sockets(SOCKET_LIST):
        #     sockets = SOCKET_LIST.copy()
        #     for sock in sockets:
        #     # Remove file descriptor if closed
        #         if sock != None and sock.fileno() < 0:
        #             SOCKET_LIST.remove(sock)

        # basically acts as a handler for keyboard interrupt using try-catch
        try: 
            self.create_listener_sock()
            # Add listener sock to input_socks so that we are alerted if any
            # connections are trying to be created and add listener sock to
            # errorable_socks so that we are alerted if an error gets thrown by this
            # listener sock.  No need to add the listener sock to writable socks
            # because we won't be writing to this socket, only listening.
            self.readable_socks.append(self.listener_sock)
            self.errorable_socks.append(self.listener_sock)
            while True:
                # if the listener socket is the only socket alive, we need to
                # broadcast a message to the basestation to set up a new connection
                # with us (the minibot)
                if len(self.readable_socks) == 1:
                    self.broadcast_to_base_station()
                    
                # Remove all closed sockets to prevent select errors. Note: not sure
                # whether to perform this before or after checking whether reconnection
                # is necessary.
                # remove_closed_sockets(self.readable_socks)
                # remove_closed_sockets(self.writable_socks)
                # remove_closed_sockets(self.errorable_socks)
                    
                # select returns new lists of sockets that are read ready (have
                # received data), write ready (have initialized their buffers, and
                # are ready to be written to), or errored out (have thrown an error)
                # select returns as soon as it detects some activity on one or more
                # of the sockets in the lists passed to it, or if the timeout time
                # has elapsed
                # Example of using select in Python: https://pymotw.com/2/select/
                read_ready_socks, write_ready_socks, errored_out_socks = select(
                    self.readable_socks,
                    self.writable_socks,
                    self.errorable_socks,
                    1,  # timeout time
                )
                # WARNING!! Be careful about closing sockets in any of these functions
                # because the local lists read_ready_socks, write_ready_socks
                # and errored_out_socks will still contain the closed socket.
                # Hence, if you do this removal, make sure the socket is removed
                # from these local lists too!!!
                self.handle_errorable_socks(errored_out_socks)
                self.handle_writable_socks(write_ready_socks)
                self.handle_readable_socks(read_ready_socks)

                # if basestation exists but is disconnected, stop minibot
                if self.bs_repr and not self.bs_repr.is_connected():
                    self.basestation_disconnected(self.bs_repr.conn_sock)
        except KeyboardInterrupt:
            print("Ctrl-C interrupt!")
            self.sigint_handler()
        except Exception as e: #TODO: Possibly remove for final version
             print(e)
    

    def create_listener_sock(self):
        """ Creates a socket that listens for TCP connections from the 
        basestation.
        """
        self.listener_sock = socket(AF_INET, SOCK_STREAM)
        # can immediately rebind if the program is killed and then restarted
        self.listener_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        # "" means bind to all addresses on this device.  Port 10000 was
        # randomly chosen as the port to bind to
        self.listener_sock.bind(("0.0.0.0", self.port_number))
        # Make socket start listening
        print("Waiting for TCP connection from basestation")
        self.listener_sock.listen()
        self.listener_sock.setblocking(False)

    def broadcast_to_base_station(self):
        """ Establishes a TCP connection to the basestation.  This connection is 
        used to receive commands from the basestation, and send replies if 
        necessary.
        """
        print("Broadcasting message to basestation.")
        # try connecting to the basestation every 2 sec until connection is made
        self.broadcast_sock.settimeout(0.2)
        data = ""
        # broadcast message to basestation
        msg_byte_str = f"{Minibot.MINIBOT_MESSAGE} {self.port_number}".encode()
        try:
            # use sendto() instead of send() for UDP
            self.broadcast_sock.sendto(msg_byte_str, Minibot.BROADCAST_ADDRESS)
            data = self.broadcast_sock.recv(4096)
        # TODO: timeout error removed from basestation
        # except timeout:
        #     print("Timed out", flush=True)
        except OSError as e:
            print(e)
            print("Try again")

        # TODO this security policy is stupid.  We should be doing
        # authentication after we create the TCP connection and also we should
        # be using some service like WebAuth to obtain a shared key to encrypt
        # messages.  Might be a fun project to work on at some point but not
        # necessary for a functional Minibot system, but necessary for a secure
        # Minibot system.
        if data:
            if data.decode('UTF-8') == 'i_am_the_base_station':
                print("Basestation replied!")
            else:
                # if verification fails we just print but don't do anything
                # about the fact that verification failed.  Please fix when
                # rewriting the security policy
                print('Verification failed.')

    def handle_readable_socks(self, read_ready_socks):
        """ Reads from each of the sockets that have received some data.  
        If a listener socket received data, we accept the incoming connection.
        If a connection socket received data, we parse and execute, 
        the incoming command.

        Arguments:
            read_ready_socks: All sockets that have received data and are ready
                to be read from.
                read_ready_socks is a MicroPython builtin list of sockets.
        """
        for sock in read_ready_socks:
            # If its a listener socket, accept the incoming connection
            if sock is self.listener_sock:
                connection, base_station_addr = sock.accept()
                print(
                    f"Connected to base station with address {base_station_addr}"
                )
                # set to non-blocking reads (when we call connection.recv,
                # should read whatever is in its buffer and return immediately)
                connection.setblocking(False)
                # initialize basestation repr to the connection sock
                self.bs_repr = BS_Repr(connection)
                # we don't need to write anything right now, so don't add to
                # writable socks
                self.readable_socks.append(connection)
                self.errorable_socks.append(connection)
            # If its a connection socket, receive the data and execute the
            # necessary command
            else:
                # if the socket receives "", it means the socket was closed
                # from the other end
                data_str = sock.recv(
                    Minibot.SOCKET_BUFFER_SIZE).decode("utf-8")

                if data_str:
                    self.parse_and_execute_commands(sock, data_str)
                else:
                    self.basestation_disconnected(sock)
                # TODO need to write back saying that the command executed.
                # successfully

    def handle_writable_socks(self, write_ready_socks):
        """ 
        iterate through all the sockets in the write_ready_socks and 
        send over all messages in the socket's message_queue
        Arguments:
            write_ready_socks: 
                All sockets that have had data written to them.
                write_ready_socks is a MicroPython builtin list of sockets.
        """

        for sock in write_ready_socks:
            socket_index = self.socket_key_index(self.writable_sock_message_queue_key, sock)
            message_queue = self.writable_sock_message_queue_value[socket_index]
            all_messages = "".join(message_queue)
            sock.sendall(all_messages.encode())
            self.writable_sock_message_queue_value[socket_index] = []
            self.writable_socks.remove(sock)

    def handle_errorable_socks(self, errored_out_socks):
        """ Iterate through all the sockets in the errored_out_socks and 
        close these socks.  All these sockets have received some error code
        due to some failure.

        Arguments:
            errored_out_socks: All sockets that have errored out.
            errored_out_socks is a Micropython builtin list of sockets.
        """
        for sock in errored_out_socks:
            print(f"Socket errored out!!!! {sock}")
            # TODO handle more conditions instead of just
            # closing the socket
            self.close_sock(sock)

    def close_sock(self, sock: socket):
        """ Removes the socket from the readable, writable and errorable 
        socket lists, and then closes the socket.
        """
        for sock_list in self.sock_lists:
            if sock in sock_list:
                sock_list.remove(sock)
        sock.close()

    def basestation_disconnected(self, basestation_sock: socket):
        """ Performs the following commands because the Minibot is
        now disconnected from the basestation:
        1. Calls the stop function to make the Minibot stop whatever its doing.
        2. Closes the socket that the Minibot has been using, 
           basestation  
        """
        print("Basestation Disconnected")
        # _thread.start_new_thread(ece.stop, ())
        self.close_sock(basestation_sock)
        self.bs_repr = None

    def parse_and_execute_commands(self, sock: socket, data_str: str):
        """ Parses the data string into individual commands.  

        Arguments: 
            sock: The socket that we just read the command from
            data_str: The raw data that we receive from the socket.

        Example: 
            If the data_str is 
            "<<<<WHEELS,forward>>>><<<<WHEELS,backward>>>><<<<WHEELS,stop>>>>"
            the commands will be parsed and executed as:

            1. WHEELS, forward
            2. WHEELS, backward
            3. WHEELS, stop
        """
        while len(data_str) > 0:
            comma = data_str.find(",")
            start = data_str.find(Minibot.START_CMD_TOKEN)
            end = data_str.find(Minibot.END_CMD_TOKEN)

            token_len = len(Minibot.START_CMD_TOKEN)
            key = data_str[start + token_len:comma]
            if(key == "SCRIPT_BEG"):
                print("BEG Data:")
                print(data_str)
            if(key == "SCRIPT_MID"):
                print("MID Data:")
                print(data_str)
            if(key == "SCRIPT_END"):
                print("END Data:")
                print(data_str)
            value = data_str[comma + 1:end]
            # executes command with key,value
            self.execute_command(sock, key, value)
            # shrink the data_str with the remaining portion of the commands
            data_str = data_str[end + token_len:]

    def execute_command(self, sock: socket, key: str, value: str):
        """ Executes a command using the given key-value pair 

        Arguments:
            key: type of the command
            value: command to be executed
        """
        # All ECE commands need to be called under separate threads because each
        # ECE function contains an infinite loop.  This is because there was
        # data loss between the Raspberry Pi and the Arduino which is why the
        # Raspberry Pi needs to continuously repeat the command to the Arduino
        # so that some of the commands get through.  Once the data loss issue
        # is fixed, we can implement a regular solution. If we did not have the
        # threads, our code execution pointer would get stuck in the infinite loop.
        if key == "BOTSTATUS":
            # update status time of the basestation
            if self.bs_repr is not None:
                self.bs_repr.update_status_time()
            self.sendKV(sock, key, "ACTIVE")
        elif key == "SCRIPT_EXEC_RESULT" or key == "SCRIPT":
            # notify attempts for executing commands no longer in use
            print("executing commands no longer in use")
        # elif key == "SCRIPT_EXEC_RESULT":
        #     # getting result of execution and sending it to basestation
        #     script_exec_result = self.blockly_python_proc.get_exec_result()
        #     self.sendKV(sock, key, script_exec_result)
        elif key == "MODE":
            if value == "object_detection":
                _thread.start_new_thread(ece.object_detection, ())
            elif value == "line_follow":
                _thread.start_new_thread(ece.line_follow, ())
        elif key == "PORTS":
            ece.set_ports(value)
        # elif key == "SCRIPTS":
        #     # The script is always named bot_script.py.
        #     if len(value) > 0:
        #         self.blockly_python_proc.spawn_script(value)
        # elif key == "SCRIPT_BEG":
        #     print("BEG Value:")
        #     print(value)
        #     self.script_str = value
        # elif key == "SCRIPT_MID":
        #     print("MID Value:")
        #     print(value)
        #     self.script_str += value
        # elif key == "SCRIPT_END":
        #     print("END Value:")
        #     print(value)
        #     self.script_str += value
        #     if(len(self.script_str) > 0):
        #         self.blockly_python_proc.spawn_script(self.script_str)
        #     self.script_str = ""
        elif key == "WHEELS":
            print("key WHEELS")
            cmds_functions_map = {
                "forward": (1, 1),
                "backward": (-1, -1),
                "left": (0, 1),
                "right": (1, 0),
                "stop": (0, 0),
            }
            if value in cmds_functions_map:
                # TODO use the appropriate power arg instead of 50 when
                # that's implemented
                arg = cmds_functions_map[value]
                ece.drivetrain.set_effort(arg[0], arg[1])
            else:
                ece.drivetrain.set_effort(0, 0)
        elif key == "SPR" or key == "PBS":
            print("Received Command:", key + "," + value)
            # ece.send_pi_command(key + "," + value)
            # message_utils.send_message(message)
        elif key == "IR":
            return_val = []
            thread = _thread.start_new_thread(ece.read_ir, (return_val))

            while _thread.is_alive(thread):
                time.sleep(0.01)

            # Note: this is for testing and will be removed for MicroPython version
            # now = time.localtime()
            # file = open("/home/pi/Documents/" +
            #             now.strftime('%H:%M:%S.%f') + ".txt", "w")

            # file.write("From Arduino\n")
            # file.write(str(return_val))
            # file.close()

            if return_val[0] == 0:
                self.sendKV(sock, key, "HIGH")
            elif return_val[0] == 1:
                self.sendKV(sock, key, "LOW")
            else:
                self.sendKV(sock, key, "")
        elif key == "RFID":
            def pass_tags(self, sock: socket, key: str, value: str):
                returned_tags = [0, 0, 0, 0]
                # replace with direct call to the rfid sensor here
                # ece.rfid(value, returned_tags)
                self.sendKV(sock, key, ' '.join(str(e) for e in returned_tags))
    
            _thread.start_new_thread(pass_tags, (self, sock, key, value))
        elif key == "TESTRFID":
            def test_rfid(self, sock: socket, key: str, value: str):
                start_time = time.time()
                returned_tags = [0, 0, 0, 0]
                ece.rfid(value, returned_tags)
                latency = time.time() - start_time
                return_str = "RFID Tag: " + ' '.join(str(e) for e in returned_tags) + " Latency: " + str(latency)
                self.sendKV(sock, key, return_str)
            
            _thread.start_new_thread(test_rfid, (self, sock, key, value))
        elif key == "TEST":
            start_time = time.time()
            returned_msg = [0, 0, 0, 0]
            ece.test(returned_msg)
            time_elapsed = time.time() - start_time
            return_str = "Return Message: " + ' '.join(str(e) for e in returned_msg) + " Latency: " + str(time_elapsed)
            self.sendKV(sock, key, return_str)

            
    def sendKV(self, sock: socket, key: str, value: str):
        """ Sends a key-value pair to the specified socket. The key value
        pair is encoded as <<<<key, value>>>> when sent to the basestation """
        # we want to write to the socket we received data on, so add
        # it to the writable socks
        self.writable_socks.append(sock)
        message = f"<<<<{key},{value}>>>>"
        # if sock in self.writable_sock_message_queue_map:
        #     self.writable_sock_message_queue_map[sock].append(message)
        # else:
        #     self.writable_sock_message_queue_map[sock] = deque((), 20, 1)
        #     self.writable_sock_message_queue_map[sock].append(message)
        socket_index = self.socket_key_index(self.writable_sock_message_queue_key, sock)
        if socket_index != -1:
            self.writable_sock_message_queue_value[socket_index].append(message)
        else:
            self.writable_sock_message_queue_key.append(sock)
            self.writable_sock_message_queue_value.append([])
            self.writable_sock_message_queue_value[socket_index].append(message)

    def sigint_handler(self):
        """ Closes open resources before terminating the program, when 
        receives a CTRL + C
        """
        print("Minibot received CTRL + C")
        self.listener_sock.close()
        self.broadcast_sock.close()
        sys.exit(0)

    def socket_key_index(self, key_list, socket):
        """ Finds the index of the socket key in the key_list passed """
        for i in range(0, len(key_list)):
            if key_list[i] == socket:
                return i
        return -1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for Minibot')
    parser.add_argument(
        '-p', type=int, dest="port_number", default=10000
    )

    args = parser.parse_args()

    import uart_scripts.ece_dummy_ops as ece
    BOT_LIB_FUNCS = "ece_dummy_ops"
    print("Using Port", args.port_number)

    minibot = Minibot(args.port_number)
    minibot.main()