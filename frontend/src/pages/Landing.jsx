import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  AppBar,
  Toolbar,
  Grid,
  Card,
  CardContent,
  Paper,
} from '@mui/material';
import QuizIcon from '@mui/icons-material/Quiz';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import SchoolIcon from '@mui/icons-material/School';

export const Landing = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #000000 0%, #0a0a0a 50%, #000000 100%)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Grid Background Pattern */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: `
            linear-gradient(rgba(139, 92, 246, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(139, 92, 246, 0.08) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
          opacity: 0.2,
        }}
      />

      {/* Navigation Bar */}
      <AppBar
        position="static"
        sx={{
          backgroundColor: 'transparent',
          borderBottom: '1px solid rgba(139, 92, 246, 0.15)',
        }}
      >
        <Container maxWidth="lg">
          <Toolbar sx={{ justifyContent: 'space-between', py: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <QuizIcon
                sx={{
                  color: '#8b5cf6',
                  fontSize: 32,
                }}
              />
              <Typography
                variant="h5"
                component="div"
                sx={{
                  fontWeight: 'bold',
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                EthQ
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 4, alignItems: 'center' }}>
              <Typography
                variant="body1"
                sx={{
                  color: 'rgba(255, 255, 255, 0.7)',
                  cursor: 'pointer',
                  transition: 'color 0.2s ease',
                  '&:hover': {
                    color: '#a78bfa',
                  },
                }}
              >
                Features
              </Typography>
              <Typography
                variant="body1"
                sx={{
                  color: 'rgba(255, 255, 255, 0.7)',
                  cursor: 'pointer',
                  transition: 'color 0.2s ease',
                  '&:hover': {
                    color: '#a78bfa',
                  },
                }}
              >
                About
              </Typography>
              <Button
                variant="outlined"
                onClick={() => navigate('/login')}
                sx={{
                  borderColor: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    borderColor: 'rgba(139, 92, 246, 0.6)',
                    backgroundColor: 'rgba(139, 92, 246, 0.05)',
                  },
                }}
              >
                Sign In
              </Button>
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      {/* Hero Section */}
      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1, py: 12 }}>
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          {/* Banner */}
          <Paper
            sx={{
              display: 'inline-block',
              px: 3,
              py: 1,
              mb: 3,
              backgroundColor: 'rgba(139, 92, 246, 0.08)',
              border: '1px solid rgba(139, 92, 246, 0.3)',
              borderRadius: 2,
            }}
          >
            <Typography
              variant="body2"
              sx={{
                color: '#c4b5fd',
                fontWeight: 500,
              }}
            >
              AI-Powered Quiz Platform • Get Started Free Today
            </Typography>
          </Paper>

          {/* Main Headline */}
          <Typography
            variant="h1"
            sx={{
              fontSize: { xs: '3rem', md: '4.5rem' },
              fontWeight: 'bold',
              color: 'white',
              mb: 3,
              lineHeight: 1.2,
            }}
          >
            Master Ethics Through
            <br />
            <Box
              component="span"
              sx={{
                background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Intelligent Quizzes
            </Box>
          </Typography>

          {/* Sub-headline */}
          <Typography
            variant="h5"
            sx={{
              color: 'rgba(255, 255, 255, 0.7)',
              mb: 5,
              maxWidth: '700px',
              mx: 'auto',
              lineHeight: 1.6,
            }}
          >
            Transform your learning experience with AI-generated quizzes. Upload PDFs, generate
            questions instantly, and track your progress with detailed analytics.
          </Typography>

          {/* CTA Buttons */}
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/login')}
              sx={{
                px: 4,
                py: 1.5,
                fontSize: '1.1rem',
                background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
                borderRadius: 2,
                textTransform: 'none',
                boxShadow: '0 4px 14px rgba(139, 92, 246, 0.25)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #7c3aed 0%, #9333ea 100%)',
                  transform: 'translateY(-1px)',
                  boxShadow: '0 6px 20px rgba(139, 92, 246, 0.35)',
                },
                transition: 'all 0.2s ease',
              }}
            >
              Get Started Free
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/login')}
              sx={{
                px: 4,
                py: 1.5,
                fontSize: '1.1rem',
                borderColor: 'rgba(255, 255, 255, 0.3)',
                color: 'white',
                borderRadius: 3,
                textTransform: 'none',
                '&:hover': {
                  borderColor: 'rgba(139, 92, 246, 0.6)',
                  backgroundColor: 'rgba(139, 92, 246, 0.05)',
                  transform: 'translateY(-1px)',
                },
                transition: 'all 0.3s ease',
              }}
            >
              View Demo
            </Button>
          </Box>
        </Box>

        {/* Features Grid */}
        <Grid container spacing={4} sx={{ mt: 8, mb: 12 }}>
          <Grid item xs={12} md={3}>
            <Card
              sx={{
                backgroundColor: 'rgba(139, 92, 246, 0.05)',
                border: '1px solid rgba(139, 92, 246, 0.15)',
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  borderColor: 'rgba(139, 92, 246, 0.3)',
                  boxShadow: '0 4px 20px rgba(139, 92, 246, 0.15)',
                },
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 4 }}>
                <AutoAwesomeIcon
                  sx={{
                    fontSize: 48,
                    color: '#8b5cf6',
                    mb: 2,
                  }}
                />
                <Typography variant="h6" sx={{ color: 'white', mb: 1, fontWeight: 600 }}>
                  AI Generation
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  Generate quizzes from PDFs using advanced AI
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card
              sx={{
                backgroundColor: 'rgba(139, 92, 246, 0.05)',
                border: '1px solid rgba(139, 92, 246, 0.15)',
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  borderColor: 'rgba(139, 92, 246, 0.3)',
                  boxShadow: '0 4px 20px rgba(139, 92, 246, 0.15)',
                },
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 4 }}>
                <SchoolIcon
                  sx={{
                    fontSize: 48,
                    color: '#8b5cf6',
                    mb: 2,
                  }}
                />
                <Typography variant="h6" sx={{ color: 'white', mb: 1, fontWeight: 600 }}>
                  Learn Ethics
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  Master ethical concepts through interactive quizzes
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card
              sx={{
                backgroundColor: 'rgba(139, 92, 246, 0.05)',
                border: '1px solid rgba(139, 92, 246, 0.15)',
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  borderColor: 'rgba(139, 92, 246, 0.3)',
                  boxShadow: '0 4px 20px rgba(139, 92, 246, 0.15)',
                },
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 4 }}>
                <AnalyticsIcon
                  sx={{
                    fontSize: 48,
                    color: '#8b5cf6',
                    mb: 2,
                  }}
                />
                <Typography variant="h6" sx={{ color: 'white', mb: 1, fontWeight: 600 }}>
                  Track Progress
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  Monitor your performance with detailed analytics
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={3}>
            <Card
              sx={{
                backgroundColor: 'rgba(139, 92, 246, 0.05)',
                border: '1px solid rgba(139, 92, 246, 0.15)',
                borderRadius: 2,
                height: '100%',
                transition: 'all 0.2s ease',
                '&:hover': {
                  transform: 'translateY(-2px)',
                  borderColor: 'rgba(139, 92, 246, 0.3)',
                  boxShadow: '0 4px 20px rgba(139, 92, 246, 0.15)',
                },
              }}
            >
              <CardContent sx={{ textAlign: 'center', py: 4 }}>
                <QuizIcon
                  sx={{
                    fontSize: 48,
                    color: '#8b5cf6',
                    mb: 2,
                  }}
                />
                <Typography variant="h6" sx={{ color: 'white', mb: 1, fontWeight: 600 }}>
                  Custom Quizzes
                </Typography>
                <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  Create and customize your own quiz content
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Dashboard Preview Section */}
        <Box
            sx={{
              mt: 8,
              position: 'relative',
              borderRadius: 4,
              overflow: 'hidden',
              border: '1px solid rgba(139, 92, 246, 0.2)',
              backgroundColor: 'rgba(10, 10, 10, 0.95)',
              backdropFilter: 'blur(10px)',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
            }}
        >
          <Box
            sx={{
              p: 4,
              background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(167, 139, 250, 0.1) 100%)',
            }}
          >
            <Typography variant="h4" sx={{ color: 'white', mb: 2, fontWeight: 600 }}>
              Your Dashboard Preview
            </Typography>
            <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 4 }}>
              Experience a clean, intuitive interface designed for efficient learning and progress tracking.
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Paper
                  sx={{
                    p: 3,
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    border: '1px solid rgba(139, 92, 246, 0.2)',
                    borderRadius: 2,
                  }}
                >
                  <Typography
                    variant="h6"
                    sx={{
                      color: '#c4b5fd',
                      mb: 1,
                    }}
                  >
                    Quiz Analytics
                  </Typography>
                  <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                    85%
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                    Average Accuracy
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper
                  sx={{
                    p: 3,
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    border: '1px solid rgba(139, 92, 246, 0.2)',
                    borderRadius: 2,
                  }}
                >
                  <Typography
                    variant="h6"
                    sx={{
                      color: '#c4b5fd',
                      mb: 1,
                    }}
                  >
                    Quizzes Taken
                  </Typography>
                  <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                    42
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                    Total Attempts
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper
                  sx={{
                    p: 3,
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    border: '1px solid rgba(139, 92, 246, 0.2)',
                    borderRadius: 2,
                  }}
                >
                  <Typography
                    variant="h6"
                    sx={{
                      color: '#c4b5fd',
                      mb: 1,
                    }}
                  >
                    Progress Trend
                  </Typography>
                  <Typography variant="h4" sx={{ color: 'white', fontWeight: 'bold' }}>
                    ↗ +12%
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.6)' }}>
                    This Month
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        </Box>

        {/* Final CTA */}
        <Box sx={{ textAlign: 'center', mt: 10, mb: 6 }}>
          <Typography variant="h4" sx={{ color: 'white', mb: 2, fontWeight: 600 }}>
            Ready to Start Learning?
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 4 }}>
            Join thousands of learners mastering ethics through intelligent quiz generation.
          </Typography>
          <Button
            variant="contained"
            size="large"
            onClick={() => navigate('/login')}
              sx={{
                px: 6,
                py: 1.5,
                fontSize: '1.1rem',
                background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
                borderRadius: 2,
                textTransform: 'none',
                boxShadow: '0 4px 14px rgba(139, 92, 246, 0.25)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #7c3aed 0%, #9333ea 100%)',
                  transform: 'translateY(-1px)',
                  boxShadow: '0 6px 20px rgba(139, 92, 246, 0.35)',
                },
                transition: 'all 0.2s ease',
              }}
          >
            Get Started Now
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

