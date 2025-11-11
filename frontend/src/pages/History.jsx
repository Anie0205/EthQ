import React, { useEffect, useState } from 'react';
import { Box, Typography, CircularProgress, Alert, Paper } from '@mui/material';
import { DashboardLayout } from '../components/DashboardLayout';
import { HistoryTable } from '../components/HistoryTable';
/* eslint-disable no-unused-vars */

// Placeholder for fetching user quiz attempts. In a real app, you'd have an API call here.
const fetchUserQuizAttempts = async () => {
  return [];
};

export const History = () => {
  const [attempts, setAttempts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getAttempts = async () => {
      try {
        const data = await fetchUserQuizAttempts(); // Replace with actual API call
        setAttempts(data);
      } catch (err) {
        setError('Failed to fetch quiz history.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    getAttempts();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 6 }}>
          <CircularProgress sx={{ color: 'primary.main' }} />
        </Box>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <Box sx={{ mt: 4 }}>
          <Alert severity="error" sx={{ borderRadius: 2 }}>{error}</Alert>
        </Box>
      </DashboardLayout>
    );
  }

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
            History
          </Typography>
          <Typography variant="body1" sx={{ color: 'text.secondary', maxWidth: 600 }}>
            Review your past quiz attempts and track improvement over time.
          </Typography>
        </Box>

        {attempts.length > 0 ? (
          <Paper
            sx={{
              p: 3,
              backgroundColor: 'rgba(10, 10, 10, 0.85)',
              border: '1px solid rgba(139, 92, 246, 0.2)',
              borderRadius: 3,
              backdropFilter: 'blur(8px)'
            }}
          >
            <HistoryTable attempts={attempts} />
          </Paper>
        ) : (
          <Paper
            sx={{
              p: 6,
              textAlign: 'center',
              background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(167, 139, 250, 0.08) 100%)',
              border: '1px solid rgba(139, 92, 246, 0.2)',
              borderRadius: 3,
            }}
          >
            <Typography variant="h6" sx={{ color: 'text.secondary', mb: 1 }}>
              No quiz attempts yet
            </Typography>
            <Typography variant="body2" sx={{ color: 'text.secondary' }}>
              Take your first quiz to populate your history.
            </Typography>
          </Paper>
        )}
      </Box>
    </DashboardLayout>
  );
};
