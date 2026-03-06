import json
from openai import OpenAI
from typing import Dict, Any
from config import LLM_API_KEY, LLM_MODEL, IF_NOT_SET_MESSAGE

if not LLM_API_KEY:
    raise ValueError(IF_NOT_SET_MESSAGE)

# Initialize the OpenAI client natively for NVIDIA
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=LLM_API_KEY
)

def call_llm(prompt: str, response_format: str = "text") -> str:
    """
    Calls the LLM and returns the text response.
    Supports basic JSON response formatting if required by prompt.
    """
    kwargs = {
         "model": LLM_MODEL,
         "messages": [
             {"role": "user", "content": prompt}
         ],
         "temperature": 0.2, # Low temperature for more deterministic behavior
    }
    
    # Simple check for JSON formatting request
    if response_format == "json":
         kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content
