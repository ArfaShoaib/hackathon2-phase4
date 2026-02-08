'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { User } from '@/lib/api';
import { getUserSession, signOut as authSignOut } from '@/lib/auth';

interface UserContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (userData: User, userToken?: string) => void;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

interface UserProviderProps {
  children: ReactNode;
}

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const router = useRouter();
  // Initialize loading to true on client-side to prevent hydration mismatch
  const [loading, setLoading] = useState(() => {
    if (typeof window !== 'undefined') {
      // Client-side: start with loading state to match server
      return true;
    }
    // Server-side: always return true
    return true;
  });

  // Check for user session on initial load
  useEffect(() => {
    const checkSession = async () => {
      try {
        const session = await getUserSession();
        if (session?.user) {
          // Map the auth session user to our User type
          const userData: User = {
            id: String(session.user.id || ''),
            email: session.user.email || '',
            createdAt: session.user.created_at ? new Date(session.user.created_at).toISOString() : new Date().toISOString(),
          };
          setUser(userData);
        }

        // Get the token from localStorage
        if (typeof window !== 'undefined') {
          const storedToken = localStorage.getItem('access_token');
          setToken(storedToken);
        }
      } catch (error) {
        console.error('Error checking session:', error);
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = (userData: User, userToken?: string) => {
    setUser(userData);
    if (userToken) {
      setToken(userToken);
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', userToken);
      }
    }
  };

  const logout = async () => {
    try {
      await authSignOut();
    } catch (error) {
      console.error('Error signing out:', error);
    } finally {
      setUser(null);
      setToken(null);
      // Redirect to the main/home page after logout
      router.push('/');
    }
  };

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      setUser({ ...user, ...userData });
    }
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    updateUser,
  };

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}