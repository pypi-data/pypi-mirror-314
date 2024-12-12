import os
import re


def find_file_identifiers(directory):
    file_identifiers = {}
    identifier_pattern = re.compile(r'file_identifier\s+"(\w+)"')

    for filename in os.listdir(directory):
        if filename.endswith(".fbs"):
            base_filename = os.path.splitext(
                filename)[0]  # Remove the .fbs extension
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                content = file.read()
                match = identifier_pattern.search(content)
                if match:
                    file_identifier = match.group(1)
                    file_identifiers[base_filename] = file_identifier

    return file_identifiers


def write_identifiers_to_file(identifiers, output_file):
    with open(output_file, "w") as file:
        file.write("class FIDS:\n")
        for key, value in identifiers.items():
            file.write(f'    {key} = "{value}"\n')


def gen_fid_python():
    directory = "./definitions"  # replace with your folder path

    identifiers = find_file_identifiers(directory)
    output_file = "./python/FILE_ID_LIST.py"
    identifiers = find_file_identifiers(directory)
    write_identifiers_to_file(identifiers, output_file)

    print(f"Identifiers saved to {output_file}")


if __name__ == "__main__":
    gen_fid_python()
