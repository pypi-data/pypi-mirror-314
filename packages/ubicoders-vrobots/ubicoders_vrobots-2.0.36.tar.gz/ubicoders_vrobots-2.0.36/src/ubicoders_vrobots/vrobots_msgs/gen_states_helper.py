import json


def read_schema(file_path):
    with open(file_path, "r") as file:
        return file.read()


def parse_schema(schema):
    lines = schema.split("\n")
    fields = []
    for line in lines:
        line = line.strip()
        if ":" in line:
            name, field_type = line.split(":")
            name = name.strip()
            field_type = field_type.strip().rstrip(";")
            fields.append((name, field_type))
    return fields


def convert_field_name(name):
    # Convert field names to follow the naming convention
    parts = name.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def generate_class(fields):
    class_template = """from .R000_states_generated import *
import json


class Vec4(Vec4MsgT):
    def __init__(self, instance: Vec4MsgT = None):
        super().__init__()
        if instance is None:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 0
        else:
            self.x = instance.x
            self.y = instance.y
            self.z = instance.z
            self.w = instance.w

    def get_dict_data(self):
        return {{
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "w": self.w,
        }}

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)


class Vec3(Vec3MsgT):
    def __init__(self, instance: Vec3MsgT = None):
        super().__init__()
        if instance is None:
            self.x = 0
            self.y = 0
            self.z = 0
        else:
            self.x = instance.x
            self.y = instance.y
            self.z = instance.z

    def get_dict_data(self):
        return {{
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }}

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)

class Collision(CollisionT):
    def __init__(self, instance: CollisionT = None):
        super().__init__()
        if instance is None:
            self.timestamp = 0.0
            self.collisionType = 0
            self.objectName = ""
            self.pos = Vec3()
            self.vel = Vec3()
            self.eul = Vec3()
            self.angvel = Vec3()
        else:
            self.timestamp = instance.timestamp
            self.collisionType = instance.collisionType
            self.objectName = instance.objectName.decode("utf-8")
            self.pos = Vec3(instance.pos)
            self.vel = Vec3(instance.vel)
            self.eul = Vec3(instance.eul)
            self.angvel = Vec3(instance.angvel)

    def get_dict_data(self):
        return {{
            "timestamp": self.timestamp,
            "collisionType": self.collisionType,
            "object_name": self.objectName,
            "pos": self.pos.get_dict_data(),
            "vel": self.vel.get_dict_data(),
            "eul": self.eul.get_dict_data(),
            "angvel": self.angvel.get_dict_data(),
        }}

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)        
        

class VRobotState(StatesMsgT):
    def __init__(self, instance: StatesMsgT = None) -> None:
        if instance is None:
{init_fields}
        else:
{else_fields}

    def get_dict_data(self):
        return {{
{dict_data_fields}
        }}

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)
"""

    init_fields = ""
    else_fields = ""
    dict_data_fields = ""

    for name, field_type in fields:
        field_name = convert_field_name(name)
        if field_type == "string":
            init_fields += f'            self.{field_name} = ""\n'
            else_fields += f'            self.{field_name} = instance.{field_name}.decode("utf-8")\n'
            dict_data_fields += f'            "{name}": self.{field_name},\n'
        elif field_type in ["int", "uint", "uint16", "uint32", "long"]:
            init_fields += f"            self.{field_name} = 0\n"
            else_fields += f"            self.{field_name} = instance.{field_name}\n"
            dict_data_fields += f'            "{name}": self.{field_name},\n'
        elif field_type in ["double", "float"]:
            init_fields += f"            self.{field_name} = 0.0\n"
            else_fields += f"            self.{field_name} = instance.{field_name}\n"
            dict_data_fields += f'            "{name}": self.{field_name},\n'
        elif field_type == "Vec3Msg":
            init_fields += f"            self.{field_name} = Vec3()\n"
            else_fields += (
                f"            self.{field_name} = Vec3(instance.{field_name})\n"
            )
            dict_data_fields += (
                f'            "{name}": self.{field_name}.get_dict_data(),\n'
            )
        elif field_type == "Vec4Msg":
            init_fields += f"            self.{field_name} = Vec4()\n"
            else_fields += (
                f"            self.{field_name} = Vec4(instance.{field_name})\n"
            )
            dict_data_fields += (
                f'            "{name}": self.{field_name}.get_dict_data(),\n'
            )
        elif field_type.startswith("["):
            init_fields += f"            self.{field_name} = []\n"

            if field_name == "collisions":
                dict_data_fields += f'            "{name}": [i.get_dict_data() for i in self.{field_name}] if self.{field_name} is not None else [],\n'
                else_fields += f"            self.{field_name} = [Collision(c) for c in instance.{field_name}]\n"
            elif field_name == "pwm":
                dict_data_fields += f'            "{name}": [int(i) for i in self.{field_name}] if self.{field_name} is not None else [],\n'
                else_fields += (
                    f"            self.{field_name} = instance.{field_name}\n"
                )
            else:
                dict_data_fields += f'            "{name}": [i for i in self.{field_name}] if self.{field_name} is not None else [],\n'
                else_fields += (
                    f"            self.{field_name} = instance.{field_name}\n"
                )
        # elif field_type == "[Collision":
        #     init_fields += f"            self.{field_name} = Collision()\n"
        #     else_fields += f"            self.{field_name} = [Collision(c) for c in instance.{field_name}]\n"
        #     dict_data_fields += f'            "{name}": [c.get_dict_data() for c in self.{field_name}],\n'

    class_code = class_template.format(
        init_fields=init_fields,
        else_fields=else_fields,
        dict_data_fields=dict_data_fields,
    )

    return class_code


def gen_states_helper():
    schema_path = "definitions/R000_states.fbs"
    schema = read_schema(schema_path)
    fields = parse_schema(schema)
    class_code = generate_class(fields)

    with open("python/states_msg_helper.py", "w") as f:
        f.write(class_code)

    print("Helper classes generated successfully.")


if __name__ == "__main__":
    gen_states_helper()
