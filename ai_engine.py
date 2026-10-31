import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def extract_meeting_tasks(meeting_text):

    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from your .env file.")

    client = genai.Client(api_key=API_KEY)

    prompt = f"""
You are MeetFlow AI, a meeting-to-execution assistant.

Analyse this real-world meeting conversation.
It may contain filler words, repeated sentences,
digressions and self-corrections.

Extract useful information and return ONLY valid JSON.

Rules:
1. Never invent an owner or deadline.
2. If an owner is missing, write "Not specified".
3. If a deadline is missing, write "Not specified".
4. Separate decisions from action items.
5. Put unclear or unresolved matters in open_questions.
6. Make task titles short and clear.

Use exactly this JSON structure:

{{
  "meeting_summary": "Short summary",
  "decisions": ["Decision 1"],
  "tasks": [
    {{
      "task": "Task description",
      "owner": "Person responsible or Not specified",
      "deadline": "Deadline or Not specified",
      "priority": "High, Medium, or Low"
    }}
  ],
  "open_questions": ["Unresolved question"]
}}

MEETING CONVERSATION:
{meeting_text}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2
        )
    )

    return json.loads(response.text)