import re

def parse_quiz_to_json(quiz_text: str, filename: str = "quiz") -> dict:
    """Parse quiz text into structured JSON format"""
    
    print(f"DEBUG: Parsing quiz text (length: {len(quiz_text)})")
    
    # Try to extract title from filename
    title = filename.replace(".pdf", "").replace("_", " ").title()
    
    questions = []
    
    # Split by question markers (1. 2. 3. etc.)
    question_sections = re.split(r'(\d+)\.\s+', quiz_text)
    
    # Process sections in pairs (number, content)
    for i in range(1, len(question_sections), 2):
        if i + 1 >= len(question_sections):
            break
            
        question_num = question_sections[i]
        content = question_sections[i + 1]
        
        lines = content.strip().split('\n')
        question_text = ""
        options = []
        answer_letter = ""
        explanation = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Extract question text (first non-empty line)
            if not question_text and not re.match(r'^[A-D][\.\)]\s+', line) and 'answer' not in line.lower() and 'explanation' not in line.lower():
                question_text = line.strip()
            
            # Extract options (A), B), C), D))
            elif re.match(r'^[A-D][\.\)]\s+', line):
                option_text = re.sub(r'^[A-D][\.\)]\s+', '', line).strip()
                options.append(option_text)
            
            # Extract answer
            elif 'answer:' in line.lower():
                match = re.search(r'answer:\s*([A-D])', line, re.IGNORECASE)
                if match:
                    answer_letter = match.group(1).strip()
            
            # Extract explanation
            elif 'explanation:' in line.lower():
                explanation_match = re.search(r'explanation:\s*(.+)', line, re.IGNORECASE)
                if explanation_match:
                    explanation = explanation_match.group(1).strip()
        
        # Only add if we have valid data
        if question_text and options and answer_letter:
            # Get the correct answer text
            answer_index = ord(answer_letter.upper()) - ord('A')
            correct_answer = ""
            if 0 <= answer_index < len(options):
                correct_answer = options[answer_index]
            
            questions.append({
                "id": len(questions) + 1,
                "question": question_text,
                "options": options,
                "answer": correct_answer or answer_letter,
                "explanation": explanation
            })
    
    # Fallback if no questions parsed
    if not questions:
        print("DEBUG: No questions parsed, using fallback")
        # Just create a simple placeholder quiz
        questions = [{
            "id": 1,
            "question": "Unable to parse quiz questions from the provided text. Please ensure the text contains properly formatted questions with options labeled A), B), C), D) and answers.",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A",
            "explanation": "This is a placeholder question."
        }]
    
    print(f"DEBUG: Successfully parsed {len(questions)} questions")
    
    return {
        "title": title,
        "questions": questions
    }