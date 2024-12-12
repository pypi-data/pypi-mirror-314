from abc import ABC, abstractmethod
from typing import List
import websocket
import _thread
import time
from ubicoders_vrobots.vrobots_msgs.fbpy_utils import serialize_commands
from ubicoders_vrobots.vrobots_msgs.python.VROBOTS_CMDS import VROBOTS_CMDS
from ubicoders_vrobots.vrobots_msgs.python.C000_commands_generated import (
    CommandMsgT,
    Vec3MsgT,
)
from ubicoders_vrobots.vrobots_msgs.python.R000_states_generated import (
    StatesMsg,
    StatesMsgT,
)
from ubicoders_vrobots.vrobots_msgs.python.states_msg_helper import VRobotState


class VirtualRobotBase0(ABC):
    def __init__(self) -> None:
        # command message
        self.cmdMsgT: CommandMsgT = CommandMsgT()
        self.cmdMsgT.name = "python"
        # states message
        self.statesMsgT = StatesMsgT()
        # states object
        self.states = VRobotState(None)

    def unpack(self, message):
        # if not states message, return
        if StatesMsg.StatesMsgBufferHasIdentifier(message, 0) is False:
            return
        # parse states message
        self.statesMsgT = StatesMsgT.InitFromPackedBuf(message, 0)
        # update states object
        self.states = VRobotState(self.statesMsgT)

    def pack(self) -> list:
        # update timestamp
        self.cmdMsgT.timestamp = time.time() * 1000
        # serialize command message
        cmd_msg = serialize_commands(self.cmdMsgT)
        return [cmd_msg]

    def pack_str(self) -> list:
        # for debugging
        return []

    def setup(self) -> list:
        # serialize reset command message
        return []

    @abstractmethod
    def loop(self):
        pass


class VirtualRobotBase1(VirtualRobotBase0):
    def __init__(self) -> None:
        super().__init__()

    def update_cmd_set_force_torque_body(
        self,
        sysId: int,
        fx: float,
        fy: float,
        fz: float,
        tx: float,
        ty: float,
        tz: float,
    ):
        force_vec3 = Vec3MsgT()
        torque_vec3 = Vec3MsgT()
        force_vec3.x = fx
        force_vec3.y = fy
        force_vec3.z = fz
        torque_vec3.x = tx
        torque_vec3.y = ty
        torque_vec3.z = tz

        self.cmdMsgT.cmdId = VROBOTS_CMDS.SET_BODY_FT
        self.cmdMsgT.sysId = sysId
        self.cmdMsgT.vec3Arr = [
            force_vec3,
            torque_vec3,
        ]

    def update_cmd_msd(self, sysId: int, pos: float):
        self.cmdMsgT.sysId = sysId
        self.cmdMsgT.cmdId = VROBOTS_CMDS.SET_MSD
        self.cmdMsgT.floatVal = float(pos)

    # m, m/s, rad, rad/s
    def update_cmd_invpen(
        self, sysId: int, pos: float, vel: float, ang: float, angvel: float
    ):
        self.cmdMsgT.sysId = sysId
        self.cmdMsgT.cmdId = VROBOTS_CMDS.SET_INVPEN
        self.cmdMsgT.floatArr = [float(pos), float(vel), float(ang), float(angvel)]

    def update_cmd_heli(self, sysId: int, force: float):
        self.cmdMsgT.sysId = sysId
        self.cmdMsgT.cmdId = VROBOTS_CMDS.SET_HELI
        self.cmdMsgT.floatVal = force

    def update_cmd_multirotor(self, sysId: int, pwm: List[int]):
        self.cmdMsgT.cmdId = VROBOTS_CMDS.SET_PWM
        self.cmdMsgT.sysId = sysId
        self.cmdMsgT.intArr = [int(pwm[i]) for i in range(4)]

    def update_cmd_omrover(self, sysId: int, actuators: List[float]):
        self.cmdMsgT.sysId = sysId
        self.cmdMsgT.cmdId = VROBOTS_CMDS.SET_OMROVER
        self.cmdMsgT.floatArr = actuators
        # print(f"After update: cmd id: {self.cmdMsgT.id}, actuators: {actuators}")

    def update_cmd_car(self, sysId: int, torque, brake, steer):
        self.cmdMsgT.sysId = sysId
        self.cmdMsgT.cmdId = VROBOTS_CMDS.SET_CAR
        self.cmdMsgT.floatArr = [torque, brake, steer]

    def update_cmd_imu(
        self,
        sysId: int,
    ):
        pass

    @abstractmethod
    def loop(self):
        pass


class MyVariables:
    def __init__(self) -> None:
        self.my_var = 0


class VirtualRobot(VirtualRobotBase1):
    def __init__(self) -> None:
        super().__init__()
        self.myvars = MyVariables()

    def loop(self):
        pass


class WebsocketClient:
    def __init__(
        self, robot: VirtualRobot, duration: float = 5.0, freq: float = 50
    ) -> None:
        self.robot = robot
        self.duration = duration
        self.dt = 1.0 / freq
        self.start_time = time.time()

        def on_message(ws, message):
            self.robot.unpack(message)

        def on_error(ws, error):
            print(f"error: {error}")

        def on_close(ws, close_status_code, close_msg):
            print("### closed ###")

        def on_open(ws):
            print("Opened connection")

            # send setup message
            setup_msg_list = self.robot.setup()
            if setup_msg_list is not None:
                [ws.send(byte_msg, opcode=0x2) for byte_msg in setup_msg_list]

            def _update_loop(*args):
                while True:
                    if self.check_stop_cond():
                        break
                    self.robot.loop()
                    byte_msg_list = self.robot.pack()
                    str_msg_list = self.robot.pack_str()
                    if byte_msg_list is not None:
                        [ws.send(byte_msg, opcode=0x2) for byte_msg in byte_msg_list]
                    if str_msg_list is not None:
                        [ws.send(str_msg) for str_msg in str_msg_list]
                    time.sleep(self.dt)  # 50 hz
                ws.close()
                print("Simulation done. Closing connection. Ctrl+C to exit.")

            _thread.start_new_thread(_update_loop, ())

        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            "ws://localhost:12740",
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
            on_message=on_message,
        )

    def check_stop_cond(self):
        dt = time.time() - self.start_time
        if dt > self.duration:
            return True
        return False

    def start(self):
        self.ws.run_forever()
        # rel.signal(2, rel.abort)  # Keyboard Interrupt
        # rel.dispatch()


class MyVRobotController:
    def __init__(self, vr: VirtualRobot = None):
        self.vr = vr

    def loop(self):
        states = self.vr.states
        print(f"states: {states}")
        # vr.update_cmd_omrover([0.0, 0.0, 10.0, 20.0])
        self.vr.update_cmd_multirotor([1600, 1600, 1600, 1600])
        # vr.update_cmd_car(3000, 0, 0)


def vr_client_main(my_controller: MyVRobotController, duration=60):
    vr = VirtualRobot()
    my_controller.vr = vr
    vr.loop = lambda: my_controller.loop()
    client = WebsocketClient(vr, duration=duration)
    client.start()


if __name__ == "__main__":
    vr_client_main(MyVRobotController())
