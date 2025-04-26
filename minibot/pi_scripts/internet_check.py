import socket

def is_internet_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Checks if the internet is connected by attempting to connect to a known host.
    Default is Google's DNS server (8.8.8.8) on port 53.
    Returns True if connection succeeds, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        return False
