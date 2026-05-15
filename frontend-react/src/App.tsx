/**
 * App.tsx — Responsive Layout (Desktop + Mobile)
 * - Desktop: sidebar cố định bên trái
 * - Mobile: sidebar là overlay drawer với backdrop
 */

import { useState, useEffect } from 'react';
import { useChatStore } from './store/chatStore';
import ChatWindow from './components/chat/ChatWindow';
import Sidebar from './components/shared/Sidebar';
import './index.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const startNewSession = useChatStore((state) => state.startNewSession);

  // Detect mobile vs desktop
  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      // Desktop: mặc định mở sidebar; Mobile: đóng
      if (!mobile) setSidebarOpen(true);
      else setSidebarOpen(false);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleNewChat = () => {
    startNewSession();
    if (isMobile) setSidebarOpen(false);
  };

  return (
    <div className="flex w-full h-full overflow-hidden" style={{ background: 'var(--chat-bg)' }}>

      {/* ── Mobile backdrop ── */}
      {isMobile && sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/60 backdrop-blur-sm"
          onClick={() => setSidebarOpen(false)}
          aria-label="Close sidebar"
        />
      )}

      {/* ── Sidebar ── */}
      <div
        className={`
          flex-shrink-0 z-30 transition-transform duration-300
          ${isMobile ? 'fixed inset-y-0 left-0' : 'relative'}
          ${isMobile && !sidebarOpen ? '-translate-x-full' : 'translate-x-0'}
        `}
        style={{ width: '260px' }}
      >
        <Sidebar
          isOpen={true}
          onToggle={() => setSidebarOpen(false)}
          onNewChat={handleNewChat}
        />
      </div>

      {/* ── Main area ── */}
      <div className="flex-1 flex flex-col overflow-hidden min-w-0">
        {/* Top bar — only shown when sidebar hidden */}
        {(!sidebarOpen || isMobile) && (
          <div
            className="flex items-center px-3 py-2 border-b flex-shrink-0"
            style={{ borderColor: 'var(--sidebar-border)', background: 'var(--chat-bg)' }}
          >
            <button
              onClick={() => setSidebarOpen(true)}
              className="p-2 rounded-lg transition-colors hover:bg-white/10 mr-2"
              style={{ color: 'var(--text-secondary)' }}
              aria-label="Open sidebar"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <span className="text-sm font-semibold" style={{ color: 'var(--text-primary)' }}>
              AI Data Analyst
            </span>

            {/* New chat icon on mobile topbar */}
            {isMobile && (
              <button
                onClick={handleNewChat}
                className="ml-auto p-2 rounded-lg transition-colors hover:bg-white/10"
                style={{ color: 'var(--text-secondary)' }}
                aria-label="New chat"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
            )}
          </div>
        )}

        <ChatWindow />
      </div>
    </div>
  );
}

export default App;
