'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useUser } from '@/contexts/user-context';
import Chatbot from '@/components/chatbot/Chatbot';

export default function ChatPage() {
  const router = useRouter();
  const { user, token, loading } = useUser();

  // Check if user is authenticated
  useEffect(() => {
    if (!loading && !user) {
      // Redirect to login if not authenticated
      router.push('/login');
    }
  }, [user, loading, router]);

  // Show loading state while checking auth
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  // Redirect if not authenticated (redundant check)
  if (!user) {
    return null; // Redirect effect will handle navigation
  }

  return (
    <div className="container mx-auto py-6 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Task Assistant</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Manage your tasks using natural language. Simply talk to the AI assistant to add, list, complete, delete, or update your tasks.
          </p>
        </div>

        {user?.id && token ? (
          <Chatbot
            userId={user.id.toString()}
            token={token}
            className="h-[600px]"
          />
        ) : (
          <div className="text-center py-8 text-red-500">
            Authentication error. Please log in again.
          </div>
        )}

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Your conversations are private and secure. Messages are stored locally on your device.</p>
        </div>
      </div>
    </div>
  );
}