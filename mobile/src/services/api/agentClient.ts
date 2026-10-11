// API Client for backend communication
import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const API_BASE_URL = __DEV__ ? 'http://localhost:8000' : 'https://api.techsupport.example.com';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth token
apiClient.interceptors.request.use(
  (config) => {
    const { token } = useAuthStore.getState();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

// API Endpoints
export const agentApi = {
  chat: (data: {
    session_id: string;
    user_id: string;
    message: string;
    device_telemetry?: any;
    screenshot_base64?: string;
  }) => apiClient.post('/api/v1/chat', data),

  getSessions: () => apiClient.get('/api/v1/sessions'),

  getSession: (sessionId: string) => apiClient.get(`/api/v1/sessions/${sessionId}`),

  submitTelemetry: (telemetry: any) => apiClient.post('/api/v1/telemetry', telemetry),

  analyzeScreenshot: (formData: FormData) => {
    const { token } = useAuthStore.getState();
    return apiClient.post('/api/v1/screenshot/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}`,
      },
    });
  },

  triggerDeepLink: (action: string, platform: 'ios' | 'android') =>
    apiClient.post('/api/v1/deeplink', { action, platform }),
};
