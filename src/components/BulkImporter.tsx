import React, { useState } from 'react';
import { Box, TextField, Button, Typography } from '@mui/material';

interface BulkImporterProps {
  onImport: (urls: string[]) => void;
}

const BulkImporter: React.FC<BulkImporterProps> = ({ onImport }) => {
  const [text, setText] = useState('');

  const extractUrls = () => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const urls = text.match(urlRegex) || [];
    onImport(urls);
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Bulk Import URLs
      </Typography>
      <TextField
        fullWidth
        multiline
        rows={6}
        variant="outlined"
        placeholder="Paste your text here. URLs will be automatically extracted."
        value={text}
        onChange={(e) => setText(e.target.value)}
        sx={{ mb: 2 }}
      />
      <Button 
        variant="contained" 
        onClick={extractUrls}
        disabled={!text.trim()}
      >
        Extract URLs
      </Button>
    </Box>
  );
};

export default BulkImporter; 