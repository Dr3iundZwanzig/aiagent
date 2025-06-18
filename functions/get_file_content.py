import os.path
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        file_ap = os.path.abspath(file_path)
        working_directory_ap = os.path.abspath(working_directory)
        finall_file = os.path.abspath(os.path.join(working_directory_ap, file_path))
        isfile = os.path.isfile(finall_file)
    except Exception as e:
        return f'Error: {e}'
    
    if not finall_file.startswith(working_directory_ap):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not isfile:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(finall_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                return file_content_string + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
        return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"