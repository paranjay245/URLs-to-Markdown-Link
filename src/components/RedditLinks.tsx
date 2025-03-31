import React, { useEffect, useState } from 'react';
import { Box, List, ListItem, ListItemText, IconButton, Typography } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';

interface RedditLinksProps {
  links: string[];
  onUpdate: (links: string[]) => void;
  onMarkdownUpdate: (markdownData: Array<{title: string, url: string}>) => void;
}

const RedditLinks: React.FC<RedditLinksProps> = ({ links, onUpdate, onMarkdownUpdate }) => {
  const [titles, setTitles] = useState<Array<{url: string, title: string}>>([]);

  useEffect(() => {
    const fetchTitles = async () => {
      const newTitles = await Promise.all(
        links.map(async (url) => {
          try {
            const response = await axios.post('http://localhost:5000/reddit-title', { url });
            return { url, title: response.data.title };
          } catch (error) {
            console.error('Error fetching title:', error);
            return { url, title: 'Error fetching title' };
          }
        })
      );
      setTitles(newTitles);
      onMarkdownUpdate(newTitles);
    };

    if (links.length > 0) {
      fetchTitles();
    }
  }, [links, onMarkdownUpdate]);

  const handleDelete = (urlToDelete: string) => {
    onUpdate(links.filter(url => url !== urlToDelete));
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Reddit Links
      </Typography>
      <List>
        {links.map((url, index) => (
          <ListItem
            key={url}
            secondaryAction={
              <IconButton edge="end" onClick={() => handleDelete(url)}>
                <DeleteIcon />
              </IconButton>
            }
          >
            <ListItemText
              primary={titles[index]?.title || 'Loading...'}
              secondary={url}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default RedditLinks; 