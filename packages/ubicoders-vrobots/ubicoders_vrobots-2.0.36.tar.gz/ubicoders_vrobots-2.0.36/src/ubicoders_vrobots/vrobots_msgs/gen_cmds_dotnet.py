from VROBOTS_CMDS import VROBOTS_CMDS


def generate_cmds_dotnet():
    cmds = {attr: value for attr, value in VROBOTS_CMDS.__dict__.items(
    ) if not attr.startswith("__") and not callable(getattr(VROBOTS_CMDS, attr))}

    enum_definitions = "\n    ".join(
        [f'{key} = {value},' for key, value in cmds.items()])

    dotnet_script = f"""public enum VROBOTS_CMDS
{{
    {enum_definitions}
}}
"""

    with open(r".\dotnet\VROBOTS_CMDS.cs", "w") as f:
        f.write(dotnet_script)


if __name__ == "__main__":
    generate_cmds_dotnet()
