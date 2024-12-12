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


def generate_enum(fields):
    enum_code = "public enum StateTypes\n{\n"
    for name, _ in fields:
        enum_code += f"    {name.upper()},\n"
    enum_code = enum_code.rstrip(',\n') + "\n}\n"
    return enum_code


def gen_states_enum():

    schema_path = "definitions/R000_states.fbs"
    schema = read_schema(schema_path)
    fields = parse_schema(schema)
    enum_code = generate_enum(fields)

    with open("dotnet/states_enum.cs", "w") as f:
        f.write(enum_code)

    print("Helper enum generated successfully.")


if __name__ == "__main__":
    gen_states_enum()
