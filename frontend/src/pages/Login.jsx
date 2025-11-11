import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  Avatar,
} from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import QuizIcon from '@mui/icons-material/Quiz';
import { LoginForm } from '../components/LoginForm';

export const Login = () => {
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    navigate('/dashboard');
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #000000 0%, #0a0a0a 50%, #000000 100%)',
        position: 'relative',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 4,
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

      <Container component="main" maxWidth="xs" sx={{ position: 'relative', zIndex: 1 }}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {/* Logo */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <QuizIcon
              sx={{
                color: '#8b5cf6',
                fontSize: 32,
              }}
            />
            <Typography
              variant="h4"
              component={Link}
              to="/"
              sx={{
                fontWeight: 'bold',
                background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                textDecoration: 'none',
              }}
            >
              EthQ
            </Typography>
          </Box>

          <Paper
            sx={{
              p: 4,
              width: '100%',
              backgroundColor: 'rgba(10, 10, 10, 0.95)',
              border: '1px solid rgba(139, 92, 246, 0.2)',
              borderRadius: 2,
              backdropFilter: 'blur(10px)',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
            }}
          >
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 3 }}>
              <Avatar
                sx={{
                  m: 1,
                  bgcolor: 'rgba(139, 92, 246, 0.1)',
                  color: '#8b5cf6',
                  width: 56,
                  height: 56,
                }}
              >
                <LockOutlinedIcon sx={{ fontSize: 32 }} />
              </Avatar>
              <Typography component="h1" variant="h5" sx={{ color: 'white', fontWeight: 600 }}>
                Welcome Back
              </Typography>
              <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.6)', mt: 1 }}>
                Sign in to continue to EthQ
              </Typography>
            </Box>
            <LoginForm onLoginSuccess={handleLoginSuccess} />
          </Paper>
        </Box>
      </Container>
    </Box>
  );
};
