// Shared Agent Protocol Types
// Synced between mobile and backend

export interface AgentState {
  messages: Message[];
  user_id: string;
  session_id: string;
  device_telemetry?: DeviceTelemetry;
  screenshot_analysis?: ScreenshotAnalysis;
  kb_search_results?: KBResult[];
  tool_executions: ToolExecution[];
  current_hypothesis?: string;
  recommended_actions: Action[];
  requires_hitl_approval: boolean;
  next_step: AgentStep;
}

export type AgentStep =
  | 'collect_telemetry'
  | 'request_screenshot'
  | 'search_kb'
  | 'analyze_symptoms'
  | 'generate_solution'
  | 'await_hitl'
  | 'end';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  metadata?: MessageMetadata;
}

export interface MessageMetadata {
  action?: string;
  screenshot?: string;
  tools_used?: string[];
  actions?: Action[];
  requires_approval?: boolean;
}

export interface Action {
  type: string;
  label: string;
  description: string;
  deepLink?: string;
  icon?: string;
}

export interface ToolExecution {
  tool_name: string;
  input_params: Record<string, unknown>;
  output: Record<string, unknown>;
  timestamp: string;
  success: boolean;
}

export interface DeviceTelemetry {
  device: {
    manufacturer: string;
    model: string;
    osVersion: string;
    platform: 'ios' | 'android';
    deviceId: string;
  };
  battery: {
    level: number;
    isCharging: boolean;
    batteryHealth?: 'good' | 'degraded' | 'unknown';
  };
  storage: {
    totalSpace: number;
    freeSpace: number;
    usedPercentage: number;
  };
  memory: {
    totalRAM: number;
    usedRAM?: number;
  };
  network: {
    isConnected: boolean;
    type: string;
    isInternetReachable: boolean;
    ipAddress?: string;
    ssid?: string;
  };
  timestamp: string;
}

export interface ScreenshotAnalysis {
  status: string;
  analysis: {
    detected_errors: string[];
    screen_context: string;
    ui_issues: string[];
    hypothesis: string;
    recommended_actions: string[];
  };
  requires_action: boolean;
}

export interface KBResult {
  title: string;
  content: string;
  source: string;
  relevance_score: number;
  os: 'ios' | 'android' | 'both';
  issue_category: string;
}

// API Response Interfaces
export interface ChatRequest {
  session_id?: string;
  user_id: string;
  message: string;
  device_telemetry?: DeviceTelemetry;
  screenshot_base64?: string;
}

export interface ChatResponse {
  session_id: string;
  message: string;
  actions?: Action[];
  requires_approval: boolean;
}

export interface DeepLinkResponse {
  platform: 'ios' | 'android';
  issue_type: string;
  deep_link: string;
  label: string;
  instruction: string;
}
