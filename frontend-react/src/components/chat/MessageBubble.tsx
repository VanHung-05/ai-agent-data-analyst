/**
 * components/chat/MessageBubble.tsx — Responsive
 */

import React, { useState, useEffect } from 'react';
import type { Message } from '../../types';
import { formatTimestamp } from '../../utils/helpers';
import SQLViewer from '../shared/SQLViewer';
import DataTable from '../shared/DataTable';
import DynamicChart from '../charts/DynamicChart';

interface MessageBubbleProps {
  message: Message;
}

const AIAvatar = () => (
  <div
    className="flex-shrink-0 w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-white text-xs font-bold shadow"
    style={{ background: 'linear-gradient(135deg, #19c37d 0%, #0ea5e9 100%)' }}
  >
    AI
  </div>
);

const UserAvatar = () => (
  <div
    className="flex-shrink-0 w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-white text-xs font-bold shadow"
    style={{ background: '#5b5bd6' }}
  >
    U
  </div>
);

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const isUser = message.role === 'user';

  useEffect(() => {
    if (message.role === 'assistant' && message.status === 'pending') {
      // Khi đang xử lý: giữ text rỗng, chỉ hiện dots animation
      setIsTyping(false);
      setDisplayedText('');
    } else if (message.role === 'assistant') {
      setIsTyping(false);
      setDisplayedText(message.content);
    } else {
      setDisplayedText(message.content);
    }
  }, [message]);

  useEffect(() => {
    if (!isTyping || displayedText.length >= message.content.length) return;
    const timer = setTimeout(() => {
      setDisplayedText((prev) => prev + message.content[prev.length]);
    }, 10);
    return () => clearTimeout(timer);
  }, [displayedText, isTyping, message.content]);

  return (
    <div className={`flex gap-2 sm:gap-3 py-4 sm:py-5 msg-enter ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* AI avatar — left */}
      {!isUser && <AIAvatar />}

      <div
        className="flex-1 min-w-0"
        style={{ maxWidth: isUser ? '85%' : '100%' }}
      >
        {isUser ? (
          /* User bubble */
          <div className="flex justify-end">
            <div
              className="px-3 sm:px-4 py-2.5 sm:py-3 text-sm leading-relaxed break-words"
              style={{
                background: 'var(--user-bubble)',
                color: 'var(--text-primary)',
                borderRadius: '18px 18px 4px 18px',
                maxWidth: '100%',
              }}
            >
              {displayedText}
            </div>
          </div>
        ) : (
          /* AI message — full width, no bubble */
          <div className="text-sm leading-relaxed" style={{ color: 'var(--text-primary)' }}>
            {/* Đang suy nghĩ — chỉ hiện khi pending */}
            {message.status === 'pending' && (
              <div className="flex items-center gap-2 py-1">
                <div className="flex items-center gap-1">
                  {[0, 160, 320].map((delay) => (
                    <span
                      key={delay}
                      className="w-2 h-2 rounded-full animate-bounce"
                      style={{
                        background: 'var(--accent)',
                        animationDelay: `${delay}ms`,
                        animationDuration: '1s',
                      }}
                    />
                  ))}
                </div>
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  Đang suy nghĩ...
                </span>
              </div>
            )}

            {/* Text — chỉ hiện khi không pending và có nội dung */}
            {message.status !== 'pending' && displayedText && (
              <p className="whitespace-pre-wrap break-words">
                {displayedText}
                {isTyping && <span className="cursor-blink ml-0.5">▊</span>}
              </p>
            )}

            {/* Error */}
            {message.error && (
              <div
                className="mt-3 px-3 sm:px-4 py-2.5 sm:py-3 rounded-xl text-sm"
                style={{
                  background: 'rgba(239,68,68,0.12)',
                  color: '#fca5a5',
                  border: '1px solid rgba(239,68,68,0.25)',
                }}
              >
                ⚠️ {message.error}
              </div>
            )}

            {/* SQL */}
            {message.sql && (
              <div className="mt-3">
                <SQLViewer sql={message.sql} />
              </div>
            )}

            {/* Data table */}
            {message.data && message.data.length > 0 && (
              <div className="mt-3">
                <DataTable data={message.data} rowCount={message.rowCount} />
              </div>
            )}

            {/* Chart */}
            {message.data && message.data.length > 0 && message.chart && (
              <div className="mt-3">
                <DynamicChart data={message.data} recommendation={message.chart} />
              </div>
            )}
          </div>
        )}

        {/* Timestamp */}
        <div
          className={`text-xs mt-1 ${isUser ? 'text-right' : 'text-left'}`}
          style={{ color: 'var(--text-muted)' }}
        >
          {formatTimestamp(message.timestamp)}
        </div>
      </div>

      {/* User avatar — right */}
      {isUser && <UserAvatar />}
    </div>
  );
};

export default MessageBubble;
