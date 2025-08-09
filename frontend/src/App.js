import React, { useState, useEffect } from 'react';
import { Button, Typography, Container, Box } from '@mui/material';

function App() {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [prediction, setPrediction] = useState(null);

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  const startListening = () => {
    setTranscript('');
    setPrediction(null);
    recognition.start();
    setListening(true);
  };

  const stopListening = () => {
    recognition.stop();
    setListening(false);
  };

  useEffect(() => {
    recognition.onresult = (event) => {
      const speechToText = event.results[0][0].transcript;
      setTranscript(speechToText);
      analyzeSpeech(speechToText);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error', event.error);
      setListening(false);
    };
  }, []);

  // Dummy feature extraction - replace with your real logic
  const extractFeatures = (text) => {
    // Example features:
    // 1) total words count
    // 2) average word length
    const words = text.trim().split(/\s+/);
    const totalWords = words.length;
    const avgWordLength = words.reduce((acc, w) => acc + w.length, 0) / totalWords;

    return [totalWords, avgWordLength, 0]; // 3rd feature placeholder
  };

  const analyzeSpeech = async (text) => {
    const features = extractFeatures(text);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features }),
      });
      const data = await response.json();
      setPrediction(data.dyslexia_probability);
    } catch (error) {
      console.error('Error fetching prediction:', error);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      <Typography variant="h4" gutterBottom>
        AI-based Dyslexia Detection Tool
      </Typography>
      <Box sx={{ mb: 2 }}>
        {!listening ? (
          <Button variant="contained" onClick={startListening}>Start Reading</Button>
        ) : (
          <Button variant="outlined" onClick={stopListening}>Stop</Button>
        )}
      </Box>
      <Typography variant="body1" sx={{ mb: 2 }}>
        Transcript: {transcript}
      </Typography>
      {prediction !== null && (
        <Typography variant="h6" sx={{ mt: 3 }}>
          Dyslexia Probability: {(prediction * 100).toFixed(2)}%
        </Typography>
      )}
    </Container>
  );
}

export default App;