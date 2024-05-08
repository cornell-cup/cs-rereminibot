from XRPLib.defaults import *

from machine import UART, Pin
import time
from uart_scripts.crc import crc16

DATA_LEN=10

def send_message(uart, msg, tries=1):
    """
    Send a message over UART.
    # TODO: send a message over UART until the recipient sends back an ACK. 

    Args:
        uart: The UART object 
        msg: The message to send as a list of ASCII numbers, including
                any non-payload bytes. 
        tries:  The number of tries to send the message
                    before giving up.
    """
    done = False
    numTries = 0
    if type(msg) == bytes:
        msg = bytearray(msg)
    else:
        msg = bytearray([msg])
    # buf = msg[:]
    while not done and numTries < tries:
        # Send the message
        uart.write("Write.\n")
        uart.write(msg)
        uart.flush()

        # TODO: implement reading for ACK
        # while uart.any():
        #     print("Reading")
        #     buf = uart.readline()
        #     print(buf)
        #     print("Finished Reading ")
        # uart.flush()
        numTries += 1
        
        
        # # Check for ACKnowledgement
        # for i in buf:
        #     if i == ACK:
        #         done = True
        #         break
        # buf = msg[:]
    # print("Sent {} in {} tries".format(msg, numTries))

def read_data(uart, msg, nbytes, validator, max_tries=100):
    """
    WARNING: UNTESTED
    Reads data from the secondary device over UART.

    Args:
        uart: The UART object
        msg: The message to send as a list of ASCII numbers, including
                any non-payload bytes. Use this to request some data
                to be loaded for reading.
        nbytes: The number of bytes to read, including any validation
                bytes, start chars, end chars, checksums, etc.
        validator: function from list of bytes -> [true, false]
                    Used to determine if data is valid or not
        max_tries:  The maximum number of tries to send the message
                    before giving up
    """
    if type(msg) == bytes:
        msg = list(msg)
    lod_msg = msg.copy()
    # print("Send load req msg")
    send_message(spi, lod_msg)  # request data load
    buf = [0] * nbytes
    done = False
    data = []
    numTries = 0
    while not done and numTries < max_tries:
        # Send empty buffer (to read)
        # print("Sent {}: {} | {}".format(len(buf), "".join([chr(c) for c in bu>
        # uart.write(buf)
        uart.readinto(buf)
        uart.flush()
        numTries += 1
        # Validate data
        # print("Received {}: {} | {}".format(len(buf), "".join([chr(c) for c in >
        if validate_crc_message(buf):
            print("Data OK")
            data = buf.copy()
            done = True
        else:
            # Ask to resend
            # print("Send load req msg")
            send_message(uart, lod_msg)
    # print("Read {} in {} tries".format(buf, numTries))
    return [data, numTries]


def make_crc_message(data):
    """
    Makes a sendable message from some data.

    Args:
        data: A list of integers or a string to send.
                (i.e. all ints must be smaller than 256)
    """
    if len(data) > DATA_LEN:
        # This is changeable to fit future needs
        raise ValueError(f"Messages can be up to {DATA_LEN} bytes.")
    
    if type(data[0]) != type(1):
        data = [ord(d) for d in data]
    start = bytes([ord(x) for x in "CC"])

    # TODO: implement checksum
    # data_hash = crc16(data)
    # data_hash_bytes = data_hash.to_bytes(2, "big")  # 2-byte CRC

    end = bytes([ord(x) for x in "RT"])
    
    # return start + data_hash_bytes + bytes(data) + end
    return start + bytes(data) + end + "\n"

# Validate whether a message is complete
def validate_crc_message(msg, data_len=DATA_LEN):
    """
    Validate whether a received message is complete.

    args:
        msg: The message (as a list of bytes)
        data_len: The length of the data bytes, not including
                    the 2 start chars, 2 end chars, and checksum
    """
    start_ok = (msg[0] == ord('C') and msg[1] == ord('C'))
    end_ok = (msg[-2] == ord('R') and msg[-1] == ord('T')) or (msg[-3] == ord('R') and msg[-2] == ord('T') and msg[-1] == ord('\n'))
    # data_hash = crc16(msg[4:4+data_len])
    # msg_hash = int.from_bytes(msg[2:4], 'big')  # bytes 2 and 3
    # hash_ok = (data_hash == msg_hash)
    
    # return start_ok and end_ok and hash_ok
    return start_ok and end_ok


def unpack_crc_message(msg):
    # unpacking w/ checksum
    # return msg[4:-2] 

    # unpacking w/o checksum
    if msg[-1] == ord('\n'):
        return msg[2:-3]
    else:
        return msg[2:-2]