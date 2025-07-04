import os.path
from google.genai import types

def get_files_info(working_directory, directory=None):
    try:
        directory_ap = os.path.abspath(directory)
        working_directory_ap = os.path.abspath(working_directory)
        finall_directory = working_directory_ap
        if directory:
            finall_directory = os.path.abspath(os.path.join(working_directory_ap, directory))
        isdir = os.path.isdir(finall_directory)
    except Exception as e:
        return f'Error: get_files_info {e}'
    
    if not finall_directory.startswith(working_directory_ap):
        return f'Error: Cannot list "{directory_ap}" as it is outside the permitted working directory'
    
    if not isdir:
        return f'Error: "{directory}" is not a directory'
    try:
        files_info = []
        for filename in os.listdir(finall_directory):
            filepath = os.path.join(finall_directory, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

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