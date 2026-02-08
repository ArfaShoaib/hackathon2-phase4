// This layout is optional since we're already handling auth in the page component
// But we can add it for consistency

import { ReactNode } from 'react';

export default function ChatLayout({
  children,
}: {
  children: ReactNode;
}) {
  return <>{children}</>;
}