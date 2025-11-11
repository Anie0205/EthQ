import os
import re
from google import genai
from dotenv import load_dotenv
from typing import Dict, List, Any

load_dotenv()

def _get_configured_client():
    """Get a configured Gemini client"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    return genai.Client()

def explain_wrong_answer(
    question_text: str,
    options: List[str],
    user_answer: str,
    correct_answer: str,
    user_justification: str = None
) -> Dict[str, Any]:
    """Generate explanation for why a user's answer was wrong"""
    client = _get_configured_client()
    
    justification_context = ""
    if user_justification:
        justification_context = f"\n\nUser's reasoning: {user_justification}"
    
    prompt = f"""You are an ethics education mentor. A student answered an ethical question incorrectly. Provide a constructive, educational explanation.

Question: {question_text}

Options:
{chr(10).join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])}

User's answer: {user_answer}
Correct answer: {correct_answer}
{justification_context}

Provide a helpful explanation in this format:
EXPLANATION: [2-3 sentences explaining why their answer was wrong, what they might have missed, and what the correct reasoning should be]
FRAMEWORKS: [List 1-2 ethical frameworks relevant to this question, comma-separated]
PARALLELS: [1-2 real-world examples or cases that parallel this ethical dilemma, comma-separated]

Be encouraging and educational, not judgmental."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text
        
        # Parse the response
        explanation = ""
        frameworks = []
        parallels = []
        
        lines = text.split('\n')
        current_section = None
        for line in lines:
            if 'EXPLANATION:' in line:
                explanation = line.replace('EXPLANATION:', '').strip()
                current_section = 'explanation'
            elif 'FRAMEWORKS:' in line:
                frameworks_text = line.replace('FRAMEWORKS:', '').strip()
                frameworks = [f.strip() for f in frameworks_text.split(',') if f.strip()]
                current_section = 'frameworks'
            elif 'PARALLELS:' in line:
                parallels_text = line.replace('PARALLELS:', '').strip()
                parallels = [p.strip() for p in parallels_text.split(',') if p.strip()]
                current_section = 'parallels'
            elif current_section == 'explanation' and line.strip():
                explanation += " " + line.strip()
            elif current_section == 'frameworks' and line.strip():
                frameworks.extend([f.strip() for f in line.split(',') if f.strip()])
            elif current_section == 'parallels' and line.strip():
                parallels.extend([p.strip() for p in line.split(',') if p.strip()])
        
        if not explanation:
            explanation = text[:500]  # Fallback to first 500 chars
        
        return {
            "explanation": explanation,
            "ethical_frameworks": frameworks[:3],  # Limit to 3
            "real_world_parallels": parallels[:2]  # Limit to 2
        }
    except Exception as e:
        return {
            "explanation": f"Error generating explanation: {str(e)}",
            "ethical_frameworks": [],
            "real_world_parallels": []
        }

def explain_ethical_conflict(
    question_text: str,
    options: List[str],
    correct_answer: str = None
) -> Dict[str, Any]:
    """Generate comprehensive explanation of an ethical conflict/dilemma"""
    client = _get_configured_client()
    
    correct_context = f"\nNote: The correct answer is {correct_answer}, but focus on explaining the ethical complexity, not just the answer." if correct_answer else ""
    
    prompt = f"""You are an ethics education expert. Break down this ethical dilemma comprehensively.

Question: {question_text}

Options:
{chr(10).join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])}
{correct_context}

Provide a detailed analysis in this format:

PROS_CONS:
For each option, list 2-3 pros and cons:
A) [pros and cons]
B) [pros and cons]
C) [pros and cons]
D) [pros and cons]

FRAMEWORKS:
List 2-3 ethical frameworks that apply to this dilemma (e.g., Utilitarianism, Deontological Ethics, Virtue Ethics, Rights-based Ethics), with brief notes on how each applies.

PARALLELS:
List 2-3 real-world cases, historical examples, or scenarios that parallel this ethical conflict. Include brief context.

EXPLANATION:
A 3-4 sentence summary explaining the core ethical tension and why this is a meaningful dilemma."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text
        
        # Parse the response
        pros_cons = {}
        frameworks = []
        parallels = []
        explanation = ""
        
        lines = text.split('\n')
        current_section = None
        current_option = None
        
        for line in lines:
            line_upper = line.upper()
            if 'PROS_CONS:' in line_upper:
                current_section = 'pros_cons'
                continue
            elif 'FRAMEWORKS:' in line_upper:
                current_section = 'frameworks'
                continue
            elif 'PARALLELS:' in line_upper:
                current_section = 'parallels'
                continue
            elif 'EXPLANATION:' in line_upper:
                current_section = 'explanation'
                explanation = line.replace('EXPLANATION:', '').replace('explanation:', '').strip()
                continue
            
            if current_section == 'pros_cons':
                # Look for option markers like "A)", "B)", etc.
                if re.match(r'^[A-D]\)', line.strip()):
                    current_option = line.strip()[0]
                    pros_cons[current_option] = {"pros": [], "cons": []}
                elif current_option and ('pro' in line.lower() or 'con' in line.lower() or '-' in line):
                    # Try to parse pros/cons
                    if 'pro' in line.lower() or line.strip().startswith('+'):
                        pros_cons[current_option]["pros"].append(line.strip().lstrip('+-').strip())
                    elif 'con' in line.lower() or line.strip().startswith('-'):
                        pros_cons[current_option]["cons"].append(line.strip().lstrip('+-').strip())
            elif current_section == 'frameworks':
                if line.strip() and not line.strip().startswith('FRAMEWORKS'):
                    frameworks.append(line.strip().lstrip('- '))
            elif current_section == 'parallels':
                if line.strip() and not line.strip().startswith('PARALLELS'):
                    parallels.append(line.strip().lstrip('- '))
            elif current_section == 'explanation' and line.strip():
                explanation += " " + line.strip()
        
        # Fallback: if parsing failed, create basic structure
        if not pros_cons:
            for i, opt in enumerate(options):
                pros_cons[chr(65+i)] = {"pros": ["Consider the ethical implications"], "cons": ["Consider potential drawbacks"]}
        
        if not explanation:
            explanation = "This question presents a complex ethical dilemma that requires careful consideration of multiple perspectives and ethical frameworks."
        
        return {
            "pros_cons": pros_cons,
            "ethical_frameworks": frameworks[:3] if frameworks else ["Utilitarianism", "Deontological Ethics"],
            "real_world_parallels": parallels[:3] if parallels else [],
            "explanation": explanation
        }
    except Exception as e:
        return {
            "pros_cons": {chr(65+i): {"pros": [], "cons": []} for i in range(len(options))},
            "ethical_frameworks": [],
            "real_world_parallels": [],
            "explanation": f"Error generating explanation: {str(e)}"
        }

