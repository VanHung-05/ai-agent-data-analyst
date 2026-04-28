/**
 * hooks/useChatStream.ts
 * ======================
 * Custom hook xử lý SSE stream từ Backend API
 * Quản lý việc gửi câu hỏi, đọc stream, và cập nhật state
 */

import { useCallback } from 'react';
import { useChatStore } from '../store/chatStore';
import type { StreamEvent } from '../types';
import { API_BASE_URL } from '../api/config';

export function useChatStream() {
  const addMessage = useChatStore((state) => state.addMessage);
  const updateMessage = useChatStore((state) => state.updateMessage);
  const setLoading = useChatStore((state) => state.setLoading);
  const setError = useChatStore((state) => state.setError);

  const sendMessage = useCallback(
    async (question: string) => {
      // Add user message
      addMessage({
        role: 'user',
        content: question,
        status: 'success',
      });

      // Create assistant message placeholder
      addMessage({
        role: 'assistant',
        content: '',
        status: 'pending',
      });
      
      // Get the ID of the last message we just added
      const messages = useChatStore.getState().messages;
      const assistantId = messages[messages.length - 1].id;

      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`${API_BASE_URL}/chat/query/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question }),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        if (!response.body) {
          throw new Error('No response body');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let accumulatedText = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n\n');
          buffer = lines[lines.length - 1];

          for (const line of lines.slice(0, -1)) {
            if (line.startsWith('data: ')) {
              try {
                const event = JSON.parse(line.slice(6)) as StreamEvent;

                if (event.type === 'progress') {
                  // Update with progress message
                  updateMessage(assistantId, {
                    content: accumulatedText + `\n⏳ ${event.step}: ${event.message}`,
                  });
                } else if (event.type === 'result') {
                  // Full result received
                  const result = event.data;
                  accumulatedText = result.answer;
                  updateMessage(assistantId, {
                    content: result.answer,
                    sql: result.generated_sql || undefined,
                    data: result.data,
                    rowCount: result.row_count,
                    chart: result.visualization_recommendation as any,
                    status: 'success',
                  });
                } else if (event.type === 'error') {
                  throw new Error(event.error);
                } else if (event.type === 'done') {
                  // Stream ended
                  break;
                }
              } catch (parseError) {
                console.error('Failed to parse stream event:', parseError);
              }
            }
          }
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        setError(errorMessage);
        updateMessage(assistantId, {
          status: 'error',
          error: errorMessage,
          content: 'Có lỗi xảy ra khi xử lý câu hỏi của bạn.',
        });
      } finally {
        setLoading(false);
      }
    },
    [addMessage, updateMessage, setLoading, setError]
  );

  return { sendMessage };
}
