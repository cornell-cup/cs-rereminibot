# Needs to run LCD screen
# accept UART messages
#    thread - can't communicate with main thread 
#    blocking - only try once? Could cause a backlog on the Pico side 
#               try multiple times? Could cause a block on the RPi 0 side
#    nonblocking - set so UART tries once and then runs update for LCD screen 

while True: 
    # Run UART receive, nonblocking 
    # Run LCD methods


