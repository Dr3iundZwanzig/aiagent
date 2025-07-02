import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions
from functions.call_function import call_function
from prompts import system_prompt
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
    
    messages =[
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    i = 0
    while True:
        call = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if call.candidates:
            for candidates in call.candidates:
                messages.append(candidates.content)

        if not call.function_calls or i == 20:
            if verbose:
                print(f"User prompt: {prompt}")
            return print(f"Response: \n{call.text}")

        result = call_function(call.function_calls,verbose)
    
        if not result.parts[0].function_response.response:
            raise Exception("Fatal error no function return")
        if verbose:
            print(f"-> {result.parts[0].function_response.response}")
        i += 1

    raise Exception("Error: no returns")
    
    
    


    






try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"Exeption: {e}")
    sys.exit(1)