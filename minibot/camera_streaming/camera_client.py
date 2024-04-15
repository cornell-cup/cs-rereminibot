# Run this on the Raspberry Pi with the camera

# USAGE
# python3 client.py --server-ip <ip address of computer>

# import the necessary packages
import imutils
from imutils.video import VideoStream
from imagezmq import imagezmq
import argparse
import socket
import time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--server-ip", required=True,
                    help="ip address of the server to which the client will connect")
    args = vars(ap.parse_args())

    sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(
        args["server_ip"]))

    rpiName = socket.gethostname()
    vs = VideoStream(usePiCamera=True, resolution=(240, 135), framerate=25).start()
    time.sleep(2.0)

    while True:
        frame = vs.read()
        sender.send_image(rpiName, frame)


if __name__ == "__main__":
    main()