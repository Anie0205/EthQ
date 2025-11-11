import axios from 'axios';
import { getAuthHeaders } from './auth';

const API_URL = import.meta.env.VITE_API_URL || 'https://ethq.onrender.com';

export const getQuizzes = async () => {
  const response = await axios.get(`${API_URL}/quizzes`, { headers: getAuthHeaders() });
  return response.data;
};

export const getQuizById = async (quizId) => {
  const response = await axios.get(`${API_URL}/quizzes/${quizId}`, { headers: getAuthHeaders() });
  return response.data;
};

export const submitQuizAnswers = async (quizId, answers, justifications = {}) => {
  const response = await axios.post(
    `${API_URL}/quizzes/${quizId}/submit`,
    { answers, justifications },
    { headers: getAuthHeaders() }
  );
  return response.data;
};

export const explainQuestionConflict = async (quizId, questionId) => {
  const response = await axios.get(
    `${API_URL}/quizzes/${quizId}/explain-conflict/${questionId}`,
    { headers: getAuthHeaders() }
  );
  return response.data;
};

export const getPostQuizAnalysis = async (attemptId) => {
  const response = await axios.get(
    `${API_URL}/quizzes/attempts/${attemptId}/analysis`,
    { headers: getAuthHeaders() }
  );
  return response.data;
};


export const createQuiz = async (quizData) => {
  const response = await axios.post(`${API_URL}/quizzes`, quizData, { headers: getAuthHeaders() });
  return response.data;
};

export const uploadQuizPDF = async (fileOrFormData) => {
  let formData;
  if (fileOrFormData instanceof FormData) {
    formData = fileOrFormData;
  } else {
    formData = new FormData();
    formData.append('file', fileOrFormData);
  }
  const headers = { ...getAuthHeaders(), 'Content-Type': 'multipart/form-data' };
  const response = await axios.post(`${API_URL}/quiz/upload`, formData, { headers });
  return response.data;
};

export const generateQuizFromText = async ({ text, level, questions }) => {
  const formData = new FormData();
  formData.append('text', text);
  formData.append('level', level);
  formData.append('questions', String(questions));
  const headers = { ...getAuthHeaders(), 'Content-Type': 'multipart/form-data' };
  const response = await axios.post(`${API_URL}/quiz/generate-text`, formData, { headers });
  return response.data;
};

export const getUserAttempts = async () => {
  const response = await axios.get(`${API_URL}/quizzes/history`, { headers: getAuthHeaders() });
  return response.data;
};

export const getAnalyticsSummary = async () => {
  const response = await axios.get(`${API_URL}/analytics/summary`, { headers: getAuthHeaders() });
  return response.data;
};
