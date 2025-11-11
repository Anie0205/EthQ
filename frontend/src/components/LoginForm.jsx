import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import { login, register } from '../api/auth';

export const LoginForm = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    try {
      if (isRegistering) {
        await register(email, password);
        alert('Registration successful! Please log in.');
        setIsRegistering(false);
      } else {
        await login(email, password);
        onLoginSuccess();
      }
    } catch (err) {
      setError('Login or registration failed. Please check your credentials.');
      console.error(err);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
      <TextField
        margin="normal"
        required
        fullWidth
        id="email"
        label="Email Address"
        name="email"
        autoComplete="email"
        autoFocus
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        sx={{
          '& .MuiOutlinedInput-root': {
            color: 'white',
            '& fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.2)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(139, 92, 246, 0.4)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#8b5cf6',
            },
          },
          '& .MuiInputLabel-root': {
            color: 'rgba(255, 255, 255, 0.7)',
            '&.Mui-focused': {
              color: '#8b5cf6',
            },
          },
        }}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        sx={{
          '& .MuiOutlinedInput-root': {
            color: 'white',
            '& fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.2)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(139, 92, 246, 0.4)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#8b5cf6',
            },
          },
          '& .MuiInputLabel-root': {
            color: 'rgba(255, 255, 255, 0.7)',
            '&.Mui-focused': {
              color: '#8b5cf6',
            },
          },
        }}
      />
      {error && (
        <Typography color="error" variant="body2" sx={{ mt: 1, color: '#ef4444' }}>
          {error}
        </Typography>
      )}
      <Button
        type="submit"
        fullWidth
        variant="contained"
        sx={{
          mt: 3,
          mb: 2,
          py: 1.5,
          background: 'linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%)',
          borderRadius: 2,
          textTransform: 'none',
          fontSize: '1rem',
          fontWeight: 600,
          boxShadow: '0 4px 14px rgba(139, 92, 246, 0.25)',
          '&:hover': {
            background: 'linear-gradient(135deg, #7c3aed 0%, #9333ea 100%)',
            transform: 'translateY(-1px)',
            boxShadow: '0 6px 20px rgba(139, 92, 246, 0.35)',
          },
          transition: 'all 0.2s ease',
        }}
      >
        {isRegistering ? 'Register' : 'Sign In'}
      </Button>
      <Button
        fullWidth
        variant="text"
        onClick={() => setIsRegistering(!isRegistering)}
        sx={{
          textTransform: 'none',
          color: 'rgba(255, 255, 255, 0.7)',
          transition: 'all 0.2s ease',
          '&:hover': {
            color: '#a78bfa',
            backgroundColor: 'rgba(139, 92, 246, 0.05)',
          },
        }}
      >
        {isRegistering ? 'Already have an account? Sign In' : "Don't have an account? Register"}
      </Button>
    </Box>
  );
};
