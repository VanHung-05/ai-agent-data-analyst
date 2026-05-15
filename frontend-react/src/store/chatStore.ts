/**
 * store/chatStore.ts — Zustand Store với Session Management
 * ==========================================================
 * Mỗi "session" = 1 phiên hội thoại hoàn chỉnh.
 * Sidebar hiển thị danh sách sessions, không phải từng câu hỏi.
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Message } from '../types';
import { generateId } from '../utils/helpers';

/* ── Types ── */
export interface ChatSession {
  id: string;
  title: string;         // Câu hỏi đầu tiên (làm tiêu đề)
  messages: Message[];
  createdAt: number;
  updatedAt: number;
}

interface ChatStore {
  // Phiên hiện tại
  currentSessionId: string;
  messages: Message[];
  isLoading: boolean;
  error: string | null;

  // Lịch sử các phiên đã lưu
  sessions: ChatSession[];

  // ── Actions: messages ──
  addMessage: (message: Omit<Message, 'id' | 'timestamp'>) => void;
  updateMessage: (id: string, updates: Partial<Message>) => void;
  removeMessage: (id: string) => void;

  // ── Actions: sessions ──
  /** Lưu phiên hiện tại vào history rồi bắt đầu phiên mới */
  startNewSession: () => void;
  /** Load một phiên cũ thành phiên hiện tại */
  loadSession: (sessionId: string) => void;
  /** Xóa 1 phiên khỏi history */
  deleteSession: (sessionId: string) => void;

  // ── Actions: state ──
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  getLastMessage: () => Message | undefined;
}

/* ── Helper: tạo title từ câu hỏi đầu tiên ── */
function makeTitle(messages: Message[]): string {
  const first = messages.find((m) => m.role === 'user');
  if (!first) return 'Cuộc trò chuyện mới';
  const text = first.content.trim();
  return text.length > 50 ? text.substring(0, 50) + '…' : text;
}

/**
 * Helper: Đồng bộ phiên hiện tại vào danh sách sessions.
 * Gọi sau mỗi lần messages thay đổi để tự động lưu.
 */
function _syncCurrentSession(
  currentSessionId: string,
  messages: Message[],
  sessions: ChatSession[],
): ChatSession[] {
  if (messages.length === 0) return sessions;

  const now = Date.now();
  const existingIdx = sessions.findIndex((s) => s.id === currentSessionId);

  const updatedSession: ChatSession = {
    id: currentSessionId,
    title: makeTitle(messages),
    messages,
    createdAt: existingIdx >= 0 ? sessions[existingIdx].createdAt : now,
    updatedAt: now,
  };

  if (existingIdx >= 0) {
    return sessions.map((s, i) => (i === existingIdx ? updatedSession : s));
  }
  return [updatedSession, ...sessions];
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      currentSessionId: generateId(),
      messages: [],
      isLoading: false,
      error: null,
      sessions: [],

      /* ── Messages ── */
      addMessage: (message) =>
        set((state) => {
          const newMessages = [
            ...state.messages,
            { ...message, id: generateId(), timestamp: Date.now() },
          ];
          return {
            messages: newMessages,
            sessions: _syncCurrentSession(
              state.currentSessionId,
              newMessages,
              state.sessions,
            ),
          };
        }),

      updateMessage: (id, updates) =>
        set((state) => {
          const newMessages = state.messages.map((msg) =>
            msg.id === id ? { ...msg, ...updates } : msg
          );
          return {
            messages: newMessages,
            sessions: _syncCurrentSession(
              state.currentSessionId,
              newMessages,
              state.sessions,
            ),
          };
        }),

      removeMessage: (id) =>
        set((state) => ({
          messages: state.messages.filter((msg) => msg.id !== id),
        })),

      /* ── Sessions ── */
      startNewSession: () => {
        // Sessions đã được auto-sync, chỉ cần tạo phiên mới
        set({
          currentSessionId: generateId(),
          messages: [],
          error: null,
          isLoading: false,
        });
      },

      loadSession: (sessionId) => {
        const state = get();

        // Phiên hiện tại đã được auto-sync, chỉ cần load phiên được chọn
        const target = state.sessions.find((s) => s.id === sessionId);
        if (!target) return;
        set({
          currentSessionId: sessionId,
          messages: target.messages,
          error: null,
          isLoading: false,
        });
      },

      deleteSession: (sessionId) => {
        const state = get();
        const newSessions = state.sessions.filter((s) => s.id !== sessionId);
        
        if (state.currentSessionId === sessionId) {
          // Nếu đang mở phiên bị xóa, reset thành phiên mới
          set({
            sessions: newSessions,
            currentSessionId: generateId(),
            messages: [],
            error: null,
            isLoading: false,
          });
        } else {
          set({ sessions: newSessions });
        }
      },

      /* ── State ── */
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),
      getLastMessage: () => {
        const state = get();
        return state.messages.length > 0
          ? state.messages[state.messages.length - 1]
          : undefined;
      },
    }),
    {
      name: 'ai-analyst-chat',          // localStorage key
      partialize: (state) => ({         // Persist sessions + phiên hiện tại
        sessions: state.sessions,
        currentSessionId: state.currentSessionId,
        messages: state.messages,
      }),
    }
  )
);
