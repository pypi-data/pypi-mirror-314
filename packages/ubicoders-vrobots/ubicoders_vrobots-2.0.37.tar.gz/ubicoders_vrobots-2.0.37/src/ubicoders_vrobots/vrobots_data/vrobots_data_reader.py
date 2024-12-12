import numpy as np
import pandas as pd

class VRDataReader:
    def __init__(self, fName):
        # Load the CSV data into member variables
        self._load_data(fName)

    def _load_data(self, fName):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(fName)

        # Assign each Nx3 numpy array directly to member variables
        self.timestamp = df["ts"].values
        self.linPos = df[["linPos_x", "linPos_y", "linPos_z"]].values
        self.linVel = df[["linVel_x", "linVel_y", "linVel_z"]].values
        self.linAcc = df[["linAcc_x", "linAcc_y", "linAcc_z"]].values
        self.force = df[["force_x", "force_y", "force_z"]].values
        self.torque = df[["torque_x", "torque_y", "torque_z"]].values
        self.euler = df[["euler_x", "euler_y", "euler_z"]].values
        self.angVel = df[["angVel_x", "angVel_y", "angVel_z"]].values
        self.accelerometer = df[["accelerometer_x", "accelerometer_y", "accelerometer_z"]].values
        self.gyroscope = df[["gyroscope_x", "gyroscope_y", "gyroscope_z"]].values
        self.magnetometer = df[["magnetometer_x", "magnetometer_y", "magnetometer_z"]].values

# Usage example
if __name__ == "__main__":
    reader = VRDataReader("test_1.csv")
    
    print("Accelerometer data:\n", reader.accelerometer)  # Returns Nx3 numpy array for accelerometer data
