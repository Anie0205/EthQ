import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';
import { Typography, Box } from '@mui/material';

export const AnalyticsChart = ({ attempts }) => {
  const accuracyTrendData = attempts.slice(-10).map((attempt, index) => ({
    name: `Attempt ${index + 1}`,
    accuracy: attempt.accuracy,
  }));

  const categoryAccuracy = {};
  attempts.forEach(attempt => {
    const category = `Category ${attempt.quiz_id % 3}`; // Placeholder
    if (!categoryAccuracy[category]) {
      categoryAccuracy[category] = { totalAccuracy: 0, count: 0 };
    }
    categoryAccuracy[category].totalAccuracy += attempt.accuracy;
    categoryAccuracy[category].count += 1;
  });

  const categoryHeatmapData = Object.keys(categoryAccuracy).map(category => ({
    category,
    averageAccuracy: categoryAccuracy[category].totalAccuracy / categoryAccuracy[category].count,
  }));

  return (
    <Box>
      <Typography variant="h6" component="div" sx={{ mb: 2 }}>
        Accuracy Trend Over Time
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={accuracyTrendData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="accuracy" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>

      <Typography variant="h6" component="div" sx={{ mt: 4, mb: 2 }}>
        Average Accuracy by Category
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={categoryHeatmapData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="averageAccuracy" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};
