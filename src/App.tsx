import React, { useState, useEffect } from 'react';
import { Box, Tabs, Tab, Container, Paper } from '@mui/material';
import BulkImporter from './components/BulkImporter';
import RedditLinks from './components/RedditLinks';
import OtherLinks from './components/OtherLinks';
import Preview from './components/Preview';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);
  const [redditLinks, setRedditLinks] = useState<string[]>([]);
  const [otherLinks, setOtherLinks] = useState<string[]>([]);
  const [markdownPreview, setMarkdownPreview] = useState<Array<{title: string, url: string}>>([]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleBulkImport = (urls: string[]) => {
    const redditRegex = /reddit\.com/;
    const redditUrls = urls.filter(url => redditRegex.test(url));
    const nonRedditUrls = urls.filter(url => !redditRegex.test(url));
    
    setRedditLinks(prev => [...new Set([...prev, ...redditUrls])]);
    setOtherLinks(prev => [...new Set([...prev, ...nonRedditUrls])]);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ width: '100%', mt: 4 }}>
        <Paper sx={{ width: '100%', mb: 2 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="Bulk Import" />
            <Tab label="Reddit Links" />
            <Tab label="Other Links" />
          </Tabs>

          <TabPanel value={tabValue} index={0}>
            <BulkImporter onImport={handleBulkImport} />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <RedditLinks 
              links={redditLinks} 
              onUpdate={setRedditLinks}
              onMarkdownUpdate={setMarkdownPreview}
            />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <OtherLinks 
              links={otherLinks}
              onUpdate={setOtherLinks}
              onMarkdownUpdate={setMarkdownPreview}
            />
          </TabPanel>
        </Paper>

        <Preview markdownData={markdownPreview} />
      </Box>
    </Container>
  );
}

export default App;
