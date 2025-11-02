from fastapi import APIRouter, UploadFile, HTTPException
from utils.pdf_extractor import extract_text_from_pdf
from services.retrieval_service import store_text_chunks
from services.mistral_service import generate_quiz
from services.quiz_parser import parse_quiz_to_json
import tempfile
import os

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/upload")
async def upload_pdf(file: UploadFile):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Extract text from PDF
            extracted_text_generator = extract_text_from_pdf(tmp_path)

            # This line is removed to avoid loading entire text into memory
            # extracted_text = " ".join(list(extracted_text_generator))

            # The check below needs to be done on the generator or by consuming it if necessary.
            # For now, we'll re-extract if we need to check.
            # TODO: Improve this check to be more memory efficient
            temp_text_for_check = " ".join(list(extract_text_from_pdf(tmp_path))) # Re-extract to check if empty
            if not temp_text_for_check.strip():
                raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
            
            # Store chunks for future contextual retrieval
            store_text_chunks(extracted_text_generator, file.filename or "unknown.pdf")

            # Re-initialize the generator for quiz generation, as it's been consumed
            extracted_text_generator = extract_text_from_pdf(tmp_path)
            
            # Generate quiz
            quiz_text = generate_quiz(extracted_text_generator)
            
            # Parse quiz into structured JSON (parse BEFORE refining if we want to refine)
            quiz_json = parse_quiz_to_json(quiz_text, file.filename or "unknown.pdf")
            
            # Note: refine_quiz is currently disabled as it returns narrative text
            # We can refine the quiz structure after parsing if needed
            
            # Debug logging
            print(f"DEBUG: Generated {len(quiz_json.get('questions', []))} questions")
            print(f"DEBUG: Quiz JSON structure: {quiz_json}")

            return quiz_json
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
