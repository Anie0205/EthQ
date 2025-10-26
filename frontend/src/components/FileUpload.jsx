import React, { useState } from "react";
import axios from "axios";
import QuizDisplay from "./QuizDisplay.jsx";
import "../App.css";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type === "application/pdf") {
        setFile(selectedFile);
        setError(null);
      } else {
        setError("Please select a PDF file");
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first");
      return;
    }

    setLoading(true);
    setError(null);
    setQuiz(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://localhost:8000/quiz/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("Quiz response:", res.data); // Debug log
      
      // Validate quiz structure
      if (res.data && res.data.questions && Array.isArray(res.data.questions) && res.data.questions.length > 0) {
        console.log(`Successfully loaded quiz with ${res.data.questions.length} questions`);
        setQuiz(res.data);
      } else {
        console.error("Invalid quiz structure received:", res.data);
        setError(`Invalid quiz data: ${JSON.stringify(res.data).substring(0, 100)}...`);
      }
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        "Failed to upload file. Make sure the backend server is running on http://localhost:8000"
      );
      console.error("Upload error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="file-input-wrapper">
        <input 
          type="file" 
          accept=".pdf"
          onChange={handleFileChange}
          disabled={loading}
        />
        {file && (
          <p style={{ marginTop: "10px", color: "#646cff" }}>
            Selected: {file.name}
          </p>
        )}
      </div>

      <button 
        onClick={handleUpload} 
        disabled={loading || !file}
        className="upload-button"
      >
        {loading ? "Processing..." : "Upload & Generate Quiz"}
      </button>

      {error && <div className="error">{error}</div>}

      {loading && <div className="loading">Generating quiz questions...</div>}

      {quiz && <QuizDisplay quiz={quiz} />}
    </div>
  );
}

export default FileUpload;
