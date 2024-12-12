import os


def remove_js(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = [line.replace('.js', '') for line in lines]

    with open(file_path, 'w') as file:
        file.writelines(modified_lines)


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.ts'):
                file_path = os.path.join(root, file)
                remove_js(file_path)
                print(f'Processed: {file_path}')


def remove_js_extension():
    directory_path = "ts"
    process_directory(directory_path)


if __name__ == "__main__":
    remove_js_extension()
