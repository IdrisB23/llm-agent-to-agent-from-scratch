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

def format_message(history: list[str]) -> str:
    """Formats the message history for the LLM."""
    # get system messages, since they provide important context
    sys_mesages = [m for m in history if m["sender"] == "system"]
    non_sys_messages = [m for m in history if m["sender"] != "system"]
    # prepend system messages to the formatted history
    formatted_history = "\n".join([
        f"{m['sender']}: {m['content']}"
        for m in sys_mesages
    ])
    # append the rest of the messages
    formatted_history += "\n" + "\n".join([
        f"{m['sender']}: {m['content']}"
        for m in non_sys_messages
    ])
    return formatted_history