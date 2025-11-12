import axios from 'axios';
import { getAuthHeaders } from './auth';
import { API_BASE_URL } from './config';

const API_URL = API_BASE_URL;

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
  // Don't set Content-Type manually - let axios set it with boundary for multipart/form-data
  const headers = { ...getAuthHeaders() };
  const response = await axios.post(`${API_URL}/quiz/upload`, formData, { headers });
  return response.data;
};

export const generateQuizFromText = async ({ text, level, questions }) => {
  const formData = new FormData();
  formData.append('text', text);
  formData.append('level', level);
  formData.append('questions', String(questions));
  // Don't set Content-Type manually - let axios set it with boundary for multipart/form-data
  const headers = { ...getAuthHeaders() };
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
