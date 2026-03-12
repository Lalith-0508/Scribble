import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def clean_and_structure_text(raw_text):

    prompt = f"""
Clean the OCR text.

Fix spelling and grammar.
Extract tasks separately.

Text:
{raw_text}

Return format:

Clean Notes:
...

Tasks:
- ...
"""

    response = model.generate_content(prompt)

    result = response.text

    tasks = []

    for line in result.split("\n"):

        if line.strip().startswith("-"):
            tasks.append(line.replace("-", "").strip())

    return result, tasks