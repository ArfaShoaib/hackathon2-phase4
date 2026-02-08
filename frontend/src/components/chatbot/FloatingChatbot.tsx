'use client';

import { useState, useEffect, useRef } from 'react';
import { Bot, X, MessageCircle } from 'lucide-react';
import Chatbot from './Chatbot';
import { useUser } from '@/contexts/user-context';

const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [hasLoaded, setHasLoaded] = useState(false);
  const { user, token, loading } = useUser();
  const chatbotRef = useRef<HTMLDivElement>(null);

  // Show floating button only when user is authenticated
  const isAuthenticated = user && token && !loading;

  // Only initialize after hydration to avoid SSR issues
  useEffect(() => {
    setHasLoaded(true);
  }, []);

  // Close chatbot when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isOpen && chatbotRef.current && !chatbotRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  if (!hasLoaded || !isAuthenticated) {
    return null;
  }

  return (
    <>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center group"
          aria-label="Open AI Assistant"
        >
          <MessageCircle className="h-6 w-6" />
          <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center animate-pulse">
            !
          </span>
        </button>
      )}

      {isOpen && (
        <div 
          ref={chatbotRef}
          className="fixed bottom-6 right-6 z-50 w-full max-w-md h-[600px] bg-white rounded-xl shadow-2xl border border-gray-200 flex flex-col"
        >
          {/* Chat Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-t-xl flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <Bot className="h-4 w-4" />
              </div>
              <h3 className="font-semibold">AI Task Assistant</h3>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-gray-200 transition-colors"
              aria-label="Close chat"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Chat Content */}
          <div className="flex-1 p-1 bg-gray-50">
            <Chatbot
              userId={user.id.toString()}
              token={token}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default FloatingChatbot;