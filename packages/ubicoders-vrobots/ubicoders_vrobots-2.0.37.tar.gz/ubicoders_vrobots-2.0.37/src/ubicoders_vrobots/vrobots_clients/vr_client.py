from ubicoders_vrobots.vrobots_clients.vr_client_utils import (
    VirtualRobot,
    vr_client_main,
)
from ubicoders_vrobots.vrobots_msgs.python.states_msg_helper import VRobotState
import cv2
import numpy as np
import time


# Process the image data with OpenCV
def process_image(left_data, right_data):
    if left_data is None or len(left_data) == 0:
        return
    if right_data is None or len(right_data) == 0:
        return

    # Decode the image data (assuming it is JPEG encoded)
    # image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    left_image = cv2.imdecode(np.frombuffer(left_data, np.uint8), cv2.IMREAD_COLOR)
    right_image = cv2.imdecode(np.frombuffer(right_data, np.uint8), cv2.IMREAD_COLOR)

    image = np.hstack((left_image, right_image))

    if image is None:
        raise ValueError("Failed to decode image")

    window_name = "Received Image"
    # cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    # Display the image
    cv2.imshow(window_name, image)
    cv2.waitKey(1)


class MyVRobotsController:
    def __init__(self, vr: VirtualRobot = None):
        self.err_int_vel = 0
        self.vr = vr

    def vel_err_int(self, vel_err):
        self.err_int_vel += vel_err
        if self.err_int_vel > 100:
            self.err_int_vel = 100
        elif self.err_int_vel < -100:
            self.err_int_vel = -100
        return self.err_int_vel

    def vel_ctrl(self, sp_vel, vel):
        error = sp_vel - vel
        throttle = error * 10 + 1200 + self.vel_err_int(error) * 3
        return throttle

    def loop(self):
        states: VRobotState = self.vr.states
        print(f"states: {states}")
        # print(f"system id: {states.sysId}")
        # print(f" time: {states.timestamp}")
        # print(f"imagedata: {states.imageData0}")

        # network_delay = time.time() * 1000 - states.timestamp
        # print(f"timestamp: {states.timestamp}")
        # print(f"network delay: {network_delay/1000} sec")

        # left_img = states.imageData0
        # right_img = states.imageData1
        # process_image(left_img, right_img)

        # altitude = -states.linPos.z
        # sp_alt = 20

        # error = sp_alt - altitude
        # sp_vel = error * 1 + states.linVel.z * 4

        # # print(f"sp_vel: {sp_vel}, vel: {states.linVel.z}")

        # throttle = self.vel_ctrl(sp_vel, states.linVel.z)

        # # vr.update_cmd_omrover([0.0, 0.0, 10.0, 20.0])
        # # self.vr.update_cmd_multirotor(2, [throttle, throttle, throttle, throttle])
        # # vr.update_cmd_car(3000, 0, 0)
        # self.vr.update_cmd_set_force_torque_body(0, 0, 0, -(10 * 2) * 9.82, 0, 0, 0.0)


if __name__ == "__main__":
    vr_client_main(MyVRobotsController(), duration=60)
