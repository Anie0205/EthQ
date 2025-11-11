import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  RadioGroup,
  FormControlLabel,
  Radio,
  CircularProgress,
  Alert,
  TextField,
  Paper,
  Collapse,
  IconButton,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { DashboardLayout } from '../components/DashboardLayout';
import { getQuizById, submitQuizAnswers, explainQuestionConflict } from '../api/quizzes';

export const Quiz = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [justifications, setJustifications] = useState({});
  const [submissionStatus, setSubmissionStatus] = useState(null);
  const [expandedQuestions, setExpandedQuestions] = useState({});
  const [conflictExplanations, setConflictExplanations] = useState({});
  const [loadingExplanations, setLoadingExplanations] = useState({});

  useEffect(() => {
    const fetchQuiz = async () => {
      if (!quizId) return;
      try {
        const data = await getQuizById(parseInt(quizId));
        setQuiz(data);
      } catch (err) {
        setError('Failed to fetch quiz.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchQuiz();
  }, [quizId]);

  const handleAnswerChange = (questionId, answer) => {
    setSelectedAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleJustificationChange = (questionId, justification) => {
    setJustifications(prev => ({ ...prev, [questionId]: justification }));
  };

  const toggleQuestionExpansion = (questionId) => {
    setExpandedQuestions(prev => ({
      ...prev,
      [questionId]: !prev[questionId]
    }));
  };

  const handleExplainConflict = async (questionId) => {
    if (conflictExplanations[questionId]) {
      toggleQuestionExpansion(questionId);
      return;
    }

    setLoadingExplanations(prev => ({ ...prev, [questionId]: true }));
    try {
      const explanation = await explainQuestionConflict(parseInt(quizId), questionId);
      setConflictExplanations(prev => ({ ...prev, [questionId]: explanation }));
      setExpandedQuestions(prev => ({ ...prev, [questionId]: true }));
    } catch (err) {
      console.error('Failed to get explanation:', err);
      setError('Failed to load explanation. Please try again.');
    } finally {
      setLoadingExplanations(prev => ({ ...prev, [questionId]: false }));
    }
  };

  const handleSubmitQuiz = async () => {
    if (!quizId) return;
    setSubmissionStatus(null);
    try {
      const result = await submitQuizAnswers(
        parseInt(quizId),
        selectedAnswers,
        justifications
      );
      navigate(`/quiz/${quizId}/results/${result.id}`);
    } catch (err) {
      setSubmissionStatus('Failed to submit quiz.');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 6 }}>
          <CircularProgress sx={{ color: 'primary.main' }} />
        </Box>
      </DashboardLayout>
    );
  }

  if (error && !quiz) {
    return (
      <DashboardLayout>
        <Box sx={{ mt: 4 }}>
          <Alert severity="error">{error}</Alert>
        </Box>
      </DashboardLayout>
    );
  }

  if (!quiz) {
    return (
      <DashboardLayout>
        <Box sx={{ mt: 4 }}>
          <Alert severity="info">Quiz not found.</Alert>
        </Box>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Box sx={{ py: 4, px: { xs: 2, sm: 3, md: 4 } }}>
        <Box sx={{ mb: 2 }}>
          <Typography variant="h3" sx={{
            fontWeight: 800,
            background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>{quiz.title}</Typography>
          <Typography variant="h6" component="h2" sx={{ color: 'text.secondary', mb: 4 }}>
            Category: {quiz.category}
          </Typography>
        </Box>

        {quiz.questions.map((question, qIndex) => {
          const questionId = question.id;
          const isExpanded = expandedQuestions[questionId];
          const explanation = conflictExplanations[questionId];
          const loadingExplanation = loadingExplanations[questionId];

          return (
            <Paper
              key={question.id}
              sx={{
                mb: 3,
                p: 3,
                backgroundColor: 'rgba(10, 10, 10, 0.8)',
                border: '1px solid rgba(139, 92, 246, 0.2)',
                borderRadius: 3,
                backdropFilter: 'blur(6px)'
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6" sx={{ flexGrow: 1, mb: 2 }}>
                  {qIndex + 1}. {question.question_text}
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<HelpOutlineIcon />}
                  onClick={() => handleExplainConflict(questionId)}
                  disabled={loadingExplanation}
                  sx={{
                    ml: 2,
                    borderColor: 'rgba(139, 92, 246, 0.3)',
                    color: '#8b5cf6',
                    textTransform: 'none',
                    '&:hover': {
                      borderColor: '#8b5cf6',
                      backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    },
                  }}
                >
                  {loadingExplanation ? 'Loading...' : explanation ? 'Hide Explanation' : 'Explain Conflict'}
                </Button>
              </Box>

              <RadioGroup
                aria-label={`question-${question.id}`}
                name={`question-${question.id}`}
                value={selectedAnswers[question.id] || ''}
                onChange={(event) => handleAnswerChange(question.id, event.target.value)}
                sx={{ mb: 2 }}
              >
                {question.options.map((option, oIndex) => (
                  <FormControlLabel
                    key={oIndex}
                    value={option}
                    control={<Radio sx={{ color: '#8b5cf6' }} />}
                    label={option}
                    sx={{
                      mb: 1,
                      '& .MuiFormControlLabel-label': {
                        color: 'rgba(255, 255, 255, 0.9)',
                      },
                    }}
                  />
                ))}
              </RadioGroup>

              <TextField
                fullWidth
                multiline
                minRows={2}
                maxRows={4}
                label="Why did you choose this answer? (Optional)"
                value={justifications[question.id] || ''}
                onChange={(e) => handleJustificationChange(question.id, e.target.value)}
                sx={{
                  mb: 2,
                  '& .MuiOutlinedInput-root': {
                    color: 'white',
                    '& fieldset': { borderColor: 'rgba(255, 255, 255, 0.2)' },
                    '&:hover fieldset': { borderColor: 'rgba(139, 92, 246, 0.4)' },
                    '&.Mui-focused fieldset': { borderColor: '#8b5cf6' },
                  },
                  '& .MuiInputLabel-root': {
                    color: 'rgba(255, 255, 255, 0.7)',
                    '&.Mui-focused': { color: '#8b5cf6' },
                  },
                }}
              />

              <Collapse in={isExpanded && !!explanation}>
                {explanation && (
                  <Paper
                    sx={{
                      p: 3,
                      mt: 2,
                      backgroundColor: 'rgba(139, 92, 246, 0.05)',
                      border: '1px solid rgba(139, 92, 246, 0.2)',
                      borderRadius: 2,
                    }}
                  >
                    <Typography variant="h6" gutterBottom sx={{ color: '#c4b5fd', mb: 2 }}>
                      Ethical Conflict Analysis
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 3, color: 'rgba(255, 255, 255, 0.9)' }}>
                      {explanation.explanation}
                    </Typography>
                  </Paper>
                )}
              </Collapse>
            </Paper>
          );
        })}

        <Button
          variant="contained"
          onClick={handleSubmitQuiz}
          sx={{
            mt: 3,
            px: 4,
            py: 1.5,
            background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
            borderRadius: 2,
            textTransform: 'none',
            fontSize: '1rem',
            fontWeight: 700,
            boxShadow: '0 4px 14px rgba(139, 92, 246, 0.25)',
            '&:hover': {
              background: 'linear-gradient(135deg, #7c3aed 0%, #9333ea 100%)',
              transform: 'translateY(-1px)',
              boxShadow: '0 6px 20px rgba(139, 92, 246, 0.35)',
            },
            transition: 'all 0.2s ease',
          }}
        >
          Submit Quiz
        </Button>

        {submissionStatus && (
          <Alert severity={submissionStatus.includes('Failed') ? 'error' : 'success'} sx={{ mt: 3 }}>
            {submissionStatus}
          </Alert>
        )}
      </Box>
    </DashboardLayout>
  );
};
