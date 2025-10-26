import os
from mistralai import Mistral
from dotenv import load_dotenv
from .retrieval_service import retrieve_context

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

def generate_quiz(text: str, query: str = "Generate a quiz from this text") -> str:
    """Generate a multiple-choice quiz using Mistral"""
    # Retrieve context from your notes/pdf retrieval system
    context = retrieve_context(query)

    # Get the client
    client = _get_configured_client()

    # Construct the prompt
    prompt = f"""You are an educational quiz generator. Generate 10 ethical multiple-choice questions from the following text.

IMPORTANT CONSTITUTIONAL AI PRINCIPLES:
1. Avoid harm: No hate, bias, or stereotypes
2. Ensure fairness: Questions must be neutral and inclusive
3. Maintain educational value: Questions should test real understanding
4. Clarity: Language must be clear and age-appropriate

Guidelines:
- Each question should have 4 options (A, B, C, D) and one correct answer
- Ensure the answers are varied, not always B or C
- Questions should be neither too easy nor too difficult
- Be fair, inclusive, and test actual understanding

Text: {text[:4000]}
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

Continue for all 10 questions. IMPORTANT: Only output the quiz in the format above, no other text."""

    messages = [{"role": "user", "content": prompt}]
    
    try:
        # Generate content using the new API
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        # Catch API errors gracefully
        return f"Error generating quiz: {str(e)}"
