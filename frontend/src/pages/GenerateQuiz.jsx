import React, { useState } from 'react';
import { Box, Typography, Button, Paper, Grid, Alert, TextField, MenuItem, Switch, FormControlLabel } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { DashboardLayout } from '../components/DashboardLayout';
import { uploadQuizPDF, createQuiz, generateQuizFromText } from '../api/quizzes';

export const GenerateQuiz = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [generated, setGenerated] = useState(null);
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('');
  const [level, setLevel] = useState('intermediate');
  const [questions, setQuestions] = useState(10);
  const [status, setStatus] = useState(null);
  const [useText, setUseText] = useState(false);
  const [textInput, setTextInput] = useState('');

  const handleUpload = async () => {
    setLoading(true);
    setError(null);
    setGenerated(null);
    setStatus(null);
    try {
      let result;
      if (useText) {
        if (!textInput.trim()) {
          setError('Please paste text to generate from.');
          setLoading(false);
          return;
        }
        result = await generateQuizFromText({ text: textInput, level, questions });
      } else {
        if (!file) {
          setError('Please select a PDF file.');
          setLoading(false);
          return;
        }
        const formData = new FormData();
        formData.append('file', file);
        formData.append('level', level);
        formData.append('questions', String(questions));
        result = await uploadQuizPDF(formData);
      }
      setGenerated(result);
      setTitle(result?.title || 'Generated Quiz');
      if (!category) setCategory('');
    } catch (e) {
      console.error(e);
      setError('Failed to generate quiz. Ensure backend is running and GEMINI_API_KEY is set.');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (redirectToQuiz = false) => {
    if (!generated) return;
    setSaving(true);
    setStatus(null);
    setError(null);
    try {
      if (!generated.questions || generated.questions.length === 0) {
        throw new Error('No questions to save');
      }

      const questionsArr = (generated.questions || []).map((q, idx) => {
        const questionText = q.question || q.question_text || '';
        const options = q.options || [];
        const correctAnswer = q.answer || q.correct_answer || '';
        if (!questionText || options.length === 0 || !correctAnswer) {
          throw new Error(`Question ${idx + 1} is missing required fields`);
        }
        return {
          id: q.id ?? idx + 1,
          question_text: questionText,
          options: options,
          correct_answer: correctAnswer
        };
      });

      const payload = { 
        title: title || 'Generated Quiz', 
        category: category || 'Uncategorized', 
        questions: questionsArr 
      };
      const savedQuiz = await createQuiz(payload);
      setStatus({ type: 'success', message: 'Quiz saved successfully!' });
      if (redirectToQuiz) {
        setTimeout(() => navigate(`/quiz/${savedQuiz.id}`), 1000);
      } else {
        setTimeout(() => navigate('/dashboard'), 1500);
      }
    } catch (e) {
      console.error('Save error:', e);
      const errorMessage = e.response?.data?.detail || e.message || 'Failed to save quiz. Please check the console for details.';
      setStatus({ type: 'error', message: errorMessage });
      setError(errorMessage);
    } finally {
      setSaving(false);
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
            Generate Quiz
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary', maxWidth: 700 }}>
            Upload a PDF or paste text and let AI generate a tailored quiz for you.
          </Typography>
        </Box>

        <Paper sx={{ p: 3, mb: 3, backgroundColor: 'rgba(10, 10, 10, 0.85)', border: '1px solid rgba(139, 92, 246, 0.2)', borderRadius: 3, backdropFilter: 'blur(8px)' }}>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12}>
              <FormControlLabel control={<Switch checked={useText} onChange={(e) => setUseText(e.target.checked)} />} label="Use pasted text instead of PDF" />
            </Grid>

            {!useText && (
              <Grid item xs={12} md={5}>
                <Button variant="outlined" component="label" fullWidth sx={{
                  borderColor: 'rgba(139, 92, 246, 0.3)',
                  color: '#8b5cf6',
                  textTransform: 'none',
                  '&:hover': { borderColor: '#8b5cf6', backgroundColor: 'rgba(139, 92, 246, 0.08)' }
                }}>
                  {file ? file.name : 'Select PDF file'}
                  <input type="file" accept="application/pdf" hidden onChange={(e) => setFile(e.target.files?.[0] || null)} />
                </Button>
              </Grid>
            )}

            {useText && (
              <Grid item xs={12}>
                <TextField
                  label="Paste text here"
                  fullWidth
                  multiline
                  minRows={6}
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                />
              </Grid>
            )}

            <Grid item xs={12} md={3}>
              <TextField select label="Level" fullWidth value={level} onChange={(e) => setLevel(e.target.value)}>
                <MenuItem value="beginner">Beginner</MenuItem>
                <MenuItem value="intermediate">Intermediate</MenuItem>
                <MenuItem value="advanced">Advanced</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField type="number" label="# Questions" fullWidth inputProps={{ min: 1, max: 20 }} value={questions} onChange={(e) => setQuestions(Number(e.target.value))} />
            </Grid>
            <Grid item xs={12} md={2}>
              <Button variant="contained" onClick={handleUpload} disabled={loading} fullWidth sx={{
                background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
                textTransform: 'none',
                fontWeight: 700,
              }}>
                {loading ? 'Generating...' : 'Generate'}
              </Button>
            </Grid>
            {error && (
              <Grid item xs={12}>
                <Alert severity="error">{error}</Alert>
              </Grid>
            )}
          </Grid>
        </Paper>

        {generated && (
          <Paper sx={{ p: 3, backgroundColor: 'rgba(10, 10, 10, 0.85)', border: '1px solid rgba(139, 92, 246, 0.2)', borderRadius: 3, backdropFilter: 'blur(8px)' }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField label="Title" fullWidth value={title} onChange={(e) => setTitle(e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField label="Category (optional)" fullWidth value={category} onChange={(e) => setCategory(e.target.value)} />
              </Grid>

              <Grid item xs={12}>
                <Typography variant="h6" sx={{ mb: 1, color: 'text.secondary' }}>Preview</Typography>
                {(generated.questions || []).map((q, idx) => (
                  <Box key={idx} sx={{ mb: 2, p: 2, border: '1px solid rgba(139, 92, 246, 0.25)', borderRadius: 2, backgroundColor: 'rgba(139, 92, 246, 0.05)' }}>
                    <Typography variant="subtitle1">{idx + 1}. {q.question || q.question_text}</Typography>
                    <ul>
                      {(q.options || []).map((opt, i) => (
                        <li key={i}>{opt}</li>
                      ))}
                    </ul>
                    <Typography variant="body2">Answer: {q.answer || q.correct_answer}</Typography>
                  </Box>
                ))}
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Button 
                    variant="contained" 
                    onClick={() => handleSave(false)} 
                    disabled={saving || !generated}
                    sx={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)', textTransform: 'none', fontWeight: 700 }}
                  >
                    {saving ? 'Saving...' : 'Save & Go to Dashboard'}
                  </Button>
                  <Button 
                    variant="outlined" 
                    onClick={() => handleSave(true)} 
                    disabled={saving || !generated}
                    sx={{ borderColor: 'rgba(139, 92, 246, 0.4)', color: '#8b5cf6', textTransform: 'none', fontWeight: 700 }}
                  >
                    {saving ? 'Saving...' : 'Save & Take Quiz Now'}
                  </Button>
                </Box>
              </Grid>

              {status && (
                <Grid item xs={12}>
                  <Alert severity={status.type === 'error' ? 'error' : 'success'}>{status.message}</Alert>
                </Grid>
              )}
            </Grid>
          </Paper>
        )}
      </Box>
    </DashboardLayout>
  );
};
