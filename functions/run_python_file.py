import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Run or execute a program within the working directory and return its output",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type = types.Type.STRING,
                description = "The file path to the file to run or execute",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir = os.path.abspath(working_directory)
    cmd = ["python", path]
    if args:
        cmd.append(*args)
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    if not working_directory in path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    try:
        print(f"cmd={cmd}")
        p = subprocess.run(cmd, timeout = 30, capture_output = True, text = True, cwd = working_dir)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    if p.returncode != 0:
        return f"Process exited with code {p.returnedcode}"
    return f"STDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}\n"
