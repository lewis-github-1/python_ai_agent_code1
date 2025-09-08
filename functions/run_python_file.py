import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(path)
    abs_work = os.path.abspath(working_directory)

    if not (abs_path.startswith(abs_work + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not (os.path.exists(abs_path)):
        return f'Error: File "{file_path}" not found.'

    if not (abs_path.endswith('.py')):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmd = [sys.executable, abs_path] + list(args)
        completed_process = subprocess.run(cmd, cwd=abs_work, capture_output=True, text=True, timeout=30)
        
        stdout = completed_process.stdout or ""
        stderr = completed_process.stderr or ""

        if not stdout.strip() and not stderr.strip():
            return "No output produced."

        parts = []
        parts.append(f"STDOUT:\n{stdout}".rstrip())
        parts.append(f"STDERR:\n{stderr}".rstrip())

        if completed_process.returncode != 0:
            parts.append(f"Process exited with code {completed_process.returncode}")

        return "\n".join(parts)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
        
