import serial
# timeout=None means there is no timeout between messages
# xonoff is software control for 
ser = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=0, stopbits=serial.STOPBITS_ONE)

while True: 
    # Run UART receive, nonblocking 
    request = ser.readline().decode() # Decoding gets rid of newline character at the end 

    # un-format request
    if request == 'Write.':
        pass
    elif validate_crc_message(request):
        request = unpack_crc_message(request)

        if request == "": # some key that represents an animation LCD[emotion]
            # Run LCD methods


            # Send OK message back
            # ser.write(b'OK')

