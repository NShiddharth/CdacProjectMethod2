import os
from dotenv import load_dotenv

# Load common env vars like API keys from a .env file if it exists
load_dotenv()

# Configuration Settings
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("NVIDIA_API_KEY")
IF_NOT_SET_MESSAGE = "NVIDIA_API_KEY environment variable is not set."

# We'll use a hypothetical or standard OpenAI-compatible client endpoint.
# By default, openai library uses https://api.openai.com/v1.
LLM_MODEL = os.getenv("LLM_MODEL", "meta/llama-3.1-8b-instruct")

# Paragraph Filtering Configuration
MIN_WORDS_PER_PARAGRAPH = 40

# Prompt templates
QUESTION_PROMPT_TEMPLATE = """
You are an expert educational content creator.
Read the following paragraph carefully and generate EXACTLY 10 distinct questions that can be answered ONLY using the information provided in the paragraph.

CRITICAL INSTRUCTION: Ensure the questions are diverse in their phrasing and type. 
Do NOT start every question with "What". 
Instead, use a variety of question starters such as "How", "Why", "Describe", "Explain", "List", "Which", and "Who". 

Do not include information from outside the paragraph. Do not repeat questions.

Here is the paragraph:
{paragraph}

Return the output strictly in the following JSON format:
{{"questions": ["question 1", "question 2", ..., "question 10"]}}
"""

ANSWER_PROMPT_TEMPLATE = """
You are an expert reading comprehension assistant.
Read the following paragraph carefully and answer the question succinctly.
Your answer must be based ONLY on the paragraph provided. Be concise and accurate.

Paragraph:
{paragraph}

Question:
{question}

Provide ONLY the text of your answer without any additional formatting or conversational text.
"""
