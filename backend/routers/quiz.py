from fastapi import APIRouter, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from utils.pdf_extractor import extract_text_from_pdf
from services.retrieval_service import store_text_chunks
from services.gemini_service import generate_quiz, reformat_quiz_output, generate_quiz_from_text
from services.quiz_parser import parse_quiz_to_json
from services.ethics_filter import refine_quiz # Import refine_quiz
import tempfile
import os

router = APIRouter(tags=["Quiz"])


def _raise_if_gemini_error(text: str, context: str):
    if not isinstance(text, str):
        return
    t = text.strip()
    if not t.startswith("Error "):
        return
    lower = t.lower()
    if "unauthorized" in lower or "401" in lower or "forbidden" in lower or "403" in lower:
        raise HTTPException(status_code=401, detail=f"Gemini unauthorized/invalid key: {context}")
    if "rate limit" in lower or "quota" in lower or "429" in lower:
        raise HTTPException(status_code=429, detail=f"Gemini rate limit/quota exhausted: {context}")
    raise HTTPException(status_code=502, detail=f"Gemini upstream error: {context}")


@router.post("/upload")
async def upload_pdf(file: UploadFile, level: str = Form("intermediate"), questions: int = Form(10)):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Extract minimal text to validate content volume
            preview_text = " ".join(list(extract_text_from_pdf(tmp_path))[:5])
            if len(preview_text.strip()) < 800:
                raise HTTPException(status_code=400, detail="PDF has insufficient extractable text. Please provide a text-based PDF or run OCR.")
            
            # Store chunks best-effort
            try:
                store_text_chunks(extract_text_from_pdf(tmp_path), file.filename or "unknown.pdf")
            except Exception as e:
                print(f"WARN: store_text_chunks failed: {e}")

            # Generate
            quiz_text = generate_quiz(extract_text_from_pdf(tmp_path), level=level, num_questions=questions)
            _raise_if_gemini_error(quiz_text, "generation")
            
            # Primary parse
            quiz_json = parse_quiz_to_json(quiz_text, file.filename or "unknown.pdf")
            
            # If too few questions parsed, attempt reformat pass then re-parse
            if len(quiz_json.get("questions", [])) < max(3, int(min(questions, 10) * 0.6)):
                reformatted = reformat_quiz_output(quiz_text, num_questions=questions)
                _raise_if_gemini_error(reformatted, "reformat")
                try:
                    reformatted_parsed = parse_quiz_to_json(reformatted, file.filename or "unknown.pdf")
                except Exception as e:
                    print(f"WARN: reformat parse failed: {e}")
                    reformatted_parsed = None
                if reformatted_parsed and len(reformatted_parsed.get("questions", [])) >= len(quiz_json.get("questions", [])):
                    quiz_json = reformatted_parsed

            # Optional refinement; keep the better of the two
            try:
                refined_quiz_text = refine_quiz(quiz_text) or ""
                if refined_quiz_text:
                    # ignore refine errors silently
                    refined_parsed = parse_quiz_to_json(refined_quiz_text, file.filename or "unknown.pdf")
                    if refined_parsed and len(refined_parsed.get("questions", [])) >= len(quiz_json.get("questions", [])):
                        quiz_json = refined_parsed
            except Exception as e:
                print(f"WARN: refine failed: {e}")

            print(f"DEBUG: Generated {len(quiz_json.get('questions', []))} questions")
            print(f"DEBUG: Quiz JSON structure: {quiz_json}")
            return JSONResponse(content=quiz_json)
            
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception as e:
                    print(f"WARN: tmp cleanup failed: {e}")
                
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Unhandled in /quiz/upload: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/generate-text")
async def generate_from_text(text: str = Form(...), level: str = Form("intermediate"), questions: int = Form(10)):
    try:
        if len((text or "").strip()) < 400:
            raise HTTPException(status_code=400, detail="Text is too short to generate a quality quiz. Provide more content.")

        # Generate from text
        quiz_text = generate_quiz_from_text(text, level=level, num_questions=questions)
        _raise_if_gemini_error(quiz_text, "generation")
        quiz_json = parse_quiz_to_json(quiz_text, "pasted_text")

        # Reformat pass if needed
        if len(quiz_json.get("questions", [])) < max(3, int(min(questions, 10) * 0.6)):
            reformatted = reformat_quiz_output(quiz_text, num_questions=questions)
            _raise_if_gemini_error(reformatted, "reformat")
            try:
                reformatted_parsed = parse_quiz_to_json(reformatted, "pasted_text")
            except Exception as e:
                print(f"WARN: reformat parse failed: {e}")
                reformatted_parsed = None
            if reformatted_parsed and len(reformatted_parsed.get("questions", [])) >= len(quiz_json.get("questions", [])):
                quiz_json = reformatted_parsed

        # Optional refinement
        try:
            refined_quiz_text = refine_quiz(quiz_text) or ""
            if refined_quiz_text:
                refined_parsed = parse_quiz_to_json(refined_quiz_text, "pasted_text")
                if refined_parsed and len(refined_parsed.get("questions", [])) >= len(quiz_json.get("questions", [])):
                    quiz_json = refined_parsed
        except Exception as e:
            print(f"WARN: refine failed: {e}")

        print(f"DEBUG: Generated {len(quiz_json.get('questions', []))} questions from text input")
        return JSONResponse(content=quiz_json)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Unhandled in /quiz/generate-text: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating from text: {str(e)}")
