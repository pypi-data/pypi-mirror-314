import socket
import time
import math
import numpy as np


class VRobotGraphClient:
    def __init__(self, server_address=("localhost", 12750)):
        self.server_address = server_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def update(self, ts, vec=None, x=0.0, y=0.0, z=0.0, verbose=0):
        if (vec is not None) and (vec.shape[0] == 3):
            x = vec[0]
            y = vec[1]
            z = vec[2]
        message = f"{ts},{x},{y},{z}"
        if verbose > 0:
            print(f"Graphing: {message}")
        self.send(message)

    def send(self, message):
        self.sock.sendto(message.encode(), self.server_address)

    def close(self):
        self.sock.close()


def main():
    gtool = VRobotGraphClient()  # Uses the default server_address
    start_time = time.time()
    try:
        while (time.time() - start_time) < 60:
            timestamp = time.time()
            x = math.sin(timestamp)
            y = math.cos(timestamp)
            z = math.sin(timestamp) * math.cos(timestamp)
            gtool.update(timestamp, np.array([x, y, z]))
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("Client stopped by user.")
    finally:
        gtool.close()
        print("Finished sending data.")


if __name__ == "__main__":
    main()
