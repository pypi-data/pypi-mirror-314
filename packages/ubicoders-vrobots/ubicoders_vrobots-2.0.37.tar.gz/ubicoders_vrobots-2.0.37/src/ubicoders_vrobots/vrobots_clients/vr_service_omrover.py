from websocket import create_connection
import time
from ubicoders_vrobots.vrobots_clients.vr_service_utils import ws_req_service
from ubicoders_vrobots.vrobots_msgs.fbpy_utils import Tobj2bytes
from ubicoders_vrobots.vrobots_msgs.python.FILE_ID_LIST import FIDS
from ubicoders_vrobots.vrobots_msgs.python.S004_srv_omrwallmsg_generated import (
    SrvOMRWall,
    SrvOMRWallT,
)


def omrover_download_map():
    # prepare msg to download map
    srv_omr_wall = SrvOMRWallT()
    srv_omr_wall.timestamp = time.time() * 1000.0
    srv_omr_wall.name = "python"
    srv_omr_wall.id = 0
    srv_omr_wall.reqSrcId = 2
    # serialize
    req_msg = Tobj2bytes(srv_omr_wall, FIDS.srv_S010_omr_walls)
    # send and receive
    rec_msg = ws_req_service(req_msg, SrvOMRWall.SrvOMRWallBufferHasIdentifier)
    if (rec_msg is None) or (len(rec_msg) == 0):
        return

    # deserialize
    objdata = SrvOMRWallT.InitFromPackedBuf(rec_msg, 0)
    name = objdata.name.decode("utf-8")
    omrover_map = objdata.vec3List
    print(f"Received {name}")
    for i, vec3 in enumerate(omrover_map):
        print(f"vec3[{i}]: {vec3.x}, {vec3.y}, {vec3.z}")


if __name__ == "__main__":
    omrover_download_map()
