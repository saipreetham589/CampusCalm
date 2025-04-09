import React from 'react';
import { Tab } from '@headlessui/react';
import ScreeningPage from './ScreeningPage';
import ChatPage from './ChatPage';
import RemindersPage from './RemindersPage';
import { useState, useEffect } from 'react';
import axios from 'axios';
import ResultScreen from './ResultScreen';
import { useLocation } from 'react-router-dom';
import {
  ChatBubbleOvalLeftIcon,
  BellIcon,
  ClipboardDocumentListIcon
} from '@heroicons/react/24/outline';

const tabs = [
  { name: 'Screening Test', icon: ClipboardDocumentListIcon },
  { name: 'AI Chat Support', icon: ChatBubbleOvalLeftIcon },
  { name: 'Self-Care Reminders', icon: BellIcon }
];


const Home = () => {
  const [resultData, setResultData] = useState(null);
  const [loadingResult, setLoadingResult] = useState(true);

  useEffect(() => {
    const userID = JSON.parse(localStorage.getItem('user'))?.UserID;
    if (!userID) return;

    axios.get(`/api/result/${userID}`)
      .then(res => {
        const { PHQ9Score, GAD7Score, Timestamp } = res.data;
        const dateTaken = new Date(Timestamp);
        const now = new Date();
        const diffMs = now - dateTaken;
        const sevenDays = 7 * 24 * 60 * 60 * 1000;
        // Check if the result is within the last 7 days
        console.log('Fetched result:', res.data);


        if (diffMs < sevenDays) {
          setResultData({
            phq9: {
              percent: Math.round((PHQ9Score / 27) * 100),
              level: getLevel(PHQ9Score, 27)
            },
            gad7: {
              percent: Math.round((GAD7Score / 21) * 100),
              level: getLevel(GAD7Score, 21)
            }
          });
        }
      })
      .catch(err => console.log('No recent result found:', err))
      .finally(() => setLoadingResult(false));
  }, []);

  const getLevel = (score, max) => {
    const percent = (score / max) * 100;
    return percent < 30 ? 'Low' : percent < 70 ? 'Mild' : 'High';
  };
  const location = useLocation();
      const [selectedIndex, setSelectedIndex] = useState(0);

      useEffect(() => {
        if (location.state?.tab !== undefined) {
          setSelectedIndex(location.state.tab);
        }
      }, [location.state]);
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-white px-4 pt-6">
      <Tab.Group selectedIndex={selectedIndex} onChange={setSelectedIndex}>
        <Tab.List className="flex flex-wrap sm:flex-nowrap space-x-0 sm:space-x-4 space-y-2 sm:space-y-0 justify-around sm:justify-start border-b border-gray-200 dark:border-gray-700 pb-2">
          {tabs.map((tab, idx) => (
            <Tab
              key={idx}
              className={({ selected }) =>
                `flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-md focus:outline-none transition 
                ${
                  selected
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300'
                }`
              }
            >
              <tab.icon className="w-5 h-5" />
              <span className="truncate">{tab.name}</span>
            </Tab>
          ))}
        </Tab.List>

        <Tab.Panels className="pt-4 pb-10">
          <Tab.Panel>
              {(() => {
                const last = parseInt(localStorage.getItem('lastScreening') || 0);
                const withinAWeek = Date.now() - last < 7 * 24 * 60 * 60 * 1000;

                if (withinAWeek) {
                  const phq9 = JSON.parse(localStorage.getItem('phq9') || '{}');
                  const gad7 = JSON.parse(localStorage.getItem('gad7') || '{}');
                  return <ResultScreen phq9={phq9} gad7={gad7} />;
                } else {
                  return <ScreeningPage />;
                }
              })()}
            </Tab.Panel>
          <Tab.Panel>
            <ChatPage />
          </Tab.Panel>
          <Tab.Panel>
            <RemindersPage />
          </Tab.Panel>
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
};

export default Home;
