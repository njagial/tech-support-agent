// React Query Hooks for mobile app
import { useQuery, useMutation, useQueryClient } from 'react-query';
import DeviceTelemetryService from '../services/telemetry/DeviceTelemetryService';
import NetworkDiagnostics from '../services/telemetry/NetworkDiagnostics';

export function useDeviceTelemetry() {
  return useQuery('device-telemetry', () => DeviceTelemetryService.collectTelemetry(), {
    staleTime: 1000 * 60 * 5,
    retry: 1,
  });
}

export function useNetworkDiagnostics() {
  return useQuery('network-diagnostics', () => NetworkDiagnostics.runDiagnostics(), {
    staleTime: 1000 * 60 * 1,
    retry: 1,
  });
}

export function useScreenshotAnalysis() {
  const queryClient = useQueryClient();

  return useMutation(
    (base64Image: string) => {
      // Call screenshot analysis API
      return fetch(`${__DEV__ ? 'http://localhost:8000' : 'https://api.techsupport.example.com'}/api/v1/screenshot/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image_base64: base64Image }),
      }).then((res) => res.json());
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('screenshot-analysis');
      },
    }
  );
}

export function useDeepLink() {
  return useMutation(
    (data: { action: string; platform: 'ios' | 'android' }) => {
      return fetch(`${__DEV__ ? 'http://localhost:8000' : 'https://api.techsupport.example.com'}/api/v1/deeplink`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      }).then((res) => res.json());
    }
  );
}
