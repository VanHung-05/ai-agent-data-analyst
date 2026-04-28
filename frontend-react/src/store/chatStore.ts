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
        set((state) => ({
          messages: [
            ...state.messages,
            { ...message, id: generateId(), timestamp: Date.now() },
          ],
        })),

      updateMessage: (id, updates) =>
        set((state) => ({
          messages: state.messages.map((msg) =>
            msg.id === id ? { ...msg, ...updates } : msg
          ),
        })),

      removeMessage: (id) =>
        set((state) => ({
          messages: state.messages.filter((msg) => msg.id !== id),
        })),

      /* ── Sessions ── */
      startNewSession: () => {
        const state = get();
        const now = Date.now();

        // Chỉ lưu nếu phiên hiện tại có ít nhất 1 tin nhắn
        if (state.messages.length > 0) {
          const existingIdx = state.sessions.findIndex(
            (s) => s.id === state.currentSessionId
          );

          const updatedSession: ChatSession = {
            id: state.currentSessionId,
            title: makeTitle(state.messages),
            messages: state.messages,
            createdAt:
              existingIdx >= 0
                ? state.sessions[existingIdx].createdAt
                : now,
            updatedAt: now,
          };

          const newSessions =
            existingIdx >= 0
              ? state.sessions.map((s, i) =>
                  i === existingIdx ? updatedSession : s
                )
              : [updatedSession, ...state.sessions];

          set({
            sessions: newSessions,
            currentSessionId: generateId(),
            messages: [],
            error: null,
            isLoading: false,
          });
        } else {
          // Không có gì để lưu, chỉ reset ID
          set({
            currentSessionId: generateId(),
            messages: [],
            error: null,
            isLoading: false,
          });
        }
      },

      loadSession: (sessionId) => {
        const state = get();

        // Lưu phiên hiện tại trước nếu có nội dung
        if (state.messages.length > 0) {
          const now = Date.now();
          const existingIdx = state.sessions.findIndex(
            (s) => s.id === state.currentSessionId
          );
          const updatedSession: ChatSession = {
            id: state.currentSessionId,
            title: makeTitle(state.messages),
            messages: state.messages,
            createdAt:
              existingIdx >= 0
                ? state.sessions[existingIdx].createdAt
                : now,
            updatedAt: now,
          };
          const savedSessions =
            existingIdx >= 0
              ? state.sessions.map((s, i) =>
                  i === existingIdx ? updatedSession : s
                )
              : [updatedSession, ...state.sessions];

          // Load session được chọn
          const target = savedSessions.find((s) => s.id === sessionId);
          if (!target) return;
          set({
            sessions: savedSessions,
            currentSessionId: sessionId,
            messages: target.messages,
            error: null,
            isLoading: false,
          });
        } else {
          const target = state.sessions.find((s) => s.id === sessionId);
          if (!target) return;
          set({
            currentSessionId: sessionId,
            messages: target.messages,
            error: null,
            isLoading: false,
          });
        }
      },

      deleteSession: (sessionId) =>
        set((state) => ({
          sessions: state.sessions.filter((s) => s.id !== sessionId),
        })),

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
      partialize: (state) => ({         // Chỉ persist sessions, không persist isLoading
        sessions: state.sessions,
      }),
    }
  )
);
