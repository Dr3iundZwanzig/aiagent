from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
from functions.config import WORKING_DIR

def call_function(function_call_part, verbose=False):
    fname = ""
    args = {}
    for function_call_parts in function_call_part:
        fname = function_call_parts.name
        args = function_call_parts.args
        if verbose == True:
            print(f"Calling function: {fname}({args})")
        else:
            print(f" - Calling function: {fname}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if fname not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fname,
                    response={"error": f"Unknown function: {fname}"},
                )
            ],
        )
    
    args["working_directory"] = WORKING_DIR
    function_result = function_map[fname](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=fname,
                response={"result": function_result},
            )
        ],
    )