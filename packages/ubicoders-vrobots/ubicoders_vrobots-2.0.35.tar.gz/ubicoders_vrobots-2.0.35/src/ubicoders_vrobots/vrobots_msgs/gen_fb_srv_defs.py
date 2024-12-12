
SrvBaseFields = [
    {
        "name": "timestamp",
        "type": "double",
    },
    {
        "name": "name",
        "type": "string",
    },
    {
        "name": "sys_id",
        "type": "uint32",
    },
    {
        "name": "req_src_id",
        "type": "uint32",
    },

]

SrvGPramsMsg = {
    "name": "GlobalParamsMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "scene",
            "type": "string",
        },
        {
            "name": "cmd_report_once",
            "type": "int",
        },
        {
            "name": "is_signed",
            "type": "int",
        },
        {
            "name": "input_breaker",
            "type": "int",
        },
        {
            "name": "player_mode",
            "type": "int",
        },
        {
            "name": "set_scene",
            "type": "string",
        },
        {
            "name": "set_signiture",
            "type": "string",
        },
        {
            "name": "set_input_breaker",
            "type": "int",
        },
        {
            "name": "set_player_mode",
            "type": "int",
        }



    ]
}

SrvWSParamsMsg = {
    "name": "WSParamsMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "cmd_report_once",
            "type": "int",
        },
        {
            "name": "cmd_connect",
            "type": "int",
        },
        {
            "name": "cmd_disconnect",
            "type": "int",
        },
        {
            "name": "is_connected",
            "type": "bool",
        },
        {
            "name": "current_url",
            "type": "string",
        },
        {
            "name": "prod_url",
            "type": "string",
        },
        {
            "name": "prod_port",
            "type": "string",
        },
        {
            "name": "dev_url",
            "type": "string",
        },
        {
            "name": "dev_port",
            "type": "string",
        },
        {
            "name": "set_prod_url",
            "type": "string",
        },
        {
            "name": "set_prod_port",
            "type": "string",
        },
        {
            "name": "set_dev_url",
            "type": "string",
        },
        {
            "name": "set_dev_port",
            "type": "string",
        }
    ]
}

SrvSimParamsMsg = {
    "name": "SimParamsMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "cmd_report_once",
            "type": "int",
        },
        {
            "name": "stream_to_rjs",
            "type": "int",
        },
        {
            "name": "stream_to_ws",
            "type": "int",
        },
        {
            "name": "noise_on",
            "type": "int",
        },
        {
            "name": "set_stream_to_rjs",
            "type": "int",
        },
        {
            "name": "set_stream_to_ws",
            "type": "int",
        },
        {
            "name": "set_noise_on",
            "type": "int",
        }
    ]
}

SrvOMRWall = {
    "name": "OMRWallMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "clear_wall",
            "type": "bool",
        },
        {
            "name": "set_wall",
            "type": "bool",
        },
        {
            "name": "vec3_list",
            "type": "[Vec3Msg]",
        },
    ]
}

SrvDrone1dPID = {
    "name": "Drone1DPIDMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "set_pid_on",
            "type": "bool",
        },
        {
            "name": "set_kp",
            "type": "bool",
        },
        {
            "name": "set_ki",
            "type": "bool",
        },
        {
            "name": "set_kd",
            "type": "bool",
        },
        {
            "name": "set_setpoint",
            "type": "bool",
        },
        {
            "name": "pid_on",
            "type": "bool",
        },
        {
            "name": "kp",
            "type": "float",
        },
        {
            "name": "ki",
            "type": "float",
        },
        {
            "name": "kd",
            "type": "float",
        },
        {
            "name": "setpoint",
            "type": "float",
        },

        # physical properties
        {
            "name": "set_left_arm_length",
            "type": "bool",
        },
        {
            "name": "left_arm_length",
            "type": "float",
        },
        {
            "name": "set_right_arm_length",
            "type": "bool",
        },
        {
            "name": "right_arm_length",
            "type": "float",
        },
        {
            "name": "set_uint_mass",
            "type": "bool",
        },
        {
            "name": "uint_mass",
            "type": "float",
        }


    ]
}

SrvIMUReplay = {
    "name": "IMUReplayMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "set_replay",
            "type": "bool",
        },
        {
            "name": "timestamp_gt",
            "type": "[float]",
        },
        {
            "name": "euler_est",
            "type": "[Vec3Msg]",
        },
        {
            "name": "euler_gt",
            "type": "[Vec3Msg]",
        },
    ]

}

SrvResetAll = {
    "name": "ResetAllMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "reset_all",
            "type": "bool",
        },
    ]
}

SrvVRobotPhysicalProperty = {
    "name": "VRobotPhysicalPropertyMsg",
    "fields": [
        *SrvBaseFields,
        {
            "name": "set_mass",
            "type": "bool",
        },
        {
            "name": "mass",
            "type": "float",
        },
        {
            "name": "set_moi3x1",
            "type": "bool",
        },
        {
            "name": "moi3x1",
            "type": "Vec3Msg"
        }
    ]
}


def generate_table(name, fields):
    table_definition = f"table {name} {{\n"
    for field in fields:
        field_name = field["name"]
        field_type = field["type"]
        table_definition += f"    {field_name}:{field_type};\n"
    table_definition += "}\n"
    return table_definition


def get_service_list():
    return [
        SrvResetAll,
        SrvGPramsMsg,
        SrvWSParamsMsg,
        SrvSimParamsMsg,
        SrvOMRWall,
        SrvDrone1dPID,
        SrvIMUReplay,
        SrvVRobotPhysicalProperty
    ]


def pad_fid(fid):
    return f"{fid:03}"


def generate_fb_definitions():
    srv_list = get_service_list()
    # TODO implement

    fb_header = "include \"vectors.fbs\";\n\n"
    fid = 0
    for srv in srv_list:
        fb_definitions = fb_header
        srv_name = srv["name"]
        srv_fields = srv["fields"]
        fb_definitions += generate_table(f"Srv{srv_name}", srv_fields)
        fb_definitions += f"root_type Srv{srv_name};\n"
        fb_definitions += f"file_identifier \"S{pad_fid(fid)}\";\n\n"

        with open(f"definitions/S{pad_fid(fid)}_srv_{srv_name.lower()}.fbs", "w") as fb_file:
            fb_file.write(fb_definitions)

        fid += 1


if __name__ == "__main__":
    generate_fb_definitions()
