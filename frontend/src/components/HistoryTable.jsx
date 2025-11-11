import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export const HistoryTable = ({ attempts }) => {
  const navigate = useNavigate();

  const handleRetakeQuiz = (quizId) => {
    navigate(`/quiz/${quizId}`);
  };

  return (
    <TableContainer component={Paper}>
      <Typography variant="h6" component="div" sx={{ p: 2 }}>
        Quiz History
      </Typography>
      <Table sx={{ minWidth: 650 }} aria-label="quiz history table">
        <TableHead>
          <TableRow>
            <TableCell>Quiz ID</TableCell>
            <TableCell align="right">Score</TableCell>
            <TableCell align="right">Total Questions</TableCell>
            <TableCell align="right">Accuracy (%)</TableCell>
            <TableCell align="right">Timestamp</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {attempts.map((attempt) => (
            <TableRow
              key={attempt.quiz_id + "-" + attempt.timestamp}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {attempt.quiz_id}
              </TableCell>
              <TableCell align="right">{attempt.score}</TableCell>
              <TableCell align="right">{attempt.total}</TableCell>
              <TableCell align="right">{attempt.accuracy.toFixed(2)}</TableCell>
              <TableCell align="right">{new Date(attempt.timestamp).toLocaleString()}</TableCell>
              <TableCell align="right">
                <Button variant="outlined" size="small" onClick={() => handleRetakeQuiz(attempt.quiz_id)}>
                  Retake
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
