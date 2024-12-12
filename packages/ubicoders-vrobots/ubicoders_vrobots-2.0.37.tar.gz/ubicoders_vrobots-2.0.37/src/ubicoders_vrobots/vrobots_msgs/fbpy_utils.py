import flatbuffers
from ubicoders_vrobots.vrobots_msgs.python.C000_commands_generated import CommandMsg
from ubicoders_vrobots.vrobots_msgs.python.R000_states_generated import (
    StatesMsg,
    StatesMsgT,
    Vec3MsgT,
)


def Tobj2bytes(msgT, fid) -> bytearray:
    builder = flatbuffers.Builder(512)
    os = msgT.Pack(builder)
    builder.Finish(os, bytes(fid, "utf-8"))
    return builder.Output()


def serialize_states(statesMsgT) -> bytearray:
    return Tobj2bytes(statesMsgT, "VRST")


def serialize_commands(cmdMsgT) -> bytearray:
    return Tobj2bytes(cmdMsgT, "CMD0")


if __name__ == "__main__":
    statesMsgT = StatesMsgT()
    statesMsgT.name = "python"
    statesMsgT.timestamp = 0
    statesMsgT.lin_acc = Vec3MsgT()
    print(statesMsgT)
    bin_msg = serialize_states(statesMsgT)
    print(bin_msg)
    check = StatesMsg.StatesMsgBufferHasIdentifier(bin_msg, 0)
    print(check)
    check = CommandMsg.CommandMsgBufferHasIdentifier(bin_msg, 0)
    print(check)
