import os

def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(path)
    abs_work = os.path.abspath(working_directory)
    