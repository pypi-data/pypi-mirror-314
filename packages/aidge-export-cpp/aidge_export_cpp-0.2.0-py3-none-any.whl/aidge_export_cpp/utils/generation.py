import re
import os
import shutil
from jinja2 import Environment, FileSystemLoader


def get_functions_from_c_file(file_path):
    functions = []
    pattern = r'\w+\s+(\w+)\s*\(([^)]*)\)\s*{'

    with open(file_path, 'r') as file:
        file_content = file.read()

    matches = re.findall(pattern, file_content)
    for match in matches:
        function_name = match[0]
        arguments = match[1].split(',')
        arguments = [arg.strip() for arg in arguments]

        return_type = get_return_type(file_content, function_name)

        function_string = f"{return_type} {function_name}({', '.join(arguments)});"
        functions.append(function_string)

    return functions


def get_return_type(file_content, function_name):
    pattern = rf'\w+\s+{function_name}\s*\([^)]*\)\s*{{'
    return_type = re.search(pattern, file_content).group()
    return_type = return_type.split()[0].strip()
    return return_type


def get_functions_from_c_folder(folder_path):
    functions = []
    
    for _, _, files in os.walk(folder_path):
        for file in files:
            functions += get_functions_from_c_file(os.path.join(folder_path, file))

    return functions


def copyfile(filename, dst_folder):

    # If directory doesn't exist, create it
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    shutil.copy(filename, dst_folder)
