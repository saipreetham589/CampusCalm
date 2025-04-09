import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ScreeningPage = () => {
  const [questions, setQuestions] = useState([]);
  const [responses, setResponses] = useState({}); // ✅ FIXED: use an object, not true
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const userID = JSON.parse(localStorage.getItem('user'))?.UserID || 1;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [qRes, rRes] = await Promise.all([
          axios.get('/api/questions'),
          axios.get('/api/responses'),
        ]);
        console.log('✅ Questions:', qRes.data);
        console.log('✅ Responses:', rRes.data);
        setQuestions(qRes.data);
        setResponses(rRes.data); // should be { QuestionID: [ {text, value}, ... ] }
        setLoading(false);
      } catch (err) {
        console.error('Error loading screening data', err);
      }
    };
    fetchData();
  }, []);

  const handleSliderChange = (value) => {
    const q = questions[current];
    setAnswers((prev) => ({
      ...prev,
      [q.QuestionID]: {
        value,
        timestamp: new Date(),
      },
    }));
  };

  const handleNext = async () => {
    if (current < questions.length - 1) {
      setCurrent((prev) => prev + 1);
      return;
    }
  
    // Final Submit
    try {
      // 1. Submit each answer
      for (const [questionID, { value }] of Object.entries(answers)) {
        await axios.post('/api/answers', {
          userID,
          questionID: parseInt(questionID),
          selectedValue: value
        });
      }
  
      const phq9Answers = Object.entries(answers).slice(0, 10);
      const gad7Answers = Object.entries(answers).slice(10, 16);

      const calcScore = (items) => {
        const sum = items.reduce((acc, [, val]) => acc + parseInt(val.value), 0);
        const max = items.length * 3;
        const percent = Math.round((sum / max) * 100);
        return { sum, percent };
      };

      const phq9 = calcScore(phq9Answers);
      const gad7 = calcScore(gad7Answers);

      // 3. Save final result
      await axios.post('/api/result', {
        userID,
        phq9Score: phq9.sum,
        gad7Score: gad7.sum
      });

      // 4. Save timestamp for 7-day lockout
      localStorage.setItem('lastScreening', Date.now());
      localStorage.setItem('phq9', JSON.stringify(phq9));
      localStorage.setItem('gad7', JSON.stringify(gad7));

      // 5. Redirect
      navigate('/result', {
        state: {
          phq9,
          gad7
        }
      });
    } catch (err) {
      console.error('Error submitting answers:', err);
      alert('Something went wrong while submitting. Please try again.');
    }
  };

  const handlePrev = () => {
    if (current > 0) {
      setCurrent((prev) => prev - 1);
    }
  };

  if (loading) return <div className="text-center mt-10">Loading questions...</div>;
  if (questions.length === 0) return <div>No questions found.</div>;

  const q = questions[current];
  const options = Array.isArray(responses[q.QuestionID]) ? responses[q.QuestionID] : [];

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-2">Mental Health Screening</h2>
      <p className="mb-4 text-sm text-gray-500">This quick assessment helps evaluate your current mental wellbeing.</p>

      <div className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
        Question {current + 1} of {questions.length}
      </div>
      <div className="text-base font-medium text-gray-800 dark:text-white mb-4">
        {q.QuestionText}
      </div>

      <input
        type="range"
        min="0"
        max={options.length - 1}
        value={answers[q.QuestionID]?.value ?? 0}
        onChange={(e) => handleSliderChange(Number(e.target.value))}
        className="w-full mb-4"
      />

      <div className="flex justify-between text-xs text-gray-600 dark:text-gray-400 mb-4">
        {options.map((opt, idx) => (
          <span key={idx} className="w-1/4 text-center">
            {opt.text}
          </span>
        ))}
      </div>

      <div className="flex justify-between mt-6">
        <button
          onClick={handlePrev}
          disabled={current === 0}
          className="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 disabled:opacity-50"
        >
          Previous
        </button>
        <button
          onClick={handleNext}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          {current === questions.length - 1 ? 'Submit' : 'Next'}
        </button>
      </div>
    </div>
  );
};

export default ScreeningPage;
