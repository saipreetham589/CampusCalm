import React, { useState, useRef, useEffect } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { UserCircleIcon, ArrowRightOnRectangleIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';

const ProfileMenu = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('user')) || {});

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <Menu as="div" className="relative inline-block text-left z-50">
      <div>
        <Menu.Button className="flex items-center space-x-2 rounded-full p-1 text-gray-700 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-700 transition">
          <UserCircleIcon className="h-7 w-7" />
        </Menu.Button>
      </div>

      <Transition
        enter="transition duration-150 ease-out"
        enterFrom="transform scale-95 opacity-0"
        enterTo="transform scale-100 opacity-100"
        leave="transition duration-100 ease-in"
        leaveFrom="transform scale-100 opacity-100"
        leaveTo="transform scale-95 opacity-0"
      >
        <Menu.Items className="absolute right-0 mt-2 w-48 origin-top-right divide-y divide-gray-100 dark:divide-gray-700 rounded-md bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black/5 focus:outline-none">
          <div className="px-1 py-1">
            <Menu.Item>
              {({ active }) => (
                <button
                  onClick={() => navigate('/profile')}
                  className={`${
                    active ? 'bg-blue-100 dark:bg-blue-600 text-blue-900 dark:text-white' : 'text-gray-700 dark:text-gray-200'
                  } group flex w-full items-center rounded-md px-4 py-2 text-sm`}
                >
                  <UserCircleIcon className="w-5 h-5 mr-2" />
                  View Profile
                </button>
              )}
            </Menu.Item>
            <Menu.Item>
              {({ active }) => (
                <button
                  onClick={handleLogout}
                  className={`${
                    active ? 'bg-blue-100 dark:bg-red-600 text-red-800 dark:text-white' : 'text-gray-700 dark:text-gray-200'
                  } group flex w-full items-center rounded-md px-4 py-2 text-sm`}
                >
                  <ArrowRightOnRectangleIcon className="w-5 h-5 mr-2" />
                  Logout
                </button>
              )}
            </Menu.Item>
          </div>
        </Menu.Items>
      </Transition>
    </Menu>
  );
};

export default ProfileMenu;
