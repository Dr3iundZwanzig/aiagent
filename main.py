import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
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

    call = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    prompt_tokens = call.usage_metadata.prompt_token_count
    response_tokens = call.usage_metadata.candidates_token_count

    print("Response:")
    print(call.text)

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    




try:
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"Exeption: {e}")
    sys.exit(1)