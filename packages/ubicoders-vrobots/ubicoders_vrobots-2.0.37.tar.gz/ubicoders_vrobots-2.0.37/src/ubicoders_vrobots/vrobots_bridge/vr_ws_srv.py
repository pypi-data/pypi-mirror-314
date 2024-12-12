import asyncio
import websockets
from ubicoders_vrobots.vrobots_msgs.python.EMPT_empty_generated import EmptyMsg

CONNECTIONS = set()


async def register(websocket):
    CONNECTIONS.add(websocket)
    # print("new connection")
    try:
        async for message in websocket:
            # print(f"message: {message}")
            if EmptyMsg.EmptyMsgBufferHasIdentifier(message, 0) is True:
                continue
            if message == b"ping" or message == "ping":
                await websocket.send(b"pong")
                continue
            # print(f"message: {message}")
            others = CONNECTIONS - {websocket}
            websockets.broadcast(others, message)

    except Exception as e:
        pass
    finally:
        pass


async def manage_connections():
    while True:
        connections = list(CONNECTIONS)
        for websocket in connections:
            try:
                await websocket.wait_closed()
            finally:
                # print("removing connection")
                CONNECTIONS.remove(websocket)
                # print(f"size of connections: {len(CONNECTIONS)}")
        await asyncio.sleep(1)


async def run_ws_server(port=12740):
    async with websockets.serve(register, "localhost", port):
        print(f"\033[92mVirtual Robots Bridge is running @ port {port}\033[0m")
        try:
            await manage_connections()
        except Exception as e:
            pass
        # await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(run_ws_server())
    except KeyboardInterrupt:
        print("Server stopped by user.")
