import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Paper,
  Chip,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import { DashboardLayout } from '../components/DashboardLayout';
import { getPostQuizAnalysis } from '../api/quizzes';

export const QuizResults = () => {
  const { quizId, attemptId } = useParams();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      if (!attemptId) return;
      try {
        const data = await getPostQuizAnalysis(parseInt(attemptId));
        setAnalysis(data);
      } catch (err) {
        setError('Failed to fetch quiz analysis.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [attemptId]);

  if (loading) {
    return (
      <DashboardLayout>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 6 }}>
          <CircularProgress sx={{ color: 'primary.main' }} />
        </Box>
      </DashboardLayout>
    );
  }

  if (error || !analysis) {
    return (
      <DashboardLayout>
        <Box sx={{ mt: 4 }}>
          <Alert severity="error">{error || 'Analysis not found.'}</Alert>
        </Box>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <Box sx={{ py: 4, px: { xs: 2, sm: 3, md: 4 } }}>
        <Typography variant="h3" sx={{
          fontWeight: 800,
          background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          mb: 2,
        }}>
          Quiz Results
        </Typography>

        <Paper
          sx={{
            p: 4,
            mb: 4,
            backgroundColor: 'rgba(10, 10, 10, 0.85)',
            border: '1px solid rgba(139, 92, 246, 0.2)',
            borderRadius: 3,
            textAlign: 'center',
            backdropFilter: 'blur(8px)'
          }}
        >
          <Typography variant="h3" sx={{ mb: 2, fontWeight: 'bold' }}>
            {analysis.score} / {analysis.total}
          </Typography>
          <Typography variant="h5" sx={{ mb: 2, color: 'rgba(255, 255, 255, 0.7)' }}>
            {analysis.accuracy.toFixed(1)}% Accuracy
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            {analysis.overall_feedback}
          </Typography>
        </Paper>

        <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
          Detailed Analysis
        </Typography>

        {analysis.explanations.map((explanation) => (
          <Accordion
            key={explanation.question_id}
            defaultExpanded={!explanation.is_correct}
            sx={{
              mb: 2,
              backgroundColor: 'rgba(10, 10, 10, 0.8)',
              border: '1px solid rgba(139, 92, 246, 0.2)',
              borderRadius: 2,
              '&:before': { display: 'none' },
            }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon sx={{ color: '#8b5cf6' }} />}
              sx={{ '& .MuiAccordionSummary-content': { alignItems: 'center' } }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                {explanation.is_correct ? (
                  <CheckCircleIcon sx={{ color: '#4ade80', fontSize: 28 }} />
                ) : (
                  <CancelIcon sx={{ color: '#f87171', fontSize: 28 }} />
                )}
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h6">Question {explanation.question_id}</Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                    Your answer: {explanation.user_answer}
                    {!explanation.is_correct && ` | Correct: ${explanation.correct_answer}`}
                  </Typography>
                </Box>
                <Chip label={explanation.is_correct ? 'Correct' : 'Incorrect'} color={explanation.is_correct ? 'success' : 'error'} size="small" />
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Box sx={{ pl: 4 }}>
                <Typography variant="body1" sx={{ mb: 3, color: 'rgba(255, 255, 255, 0.9)' }}>
                  {explanation.explanation}
                </Typography>
              </Box>
            </AccordionDetails>
          </Accordion>
        ))}

        <Box sx={{ display: 'flex', gap: 2, mt: 4 }}>
          <Button
            variant="outlined"
            onClick={() => navigate('/dashboard')}
            sx={{
              borderColor: 'rgba(139, 92, 246, 0.3)',
              color: '#8b5cf6',
              textTransform: 'none',
              '&:hover': { borderColor: '#8b5cf6', backgroundColor: 'rgba(139, 92, 246, 0.1)' },
            }}
          >
            Back to Dashboard
          </Button>
          <Button
            variant="contained"
            onClick={() => navigate(`/quiz/${quizId}`)}
            sx={{
              background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 700,
              '&:hover': { background: 'linear-gradient(135deg, #7c3aed 0%, #9333ea 100%)' },
            }}
          >
            Retake Quiz
          </Button>
        </Box>
      </Box>
    </DashboardLayout>
  );
};

