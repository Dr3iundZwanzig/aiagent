import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

call = client.models.generate_content(model="gemini-2.0-flash-001", contents="Why is Boot.dev such great place to learn backend developmen? Use one paragraph maximum.")

print(call.text)
print(call.usage_metadata.prompt_token_count)
print(call.usage_metadata.candidates_token_count)