# Needs to run LCD screen
# accept UART messages
#    thread - can't communicate with main thread 
#    blocking - only try once? Could cause a backlog on the Pico side 
#               try multiple times? Could cause a block on the RPi 0 side
#    nonblocking - set so UART tries once and then runs update for LCD screen 

import serial
# timeout=None means there is no timeout between messages
# xonoff is software control for 
ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=None, xonxoff=True)

while True: 
    # Run UART receive, nonblocking 
    # request = 

    # un-format request
    if validate_crc_message(request, data_len=22):
        request = unpack_crc_message(request)

    if request == "": # some key that represents an animation LCD[emotion]
        # Run LCD methods


        # Send OK message back
        ser.write(b'OK')

