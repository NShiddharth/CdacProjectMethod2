import json
from typing import List
from llm.antigravity_client import call_llm
from config import QUESTION_PROMPT_TEMPLATE

def generate_questions(paragraph_text: str) -> List[str]:
    """
    Generates exactly 10 questions for a given paragraph using the LLM.
    Parses the JSON response from the LLM and returns a list of question strings.
    """
    prompt = QUESTION_PROMPT_TEMPLATE.format(paragraph=paragraph_text)
    
    try:
        response_text = call_llm(prompt=prompt, response_format="json")
        data = json.loads(response_text)
        
        # Ensure 'questions' key exists and gives a list
        questions = data.get("questions", [])
        
        # We handle failures safely by making sure it's exactly 10 if possible, 
        # or otherwise truncate/pad, but the prompt strictly says exactly 10.
        if not isinstance(questions, list):
            return []
            
        return questions[:10]
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from LLM: {e}")
        return []
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []
