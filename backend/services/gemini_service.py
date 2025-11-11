import os
from google import genai
from dotenv import load_dotenv
from .retrieval_service import retrieve_context

# Load environment variables
load_dotenv()

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

def _level_guidance(level: str) -> str:
    level = (level or "").strip().lower()
    if level in ("beginner", "easy"):
        return "Beginner level: simpler wording, foundational concepts, straightforward distractors."
    if level in ("advanced", "hard"):
        return "Advanced level: nuanced scenarios, multi-step reasoning, strong distractors."
    return "Intermediate level: moderate difficulty, balanced distractors."

def generate_quiz(text_iterator, query: str = "Generate a quiz from this text", level: str = "intermediate", num_questions: int = 10) -> str:
    """Generate a multiple-choice quiz using Gemini"""
    # Concatenate text from iterator, respecting context window limits
    full_text_list = []
    current_length = 0
    for chunk in text_iterator:
        if current_length + len(chunk) <= 4000:
            full_text_list.append(chunk)
            current_length += len(chunk)
        else:
            remaining_space = 4000 - current_length
            full_text_list.append(chunk[:remaining_space])
            current_length += remaining_space
            break
    text_for_gemini = " ".join(full_text_list)

    # Retrieve context from your notes/pdf retrieval system
    context = retrieve_context(query)

    # Get the client
    client = _get_configured_client()

    # Construct the prompt
    guidance = _level_guidance(level)
    qn = max(1, min(int(num_questions or 10), 20))
    prompt = f"""You are an educational quiz generator. Generate {qn} ethical multiple-choice questions from the following text.

IMPORTANT CONSTITUTIONAL AI PRINCIPLES:
1. Avoid harm: No hate, bias, or stereotypes
2. Ensure fairness: Questions must be neutral and inclusive
3. Maintain educational value: Questions should test real understanding
4. Clarity: Language must be clear and age-appropriate

Difficulty Guidance: {guidance}

Guidelines:
- Each question should have 4 options (A, B, C, D) and one correct answer
- Ensure the answers are varied, not always B or C
- Questions should be neither too easy nor too difficult
- Be fair, inclusive, and test actual understanding

Text: {text_for_gemini}
Context: {context}

Provide your response in EXACTLY this format (do not include commentary or explanations outside this format):

1. Question text here
A) Option A
B) Option B  
C) Option C
D) Option D
Answer: A
Explanation: Brief explanation

2. Question text here
A) Option A
B) Option B
C) Option C
D) Option D
Answer: B
Explanation: Brief explanation

Continue until you produce {qn} questions. IMPORTANT: Only output the quiz in the format above, no other text."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

def generate_quiz_from_text(text: str, level: str = "intermediate", num_questions: int = 10) -> str:
    client = _get_configured_client()
    guidance = _level_guidance(level)
    qn = max(1, min(int(num_questions or 10), 20))
    text_for_gemini = (text or "")[:8000]
    prompt = f"""You are an educational quiz generator. Generate {qn} ethical multiple-choice questions from the following text.

Difficulty Guidance: {guidance}

Guidelines:
- Each question should have 4 options (A, B, C, D) and one correct answer
- Ensure the answers are varied, not always B or C
- Be fair, inclusive, and test actual understanding

Text: {text_for_gemini}

Provide your response in EXACTLY this format (no extra commentary):
1. Question text here
A) Option A
B) Option B
C) Option C
D) Option D
Answer: A
Explanation: Brief explanation

Continue until you produce {qn} questions."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

def reformat_quiz_output(raw_text: str, num_questions: int = 10) -> str:
    """Ask Gemini to reformat an existing quiz-like text into strict A/B/C/D/Answer markup."""
    client = _get_configured_client()
    qn = max(1, min(int(num_questions or 10), 20))
    prompt = f"""Reformat the following content into EXACTLY the quiz format below for {qn} questions. If content is insufficient, output as many as possible but keep the format strictly.

CONTENT:
{raw_text}

REQUIRED FORMAT (no extra commentary):
1. Question text here
A) Option A
B) Option B
C) Option C
D) Option D
Answer: A
Explanation: Brief explanation

2. Question text here
A) Option A
B) Option B
C) Option C
D) Option D
Answer: B
Explanation: Brief explanation"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error reformatting quiz: {str(e)}"

