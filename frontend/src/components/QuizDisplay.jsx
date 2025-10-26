import React, { useState } from "react";
import "../App.css";

function QuizDisplay({ quiz }) {
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  // Safety check
  if (!quiz || !quiz.questions || !Array.isArray(quiz.questions)) {
    return <div className="error">Invalid quiz data received</div>;
  }

  const handleSelect = (qId, option) => {
    setAnswers({ ...answers, [qId]: option });
  };

  const handleSubmit = () => {
    setShowResults(true);
  };

  const score = quiz.questions.filter(
    q => answers[q.id] === q.answer
  ).length;

  const totalQuestions = quiz.questions.length;
  const percentage = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;

  return (
    <div className="quiz-display-container">
      <div className="quiz-header">
        <h2>{quiz.title}</h2>
        {!showResults && (
          <div className="progress-info">
            <span>Progress: {Object.keys(answers).length}/{totalQuestions} answered</span>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${(Object.keys(answers).length / totalQuestions) * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {quiz.questions.map(q => {
        const isCorrect = answers[q.id] === q.answer;
        const showAnswer = showResults;
        
        return (
          <div 
            key={q.id} 
            className={`question-card ${showAnswer ? (isCorrect ? 'correct' : 'incorrect') : ''}`}
          >
            <h3>Question {q.id}</h3>
            <p className="question-text">{q.question}</p>
            
            <div className="options-container">
              {q.options.map((opt, idx) => {
                const isSelected = answers[q.id] === opt;
                const isAnswer = showAnswer && opt === q.answer;
                
                return (
                  <label 
                    key={idx} 
                    className={`option-label ${isSelected ? 'selected' : ''} ${isAnswer ? 'correct-answer' : ''}`}
                  >
                    <input
                      type="radio"
                      name={`q${q.id}`}
                      value={opt}
                      checked={isSelected}
                      onChange={() => handleSelect(q.id, opt)}
                      disabled={showResults}
                    />
                    <span>{opt}</span>
                  </label>
                );
              })}
            </div>

            {showAnswer && q.explanation && (
              <div className="explanation">
                <strong>Explanation:</strong> {q.explanation}
              </div>
            )}
          </div>
        );
      })}

      <div className="quiz-footer">
        {!showResults ? (
          <button 
            onClick={handleSubmit}
            disabled={Object.keys(answers).length !== totalQuestions}
            className="submit-button"
          >
            Submit Quiz
          </button>
        ) : (
          <div className="results">
            <div className="score-display">
              <h2>Your Score: {score}/{totalQuestions}</h2>
              <div className="score-percentage">{percentage}%</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default QuizDisplay;
