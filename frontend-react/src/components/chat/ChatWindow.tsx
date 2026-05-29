/**
 * components/chat/ChatWindow.tsx — Responsive
 */

import React, { useRef, useEffect, useCallback, useState } from 'react';
import { useChatStore } from '../../store/chatStore';
import { useChatStream } from '../../hooks/useChatStream';
import MessageBubble from './MessageBubble';
import ChatInput from './ChatInput';

/** Khoảng cách (px) từ đáy để coi là "đang xem tin mới nhất" */
const NEAR_BOTTOM_PX = 120;

const SUGGESTION_PROMPTS = [
  'Tổng doanh thu từng danh mục?',
  'Top 10 sản phẩm bán chạy nhất?',
  'Xu hướng đơn hàng theo tháng 2018?',
  'Tỉ lệ đánh giá 5 sao theo danh mục?',
];

const ChatWindow: React.FC = () => {
  const messages = useChatStore((state) => state.messages);
  const isLoading = useChatStore((state) => state.isLoading);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const stickToBottomRef = useRef(true);
  const prevMessageCountRef = useRef(0);
  const [showScrollDown, setShowScrollDown] = useState(false);
  const { sendMessage } = useChatStream();

  const isNearBottom = useCallback(() => {
    const el = scrollContainerRef.current;
    if (!el) return true;
    return el.scrollHeight - el.scrollTop - el.clientHeight <= NEAR_BOTTOM_PX;
  }, []);

  const scrollToBottom = useCallback((behavior: ScrollBehavior = 'auto') => {
    messagesEndRef.current?.scrollIntoView({ behavior });
  }, []);

  const handleScroll = useCallback(() => {
    const near = isNearBottom();
    stickToBottomRef.current = near;
    setShowScrollDown(!near);
  }, [isNearBottom]);

  useEffect(() => {
    const prevCount = prevMessageCountRef.current;
    const count = messages.length;
    prevMessageCountRef.current = count;

    // Tin nhắn mới (user gửi hoặc assistant placeholder) → luôn kéo xuống
    if (count > prevCount) {
      stickToBottomRef.current = true;
    }

    if (stickToBottomRef.current || isNearBottom()) {
      stickToBottomRef.current = true;
      setShowScrollDown(false);
      scrollToBottom(count > prevCount ? 'smooth' : 'auto');
    } else {
      setShowScrollDown(true);
    }
  }, [messages, isNearBottom, scrollToBottom]);

  return (
    <div className="flex-1 flex flex-col overflow-hidden relative" style={{ background: 'var(--chat-bg)' }}>
      {/* ── Messages area ── */}
      <div
        ref={scrollContainerRef}
        className="flex-1 overflow-y-auto"
        onScroll={handleScroll}
      >
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

      {/* Nút cuộn xuống khi user đang đọc tin cũ */}
      {showScrollDown && (
        <ScrollToBottomButton
          isLoading={isLoading}
          onClick={() => {
            stickToBottomRef.current = true;
            setShowScrollDown(false);
            scrollToBottom('smooth');
          }}
        />
      )}

      {/* ── Input area ── */}
      <ChatInput />
    </div>
  );
};

interface ScrollToBottomButtonProps {
  isLoading: boolean;
  onClick: () => void;
}

const ScrollToBottomButton: React.FC<ScrollToBottomButtonProps> = ({ isLoading, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    className="absolute left-1/2 -translate-x-1/2 z-10 flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium shadow-lg transition-all hover:brightness-110"
    style={{
      bottom: 'calc(88px + env(safe-area-inset-bottom, 0px))',
      background: 'var(--chat-surface)',
      color: 'var(--text-primary)',
      border: '1px solid var(--input-border)',
    }}
    aria-label="Cuộn xuống tin mới nhất"
  >
    {isLoading ? 'Đang trả lời…' : 'Tin mới'}
    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
    </svg>
  </button>
);

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
