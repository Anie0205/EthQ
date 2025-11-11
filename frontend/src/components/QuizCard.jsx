import React from 'react';
import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const QuizCard = ({ quiz }) => {
  const navigate = useNavigate();

  const handleTakeQuiz = () => {
    navigate(`/quiz/${quiz.id}`);
  };

  return (
    <Card sx={{ maxWidth: 345, mb: 2 }}>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {quiz.title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Category: {quiz.category}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Questions: {quiz.questions.length}
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Button variant="contained" onClick={handleTakeQuiz}>
            Take Quiz
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};
