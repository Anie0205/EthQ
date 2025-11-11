import React from 'react';
import { Box, Typography, Chip, Stack, Paper, Divider, List, ListItem, ListItemText } from '@mui/material';

export const AnalyticsSummary = ({ summary }) => {
  if (!summary || !summary.has_data) {
    return (
      <Paper sx={{ p: 2 }}>
        <Typography>No analytics yet. Take some quizzes to generate insights.</Typography>
      </Paper>
    );
  }

  const {
    trend_slope,
    rolling_avg,
    volatility,
    best_categories = [],
    weak_categories = [],
    category_accuracy = {},
    mastery_by_category = {},
    attempts_count,
    last_accuracy,
    best_attempt,
    worst_attempt,
    improvement_pct_recent,
    consistency_score,
    target_next_accuracy,
    recommendations = [],
  } = summary;

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" sx={{ mb: 1 }}>Insights</Typography>

      <Typography variant="body2">Attempts: {attempts_count}</Typography>
      <Typography variant="body2">Last Accuracy: {last_accuracy.toFixed(1)}%</Typography>
      <Typography variant="body2">Rolling Average (recent): {rolling_avg.toFixed(1)}%</Typography>
      <Typography variant="body2">Trend (per attempt): {trend_slope.toFixed(3)}</Typography>
      <Typography variant="body2">Consistency Score: {consistency_score.toFixed(0)}/100</Typography>
      <Typography variant="body2">Volatility (std dev): {volatility.toFixed(1)}%</Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>Target Next Accuracy: {target_next_accuracy.toFixed(1)}%</Typography>

      <Typography variant="subtitle2">Recent Improvement</Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>{improvement_pct_recent.toFixed(1)}% vs previous period</Typography>

      <Divider sx={{ my: 1 }} />

      <Typography variant="subtitle2">Best Categories</Typography>
      <Stack direction="row" spacing={1} sx={{ mb: 1, flexWrap: 'wrap' }}>
        {best_categories.map((c) => (
          <Chip key={c} label={`${c} ${(category_accuracy[c]||0).toFixed(0)}% (${mastery_by_category[c]||''})`} color="success" size="small" />
        ))}
      </Stack>

      <Typography variant="subtitle2">Needs Improvement</Typography>
      <Stack direction="row" spacing={1} sx={{ mb: 1, flexWrap: 'wrap' }}>
        {weak_categories.map((c) => (
          <Chip key={c} label={`${c} ${(category_accuracy[c]||0).toFixed(0)}% (${mastery_by_category[c]||''})`} color="warning" size="small" />
        ))}
      </Stack>

      <Divider sx={{ my: 1 }} />

      <Typography variant="subtitle2">Best / Worst Attempts</Typography>
      <Typography variant="body2">Best: Quiz {best_attempt?.quiz_id} — {best_attempt?.accuracy?.toFixed?.(1) ?? best_attempt?.accuracy}%</Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>Worst: Quiz {worst_attempt?.quiz_id} — {worst_attempt?.accuracy?.toFixed?.(1) ?? worst_attempt?.accuracy}%</Typography>

      <Typography variant="subtitle2">Recommendations</Typography>
      {recommendations.length ? (
        <List dense>
          {recommendations.map((r, idx) => (
            <ListItem key={idx} sx={{ py: 0 }}>
              <ListItemText primaryTypographyProps={{ variant: 'body2' }} primary={r} />
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography variant="body2">On track. Keep going!</Typography>
      )}
    </Paper>
  );
};
