import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions
from functions.call_function import call_function
import sys

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = sys.argv[1:]
    if not args:
        print('Usage: python3 main.py "PROMPT"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = sys.argv[1]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
  



    messages =[
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    call = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    prompt_tokens = call.usage_metadata.prompt_token_count
    response_tokens = call.usage_metadata.candidates_token_count

    
    if not call.function_calls:
        return print(f"Response: \n{call.text}")

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    result = call_function(call.function_calls,verbose)
    
    if not result.parts[0].function_response.response:
        raise Exception("Fatal error no function return")
    if verbose:
        print(f"-> {result.parts[0].function_response.response}")

    raise Exception("Error: no returns")
    
    
    


    






try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"Exeption: {e}")
    sys.exit(1)