import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = sys.argv[1:]

    messages =[
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    call = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    
    
    print(call.text)
    print(f"Prompt tokens: {call.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {call.usage_metadata.candidates_token_count}")
    




try:
    if __name__ == "__main__":
        main()
except Exception:
    print("Usage: python3 main.py <PROMPT>")
    sys.exit(1)