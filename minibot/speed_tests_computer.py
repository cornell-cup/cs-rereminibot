import socket
import time
import numpy as np

def measure_latency(host, port, num_tests=10):
    total_latency = 0
    latencies = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        for i in range(num_tests):
            print("Starting Test " + str(i + 1))
            start_time = time.time()
            s.sendall(b"ping")
            response = s.recv(1024)
            end_time = time.time()
            roundtrip_latency = (end_time - start_time) * 1000  # Convert to milliseconds
            total_latency += roundtrip_latency
            print("Roundtrip Latency:", roundtrip_latency, "ms")
            latencies.append(roundtrip_latency)
    
    average_latency = total_latency / num_tests
    np.savetxt("LatencyMeasurements.txt", np.array(latencies))
    print("Average Latency:", average_latency, "ms")

if __name__ == "__main__":
    # This socket is used to listen for new incoming Minibot broadcasts
    # The Minibot broadcast will allow us to learn the Minibot's ipaddress
    # so that we can connect to the Minibot
    connection_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    connection_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            

    # an arbitrarily small time
    connection_sock.settimeout(0.01)

    # empty string means 0.0.0.0, which is all IP addresses on the local
    # machine, because some machines can have multiple Network Interface
    # Cards, and therefore will have multiple ip_addresses
    server_address = ("0.0.0.0", 5001)

    connection_sock.bind(server_address)
    
    connected = False
    pico_address = None
    while not connected:
        print("Trying to Connect!")
        response = "i_am_the_base_station"
        # a minibot should send this message in order to receive the ip_address
        request_password = "i_am_a_minibot"

        buffer_size = 4096

        # Continuously read from the socket, collecting every single broadcast
        # message sent by every Minibot
        address_data_map = {}
        try:
            data, address = connection_sock.recvfrom(buffer_size)
            while data:
                data = str(data.decode('UTF-8'))
                address_data_map[address] = data
                data, address = connection_sock.recvfrom(buffer_size)
        # nothing to read
        except socket.timeout:
            pass

        # create a new Minibot object to represent each Minibot that sent a
        # broadcast to the basestation
        for address in address_data_map:
            # data should consist of "password port_number"
            data_lst = address_data_map[address].split(" ")
            if data_lst[0] == request_password:
                # Tell the minibot that you are the base station
                connection_sock.sendto(response.encode(), address)
                pico_address = address[0]
                pico_port = data_lst[1]
                connected = True

    print("Connected!")
    print("Address:", pico_address)
    print("Port:", pico_port)
    num_tests = int(input("Enter the number of tests to perform: "))
    measure_latency(pico_address, int(pico_port), num_tests)