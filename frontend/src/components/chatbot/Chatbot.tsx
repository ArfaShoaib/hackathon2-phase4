'use client';

import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Sparkles } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatbotProps {
  userId: string;
  token: string;
  className?: string;
}

const Chatbot = ({ userId, token, className = '' }: ChatbotProps) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasMounted, setHasMounted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Mark as mounted to prevent server/client mismatch
  useEffect(() => {
    setHasMounted(true);
    
    // Initialize with welcome message after mounting
    setMessages([
      {
        id: 'welcome-' + Date.now(),
        role: 'assistant',
        content: 'Hello! I\'m your AI Task Assistant. You can ask me to help manage your tasks using natural language. Try saying "Add a task to buy groceries" or "Show my pending tasks".',
        timestamp: new Date()
      }
    ]);
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: 'user-' + Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Determine the API base URL
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

      console.log('=== CHAT REQUEST DEBUG ===');
      console.log('API Base URL:', API_BASE_URL);
      console.log('User ID:', userId);
      console.log('Token (first 20 chars):', token?.substring(0, 20));
      console.log('Full headers:', {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token?.substring(0, 20)}...`
      });
      console.log('Request body:', {
        message: inputValue,
        conversation_id: getConversationId()
      });

      // Prepare request body - only include conversation_id if it exists
      const requestBody: any = {
        message: inputValue,
      };

      const conversationId = getConversationId();
      if (conversationId !== undefined) {
        requestBody.conversation_id = conversationId;
      }

      // Call the backend chat API
      const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,  // This is the key header
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Store conversation ID in localStorage
      if (data.conversation_id) {
        localStorage.setItem(`chat-conversation-${userId}`, data.conversation_id.toString());
      }

      // Add AI response
      const assistantMessage: Message = {
        id: 'assistant-' + Date.now(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: 'error-' + Date.now(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const getConversationId = (): string | undefined => {
    if (typeof window !== 'undefined') {
      const savedId = localStorage.getItem(`chat-conversation-${userId}`);
      return savedId ? savedId : undefined;
    }
    return undefined;
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const quickActions = [
    "Add task: Buy groceries",
    "Show my tasks",
    "Complete task #1",
    "Delete task 'old task'"
  ];

  // Don't render anything until mounted to prevent hydration errors
  if (!hasMounted) {
    return (
      <div className={`flex flex-col h-full bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden ${className}`}>
        <div className="flex-1 flex items-center justify-center bg-gray-50">
          <div className="text-gray-500">Loading chat...</div>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex flex-col h-full bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden ${className}`}>
      {/* Chat Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <Sparkles className="h-6 w-6" />
          </div>
          <div>
            <h3 className="font-semibold">AI Task Assistant</h3>
            <p className="text-xs opacity-80">Powered by AI • Always here to help</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[500px] bg-gray-50">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              {/* Avatar */}
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                msg.role === 'user'
                  ? 'ml-3 bg-blue-500'
                  : 'mr-3 bg-gradient-to-r from-blue-500 to-purple-600'
              }`}>
                {msg.role === 'user' ? (
                  <User className="h-4 w-4 text-white" />
                ) : (
                  <Bot className="h-4 w-4 text-white" />
                )}
              </div>

              {/* Message Bubble */}
              <div className={`rounded-2xl px-4 py-3 ${
                msg.role === 'user'
                  ? 'bg-blue-500 text-white rounded-br-md'
                  : 'bg-white text-gray-800 border border-gray-200 rounded-bl-md shadow-sm'
              }`}>
                <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                <div className={`text-xs mt-1 ${
                  msg.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                }`}>
                  {formatTime(msg.timestamp)}
                </div>
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="flex max-w-[85%]">
              {/* Bot Avatar */}
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 mr-3 flex items-center justify-center">
                <Bot className="h-4 w-4 text-white" />
              </div>

              {/* Typing Indicator */}
              <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-md px-4 py-3">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="px-4 py-2 border-t bg-white">
        <div className="flex flex-wrap gap-2">
          {quickActions.map((action, idx) => (
            <button
              key={idx}
              onClick={() => setInputValue(action)}
              className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-2.5 py-1.5 rounded-full transition-colors"
            >
              {action.length > 18 ? `${action.substring(0, 15)}...` : action}
            </button>
          ))}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t bg-white p-3">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message to your AI assistant..."
            className="flex-1 border border-gray-300 rounded-full px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 placeholder-gray-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-500 hover:to-purple-700 text-white rounded-full w-11 h-11 flex items-center justify-center disabled:opacity-50 transition-all"
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <Send className="h-4 w-4" />
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chatbot;