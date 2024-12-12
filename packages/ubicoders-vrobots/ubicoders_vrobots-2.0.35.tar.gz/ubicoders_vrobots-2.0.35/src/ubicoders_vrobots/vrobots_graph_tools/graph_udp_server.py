import asyncio
from collections import deque
import time
import numpy as np


def parse_message(message):
    """Parse incoming message to extract X, Y, Z values."""
    try:
        timestamp, x, y, z = message.split(",")
        return np.array([float(timestamp), float(x), float(y), float(z)])
    except:
        return np.array([0.0, 0.0, 0.0, 0.0])


class UDPServerProtocol:
    def __init__(self, data_queue, port=12750, timeout=1):
        self.clients = {}
        self.timeout = timeout
        self.data_queue = data_queue
        self.port = port
        self.base_time = time.time()

    def connection_made(self, transport):
        self.transport = transport
        # print("Server started and waiting for messages...")
        asyncio.create_task(self.check_inactive_clients())

    def error_received(self, exc):
        print(f"Error received: {exc}")

    def datagram_received(self, data, addr):
        message = data.decode()
        data_point = parse_message(message)
        if len(self.clients) < 1:
            self.data_queue.clear()
            self.base_time = data_point[0]  # Set base_time to the first timestamp
        if self.base_time < 1:
            self.base_time = data_point[0]
        # print(f"Base time: {self.base_time}")
        # Convert timestamp to relative time by subtracting base_time
        data_point[0] -= self.base_time
        self.clients[addr] = time.time()
        self.data_queue.append(data_point)

        # print(f"Message from {addr}: {message}")

    async def check_inactive_clients(self):
        while True:
            await asyncio.sleep(0.5)
            current_time = time.time()
            inactive_clients = [
                addr
                for addr, last_time in self.clients.items()
                if current_time - last_time > self.timeout
            ]
            for addr in inactive_clients:
                # print(f"Removing inactive client: {addr}")
                del self.clients[addr]


async def start_udp_server(data_handler, port=12750):
    loop = asyncio.get_running_loop()
    print(f"\033[92mUDP server running on {port}\033[0m")
    await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(data_handler, port), local_addr=("0.0.0.0", port)
    )


async def main():
    # Create a deque to handle incoming data
    data_queue = deque()

    # Start the UDP server on the specified port
    await start_udp_server(data_queue, port=12750)
    # Keep the server running indefinitely
    while True:
        await asyncio.sleep(3600)  # Sleep for an hour, or any long duration


# Run the main function in the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
