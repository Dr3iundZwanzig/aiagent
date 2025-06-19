import os.path
import subprocess

def run_python_file(working_directory, file_path):
    try:
        working_directory_ap = os.path.abspath(working_directory)
        finall_file = os.path.abspath(os.path.join(working_directory_ap, file_path))
        exist = os.path.exists(finall_file)
    except Exception as e:
        return f'Error: {e}'
    
    if not finall_file.startswith(working_directory_ap):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not exist:
        return f'Error: File "{file_path}" not found.'
    
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python", finall_file]
        
        run = subprocess.run(
            commands,
            capture_output=True,
            text=True ,check=True,
            timeout=30,
            cwd=working_directory_ap,
        )
        output = []
        if run.stdout:
            output.append(f"STDOUT:\n{run.stdout}")
        if run.stderr:
            output.append(f"STDERR:\n{run.stderr}")
        if run.returncode != 0:
            output.append(f"Process exited with code {run.returncode}")
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f'Error: executing Python file: {e}'