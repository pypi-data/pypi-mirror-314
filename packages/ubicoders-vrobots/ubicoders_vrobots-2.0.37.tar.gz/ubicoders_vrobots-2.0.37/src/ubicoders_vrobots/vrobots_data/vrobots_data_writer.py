import os

class VRDataWriter:
    def __init__(self, fName):
        # Ensure the directory exists
        self._create_folder_if_not_exists(fName)
        
        # Get a unique filename in case the file already exists
        self.fName = self._get_unique_filename(fName)
        self.file = open(self.fName, "w")
        self.file.write("ts,linPos_x,linPos_y,linPos_z,linVel_x,linVel_y,linVel_z,linAcc_x,linAcc_y,linAcc_z,force_x,force_y,force_z,torque_x,torque_y,torque_z,euler_x,euler_y,euler_z,angVel_x,angVel_y,angVel_z,accelerometer_x,accelerometer_y,accelerometer_z,gyroscope_x,gyroscope_y,gyroscope_z,magnetometer_x,magnetometer_y,magnetometer_z\n")
        
    def _create_folder_if_not_exists(self, fName):
        folder_path = os.path.dirname(fName)
        if folder_path and not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def _get_unique_filename(self, fName):
        base_name, ext = os.path.splitext(fName)
        index = 1
        new_name = fName
        
        # Check if the file already exists and keep incrementing index until we find a unique name
        while os.path.exists(new_name):
            new_name = f"{base_name}_{index}{ext}"
            index += 1
            
        return new_name

    def record(self, states):
        ts = states.timestamp
        if (ts < 1):
            return
        # Initialize the "data" dictionary if it does not exist in this current path
        self.file.write(f"{states.timestamp},{states.linPos.x},{states.linPos.y},{states.linPos.z},{states.linVel.x},{states.linVel.y},{states.linVel.z},{states.linAcc.x},{states.linAcc.y},{states.linAcc.z},{states.force.x},{states.force.y},{states.force.z},{states.torque.x},{states.torque.y},{states.torque.z},{states.euler.x},{states.euler.y},{states.euler.z},{states.angVel.x},{states.angVel.y},{states.angVel.z},{states.accelerometer.x},{states.accelerometer.y},{states.accelerometer.z},{states.gyroscope.x},{states.gyroscope.y},{states.gyroscope.z},{states.magnetometer.x},{states.magnetometer.y},{states.magnetometer.z}\n")
        

    def close(self):
        self.file.close()


if __name__ == "__main__":
    ds = VRDataWriter("test.csv")
    ds.close()
    print("Done")
