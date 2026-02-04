import os
from groq import Groq
import json
client = Groq(api_key=os.getenv("GROQ_API_KEY"),base_url="https://api.groq.com")

def validate_answer_with_ai(question, answer):
    prompt = f"""
You are an agriculture expert.

Question:
{question}

Answer:
{answer}

Decide if the answer is reasonably helpful and relevant to question.

Return STRICT JSON in this format:
{{
  "is_valid": true/false,
  "confidence": number (0-100),
  "reason": "short explanation"
}}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an agricultural expert validating farmer answers."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return completion.choices[0].message.content

    except Exception as e:
        return json.dumps({
            "is_valid": False,
            "confidence": 0,
            "reason": f"AI Error: {str(e)}"
        })