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

/** Map step code → thông báo tiếng Việt thân thiện */
const STEP_LABELS: Record<string, string> = {
  policy_block: 'Kiểm tra chính sách an toàn...',
  llm_init: 'Khởi động AI...',
  router: 'Đang phân tích câu hỏi...',
  conversation: 'Đang soạn câu trả lời...',
  db_connect: 'Đang kết nối cơ sở dữ liệu...',
  sql_generate: 'Đang viết câu lệnh truy vấn...',
  sql_execute: 'Đang truy vấn dữ liệu...',
  visualize: 'Đang chuẩn bị biểu đồ...',
  nlg: 'Đang diễn giải kết quả...',
  fallback: 'Đang thử lại...',
  done: 'Hoàn tất!',
};

function friendlyStep(step: string): string {
  return STEP_LABELS[step] ?? `⏳ ${step}...`;
}

interface QueueTask {
  question: string;
  assistantId: string;
}

const taskQueue: QueueTask[] = [];
let isProcessing = false;

async function processQueue() {
  if (isProcessing || taskQueue.length === 0) return;
  isProcessing = true;

  const { updateMessage, setLoading, setError } = useChatStore.getState();
  setLoading(true);

  while (taskQueue.length > 0) {
    const task = taskQueue.shift();
    if (!task) continue;
    
    const { question, assistantId } = task;

    // Đổi trạng thái từ queued sang pending để hiển thị đang làm
    updateMessage(assistantId, {
      content: 'Khởi động AI...',
      status: 'pending',
    });
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
      let hasExplicitAnswerEvent = false;

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
                updateMessage(assistantId, {
                  content: friendlyStep(event.step),
                  status: 'pending',
                });
              } else if (event.type === 'result') {
                const result = event.data;
                if (result.answer && !hasExplicitAnswerEvent) {
                  accumulatedText = result.answer;
                }
                updateMessage(assistantId, {
                  content: accumulatedText,
                  sql: result.generated_sql || undefined,
                  data: result.data,
                  rowCount: result.row_count,
                  chart: result.visualization_recommendation,
                  status: accumulatedText ? 'success' : 'pending',
                });
              } else if (event.type === 'chart_recommendation') {
                updateMessage(assistantId, {
                  chart: event.data,
                });
              } else if (event.type === 'answer') {
                hasExplicitAnswerEvent = true;
                const nextText = event.delta ? `${accumulatedText}${event.delta}` : (event.text ?? accumulatedText);
                accumulatedText = nextText;
                updateMessage(assistantId, {
                  content: accumulatedText,
                  status: 'success',
                });
              } else if (event.type === 'error') {
                const errorMsg = event.error || 'Đã xảy ra lỗi không xác định.';
                setError(errorMsg);
                updateMessage(assistantId, {
                  status: 'error',
                  error: errorMsg,
                  content: 'Có lỗi xảy ra khi xử lý câu hỏi của bạn.',
                });
                break;
              } else if (event.type === 'done') {
                updateMessage(assistantId, {
                  status: accumulatedText ? 'success' : 'error',
                });
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
    }
  }

  // Khi hết queue
  isProcessing = false;
  setLoading(false);
}

export function useChatStream() {
  const addMessage = useChatStore((state) => state.addMessage);

  const sendMessage = useCallback(
    (question: string) => {
      // 1. Ghi nhận ngay câu hỏi của user
      addMessage({
        role: 'user',
        content: question,
        status: 'success',
      });

      // 2. Tạo placeholder assistant message với trạng thái queued
      addMessage({
        role: 'assistant',
        content: '⏳ Đang chờ đến lượt...',
        status: 'queued',
      });

      // Lấy ID của assistant message vừa thêm vào
      const messages = useChatStore.getState().messages;
      const assistantId = messages[messages.length - 1].id;

      // 3. Đưa vào hàng đợi và chạy
      taskQueue.push({ question, assistantId });
      processQueue();
    },
    [addMessage]
  );

  return { sendMessage };
}
