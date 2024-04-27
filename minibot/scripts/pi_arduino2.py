from machine import UART, Pin
import time
import _thread
import scripts.message_utils as msglib

# Methods in this file are called when needing to send information to or 
# get information from the Raspberry Pi, connected to the Pico W (onboard the XRP) using UART

uart = None

class TransmitLock():
    # TODO: implement this class with condition variables
    """ Class to handle locking amongst movement threads.
    self.is_transmitting = 0 if nothing is transmitting.
    self.is_transmitting = -1 if one thread is waiting for another thread to finish.
    self.is_transmitting = 1 if a thread is transmitting
    """

    def __init__(self):
        self.lock = _thread.allocate_lock()
        self.is_transmitting = 0
        self.timestamp = 0

    def can_continue_transmitting(self):
        """ Whether the thread that has currently acquired the lock
            can continue to transmit, or not because another thread is waiting to
            acquire the lock
        """
        with self.lock:
            return self.is_transmitting == 1

    def end_transmit(self):
        with self.lock:
            self.is_transmitting = 0

    def start_transmit(self, timestamp):
        """ Tries to acquire the lock to start transmitting.  If the lock is acquired
            by another thread, sets self.is_transmitting = -1 to tell the other thread
            that it needs to stop transmitting and hand over the lock to the current thread.
            Arguments:
                timestamp: (int) The timestamp of the current thread.  This timestamp is used to
                    figure out which thread was waiting for the lock first, so that the thread that
                    was waiting first gets priority when accessing the lock
            Returns:  (bool) True if the transmit_lock was successfully acquired, False otherwise.
            """
        with self.lock:
            if self.is_transmitting == 0:
                # the timestamp field indicates the priority of the thread that
                # was waiting first for the lock.  If the current thread's timestamp
                # statement does not have its e priority of the
                # thread that was waiting first, do not let it enter this code block
                if self.timestamp == timestamp or self.timestamp == 0:
                    self.is_transmitting = 1
                    # reset the timestamp field, because the current thread
                    # managed to acquire the lock
                    self.timestamp = 0
                    return True
                # if some other thread is transmitting (self.is_transmitting != 0)
                # and no other thread has told the thread to stop transmitting
                # (self.is_transmitting != -1), then that means the current thread
                # is the first thread that will be waiting for the lock.  Hence,
                # the current thread tells the thread that is trasmitting to stop
                # trasmitting (by setting self.is_transmitting = -1).  The current
                # thread also records its timestamp to indicate that its the next
                # thread that will get to acquire the lock
            elif self.is_transmitting == 1:
                self.is_transmitting = -1
                self.timestamp = timestamp
            # otherwise if self.is_transmitting == -1, don't do anything
            # just return False, this is because some other thread has already
            # told the currently transmitting thread to stop transmitting,
            # and that other thread has already saved its timestamp in
            # self.timestamp so the other thread will acquire the lock before
            # you can.
        return False


tlock = TransmitLock()


def acquire_lock():
    """ Acquires the lock to start sending data over UART to
    the Raspberry Pi 0.
    """
    uart = UART(baudrate=115200)
    uart.init(baudrate=115200)
    priority = time.time()
    while not tlock.start_transmit(priority):
        time.sleep(0.01)


def release_lock():
    """ Releases the lock that was used to send data over UART to
    the Raspberry Pi.
    """
    uart.deinit()
    tlock.end_transmit()


def motor(id, dir, power, time):
    """
    Ask the Raspberry Pi to move the motor identified with [id] in direction [dir] at
    [power]% power for [time] seconds.
    """
    acquire_lock()
    data = [ord('M'), id, ord('D'), dir, ord('P'), power, ord('T'), time]
    msg = msglib.make_crc_message(data)
    msglib.send_message(uart, msg)
    release_lock()


def servo(id, angle):
    """
    Ask the Raspberry Pi to move the servo identified with [id] to the angle
    [angle] (in degrees)
    """
    acquire_lock()
    # Angle is 0 to 180 so no need for 2 bytes
    data = [ord('S'), ord('R'), ord('V'), ord('O'), id, ord('A'), angle]
    msg = msglib.make_crc_message(data)
    msglib.send_message(uart, msg)
    release_lock()


def rfid(id, returned_tags):
    """
    Ask the Raspberry Pi to provide each of the RFID Tag bytes(id1, id2, id3, id4)
    """
    acquire_lock()
    load_req = [ord('R'), ord('F'), ord('I'), ord('D')]
    load_msg = msglib.make_crc_message(load_req)
    data, numTries = msglib.read_data(
        uart, load_msg, 22, msglib.validate_crc_message)
    data = msglib.unpack_crc_message(data)
    if len(data) != 0:
        returned_tags[0] = data[0]
        returned_tags[1] = data[1]
        returned_tags[2] = data[2]
        returned_tags[3] = data[3]
    #print("Data:" + data)
    release_lock()


def stop():
    """
    Ask the Raspberry Pi to stop moving all motors.
    To stop an individual motor, set its power to 0 with motor()
    """
    acquire_lock()
    data = [ord('S'), ord('T'), ord('O'), ord('P')]
    msg = msglib.make_crc_message(data)
    msglib.send_message(uart, msg)
    release_lock()


def sensor(id):
    """
    Ask the Raspberry Pi to read a value from the sensor identified by [id].
    """
    acquire_lock()
    load_req = [ord('L'), ord('O'), ord('A'), ord('D'), id]
    load_msg = msglib.make_crc_message(load_req)
    data, numTries = msglib.read_data(
        uart, load_msg, 22, msglib.validate_crc_message)
    data = msglib.unpack_crc_message(data)
    release_lock()
    return data

def transmit_once(cmd):
    """ Sends each character in the cmd to the Raspberry Pi

    Arguments:
        cmd: (str) The command to be sent to the Arduino
            (eg. "F" to tell the Arduino to start driving
             the Minibot forward)
    """
    for char in cmd:
        print(char)
        uart.write([ord(char)])
        
def set_ports(ports):
    """ Tell minibot which motors and sensor correspond to
    which ports.

    Arguments:
        ports: ([str, int]) List where the first element is a port name
            and the second element is the corresponding port number
    """
    acquire_lock()
    ports = ports.split()
    port_name = ports[0]
    port_number = str(ports[1])
    ports_dict = {
        "LMOTOR": "LM",
        "RMOTOR": "RM",
        "MOTOR3": "M",
        "LINE": "L",
        "INFRARED": "I",
        "RFID": "R",
        "ULTRASONIC": "U"
    }
    arr = list(port_number) + list(ports_dict[port_name])
    transmit_once(arr)
    release_lock()
