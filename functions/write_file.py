import os

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
