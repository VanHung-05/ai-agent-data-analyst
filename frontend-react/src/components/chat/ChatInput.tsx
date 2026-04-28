/**
 * components/chat/ChatInput.tsx — Responsive + mobile safe area
 */

import React, { useState, useRef, useEffect } from 'react';
import { useChatStore } from '../../store/chatStore';
import { useChatStream } from '../../hooks/useChatStream';

const ChatInput: React.FC = () => {
  const [input, setInput] = useState('');
  const isLoading = useChatStore((state) => state.isLoading);
  const { sendMessage } = useChatStream();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea height
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  }, [input]);

  const handleSubmit = () => {
    if (!input.trim()) return;
    sendMessage(input.trim());
    setInput('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const canSend = !!input.trim();

  return (
    <div
      className="flex-shrink-0 px-3 sm:px-4 md:px-6 pt-2 pb-safe"
      style={{
        background: 'var(--chat-bg)',
        paddingBottom: 'max(16px, env(safe-area-inset-bottom, 16px))',
      }}
    >
      <div className="max-w-3xl mx-auto">
        {/* Input box */}
        <div
          className="flex items-end gap-2 rounded-2xl px-3 sm:px-4 py-2 shadow-lg"
          style={{
            background: 'var(--input-bg)',
            border: '1px solid var(--input-border)',
          }}
        >
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={false}
            placeholder="Hỏi về dữ liệu..."
            className="flex-1 resize-none bg-transparent outline-none text-sm leading-relaxed py-1.5"
            style={{
              color: 'var(--text-primary)',
              maxHeight: '160px',
              /* Fix iOS zoom on focus */
              fontSize: '16px',
            }}
          />

          {/* Send button */}
          <button
            onClick={handleSubmit}
            disabled={!canSend}
            className="flex-shrink-0 w-8 h-8 sm:w-9 sm:h-9 rounded-lg flex items-center justify-center transition-all duration-150 active:scale-90"
            style={{
              background: canSend ? 'var(--accent)' : 'rgba(255,255,255,0.08)',
              color: canSend ? '#fff' : 'var(--text-muted)',
              cursor: canSend ? 'pointer' : 'not-allowed',
            }}
            aria-label="Gửi"
          >
            {isLoading && !input.trim() ? (
              <svg className="w-4 h-4 spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5}
                  d="M12 3v1m0 16v1m8.66-9h-1M4.34 12h-1m15.07-6.07-.71.71M5.64 18.36l-.71.71m12.02 0-.71-.71M5.64 5.64l-.71-.71" />
              </svg>
            ) : (
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5}
                  d="M5 10l7-7m0 0l7 7m-7-7v18" />
              </svg>
            )}
          </button>
        </div>

        {/* Hint — hide on very small screens */}
        <p
          className="text-center text-xs mt-1.5 hidden sm:block"
          style={{ color: 'var(--text-muted)' }}
        >
          Enter gửi · Shift+Enter xuống dòng · AI có thể mắc lỗi
        </p>
      </div>
    </div>
  );
};

export default ChatInput;
