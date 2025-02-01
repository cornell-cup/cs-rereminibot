from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from socket import SOL_SOCKET, SO_REUSEADDR
import network

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

def setup_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect("CornellCup-Web", "disneyworld!")

    # Wait for connection to be established
    while not sta_if.isconnected():
        pass

    print("Connected to WiFi")

def broadcast_to_base_station():   
    """ Establishes a TCP connection to the basestation.  This connection is 
    used to receive commands from the basestation, and send replies if 
    necessary.
    """
    # Create a UDP socket.  We want to establish a TCP (reliable) connection
    # between the basestation and the XRP
    broadcast_sock = socket(AF_INET, SOCK_DGRAM)
    # can immediately rebind if the program is killed and then restarted
    broadcast_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # can broadcast messages to all
    # self.broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    connected = False
    while not connected:
        print("Broadcasting message to basestation.")
        # try connecting to the basestation every 2 sec until connection is made
        broadcast_sock.settimeout(0.2)
        data = ""
        # broadcast message to basestation
        msg_byte_str = f"{MINIBOT_MESSAGE} {10000}".encode()
        try:
            # use sendto() instead of send() for UDP
            broadcast_sock.sendto(msg_byte_str, BROADCAST_ADDRESS)
            data = broadcast_sock.recv(4096)
        # TODO: timeout error removed from basestation
        # except timeout:
        #     print("Timed out", flush=True)
        except OSError as e:
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
                connected = True
            else:
                # if verification fails we just print but don't do anything
                # about the fact that verification failed.  Please fix when
                # rewriting the security policy
                print('Verification failed.')

def create_roundtrip_socket_connection():
    """ Creates a socket that listens for TCP connections from the 
    basestation.
    """
    sock = socket(AF_INET, SOCK_STREAM)
    # can immediately rebind if the program is killed and then restarted
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # "" means bind to all addresses on this device.  Port 10000 was
    # randomly chosen as the port to bind to
    sock.bind(("0.0.0.0", 10000))
    # Make socket start listening
    print("Waiting for TCP connection from basestation")
    sock.listen(1)
    
    print("Waiting for connection...")
    conn, addr = sock.accept()
    print("Connected to laptop:", addr)
    
    return conn
    
def communicate_with_laptop(conn):
    """Communicate with the laptop over the TCP connection."""
    while True:
        data = conn.recv(1024).decode()  # Receive data from the laptop
        if not data:
            print("No data received.")
            break
        print("Received message from laptop:", data)
        
        # Assuming you want to send back a response
        response = "Hello from Pico W!"
        conn.sendall(response.encode())  # Send response back to the laptop

    conn.close()    
   
# Connect to Wi-Fi
setup_wifi()

# Broadcast and establish connection with laptop
broadcast_to_base_station()   
   
# Accept TCP Connection from Laptop
roundtrip_conn = create_roundtrip_socket_connection()

# Communicate with laptop over TCP
communicate_with_laptop(roundtrip_conn)
    
print("Test Complete.")