import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions
from call_function import call_function
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

    if verbose:
        print(f"User prompt: {prompt}")
    
    messages =[
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    i = 0
    while True:
        i += 1
        if i > 20:
            print("Maximum iterations reached")
            sys.exit(1)
        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages, verbose):
    call = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", call.usage_metadata.prompt_token_count)
        print("Response tokens:", call.usage_metadata.candidates_token_count)

    if call.candidates:
        for candidates in call.candidates:
            function_call_content = candidates.content
            messages.append(function_call_content)

    if not call.function_calls:
        return call.text
    
    function_responses = []
    for function_call_part in call.function_calls:
        function_call_results = call_function(function_call_part, verbose)
        if not function_call_results.parts[0].function_response.response or not function_call_results.parts:
            raise Exception("Fatal error no function return")
        if verbose:
            print(f"-> {function_call_results.parts[0].function_response.response}")
        function_responses.append(function_call_results.parts[0])
    if not function_responses:
        raise Exception("no function responses generated")
        
    messages.append(types.Content(role="tool", parts=function_responses))
    


    







if __name__ == "__main__":
    main()
