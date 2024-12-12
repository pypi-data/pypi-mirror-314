import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
import sys
from collections import deque
import time


class DataVizPyQt(QtCore.QObject):
    def __init__(self, data_deque):
        super().__init__()
        self.data_deque = data_deque

        # Create the main window
        self.win = pg.GraphicsLayoutWidget(
            show=True, title="Real-Time 3D Vector Components"
        )
        self.win.resize(720, 640)

        # Create plots in a single row
        self.plot1 = self.win.addPlot(
            title="X Axis",
            row=0,
            col=0,
        )
        self.curve1 = self.plot1.plot(pen="r")

        self.plot2 = self.win.addPlot(title="Y Axis", row=1, col=0)
        self.curve2 = self.plot2.plot(pen="g")

        self.plot3 = self.win.addPlot(title="Z Axis", row=2, col=0)
        self.curve3 = self.plot3.plot(pen="b")

    @QtCore.pyqtSlot()
    def update(self):
        # Check if there's data in the deque
        if len(self.data_deque) > 0:
            stacked_data = np.array(self.data_deque)
            times, x_data, y_data, z_data = (
                stacked_data[:, 0],
                stacked_data[:, 1],
                stacked_data[:, 2],
                stacked_data[:, 3],
            )
            # Update curves with deque data
            self.curve1.setData(times, x_data)
            self.curve2.setData(times, y_data)
            self.curve3.setData(times, z_data)


class Worker(QtCore.QThread):
    new_data = QtCore.pyqtSignal()

    def __init__(self, data_deque, update_rate=10):
        super().__init__()
        self.data_deque = data_deque
        self.update_rate = update_rate
        self.data_array = np.random.randn(10000, 3)  # Generate a large Nx3 array
        self.index = 0

    def run(self):
        base_time = time.time()
        while self.index < len(self.data_array):
            # Add new data to the deque
            current_data = np.array(
                [
                    time.time() - base_time,
                    *self.data_array[self.index],
                ]
            )
            self.data_deque.append(current_data)
            self.index += 1

            # Emit the signal to trigger plot update
            self.new_data.emit()

            # Sleep to maintain update rate
            QtCore.QThread.msleep(int(1000 / self.update_rate))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Create QApplication in main
    data_deque = deque(maxlen=250)
    plotter = DataVizPyQt(data_deque)

    # Create and start the worker thread
    worker = Worker(data_deque, update_rate=100)
    worker.new_data.connect(plotter.update)
    worker.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
