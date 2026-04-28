/**
 * utils/helpers.ts — Utility Functions
 * ====================================
 */

export function generateId(): string {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export function formatTimestamp(timestamp: number): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

export function parseJSONLine(line: string): Record<string, any> {
  try {
    return JSON.parse(line);
  } catch {
    console.warn('Failed to parse JSON line:', line);
    return {};
  }
}

export function isValidJSON(str: string): boolean {
  try {
    JSON.parse(str);
    return true;
  } catch {
    return false;
  }
}
