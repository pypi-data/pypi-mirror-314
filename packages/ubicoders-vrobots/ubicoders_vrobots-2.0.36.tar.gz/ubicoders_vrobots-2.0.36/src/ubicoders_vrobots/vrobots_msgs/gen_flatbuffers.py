import subprocess
import json


def get_args_base():
    return [
        # '--gen-onefile',
        "--cs-gen-json-serializer",
        "--gen-object-api",
        "--gen-all",
    ]


def get_args_dot_net(fname):
    args = get_args_base()
    args.extend(["-n", "-o", rf".\dotnet", rf".\definitions\{fname}.fbs"])
    return args


def get_args_python(fname):
    args = get_args_base()
    args.append("--gen-onefile")
    args.extend(["--python", "-o", rf".\python",
                rf".\definitions\{fname}.fbs"])
    return args


def get_args_typescript(fname):
    args = get_args_base()
    args.append("--gen-onefile")
    args.extend(
        ["--ts", "-o", rf".\ts\{fname}", rf".\definitions\{fname}.fbs"])
    return args


def get_cmds_map():
    with open(r"./definitions/cmds.json") as f:
        return json.load(f)


# assumes window.
def generate_msg(fname):
    command = r".\flatc.exe"

    print(f"Generating {fname} dotnet")
    args = get_args_dot_net(fname)
    subprocess.run([command] + args)

    print(f"Generating {fname} python")
    args = get_args_python(fname)
    subprocess.run([command] + args)

    print(f"Generating {fname} typescript")
    args = get_args_typescript(fname)
    subprocess.run([command] + args)


# for *.fbs in definitions, generate message.
def compile_fb():
    import os

    # # clear the folders
    # for folder in ["dotnet", "python", "ts"]:
    #     for file in os.listdir(f"./{folder}"):
    #         os.remove(f"./{folder}/{file}")

    for file in os.listdir(r"./definitions"):
        if "vectors" in file:
            continue

        if file.endswith(".fbs"):
            fname = file[:-4]
            generate_msg(fname)


if __name__ == "__main__":
    compile_fb()
