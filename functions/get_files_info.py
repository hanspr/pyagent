import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name = "get_files_info",
    description = "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "directory": types.Schema(
                type = types.Type.STRING,
                description = "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory = "."):
    path = os.path.abspath(os.path.join(working_directory, directory))
    if not working_directory in path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    results = []
    files = os.listdir(path)
    for file in files:
        isdir = "False"
        filesize = 0
        if file.startswith(".") or file.startswith("__"):
            continue
        if os.path.isdir(os.path.join(path, file)):
            isdir = "True"
            #subdir = get_files_info(os.path.join(path, file), ".")
            #results.append(subdir)
        if os.path.isfile(os.path.join(path, file)):
            filesize = os.path.getsize(os.path.join(path, file))
        results.append(f"- {file}: file_size={filesize} bytes, is_dir={isdir}")
    return "\n".join(results)
