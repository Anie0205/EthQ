import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def _get_configured_client():
    """Get a configured Mistral client, checking API key at runtime"""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError(
            "MISTRAL_API_KEY environment variable is not set. "
            "Please set your Mistral API key."
        )
    
    return Mistral(api_key=api_key)

CONSTITUTION_RULES = """
1. Avoid harm: No hate, bias, or stereotypes.
2. Ensure fairness: Questions must be neutral and inclusive.
3. Maintain educational value: Questions should test real understanding.
4. Clarity: Language must be clear and age-appropriate.
"""

def refine_quiz(quiz_text: str) -> str:
    """Refine quiz questions using Constitutional AI principles"""
    client = _get_configured_client()
    
    prompt = f"""Here are some quiz questions:

{quiz_text}

Based on the following Constitutional AI principles, critique and regenerate the quiz to improve fairness, clarity, and educational value:

{CONSTITUTION_RULES}

Please provide an improved version of the quiz that follows these principles."""

    messages = [{"role": "user", "content": prompt}]
    
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error refining quiz: {str(e)}"