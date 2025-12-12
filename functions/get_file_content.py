import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = "Read the content of a file.",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file path of the file we want to read its content from.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    path = os.path.abspath(os.path.join(working_directory, file_path))
    if not working_directory in path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
	    return f"{e}"
    if len(file_content_string) == MAX_CHARS:
        file_content_string = file_content_string + f'\n[...File "{file_path}" truncated at 10000 characters]'
    return file_content_string
