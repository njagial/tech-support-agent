import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';
import type { ChatSession, ConversationMessage, DeviceTelemetry } from '../types';

interface ChatState {
  // Data
  currentSessionId: string | null;
  sessions: Record<string, ChatSession>;
  deviceTelemetry: DeviceTelemetry | null;

  // Status
  isTyping: boolean;
  lastSynced: string | null;

  // Actions
  loadSession: () => Promise<void>;
  createSession: () => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  setDeviceTelemetry: (telemetry: DeviceTelemetry) => void;
  addMessageToSession: (message: ConversationMessage) => void;
  updateSessionMessages: (sessionId: string, messages: ConversationMessage[]) => void;
}

const API_BASE_URL = __DEV__ ? 'http://localhost:8000' : 'https://api.techsupport.example.com';

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      currentSessionId: null,
      sessions: {},
      deviceTelemetry: null,
      isTyping: false,
      lastSynced: null,

      loadSession: async () => {
        const { currentSessionId, sessions } = get();

        if (!currentSessionId || sessions[currentSessionId]) {
          return;
        }

        // Fetch session from API
        try {
          const response = await axios.get(`${API_BASE_URL}/api/v1/sessions/${currentSessionId}`);
          set({ sessions: { [currentSessionId]: response.data }, lastSynced: new Date().toISOString() });
        } catch (error) {
          // Create new session if not found
          await get().createSession();
        }
      },

      createSession: async () => {
        const sessionId = uuidv4();

        set((state) => ({
          currentSessionId: sessionId,
          sessions: {
            ...state.sessions,
            [sessionId]: {
              id: sessionId,
              messages: [],
              createdAt: new Date().toISOString(),
              updatedAt: new Date().toISOString(),
            },
          },
        }));
      },

      sendMessage: async (content) => {
        const { currentSessionId, sessions, deviceTelemetry, isTyping } = get();

        if (!currentSessionId || isTyping) return;

        const userMessage: ConversationMessage = {
          id: uuidv4(),
          role: 'user',
          content,
          timestamp: new Date().toISOString(),
        };

        // Add user message
        set((state) => {
          const session = state.sessions[currentSessionId!];
          return {
            sessions: {
              ...state.sessions,
              [currentSessionId!]: {
                ...session,
                messages: [...session.messages, userMessage],
                updatedAt: new Date().toISOString(),
              },
            },
          };
        });

        // Set typing state
        set({ isTyping: true });

        try {
          // Call API
          const response = await axios.post(`${API_BASE_URL}/api/v1/chat`, {
            session_id: currentSessionId,
            user_id: 'user_' + uuidv4().slice(0, 8), // Mock user ID
            message: content,
            device_telemetry: deviceTelemetry,
          });

          // Add assistant response
          const assistantMessage: ConversationMessage = {
            id: uuidv4(),
            role: 'assistant',
            content: response.data.message,
            timestamp: new Date().toISOString(),
            metadata: {
              actions: response.data.actions,
              requiresApproval: response.data.requires_approval,
            },
          };

          set((state) => {
            const session = state.sessions[currentSessionId!];
            return {
              sessions: {
                ...state.sessions,
                [currentSessionId!]: {
                  ...session,
                  messages: [...session.messages, assistantMessage],
                  updatedAt: new Date().toISOString(),
                },
              },
              isTyping: false,
              lastSynced: new Date().toISOString(),
            };
          });
        } catch (error) {
          // Handle error
          console.error('Error sending message:', error);
          const errorMessage: ConversationMessage = {
            id: uuidv4(),
            role: 'assistant',
            content: 'Sorry, I encountered an error processing your request. Please try again.',
            timestamp: new Date().toISOString(),
          };

          set((state) => {
            const session = state.sessions[currentSessionId!];
            return {
              sessions: {
                ...state.sessions,
                [currentSessionId!]: {
                  ...session,
                  messages: [...session.messages, errorMessage],
                  updatedAt: new Date().toISOString(),
                },
              },
              isTyping: false,
            };
          });
        }
      },

      setDeviceTelemetry: (telemetry) => {
        set({ deviceTelemetry: telemetry, lastSynced: new Date().toISOString() });
      },

      addMessageToSession: (message) => {
        const { currentSessionId, sessions } = get();
        if (!currentSessionId) return;

        set((state) => {
          const session = state.sessions[currentSessionId];
          return {
            sessions: {
              ...state.sessions,
              [currentSessionId]: {
                ...session,
                messages: [...session.messages, message],
                updatedAt: new Date().toISOString(),
              },
            },
          };
        });
      },

      updateSessionMessages: (sessionId, messages) => {
        set((state) => ({
          sessions: {
            ...state.sessions,
            [sessionId]: {
              ...state.sessions[sessionId],
              messages,
              updatedAt: new Date().toISOString(),
            },
          },
        }));
      },
    }),
    {
      name: 'chat-storage',
      storage: createJSONStorage(() => ({
        getItem: async (key) => {
          const { getItem } = await import('@react-native-async-storage/async-storage');
          return getItem(key);
        },
        setItem: async (key, value) => {
          const { setItem } = await import('@react-native-async-storage/async-storage');
          return setItem(key, value);
        },
        removeItem: async (key) => {
          const { removeItem } = await import('@react-native-async-storage/async-storage');
          return removeItem(key);
        },
      })),
    }
  )
);

// Context for provider
import React from 'react';
import { useChatStore } from './chatStore';

export const ChatProvider: React.FC<React.PropsWithChildren> = ({ children }) => {
  const { loadSession, createSession } = useChatStore();

  React.useEffect(() => {
    // Initialize session on mount
    loadSession().catch(console.error);
  }, [loadSession]);

  return <>{children}</>;
};
