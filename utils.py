from google import genai
from dotenv import load_dotenv
from os.path import join, dirname
import os

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GEMINI_API_KEY)

def prompt_gemini(msg: str, model_id: str = "gemini-2.5-flash") -> str:
    response = client.models.generate_content(model=model_id, contents=msg)
    return response.text