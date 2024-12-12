import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import time
import threading, sys
import signal


class DataVizMatplotlib:
    def __init__(self, data_deque):
        self.data_deque = data_deque
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 6))

        # Initialize empty plots
        (self.line1,) = self.ax1.plot([], [], "r-", label="X Axis")
        (self.line2,) = self.ax2.plot([], [], "g-", label="Y Axis")
        (self.line3,) = self.ax3.plot([], [], "b-", label="Z Axis")

        # Set up plot titles and labels
        self.ax1.set_title("X Axis")
        self.ax2.set_title("Y Axis")
        self.ax3.set_title("Z Axis")

        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_xlabel("Time (s)")
            ax.legend(loc="upper right")

    def update_plot(self, frame):
        if len(self.data_deque) > 0:
            stacked_data = np.array(self.data_deque)
            times, x_data, y_data, z_data = (
                stacked_data[:, 0],
                stacked_data[:, 1],
                stacked_data[:, 2],
                stacked_data[:, 3],
            )
            # Update plot data
            self.line1.set_data(times, x_data)
            self.line2.set_data(times, y_data)
            self.line3.set_data(times, z_data)

            # Dynamically adjust x-axis and y-axis limits based on data
            min_time, max_time = times.min(), times.max()
            min_x, max_x = x_data.min(), x_data.max()
            min_y, max_y = y_data.min(), y_data.max()
            min_z, max_z = z_data.min(), z_data.max()

            self.ax1.set_xlim(min_time, max_time)
            self.ax1.set_ylim(min_x - 0.5, max_x + 0.5)
            self.ax2.set_xlim(min_time, max_time)
            self.ax2.set_ylim(min_y - 0.5, max_y + 0.5)
            self.ax3.set_xlim(min_time, max_time)
            self.ax3.set_ylim(min_z - 0.5, max_z + 0.5)

        return self.line1, self.line2, self.line3

    def start_animation(self, interval=50):
        self.anim = FuncAnimation(
            self.fig, self.update_plot, interval=interval, cache_frame_data=False
        )
        plt.show()


class DataGenerator(threading.Thread):
    def __init__(self, data_deque, update_rate=10):
        super().__init__()
        self.data_deque = data_deque
        self.update_rate = update_rate
        self.data_array = np.random.randn(10000, 3)  # Generate a large Nx3 array
        self.index = 0
        self.stop_event = threading.Event()  # Stop event for clean exit

    def run(self):
        base_time = time.time()
        while self.index < len(self.data_array) and not self.stop_event.is_set():
            current_data = np.array(
                [
                    time.time() - base_time,
                    *self.data_array[self.index],
                ]
            )
            self.data_deque.append(current_data)
            self.index += 1
            time.sleep(1 / self.update_rate)

    def stop(self):
        self.stop_event.set()  # Set the stop event


def main():
    data_deque = deque(maxlen=50 * 5)
    plotter = DataVizMatplotlib(data_deque)

    # Start data generation in a separate thread
    data_gen = DataGenerator(data_deque, update_rate=50)
    data_gen.start()

    # Handle Ctrl+C for a clean exit
    def signal_handler(sig, frame):
        print("Exiting...")
        data_gen.stop()  # Signal the thread to stop
        plt.close("all")  # Close the matplotlib plots
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Start the animation
    plotter.start_animation(interval=50)


if __name__ == "__main__":
    main()
