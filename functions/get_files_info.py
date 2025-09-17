import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(path)
    abs_work = os.path.abspath(working_directory)

    if not abs_path.startswith(abs_work):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'

    lines = []
    try:
        for i in os.listdir(abs_path):
            item_path = os.path.join(abs_path, i)
            get_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            lines.append(f'- {i}: file_size={get_size} bytes, is_dir={is_dir}')

        return '\n'.join(lines)
    except Exception as e:
        return f"Error: {str(e)}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
