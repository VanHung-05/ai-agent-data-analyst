/**
 * components/chat/ChatWindow.tsx — Responsive
 */

import React, { useRef, useEffect } from 'react';
import { useChatStore } from '../../store/chatStore';
import { useChatStream } from '../../hooks/useChatStream';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';

const SUGGESTION_PROMPTS = [
  'Tổng doanh thu từng danh mục?',
  'Top 10 sản phẩm bán chạy nhất?',
  'Xu hướng đơn hàng theo tháng 2018?',
  'Tỉ lệ đánh giá 5 sao theo danh mục?',
];

const ChatWindow: React.FC = () => {
  const messages = useChatStore((state) => state.messages);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { sendMessage } = useChatStream();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 flex flex-col overflow-hidden" style={{ background: 'var(--chat-bg)' }}>
      {/* ── Messages area ── */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <WelcomeScreen onSend={sendMessage} />
        ) : (
          <div className="max-w-3xl mx-auto px-3 sm:px-4 md:px-6 py-4 sm:py-6 space-y-1">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* ── Input area ── */}
      <ChatInput />
    </div>
  );
};

/* ── Welcome Screen — responsive grid ── */
interface WelcomeScreenProps {
  onSend: (text: string) => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onSend }) => (
  <div className="flex flex-col items-center justify-center h-full px-4 pb-4">
    {/* Icon */}
    <div
      className="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center mb-4 sm:mb-5 shadow-xl"
      style={{ background: 'linear-gradient(135deg, #19c37d 0%, #0ea5e9 100%)' }}
    >
      <svg className="w-7 h-7 sm:w-8 sm:h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    </div>

    <h1
      className="text-2xl sm:text-3xl font-semibold mb-2 text-center"
      style={{ color: 'var(--text-primary)' }}
    >
      AI Data Analyst
    </h1>
    <p
      className="text-xs sm:text-sm mb-6 sm:mb-10 text-center px-4"
      style={{ color: 'var(--text-secondary)' }}
    >
      Đặt câu hỏi về dữ liệu Olist E-Commerce bằng ngôn ngữ tự nhiên
    </p>

    {/* Suggestion cards — 1 col on mobile, 2 cols on sm+ */}
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-3 w-full max-w-2xl">
      {SUGGESTION_PROMPTS.map((prompt, i) => (
        <button
          key={i}
          onClick={() => onSend(prompt)}
          className="text-left px-4 py-3 rounded-xl text-sm transition-all duration-150 hover:brightness-110 active:scale-[0.98]"
          style={{
            background: 'var(--chat-surface)',
            color: 'var(--text-primary)',
            border: '1px solid var(--input-border)',
            lineHeight: '1.4',
          }}
        >
          {prompt}
        </button>
      ))}
    </div>
  </div>
);

export default ChatWindow;
