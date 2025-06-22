import os.path
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory_ap = os.path.abspath(working_directory)
        finall_file = os.path.abspath(os.path.join(working_directory_ap, file_path))
        exist = os.path.exists(finall_file)
    except Exception as e:
        return f'Error: {e}'
    
    if not finall_file.startswith(working_directory_ap):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    
    if not exist:
        try:
            os.makedirs(os.path.dirname(finall_file), exist_ok=True)
        except Exception as e:
            return f'Error: creating directory: {e}'
    if os.path.exists(finall_file) and os.path.isdir(finall_file):
        return f'Error: "{file_path}" is a directory, not a file'

    try:    
        with open(finall_file, "w") as w:
            w.write(content)
        return f'Successfully wrote to "{file_path} ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: writing to file: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a specified file with content within the working directory.Creates a new file if the given file does not exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file",

            )
        },
        required=["file_path", "content"],
    ),
) 