import asyncio
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import sys
from collections import deque
from .graph_udp_server import UDPServerProtocol
from .data_viz_pyqt import DataVizPyQt


class Worker(QtCore.QThread):
    new_data = QtCore.pyqtSignal()

    def __init__(self, data_deque, port=12750):
        super().__init__()
        self.data_deque = data_deque
        self.port = port
        self.loop = asyncio.new_event_loop()  # Create a new event loop for this thread

    async def run_udp_server(self):
        print(f"\033[92mUDP server running on {self.port}\033[0m")
        await self.loop.create_datagram_endpoint(
            lambda: UDPServerProtocol(self.data_deque, self.port),
            local_addr=("0.0.0.0", self.port),
        )
        # Keep the loop running indefinitely
        while True:
            await asyncio.sleep(1)

    def run(self):
        asyncio.set_event_loop(self.loop)  # Set the event loop for this thread
        self.loop.run_until_complete(self.run_udp_server())  # Start the UDP server
        self.loop.run_forever()  # Keep the loop running


def graph_server_pyqt(data_length=1000, port=12750):
    app = QtWidgets.QApplication(sys.argv)
    data_deque = deque(maxlen=data_length)
    plotter = DataVizPyQt(data_deque)

    # Create and start the worker thread for UDP server
    worker = Worker(data_deque, port=port)
    worker.start()

    # Update plot at intervals to reflect incoming data
    timer = QtCore.QTimer()
    timer.timeout.connect(plotter.update)
    timer.start(50)  # Update every 50ms

    sys.exit(app.exec_())


if __name__ == "__main__":
    graph_server_pyqt()
