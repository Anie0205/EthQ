# EthQ - Ethical Quiz Generator

A full-stack application that generates ethical quiz questions from PDF documents using AI.

## Project Structure

- `backend/` - FastAPI backend with AI quiz generation
- `frontend/` - React + Vite frontend

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv ethenv
```

3. Activate the virtual environment:
   - Windows:
   ```bash
   ethenv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source ethenv/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory with your API keys:
```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

6. Start the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be running at `http://localhost:8000`
API documentation available at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be running at `http://localhost:3000`

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Click "Choose File" and select a PDF document
3. Click "Upload & Generate Quiz"
4. Wait for the AI to process the document and generate quiz questions
5. View the generated ethical quiz questions

## API Endpoints

### POST `/quiz/upload`
Upload a PDF file and generate a quiz.

**Request:**
- Content-Type: multipart/form-data
- Body: file (PDF)

**Response:**
```json
{
  "quiz": "Generated quiz content",
  "filename": "example.pdf"
}
```

## Features

- PDF text extraction
- AI-powered quiz generation using Mistral AI
- Ethics filtering for appropriate content
- RAG (Retrieval Augmented Generation) for contextual questions
- Modern React UI with Vite
- FastAPI backend with CORS support

## Development

### Backend Development
- Uses FastAPI for the API
- Implements vector storage with ChromaDB
- Text extraction with PyMuPDF
- LLM integration with Mistral AI

### Frontend Development
- React 18
- Vite for fast development
- Axios for API calls
- Modern CSS styling

## Troubleshooting

### Backend not connecting
- Ensure the backend server is running on port 8000
- Check that all dependencies are installed
- Verify the MISTRAL_API_KEY is set correctly

### CORS errors
- The backend CORS is configured to allow all origins
- If issues persist, check the CORS middleware in `backend/main.py`

### File upload issues
- Ensure the file is a valid PDF
- Check file size limits
- Verify backend logs for errors

## License

MIT
