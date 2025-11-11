import os
from google import genai
from dotenv import load_dotenv
import yaml # Import yaml

# Load environment variables
load_dotenv()

# Path to the constitution file
CONSTITUTION_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'constitution.yaml')

def _get_configured_client():
    """Get a configured Gemini client, checking API key at runtime"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Please set your Gemini API key."
        )
    
    # The client gets the API key from the environment variable `GEMINI_API_KEY`
    return genai.Client()

def _load_constitution_rules():
    """Load constitution rules from YAML file"""
    try:
        with open(CONSTITUTION_FILE_PATH, 'r') as f:
            constitution = yaml.safe_load(f)
        rules = [item['rule'] for item in constitution.get('rules', [])]
        # Format rules for the prompt
        return "\n".join([f"{i+1}. {rule}" for i, rule in enumerate(rules)])
    except FileNotFoundError:
        print(f"Warning: {CONSTITUTION_FILE_PATH} not found. Using default rules.")
        return """
1. Avoid harm: No hate, bias, or stereotypes.
2. Ensure fairness: Questions must be neutral and inclusive.
3. Maintain educational value: Questions should test real understanding.
4. Clarity: Language must be clear and age-appropriate.
"""
    except Exception as e:
        print(f"Error loading constitution rules: {e}. Using default rules.")
        return """
1. Avoid harm: No hate, bias, or stereotypes.
2. Ensure fairness: Questions must be neutral and inclusive.
3. Maintain educational value: Questions should test real understanding.
4. Clarity: Language must be clear and age-appropriate.
"""

# Load rules once at startup
CONSTITUTION_RULES = _load_constitution_rules()

def refine_quiz(quiz_text: str) -> str:
    """Refine quiz questions using Constitutional AI principles"""
    client = _get_configured_client()
    
    prompt = f"""Here are some quiz questions:

{quiz_text}

Based on the following Constitutional AI principles, critique and regenerate the quiz to improve fairness, clarity, and educational value:

{CONSTITUTION_RULES}

Please provide an improved version of the quiz that follows these principles."""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error refining quiz: {str(e)}"