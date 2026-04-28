/**
 * types/index.ts — TypeScript Interfaces
 * ========================================
 * Định nghĩa tất cả các data structures dựa trên Backend API response schema
 */

export type MessageRole = 'user' | 'assistant';

export interface VisualizationRecommendation {
  chart_type: string;
  x?: string;
  y?: string;
  title?: string;
  label?: string;
  value?: string;
  reason?: string;
  routed_agent?: string;
  [key: string]: any; // Allow extra fields
}

export interface QueryResponse {
  question: string;
  current_agent: string;
  routing_info: Record<string, any>;
  answer: string;
  generated_sql: string | null;
  data: Record<string, any>[];
  row_count: number;
  visualization_recommendation: Record<string, any>;
  error: string | null;
}

export interface StepEvent {
  type: 'progress';
  step: string;
  message: string;
}

export interface ResultEvent {
  type: 'result';
  data: QueryResponse;
}

export interface ErrorEvent {
  type: 'error';
  error: string;
}

export interface DoneEvent {
  type: 'done';
}

export type StreamEvent = StepEvent | ResultEvent | ErrorEvent | DoneEvent;

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  sql?: string;
  data?: Record<string, any>[];
  chart?: VisualizationRecommendation;
  timestamp: number;
  status: 'pending' | 'success' | 'error';
  error?: string;
  rowCount?: number;
}

export interface RoutingInfo {
  intent: string;
  scores: Record<string, number>;
  selected_agents: string[];
  routing_method: string;
}

export interface RoutingResponse {
  question: string;
  routing_info: RoutingInfo;
}

export interface SchemaInfo {
  [key: string]: any;
}
