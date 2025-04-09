import React, { useState, useEffect, useRef } from 'react';
import { MicrophoneIcon, PaperAirplaneIcon } from '@heroicons/react/24/solid';
import VoiceVisualizer from '../components/voice/VoiceVisualizer';


const ChatPage = () => {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hi there! How can I support you today?' },
  ]);
  const [input, setInput] = useState('');
  const [voiceMode, setVoiceMode] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [streamingReply, setStreamingReply] = useState('');
  const chatRef = useRef();
  const messagesEndRef = useRef(null);


  // useEffect(() => {
  //   messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  // }, [messages, streamingReply]);

  const handleSend = async () => {
    if (!input.trim()) return;
  
    const user = JSON.parse(localStorage.getItem("user"));
    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { from: 'user', text: userMessage }]);
    setStreamingReply(''); // reset typing effect
  
    try {
      const res = await fetch("http://localhost:5056/api/text-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          
        })
      });
  
      const data = await res.json();
      const fullReply = data.response;
  
      // ⌨️ Simulate typing
      for (let i = 0; i < fullReply.length; i++) {
        await new Promise(r => setTimeout(r, 20));
        setStreamingReply(prev => prev + fullReply[i]);
      }
  
      await new Promise(r => setTimeout(r, 300));
      setMessages(prev => [...prev, { from: 'bot', text: fullReply }]);
      setStreamingReply('');
  
    } catch (err) {
      console.error('Chat error:', err);
      setMessages(prev => [...prev, { from: 'bot', text: 'Something went wrong.' }]);
    }
  };

  // Function to handle voice mode toggle
  const toggleVoiceMode = async () => {
    const newState = !voiceMode;
    setVoiceMode(newState);
    const user = JSON.parse(localStorage.getItem("user"));
  
    if (newState) {
      const keepGoing = { value: true };
  
      window.stopVoiceLoop = () => {
        keepGoing.value = false;
        setVoiceMode(false);
      };
  
      while (keepGoing.value) {
        setIsListening(true);
        setIsSpeaking(false); // reset speaking
  
        try {
          const res = await fetch('http://localhost:5055/api/voice-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              charID: user?.CharID   // ✅ now properly passed here
            })
          });
  
          const data = await res.json();
          if (!keepGoing.value) break;
  
          setIsListening(false);
          await new Promise((r) => setTimeout(r, 100));
  
          if (data.success && data.input && data.response) {
            setMessages(prev => [...prev, { from: 'user', text: data.input }]);
  
            const fullReply = data.response;
  
            setIsSpeaking(true);
            setStreamingReply(fullReply);
  
            await new Promise((r) => setTimeout(r, 300));
            setMessages(prev => [...prev, { from: 'bot', text: fullReply }]);
            setStreamingReply('');
  
            // ⏳ Simulated TTS duration (adjust if needed)
            const estimatedVoiceTime = Math.min(2000, fullReply.length * 20);
            await new Promise(r => setTimeout(r, estimatedVoiceTime));
  
            setIsSpeaking(false);
          } else {
            console.warn('No voice input or response');
            continue;
          }
  
        } catch (err) {
          console.error('Voice chat error:', err);
          break;
        }
      }
  
      setVoiceMode(false);
      setIsListening(false);
      setIsSpeaking(false);
    }
  };


  return (
    <div className="w-full flex justify-center pt-6 relative">
      <div className="w-full max-w-5xl h-[600px] bg-gray-100 dark:bg-gray-800 rounded-xl shadow-lg flex flex-col overflow-hidden border border-gray-300 dark:border-gray-700">

        {/* Overlay for Listening / Speaking */}
        {voiceMode && (
          <div className="absolute inset-0 bg-black bg-opacity-75 flex flex-col items-center justify-center z-50">
            {isListening && (
              <div className="text-white text-2xl font-semibold mb-2">Loona...</div>
            )}
            {isSpeaking && (
              <div className="text-white text-xl font-semibold mb-2">Wait...</div>
            )}
            {!isListening && !isSpeaking && (
              <div className="text-white text-xl mb-2 opacity-70">Waiting for response...</div>
            )}
            <VoiceVisualizer isActive={isListening || isSpeaking} />
            <button
              onClick={() => window.stopVoiceLoop?.()}
              className="mt-6 px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded"
            >
              Stop Loona
            </button>
          </div>
        )}

        {/* Message List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4" ref={chatRef}>
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm break-words ${msg.from === 'bot' ? 'bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-white': 'bg-blue-600 text-white'}`}>
                {msg.text}
              </div>
            </div>
          ))}
          {streamingReply && (
            <div className="flex justify-start">
              <div className="max-w-[75%] px-4 py-2 rounded-2xl text-sm bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-white">
                {streamingReply}
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
          
        </div>

        {/* Input Area */}
        <div className="p-3 bg-gray-200 dark:bg-gray-900 border-t border-gray-300 dark:border-gray-700 flex items-center gap-3">
          <button onClick={toggleVoiceMode}>
            <MicrophoneIcon className="w-6 h-6 text-gray-600 dark:text-white hover:text-blue-500" />
          </button>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type a message..."
            className="flex-1 bg-transparent text-base text-gray-900 dark:text-white outline-none placeholder-gray-500"
          />
          <button onClick={handleSend}>
            <PaperAirplaneIcon className="w-6 h-6 text-blue-500 hover:text-blue-400 transform" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
