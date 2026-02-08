'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useUser } from '@/contexts/user-context';
import { Spinner } from './ui/spinner';


interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  fallback = (
    <div className="flex justify-center items-center h-screen">
      <Spinner />
    </div>
  )
}) => {
  const { user, loading } = useUser();
  const router = useRouter();
  const [hasCheckedAuth, setHasCheckedAuth] = useState(false);

  useEffect(() => {
    if (!loading) {
      if (!user) {
        // Redirect to login page
        router.push('/login'); // Adjust the login path as needed
      } else {
        setHasCheckedAuth(true);
      }
    }
  }, [user, loading, router]);

  // Show fallback while checking auth status or if not authenticated
  if (loading || !hasCheckedAuth) {
    return fallback;
  }

  // Render children if authenticated
  return <>{children}</>;
};