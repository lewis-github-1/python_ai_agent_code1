import os
from functions.config import MAX_FILE_CHARS
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        path = os.path.join(working_directory, file_path)
        abs_path = os.path.abspath(path)
        abs_work = os.path.abspath(working_directory)

        if not abs_path.startswith(abs_work + os.sep) and abs_path != abs_work:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: {file_path}'
        
        with open(abs_path, 'r') as f:
            file_content_string = f.read(MAX_FILE_CHARS)
            
        if len(file_content_string) > MAX_FILE_CHARS:
            file_content_string = file_content_string[:MAX_FILE_CHARS]
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string


    except Exception as e:
        return f'Error: {str(e)}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows content of files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
