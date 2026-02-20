from chatbot import client
import json

def validate_answer_with_ai(question, answer):
    prompt = f"""
You are a strict Agricultural Quality Assurance Auditor. 
Your job is to evaluate if an AI response provides a detailed, actionable, and agronomic solution to a farmer.

Input Data:
----------------
Question: {question}
Answer: {answer}
----------------

Strict Evaluation Criteria:
1. **Specificity:** The answer MUST name specific inputs (e.g., "Urea", "Imidacloprid") or specific actions (e.g., "install drip irrigation", "spray every 15 days"). 
2. **Actionability:** Vague advice like "solve it", "use fertilizer", "take care of crops", or "consult an expert" is FAILURE.
3. **Length & Depth:** One-line or two-word answers are automatically considered unhelpful.

Scoring Guide:
- **0-40 (Critical Fail):** Gibberish, "Solve it", "Yes/No", or generic advice like "Use water."
- **41-70 (Weak):** Correct topic but lacks details (e.g., "Use nitrogen" without saying which fertilizer).
- **71-100 (Pass):** Specific, expert advice with chemical names, quantities, or methods.

Output Requirements:
- Set "is_valid" to true ONLY if confidence is above 75.
- "reason" must explicitly state what specific detail was missing if the score is low.

Return STRICT JSON:
{{
  "is_valid": boolean,
  "confidence": number, 
  "reason": "string"
}}
"""

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
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
            # it represents behaviour of ai model -> Very stable focused and factual
            temperature=0.2
        )

        return completion.choices[0].message.content

    except Exception as e:
        # json.dumps convert python dictionary to json string
        return json.dumps({
            "is_valid": False,
            "confidence": 0,
            "reason": f"AI Error: {str(e)}"
        })