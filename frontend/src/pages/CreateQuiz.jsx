import React, { useState } from 'react';
import { Box, Typography, TextField, Button, Paper, Grid, IconButton } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { DashboardLayout } from '../components/DashboardLayout';
import { createQuiz } from '../api/quizzes';

export const CreateQuiz = () => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  const [questions, setQuestions] = useState([
    { question_text: '', optionsText: '', correct_answer: '' },
  ]);
  const [status, setStatus] = useState(null);

  const addQuestion = () => {
    setQuestions((prev) => [...prev, { question_text: '', optionsText: '', correct_answer: '' }]);
  };

  const removeQuestion = (idx) => {
    setQuestions((prev) => prev.filter((_, i) => i !== idx));
  };

  const updateQuestionField = (idx, field, value) => {
    setQuestions((prev) => prev.map((q, i) => (i === idx ? { ...q, [field]: value } : q)));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);

    try {
      const payload = {
        title,
        category,
        questions: questions.map((q, idx) => ({
          id: idx + 1,
          question_text: q.question_text.trim(),
          options: q.optionsText.split(',').map((s) => s.trim()).filter(Boolean),
          correct_answer: q.correct_answer.trim(),
        })),
      };

      await createQuiz(payload);
      setStatus({ type: 'success', message: 'Quiz created successfully.' });
      setTitle('');
      setCategory('');
      setQuestions([{ question_text: '', optionsText: '', correct_answer: '' }]);
    } catch (err) {
      console.error(err);
      setStatus({ type: 'error', message: 'Failed to create quiz.' });
    }
  };

  return (
    <DashboardLayout>
      <Box sx={{ py: 4, px: { xs: 2, sm: 3, md: 4 } }}>
        <Box sx={{ mb: 4 }}>
          <Typography 
            variant="h3" 
            component="h1" 
            sx={{ 
              fontWeight: 800,
              background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.02em',
            }}
          >
            Create Quiz
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary', maxWidth: 600 }}>
            Build a custom quiz with your own questions and answers.
          </Typography>
        </Box>

        <Paper sx={{ p: 3, backgroundColor: 'rgba(10, 10, 10, 0.85)', border: '1px solid rgba(139, 92, 246, 0.2)', borderRadius: 3, backdropFilter: 'blur(8px)' }}>
          <Box component="form" onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField label="Title" fullWidth required value={title} onChange={(e) => setTitle(e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Category" fullWidth required value={category} onChange={(e) => setCategory(e.target.value)} />
              </Grid>

              {questions.map((q, idx) => (
                <Grid item xs={12} key={idx}>
                  <Paper variant="outlined" sx={{ p: 2, borderColor: 'rgba(139, 92, 246, 0.2)', backgroundColor: 'rgba(10,10,10,0.6)' }}>
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={12}>
                        <Typography variant="subtitle1" sx={{ color: 'text.secondary' }}>Question {idx + 1}</Typography>
                      </Grid>
                      <Grid item xs={12}>
                        <TextField
                          label="Question Text"
                          fullWidth
                          required
                          value={q.question_text}
                          onChange={(e) => updateQuestionField(idx, 'question_text', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={12} md={8}>
                        <TextField
                          label="Options (comma-separated)"
                          fullWidth
                          required
                          value={q.optionsText}
                          onChange={(e) => updateQuestionField(idx, 'optionsText', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <TextField
                          label="Correct Answer"
                          fullWidth
                          required
                          value={q.correct_answer}
                          onChange={(e) => updateQuestionField(idx, 'correct_answer', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <IconButton color="error" onClick={() => removeQuestion(idx)} disabled={questions.length === 1} sx={{ mr: 1 }}>
                          <DeleteIcon />
                        </IconButton>
                        <IconButton color="primary" onClick={addQuestion}>
                          <AddIcon />
                        </IconButton>
                      </Grid>
                    </Grid>
                  </Paper>
                </Grid>
              ))}

              <Grid item xs={12}>
                <Button type="submit" variant="contained" sx={{
                  px: 4,
                  py: 1.25,
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
                  borderRadius: 2,
                  textTransform: 'none',
                  fontWeight: 700,
                }}>Create Quiz</Button>
              </Grid>

              {status && (
                <Grid item xs={12}>
                  <Typography color={status.type === 'error' ? 'error' : 'primary'}>{status.message}</Typography>
                </Grid>
              )}
            </Grid>
          </Box>
        </Paper>
      </Box>
    </DashboardLayout>
  );
};
