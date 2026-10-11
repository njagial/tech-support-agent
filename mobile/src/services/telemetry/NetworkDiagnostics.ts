// Network Diagnostics Service
import NetInfo, { NetInfoState } from '@react-native-community/netinfo';
import { Platform } from 'react-native';

export interface NetworkDiagnosticResult {
  connectivity: {
    isConnected: boolean;
    type: string;
    strength?: number;
  };
  latency?: number;
  dns: {
    resolves: boolean;
    latency?: number;
  };
  recommendation: string;
  timestamp: string;
}

class NetworkDiagnostics {
  /**
   * Run comprehensive network diagnostics
   */
  async runDiagnostics(): Promise<NetworkDiagnosticResult> {
    const netInfo = await NetInfo.fetch();

    const [pingResult, dnsResult] = await Promise.all([
      this.measureLatency(),
      this.testDNSResolution(),
    ]);

    const result: NetworkDiagnosticResult = {
      connectivity: {
        isConnected: netInfo.isConnected ?? false,
        type: netInfo.type,
        strength: await this.getSignalStrength(netInfo),
      },
      latency: pingResult.latency,
      dns: dnsResult,
      recommendation: this.generateRecommendation(netInfo, pingResult, dnsResult),
      timestamp: new Date().toISOString(),
    };

    return result;
  }

  /**
   * Measure network latency by timing a HEAD request
   */
  private async measureLatency(): Promise<{ latency?: number; success: boolean }> {
    try {
      const start = Date.now();
      const response = await fetch('https://www.google.com/generate_204', {
        method: 'HEAD',
        cache: 'no-cache',
      });
      const latency = Date.now() - start;
      return { latency, success: response.ok };
    } catch (error) {
      return { success: false };
    }
  }

  /**
   * Test DNS resolution
   */
  private async testDNSResolution(): Promise<{ resolves: boolean; latency?: number }> {
    try {
      const start = Date.now();
      await fetch('https://dns.google/resolve?name=google.com&type=A', {
        method: 'GET',
      });
      const latency = Date.now() - start;
      return { resolves: true, latency };
    } catch (error) {
      return { resolves: false };
    }
  }

  /**
   * Get Wi-Fi signal strength
   */
  private async getSignalStrength(netInfo: NetInfoState): Promise<number | undefined> {
    if (Platform.OS === 'android' && netInfo.type === 'wifi') {
      return undefined;
    }
    return undefined;
  }

  /**
   * Generate actionable recommendation
   */
  private generateRecommendation(
    netInfo: NetInfoState,
    pingResult: { latency?: number; success: boolean },
    dnsResult: { resolves: boolean }
  ): string {
    if (!netInfo.isConnected) {
      return 'No network connection. Check if Wi-Fi or mobile data is enabled.';
    }

    if (!dnsResult.resolves) {
      return 'DNS resolution failing. Try switching DNS servers or reconnecting.';
    }

    if (pingResult.latency && pingResult.latency > 500) {
      return 'High latency detected. Move closer to Wi-Fi router or switch to mobile data.';
    }

    return 'Network connection is healthy.';
  }

  /**
   * Subscribe to real-time network changes
   */
  subscribeToNetworkChanges(
    callback: (state: NetInfoState) => void
  ): () => void {
    return NetInfo.addEventListener(callback);
  }
}

export default new NetworkDiagnostics();
