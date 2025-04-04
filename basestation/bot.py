import socket
import time
from typing import Optional

from basestation.util.locked_variable import LockedVariable

class Bot:
    """ Represents a Minibot that the Basestation is connected to, it is a 
    Minibot interface that the basestation can interact with.  This class 
    handles all socket communication with the Minibot
    """
    SOCKET_BUFFER_SIZE = 1024
    START_CMD_TOKEN = "<<<<"
    END_CMD_TOKEN = ">>>>"
    TIMEOUT_LIMIT = 5

    def __init__(self, bot_name: str, ip_address: str, port: int = 10000):
        """ Creates the Minibot representation.
        Arguments:
            bot_name:   The name of the Minibot
            ip_address: The ip address of the Minibot
            port:       The port on which the Minibot's listening/server socket 
                        is running on.  This information is needed when trying 
                        to initiate a connection with the Minibot.
        """
        self.port = port
        self.ip_address = ip_address
        # Initiate connection with the Minibot.  If the initiation is successful,
        # self.sock will contain the endpoint on which we can communication with
        # the Minibot
        self.sock = socket.create_connection((ip_address, port))
        # an arbitrarily small time
        self.sock.settimeout(0.01)
        self._name = bot_name
        self.last_status_time = time.time()
        self.is_socket_connected = True
        self.script_exec_result_var = LockedVariable(None, "Waiting for execution completion")
        self.script_alive_var = LockedVariable(False, True)
        self.rfid_tags = ""
        self.accelerometer_values = [None, None, None]

    def try_receive_data(self, peek: bool = False) -> Optional[str]:
        """ Tries to receive data from the Minibot. 

        Arguments:
            peek:  Whether to empty the socket buffer.  If False empty buffer,
                if True, do not. 
        Returns:  The data, or None if the socket is disconnected 
        """
        line = ""
        try:
            if peek:
                data = self.sock.recv(Bot.SOCKET_BUFFER_SIZE, socket.MSG_PEEK)
            else:
                data = self.sock.recv(Bot.SOCKET_BUFFER_SIZE)
            line = data.decode("utf-8")
            line = line if len(line) > 0 else None  # if "" then line = None
            if line is None:
                self.sock.close()
                self.is_socket_connected = False
        except socket.timeout:
            pass
        except ConnectionResetError:
            print("Minibot disconnected")
            line = None
            self.is_socket_connected = False
        return line

    def sendKV(self, key: str, value: str):
        """ Send message with specified key and value. """
        if not self.is_socket_connected:
            return
        data = f"<<<<{key},{value}>>>>".encode()

        # check whether the socket connection is still open
        line = self.try_receive_data(peek=True)
        # If the socket connection is not disconnected
        if line is not None:
            self.sock.sendall(data)

    def readKV(self):
        """ Reads from the socket connection between the basestation and the Minibot
        <<<<BOTSTATUS,ACTIVE>>>>
        """
        if not self.is_socket_connected:
            return
        data_str = self.try_receive_data()
        # print(f"Data str {data_str}")
        if data_str is None:
            return

        while len(data_str) > 0:
            comma = data_str.find(",")
            start = data_str.find(Bot.START_CMD_TOKEN)
            end = data_str.find(Bot.END_CMD_TOKEN)

            token_len = len(Bot.START_CMD_TOKEN)
            key = data_str[start + token_len:comma]
            value = data_str[comma + 1:end]

            # checks if BOTSTATUS is ACTIVE and resets the last status time
            if key == "BOTSTATUS" and value == "ACTIVE":
                # set to current time in seconds
                self.last_status_time = time.time()
            elif key == "SCRIPT_EXEC_RESULT":
                if self.script_exec_result_lock.acquire(blocking=False):
                    self.script_exec_result = value
                    self.script_exec_result_lock.release()
                else:
                    self.script_exec_result = "Waiting for execution completion"
            elif key == "RFID":
                if value == "":
                    self.rfid_tags = ""
                else:
                    self.rfid_tags = value
            elif key == "IMU":
                try:
                    self.accelerometer_values = [float(x) for x in value.split(" ")]
                except: 
                    self.accelerometer_values = [None, None, None]

                if (len(self.accelerometer_values)) != 3:
                    self.accelerometer_values = [None, None, None]

                print(f"IMU {self.accelerometer_values}")
            data_str = data_str[end + token_len:]

    def get_imu(self):
        # if script == True:
        self.sendKV("IMU", "")
        self.readKV()
        return self.accelerometer_values

    def is_connected(self) -> bool:
        """ Checks whether the Minibot has sent a heartbeat message recently 
        """
        time_diff = time.time() - self.last_status_time
        return time_diff < Bot.TIMEOUT_LIMIT and self.is_socket_connected

    @property
    def name(self):
        return self._name