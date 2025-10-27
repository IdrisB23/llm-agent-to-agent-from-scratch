from google import genai
from dotenv import load_dotenv
from os.path import join, dirname
import os
import queue
import threading
import time


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GEMINI_API_KEY)


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


def prompt_gemini(msg: str) -> str:
    response = client.models.generate_content(model="gemini-2.5-flash", contents=msg)
    return response.text


# Use the robust two-queue setup
request_q = queue.Queue()
response_q = queue.Queue()
messages = []
sys_message = {
    "type": "conversation.start",
    "sender": "system",
    "receiver": "Agent B",
    "timestamp": time.time(),
    "content": "Start collaboration on task: compute a simple math problem. Once a solution is found, reply with STOP to end the conversation. Example:"
    "Agent A: What is 2 + 2?\n Agent B: The answer is 4.\n Agent A: STOP",
    "metadata": {"intent": "propose", "conversation_id": "conv_12345"},
}
messages.append(sys_message)
request_q.put(sys_message)


def agent_a(req_q, res_q):
    """Initiates conversation and asks follow-up questions."""

    conversation_round = 1
    max_rounds = 3

    # 2. Main loop for continuous communication
    while True:
        # Wait for the response from Agent B
        response = res_q.get()
        response = response["content"]
        print(f"A <- B: {response}")

        # 3. Check for the stop signal from B (in case B can also stop)
        if response.strip().upper() == "STOP":
            print("Agent A received stop signal. Shutting down.")
            req_q.put(response)
            res_q.put(response)
            break

        # 4. Decide whether to continue or stop
        if conversation_round >= max_rounds:
            print("Agent A is ending the conversation.")
            req_q.put("STOP")  # Send the stop signal
            break

        # 5. Formulate the next question
        conversation_round += 1
        formatted_history = format_message(messages)
        answer = prompt_gemini(formatted_history + "\nAgent A:")

        print(f"A -> B: {answer}")
        a_message = {
            "sender": "Agent A",
            "receiver": "Agent B",
            "timestamp": time.time(),
            "type": "message.create",
            "content": answer,
            "metadata": {
                "intent": "continue_conversation",
                "conversation_id": "conv_12345",
            },
        }
        messages.append(a_message)
        req_q.put(a_message)
        time.sleep(0.5)  # A little pause for readability


def agent_b(req_q, res_q):
    """Responds to questions continuously."""

    # 1. Main loop to always be "listening"
    while True:
        # Wait for a question from Agent A
        question = req_q.get()
        question = question["content"]

        # 2. Check for the stop signal
        if question.strip().upper() == "STOP":
            print("Agent B received stop signal. Shutting down.")
            # Optional: Acknowledge the stop signal to let Agent A exit cleanly
            req_q.put("STOP")
            res_q.put("STOP")
            break

        print(f"B <- A: {question}")

        answer = "I'm not sure."

        formatted_history = format_message(messages)
        answer = prompt_gemini(formatted_history + "\nAgent B:")

        # 4. Send the answer back
        print(f"B -> A: {answer}")
        b_message = {
            "sender": "Agent B",
            "receiver": "Agent A",
            "timestamp": time.time(),
            "type": "message.create",
            "content": answer,
            "metadata": {
                "intent": "continue_conversation",
                "conversation_id": "conv_12345",
            },
        }
        messages.append(b_message)
        res_q.put(b_message)
        time.sleep(1)  # Mimic processing time


# --- Main Execution ---
print("Starting continuous agent communication...\n")

thread_a = threading.Thread(target=agent_a, args=(request_q, response_q))
thread_b = threading.Thread(target=agent_b, args=(request_q, response_q))

thread_a.start()
thread_b.start()

# Wait for both threads to finish
thread_a.join()
thread_b.join()

print("\nFinal conversation log: ", messages)

print(format_message(messages))

print("\n...Communication finished.")
