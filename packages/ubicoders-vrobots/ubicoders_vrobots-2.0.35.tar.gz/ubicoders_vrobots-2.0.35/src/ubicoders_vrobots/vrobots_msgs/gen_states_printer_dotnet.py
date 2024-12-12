def read_schema(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def parse_schema(schema):
    lines = schema.split('\n')
    fields = []
    for line in lines:
        line = line.strip()
        if ':' in line:
            name, field_type = line.split(':')
            name = name.strip()
            field_type = field_type.strip().rstrip(';')
            fields.append((name, field_type))
    return fields


def generate_unity_script(fields):
    body = ""
    for name, field_type in fields:
        if field_type == 'Vec3Msg':
            body += f"            if (_stateType == StateTypes.{name.upper()}) PrintVec3Msg(_states.{name.capitalize()});\n"
        elif field_type == 'Vec4Msg':
            body += f"            if (_stateType == StateTypes.{name.upper()}) PrintVec4Msg(_states.{name.capitalize()});\n"
        elif field_type == 'float' or field_type == 'double':
            body += f"            if (_stateType == StateTypes.{name.upper()}) Debug.Log(\"{name.capitalize()}: \" + _states.{name.capitalize()});\n"
        elif field_type == 'uint32':
            body += f"            if (_stateType == StateTypes.{name.upper()}) Debug.Log(\"{name.capitalize()}: \" + _states.{name.capitalize()});\n"
        elif field_type == 'string':
            body += f"            if (_stateType == StateTypes.{name.upper()}) Debug.Log(\"{name.capitalize()}: \" + _states.{name.capitalize()});\n"
        # Add other field types as needed

    return body


def generate_state_console_print_helper():
    schema_path = "definitions/R000_states.fbs"
    schema = read_schema(schema_path)
    fields = parse_schema(schema)
    unity_script = generate_unity_script(fields)

    with open("dotnet/StatePrinterHelp.txt", "w") as f:
        f.write(unity_script)

    print("Unity script generated successfully.")


if __name__ == "__main__":
    generate_state_console_print_helper()
