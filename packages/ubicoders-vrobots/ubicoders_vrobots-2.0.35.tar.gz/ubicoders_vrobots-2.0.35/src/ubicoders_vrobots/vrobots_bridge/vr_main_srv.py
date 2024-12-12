import asyncio
import socket
import requests
from websocket import create_connection
from .vr_rest_srv import run_rest_server
from .vr_ws_srv import run_ws_server


def is_port_in_use(port):
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("localhost", port)) == 0


def ping_rest_server(port):
    """Send a curl-like request to localhost:<port>."""
    try:
        response = requests.get(f"http://localhost:{port}/ping")
        result = response.json()
        # print(f"Response from localhost:{port}:\n{result}")
        if result["status"] == 1:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        # print(f"Failed to connect to localhost:{port}:\n{e}")
        return False


def ping_ws_server(port):
    """Check if a WebSocket server is running on localhost:<port> and interact with it."""
    try:
        ws_url = f"ws://localhost:{port}"
        ws = create_connection(ws_url)
        ws.settimeout(3)
        message = "ping"
        ws.send(message)
        # print("sent ping msg. waiting for response...")
        result = ws.recv()
        ws.close()
        if result == "pong" or result == b"pong":
            return True
        else:
            return False
    except Exception as e:
        # print(f"Failed to connect to WebSocket server at ws://localhost:{port}:\n{e}")
        return False


async def run_servers():
    servers_2_run = []
    is_alive = ping_rest_server(12741)
    if not is_alive:
        servers_2_run.append(asyncio.create_task(run_rest_server(12741)))
    else:
        print(f"REST server is already running at 12741.")
    is_alive = ping_ws_server(12740)
    if not is_alive:
        servers_2_run.append(asyncio.create_task(run_ws_server(12740)))
    else:
        print("WebSocket server is already running at 12740.")

    if len(servers_2_run) > 0:
        await asyncio.gather(*servers_2_run)

    print("All servers are running.")


def main():
    try:
        asyncio.run(run_servers())
    except KeyboardInterrupt:
        print("Servers stopped by user.")


if __name__ == "__main__":
    main()
