import asyncio
import threading
from collections import deque
from ubicoders_vrobots.vrobots_graph_tools.data_viz_matplotlib import DataVizMatplotlib
from .graph_udp_server import start_udp_server
import signal
import sys


def run_udp_server(data_deque, stop_event, port=12750):
    async def run_udp_server_async():
        await start_udp_server(data_deque, port=port)
        while not stop_event.is_set():
            await asyncio.sleep(1)

    asyncio.run(run_udp_server_async())


async def graph_server_matplotlib_core(port=12750, data_length=1000):
    data_deque = deque(maxlen=data_length)
    plotter = DataVizMatplotlib(data_deque)
    stop_event = threading.Event()

    # Start the UDP server in a separate thread with a stop event
    udp_thread = threading.Thread(
        target=run_udp_server, args=(data_deque, stop_event, port)
    )
    udp_thread.start()

    # Start the Matplotlib animation
    plotter.start_animation(interval=50)

    # Keep the coroutine running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        stop_event.set()  # Signal the UDP server thread to stop
        udp_thread.join()  # Wait for the UDP server thread to finish


def graph_server_matplotlib(port=12750, data_length=1000):
    try:
        asyncio.run(graph_server_matplotlib_core(port=port, data_length=data_length))
    except KeyboardInterrupt:
        print("Interrupted by user")


if __name__ == "__main__":
    graph_server_matplotlib()
