import React, { useState, useContext } from 'react';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import Loader from './Loader';
import './InputForm.css';

const InputForm = ({ setGeneratedContent }) => {
  const [medicineName, setMedicineName] = useState('');
  const [loading, setLoading] = useState(false);
  const { user } = useContext(AuthContext);

  const handleGenerate = async () => {
    if (!medicineName.trim()) return;

    setLoading(true);
    try {
      console.log('Generating content for:', medicineName);
      const response = await axios.post('http://localhost:5000/generate', { medicineName });
      const generatedContent = response.data.content;
      console.log('Generated content:', generatedContent);

      setGeneratedContent(medicineName, generatedContent);
      setMedicineName('');

      if (user) {
        const token = localStorage.getItem('token');
        if (token) {
          await axios.post(
            'http://localhost:5000/generate/save',
            { medicineName, content: generatedContent },
            { headers: { 'Authorization': `Bearer ${token}` } }
          );
          console.log('Content saved');
        } else {
          console.error('No token found, content not saved');
        }
      }
    } catch (error) {
      if (error.response) {
        console.error('Failed to generate content:', error.response.data);
      } else {
        console.error('Failed to generate content:', error.message);
      }
    } finally {
      setLoading(false);
    }
  };

  // 🎙️ Voice Search Functionality
  const startListening = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';

    recognition.onstart = () => console.log("Listening...");
    recognition.onerror = (event) => console.error("Voice recognition error:", event);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("Recognized text:", transcript);
      setMedicineName(transcript); // Auto-fill input with voice result
    };

    recognition.start();
  };

  return (
    <>
      <div className="input-form-container">
        <form onSubmit={(e) => { e.preventDefault(); handleGenerate(); }} className="input-form">
          <input
            className="input-field"
            type="text"
            value={medicineName}
            onChange={(e) => setMedicineName(e.target.value)}
            placeholder="Enter a medicine name or use voice search..."
            disabled={loading}
          />
          <div className="button-container">
            <button className="submit-button" type="button" onClick={startListening}>
              🎙️ Speak
            </button>
            <button className="submit-button" type="submit" disabled={loading}>
              {loading ? 'Generating...' : '⮞'}
            </button>
          </div>
        </form>
      </div>
      <Loader loading={loading} />
    </>
  );
};

export default InputForm;
