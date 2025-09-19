import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(path)
    abs_work = os.path.abspath(working_directory)

    if not (abs_path == abs_work or abs_path.startswith(abs_work + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    parent = os.path.dirname(abs_path) or abs_work
    try:
        if not os.path.exists(parent):
            os.makedirs(parent)        
        
        with open(abs_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory where the text gets written.",
            ),
            "content": types.Schema(
                    type=types.Type.STRING,
                    description="The exact text to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)