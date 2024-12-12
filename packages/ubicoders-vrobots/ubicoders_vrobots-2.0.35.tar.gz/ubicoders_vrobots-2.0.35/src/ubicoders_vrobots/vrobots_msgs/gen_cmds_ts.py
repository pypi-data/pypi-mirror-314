from VROBOTS_CMDS import VROBOTS_CMDS


def generate_cmds_typescript():
    cmds = {attr: value for attr, value in VROBOTS_CMDS.__dict__.items(
    ) if not attr.startswith("__") and not callable(getattr(VROBOTS_CMDS, attr))}

    enum_definitions = "\n    ".join(
        [f'{key} = {value},' for key, value in cmds.items()])

    typescript_script = f"""
    enum VROBOTS_CMDS {{
        {enum_definitions}
    }}

    export default VROBOTS_CMDS;
    """

    with open(r".\ts\VROBOTS_CMDS.ts", "w") as f:
        f.write(typescript_script)


if __name__ == "__main__":
    generate_cmds_typescript()
