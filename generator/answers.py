from llm.antigravity_client import call_llm
from config import ANSWER_PROMPT_TEMPLATE

def generate_answer(paragraph_text: str, question_text: str) -> str:
    """
    Calls the LLM to answer a specific question using exclusively the provided paragraph text.
    Returns the answer as a string.
    """
    prompt = ANSWER_PROMPT_TEMPLATE.format(paragraph=paragraph_text, question=question_text)
    
    try:
        answer = call_llm(prompt=prompt)
        return answer.strip()
    except Exception as e:
        print(f"Error generating answer for question '{question_text}': {e}")
        return "Error generating answer."
