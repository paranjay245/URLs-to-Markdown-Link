import React from 'react';
import { Box, Paper, Typography, TextField } from '@mui/material';

interface PreviewProps {
  markdownData: Array<{title: string, url: string}>;
}

const Preview: React.FC<PreviewProps> = ({ markdownData }) => {
  const markdownText = markdownData
    .map(({ title, url }) => `[${title}](${url})`)
    .join('\n');

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Markdown Preview
      </Typography>
      <Paper sx={{ p: 2 }}>
        <TextField
          fullWidth
          multiline
          rows={6}
          variant="outlined"
          value={markdownText}
          InputProps={{
            readOnly: true,
          }}
        />
      </Paper>
    </Box>
  );
};

export default Preview; 