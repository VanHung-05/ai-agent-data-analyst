/**
 * components/shared/Sidebar.tsx
 * Hiển thị danh sách phiên hội thoại (sessions), không phải từng câu hỏi
 */

import React, { useState, useEffect } from 'react';
import { useChatStore } from '../../store/chatStore';
import type { ChatSession } from '../../store/chatStore';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  onNewChat: () => void;
}

/* ── Group sessions theo ngày ── */
function groupByDate(sessions: ChatSession[]) {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);

  const groups: Record<string, ChatSession[]> = {
    'Hôm nay': [],
    'Hôm qua': [],
    'Tuần trước': [],
    'Cũ hơn': [],
  };

  sessions.forEach((s) => {
    const d = new Date(s.updatedAt);
    if (d.toDateString() === today.toDateString()) {
      groups['Hôm nay'].push(s);
    } else if (d.toDateString() === yesterday.toDateString()) {
      groups['Hôm qua'].push(s);
    } else if (today.getTime() - d.getTime() < 7 * 86400_000) {
      groups['Tuần trước'].push(s);
    } else {
      groups['Cũ hơn'].push(s);
    }
  });

  return groups;
}

const Sidebar: React.FC<SidebarProps> = ({ onToggle, onNewChat }) => {
  const sessions = useChatStore((s) => s.sessions);
  const currentSessionId = useChatStore((s) => s.currentSessionId);
  const loadSession = useChatStore((s) => s.loadSession);
  const deleteSession = useChatStore((s) => s.deleteSession);
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [modelName, setModelName] = useState<string>('Đang tải...');

  useEffect(() => {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    fetch(`${baseUrl}/health`)
      .then((res) => res.json())
      .then((data) => {
        if (data.model) {
          setModelName(data.model);
        } else {
          setModelName('AI Model');
        }
      })
      .catch((err) => {
        console.error('Failed to fetch health model status', err);
        setModelName('AI Model');
      });
  }, []);

  // Sắp xếp mới nhất lên đầu
  const sorted = [...sessions].sort((a, b) => b.updatedAt - a.updatedAt);
  const groups = groupByDate(sorted);

  const handleLoad = (sessionId: string) => {
    if (sessionId !== currentSessionId) {
      loadSession(sessionId);
    }
  };

  return (
    <aside
      className="flex flex-col h-full w-[260px]"
      style={{ background: 'var(--sidebar-bg)', borderRight: '1px solid var(--sidebar-border)' }}
    >
      {/* ── Top bar ── */}
      <div className="flex items-center justify-between px-3 pt-3 pb-2 flex-shrink-0">
        <button
          onClick={onToggle}
          className="p-2 rounded-lg transition-colors hover:bg-white/10"
          style={{ color: 'var(--text-secondary)' }}
          aria-label="Đóng sidebar"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <button
          onClick={onNewChat}
          className="p-2 rounded-lg transition-colors hover:bg-white/10"
          style={{ color: 'var(--text-secondary)' }}
          aria-label="Phiên hội thoại mới"
          title="Phiên hội thoại mới"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
      </div>

      {/* ── Session list ── */}
      <div className="flex-1 overflow-y-auto px-2 py-1">
        {sorted.length === 0 ? (
          <div
            className="text-xs text-center py-8 px-3 leading-relaxed"
            style={{ color: 'var(--text-muted)' }}
          >
            Chưa có phiên hội thoại nào
          </div>
        ) : (
          <div className="space-y-4">
            {Object.entries(groups).map(([label, items]) => {
              if (items.length === 0) return null;
              return (
                <div key={label}>
                  <p
                    className="text-xs px-2 py-1 font-medium mb-0.5"
                    style={{ color: 'var(--text-muted)' }}
                  >
                    {label}
                  </p>
                  <div className="space-y-0.5">
                    {items.map((session) => {
                      const isActive = session.id === currentSessionId;
                      const isHovered = hoveredId === session.id;
                      return (
                        <div
                          key={session.id}
                          className="group relative flex items-center rounded-lg transition-colors"
                          style={{
                            background: isActive
                              ? 'rgba(255,255,255,0.12)'
                              : isHovered
                                ? 'rgba(255,255,255,0.07)'
                                : 'transparent',
                          }}
                          onMouseEnter={() => setHoveredId(session.id)}
                          onMouseLeave={() => setHoveredId(null)}
                        >
                          {/* Session button */}
                          <button
                            onClick={() => handleLoad(session.id)}
                            className="flex-1 text-left px-3 py-2.5 text-sm min-w-0"
                            style={{ color: 'var(--text-primary)' }}
                            title={session.title}
                          >
                            <span className="truncate block leading-snug">
                              {session.title}
                            </span>
                            <span
                              className="text-xs mt-0.5 block"
                              style={{ color: 'var(--text-muted)' }}
                            >
                              {session.messages.length} tin nhắn
                            </span>
                          </button>

                          {/* Delete button — hiện khi hover */}
                          {isHovered && (
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                deleteSession(session.id);
                              }}
                              className="flex-shrink-0 p-1.5 mr-1.5 rounded transition-colors hover:bg-white/15"
                              style={{ color: 'var(--text-muted)' }}
                              aria-label="Xóa phiên này"
                              title="Xóa"
                            >
                              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ── Bottom: model ── */}
      <div
        className="px-3 py-3 flex-shrink-0"
        style={{ borderTop: '1px solid var(--sidebar-border)' }}
      >
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-400 flex-shrink-0" />
          <span className="text-xs truncate" style={{ color: 'var(--text-muted)' }}>
            {modelName}
          </span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
