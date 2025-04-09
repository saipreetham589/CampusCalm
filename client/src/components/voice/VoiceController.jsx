import React, { useState } from 'react';
import VoiceVisualizer from './VoiceVisualizer';

const VoiceController = ({ onVoiceInput }) => {
  const [listening, setListening] = useState(false);

  const toggleVoiceMode = () => {
    const newState = !listening;
    setListening(newState);

    if (newState) {
      // 👇 Later connect this to Azure STT endpoint
      console.log('🎤 Voice mode started');

      // Simulate backend response after a delay
      setTimeout(() => {
        const fakeTranscript = "I'm here to help, how are you feeling?";
        if (onVoiceInput) {
          onVoiceInput(fakeTranscript);
        }
        setListening(false);
      }, 3000);
    } else {
      console.log('🛑 Voice mode stopped');
    }
  };

  return (
    <div className="flex flex-col items-center mt-2">
      {listening && <VoiceVisualizer />}

      <button
        onClick={toggleVoiceMode}
        className={`mt-4 px-4 py-2 text-white rounded-full ${
          listening ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'
        }`}
      >
        {listening ? 'Stop Voice Mode' : 'Start Voice Mode'}
      </button>
    </div>
  );
};

export default VoiceController;
