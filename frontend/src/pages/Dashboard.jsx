import React, { useEffect, useState } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  CircularProgress, 
  Alert, 
  Paper,
  Card,
  CardContent,
  Fade,
  Grow,
  useTheme,
  alpha
} from '@mui/material';
import { 
  TrendingUp, 
  Assessment, 
  History, 
  Quiz as QuizIcon,
  Speed,
  TrackChanges,
  BarChart as BarChartIcon
} from '@mui/icons-material';
import { DashboardLayout } from '../components/DashboardLayout';
import { QuizCard } from '../components/QuizCard';
import { AnalyticsChart } from '../components/AnalyticsChart';
import { HistoryTable } from '../components/HistoryTable';
import { AnalyticsSummary } from '../components/AnalyticsSummary';
import { getQuizzes, getUserAttempts, getAnalyticsSummary } from '../api/quizzes';

export const Dashboard = () => {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quizAttempts, setQuizAttempts] = useState([]);
  const [summary, setSummary] = useState(null);
  const theme = useTheme();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [qz, attempts, sum] = await Promise.all([
          getQuizzes(),
          getUserAttempts().catch(() => []),
          getAnalyticsSummary().catch(() => null)
        ]);
        setQuizzes(qz);
        setQuizAttempts(attempts || []);
        setSummary(sum);
      } catch (err) {
        setError('Failed to load dashboard data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <Box 
          sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            minHeight: '60vh',
            flexDirection: 'column',
            gap: 2
          }}
        >
          <CircularProgress 
            size={60} 
            sx={{ 
              color: 'primary.main',
              '& .MuiCircularProgress-circle': {
                strokeLinecap: 'round',
              }
            }} 
          />
          <Typography variant="body1" sx={{ color: 'text.secondary' }}>
            Loading your dashboard...
          </Typography>
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

  const StatCard = ({ icon: Icon, label, value, color, delay = 0 }) => (
    <Grow in={true} timeout={600 + delay}>
      <Card
        sx={{
          height: '100%',
          background: `linear-gradient(135deg, ${alpha(color, 0.1)} 0%, ${alpha(color, 0.05)} 100%)`,
          backdropFilter: 'blur(10px)',
          border: `1px solid ${alpha(color, 0.2)}`,
          borderRadius: 3,
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: `0 8px 24px ${alpha(color, 0.3)}`,
            border: `1px solid ${alpha(color, 0.4)}`,
          },
        }}
      >
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
            <Box
              sx={{
                p: 1.5,
                borderRadius: 2,
                background: `linear-gradient(135deg, ${alpha(color, 0.2)} 0%, ${alpha(color, 0.1)} 100%)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Icon sx={{ color, fontSize: 28 }} />
            </Box>
            <Box sx={{ flex: 1 }}>
              <Typography variant="caption" sx={{ color: 'text.secondary', textTransform: 'uppercase', letterSpacing: 1 }}>
                {label}
              </Typography>
              <Typography variant="h5" sx={{ fontWeight: 700, color: 'text.primary', mt: 0.5 }}>
                {value}
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Grow>
  );

  return (
    <DashboardLayout>
      <Box sx={{ py: 4, px: { xs: 2, sm: 3, md: 4 } }}>
        {/* Header Section */}
        <Fade in={true} timeout={800}>
          <Box sx={{ mb: 5 }}>
            <Typography 
              variant="h3" 
              component="h1" 
              sx={{ 
                fontWeight: 800,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 1,
                letterSpacing: '-0.02em',
              }}
            >
              Dashboard
            </Typography>
            <Typography variant="body1" sx={{ color: 'text.secondary', maxWidth: 600 }}>
              Track your progress, analyze your performance, and discover insights about your ethical reasoning journey.
            </Typography>
          </Box>
        </Fade>

        {/* Stats Cards */}
        {summary && summary.has_data && (
          <Fade in={true} timeout={1000}>
            <Grid container spacing={3} sx={{ mb: 5 }}>
              <Grid item xs={12} sm={6} md={3}>
                <StatCard
                  icon={Assessment}
                  label="Total Attempts"
                  value={summary.attempts_count || 0}
                  color="#8b5cf6"
                  delay={0}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <StatCard
                  icon={TrendingUp}
                  label="Last Accuracy"
                  value={`${(summary.last_accuracy || 0).toFixed(1)}%`}
                  color="#a78bfa"
                  delay={100}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <StatCard
                  icon={Speed}
                  label="Consistency"
                  value={`${(summary.consistency_score || 0).toFixed(0)}/100`}
                  color="#6366f1"
                  delay={200}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <StatCard
                  icon={TrackChanges}
                  label="Target"
                  value={`${(summary.target_next_accuracy || 0).toFixed(1)}%`}
                  color="#8b5cf6"
                  delay={300}
                />
              </Grid>
            </Grid>
          </Fade>
        )}

        {/* Quizzes Section */}
        <Fade in={true} timeout={1200}>
          <Box sx={{ mb: 5 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Box
                sx={{
                  p: 1.5,
                  borderRadius: 2,
                  background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(167, 139, 250, 0.2) 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <QuizIcon sx={{ color: '#8b5cf6', fontSize: 28 }} />
              </Box>
              <Typography 
                variant="h4" 
                component="h2"
                sx={{ 
                  fontWeight: 700,
                  color: 'text.primary',
                }}
              >
                Available Quizzes
              </Typography>
            </Box>
            <Grid container spacing={3}>
              {quizzes.length > 0 ? (
                quizzes.map((quiz, index) => (
                  <Grid item key={quiz.id} xs={12} sm={6} md={4}>
                    <Grow in={true} timeout={800 + index * 100}>
                      <Box>
                        <QuizCard quiz={quiz} />
                      </Box>
                    </Grow>
                  </Grid>
                ))
              ) : (
                <Grid item xs={12}>
                  <Paper
                    sx={{
                      p: 4,
                      textAlign: 'center',
                      background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
                      border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
                      borderRadius: 3,
                    }}
                  >
                    <QuizIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                    <Typography variant="h6" sx={{ color: 'text.secondary', mb: 1 }}>
                      No quizzes available
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Try creating or generating a new quiz to get started!
                    </Typography>
                  </Paper>
                </Grid>
              )}
            </Grid>
          </Box>
        </Fade>

        {/* Analytics Section */}
        <Fade in={true} timeout={1400}>
          <Box sx={{ mb: 5 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Box
                sx={{
                  p: 1.5,
                  borderRadius: 2,
                  background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(167, 139, 250, 0.2) 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <BarChartIcon sx={{ color: '#8b5cf6', fontSize: 28 }} />
              </Box>
              <Typography 
                variant="h4" 
                component="h2"
                sx={{ 
                  fontWeight: 700,
                  color: 'text.primary',
                }}
              >
                Performance Analytics
              </Typography>
            </Box>
            <Grid container spacing={3}>
              <Grid item xs={12} md={5}>
                <AnalyticsSummary summary={summary} />
              </Grid>
              <Grid item xs={12} md={7}>
                {quizAttempts.length > 0 ? (
                  <AnalyticsChart attempts={quizAttempts} summary={summary} />
                ) : (
                  <Paper
                    sx={{
                      p: 4,
                      textAlign: 'center',
                      background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
                      border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
                      borderRadius: 3,
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <BarChartIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                    <Typography variant="h6" sx={{ color: 'text.secondary', mb: 1 }}>
                      No data yet
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Take some quizzes to see your analytics!
                    </Typography>
                  </Paper>
                )}
              </Grid>
            </Grid>
          </Box>
        </Fade>

        {/* History Section */}
        <Fade in={true} timeout={1600}>
          <Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
              <Box
                sx={{
                  p: 1.5,
                  borderRadius: 2,
                  background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(167, 139, 250, 0.1) 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <History sx={{ color: '#8b5cf6', fontSize: 28 }} />
              </Box>
              <Typography 
                variant="h4" 
                component="h2"
                sx={{ 
                  fontWeight: 700,
                  color: 'text.primary',
                }}
              >
                Quiz History
              </Typography>
            </Box>
            {quizAttempts.length > 0 ? (
              <HistoryTable attempts={quizAttempts} />
            ) : (
              <Paper
                sx={{
                  p: 4,
                  textAlign: 'center',
                  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
                  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
                  borderRadius: 3,
                }}
              >
                <History sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" sx={{ color: 'text.secondary', mb: 1 }}>
                  No quiz history yet
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  Start taking quizzes to build your history!
                </Typography>
              </Paper>
            )}
          </Box>
        </Fade>
      </Box>
    </DashboardLayout>
  );
};
