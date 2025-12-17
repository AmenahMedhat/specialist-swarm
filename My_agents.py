import os
from groq import Groq
from dotenv import load_dotenv
from state import AgentState

# Load environment variables from .env
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))



def supervisor(state: AgentState):
    # Supervisor node does NOT modify state
    return {}



def researcher(state: AgentState):
    prompt = f"""
    Give 3 short bullet points explaining:
    {state['question']}
    Keep it very simple.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    notes_text = response.choices[0].message.content
    notes = [line for line in notes_text.split("\n") if line.strip()]

    return {"research_notes": notes}


def writer(state: AgentState):
    notes = "\n".join(state["research_notes"])

    prompt = f"""
    Using the notes below, write one short clear paragraph:

    {notes}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    answer = response.choices[0].message.content.strip()

    return {"answer": answer}


def check_answer(state: AgentState):
    feedback = state.get("user_feedback", "").lower().strip()

    if feedback in ["yes", "y", "satisfied"]:
        return {"satisfied": True}

    return {"satisfied": False}

