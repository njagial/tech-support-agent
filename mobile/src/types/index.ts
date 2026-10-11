// Mobile app type definitions

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

export interface ConversationMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  metadata?: {
    action?: string;
    screenshot?: string;
    toolsUsed?: string[];
    actions?: {
      type: string;
      label: string;
      description: string;
      deepLink?: string;
    }[];
    requiresApproval?: boolean;
  };
}

export interface ChatSession {
  id: string;
  messages: ConversationMessage[];
  deviceTelemetry?: DeviceTelemetry;
  createdAt: string;
  updatedAt: string;
}

export interface DiagnosticCardAction {
  type: string;
  label: string;
  description: string;
  deepLink?: string;
  icon?: string;
}

export type ToolType =
  | 'device_telemetry'
  | 'network_diagnostics'
  | 'kb_search'
  | 'screenshot_analysis'
  | 'deep_link_generator';

export interface AgentState {
  messages: ConversationMessage[];
  currentHypothesis?: string;
  recommendedActions: DiagnosticCardAction[];
  requiresHITLApproval: boolean;
  nextStep: string;
}
