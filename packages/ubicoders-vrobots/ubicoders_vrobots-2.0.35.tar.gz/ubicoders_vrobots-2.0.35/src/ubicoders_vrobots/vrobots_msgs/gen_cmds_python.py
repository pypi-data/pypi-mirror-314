import shutil


def gen_cmds_python():
    # Define the source and destination file paths
    source_file = 'VROBOTS_CMDS.py'
    destination_file = "python/" + source_file
    shutil.copy(source_file, destination_file)


if __name__ == "__main__":
    gen_cmds_python()
