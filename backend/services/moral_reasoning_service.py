import os
from google import genai
from dotenv import load_dotenv
from typing import Dict, List, Any
from collections import defaultdict

load_dotenv()

def _get_configured_client():
    """Get a configured Gemini client"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    return genai.Client()

def analyze_moral_reasoning_patterns(justifications: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze user's justifications to identify moral reasoning patterns"""
    if not justifications:
        return {
            "primary_framework": "Unknown",
            "secondary_frameworks": [],
            "reasoning_patterns": {},
            "summary": "Not enough data to analyze reasoning patterns.",
            "recommendations": ["Take more quizzes and provide justifications to unlock your ethical bias profile."]
        }
    
    client = _get_configured_client()
    
    # Prepare context from justifications
    justification_texts = []
    for j in justifications:
        if j.get('justification_text'):
            justification_texts.append(f"Question {j.get('question_id', '?')}: {j.get('justification_text')}")
    
    context = "\n".join(justification_texts[:20])  # Limit to last 20 for context window
    
    prompt = f"""You are an ethics education expert analyzing a student's moral reasoning patterns based on their justifications for ethical quiz answers.

Student's justifications:
{context}

Analyze their reasoning patterns and identify:
1. Primary ethical framework they tend to use (Utilitarian, Deontological, Virtue Ethics, Rights-based, Care Ethics, etc.)
2. Secondary frameworks they also draw upon
3. Key reasoning patterns (e.g., focus on consequences, rules, character, rights, relationships)
4. A 2-3 sentence summary of their ethical reasoning style
5. 2-3 personalized recommendations for growth

Format your response:
PRIMARY: [framework name]
SECONDARY: [framework1, framework2]
PATTERNS: [pattern1: description, pattern2: description]
SUMMARY: [2-3 sentences]
RECOMMENDATIONS: [recommendation1, recommendation2, recommendation3]"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text
        
        # Parse response
        primary = "Unknown"
        secondary = []
        patterns = {}
        summary = ""
        recommendations = []
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line_upper = line.upper()
            if 'PRIMARY:' in line_upper:
                primary = line.replace('PRIMARY:', '').replace('primary:', '').strip()
                current_section = None
            elif 'SECONDARY:' in line_upper:
                secondary_text = line.replace('SECONDARY:', '').replace('secondary:', '').strip()
                secondary = [s.strip() for s in secondary_text.split(',') if s.strip()]
                current_section = None
            elif 'PATTERNS:' in line_upper:
                current_section = 'patterns'
                patterns_text = line.replace('PATTERNS:', '').replace('patterns:', '').strip()
                if patterns_text:
                    # Try to parse pattern: description pairs
                    parts = patterns_text.split(':')
                    if len(parts) >= 2:
                        patterns[parts[0].strip()] = ':'.join(parts[1:]).strip()
            elif 'SUMMARY:' in line_upper:
                current_section = 'summary'
                summary = line.replace('SUMMARY:', '').replace('summary:', '').strip()
            elif 'RECOMMENDATIONS:' in line_upper:
                current_section = 'recommendations'
                rec_text = line.replace('RECOMMENDATIONS:', '').replace('recommendations:', '').strip()
                if rec_text:
                    recommendations.append(rec_text)
            elif current_section == 'patterns' and line.strip() and ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    patterns[parts[0].strip()] = parts[1].strip()
            elif current_section == 'summary' and line.strip():
                summary += " " + line.strip()
            elif current_section == 'recommendations' and line.strip():
                recommendations.append(line.strip().lstrip('- '))
        
        if not summary:
            summary = "Your ethical reasoning shows thoughtful consideration of moral dilemmas."
        
        if not recommendations:
            recommendations = [
                "Continue reflecting on different ethical frameworks",
                "Consider multiple perspectives in complex situations"
            ]
        
        return {
            "primary_framework": primary,
            "secondary_frameworks": secondary[:3],
            "reasoning_patterns": patterns,
            "summary": summary,
            "recommendations": recommendations[:3]
        }
    except Exception as e:
        return {
            "primary_framework": "Unknown",
            "secondary_frameworks": [],
            "reasoning_patterns": {},
            "summary": f"Error analyzing reasoning: {str(e)}",
            "recommendations": ["Continue taking quizzes to build your profile."]
        }

