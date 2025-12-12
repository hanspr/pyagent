import os
from functions.config import MAX_CHARS
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Write a file to be executed",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file path to write the file",
            ),
            "content": types.Schema(
                type = types.Type.STRING,
                description = "Content to write to the selected file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    path = os.path.abspath(os.path.join(working_directory, file_path))
    dirpath = os.path.dirname(path)
    if not working_directory in path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(dirpath):
        try:
            os.makedirs(dirpath)
        except Exepcion as e:
            return f"{e}"
    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
	    return f"{e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
