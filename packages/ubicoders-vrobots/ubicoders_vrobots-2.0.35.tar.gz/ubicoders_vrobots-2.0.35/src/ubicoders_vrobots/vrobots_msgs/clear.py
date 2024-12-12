import os
import shutil

# Define the directories to target
target_dirs = ["ts", "python", "dotnet"]


def delete_files_in_directories(base_path):
    for dirpath, dirnames, filenames in os.walk(base_path):
        for dirname in dirnames:
            if dirname in target_dirs:
                dir_to_clean = os.path.join(dirpath, dirname)
                print(f"Cleaning directory: {dir_to_clean}")
                for filename in os.listdir(dir_to_clean):
                    file_path = os.path.join(dir_to_clean, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                            print(f"Deleted file: {file_path}")
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            print(f"Deleted directory: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")


def clear_all():
    base_path = os.getcwd()  # Change this to the root directory you want to start from
    delete_files_in_directories(base_path)


if __name__ == "__main__":
    clear_all()
