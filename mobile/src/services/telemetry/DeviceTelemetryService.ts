// Device Telemetry Service
import DeviceInfo from 'react-native-device-info';
import NetInfo from '@react-native-community/netinfo';
import { Platform } from 'react-native';
import * as Device from 'expo-device';
import RNFS from 'react-native-fs';
import * as Crypto from 'expo-crypto';

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

class DeviceTelemetryService {
  /**
   * Collect comprehensive device telemetry
   */
  async collectTelemetry(): Promise<DeviceTelemetry> {
    try {
      const [
        batteryLevel,
        isCharging,
        netInfo,
        totalSpace,
        freeSpace,
        totalMemory,
      ] = await Promise.all([
        DeviceInfo.getBatteryLevel(),
        DeviceInfo.isBatteryCharging(),
        NetInfo.fetch(),
        DeviceInfo.getTotalDiskCapacity(),
        DeviceInfo.getFreeDiskStorage(),
        DeviceInfo.getTotalMemory(),
      ]);

      // Hash device ID for privacy
      const uniqueId = await DeviceInfo.getUniqueId();
      const hashedId = await this.hashDeviceId(uniqueId);

      const telemetry: DeviceTelemetry = {
        device: {
          manufacturer: await DeviceInfo.getManufacturer(),
          model: DeviceInfo.getModel(),
          osVersion: DeviceInfo.getSystemVersion(),
          platform: Platform.OS as 'ios' | 'android',
          deviceId: hashedId,
        },
        battery: {
          level: Math.round(batteryLevel * 100),
          isCharging,
          batteryHealth: await this.estimateBatteryHealth(batteryLevel),
        },
        storage: {
          totalSpace: Math.round(totalSpace / (1024 ** 3)),
          freeSpace: Math.round(freeSpace / (1024 ** 3)),
          usedPercentage: Math.round(((totalSpace - freeSpace) / totalSpace) * 100),
        },
        memory: {
          totalRAM: Math.round(totalMemory / (1024 ** 3)),
        },
        network: {
          isConnected: netInfo.isConnected ?? false,
          type: netInfo.type,
          isInternetReachable: netInfo.isInternetReachable ?? false,
          ipAddress: netInfo.details?.ipAddress,
          ssid: netInfo.details?.ssid,
        },
        timestamp: new Date().toISOString(),
      };

      return telemetry;
    } catch (error) {
      console.error('Error collecting telemetry:', error);
      throw error;
    }
  }

  /**
   * Hash device ID using SHA-256 for privacy
   */
  private async hashDeviceId(deviceId: string): Promise<string> {
    try {
      const hash = await Crypto.digestStringAsync('SHA256', deviceId, {
        encoding: 'utf8',
      });
      return hash;
    } catch (error) {
      // Fallback for older Expo versions
      return Crypto.digestStringSync('SHA256', deviceId);
    }
  }

  /**
   * Estimate battery health based on current level
   */
  private async estimateBatteryHealth(
    currentLevel: number
  ): Promise<'good' | 'degraded' | 'unknown'> {
    if (currentLevel < 20) return 'degraded';
    return 'good';
  }

  /**
   * Run quick storage diagnostics
   */
  async diagnoseStorageIssues(): Promise<{
    status: 'healthy' | 'warning' | 'critical';
    message: string;
    freeSpaceGB: number;
  }> {
    const freeSpace = await DeviceInfo.getFreeDiskStorage();
    const freeSpaceGB = Math.round(freeSpace / (1024 ** 3));

    if (freeSpaceGB < 1) {
      return {
        status: 'critical',
        message: 'Storage critically low. Delete unused apps or media.',
        freeSpaceGB,
      };
    } else if (freeSpaceGB < 5) {
      return {
        status: 'warning',
        message: 'Storage running low. Consider freeing up space.',
        freeSpaceGB,
      };
    }

    return {
      status: 'healthy',
      message: 'Storage levels are healthy.',
      freeSpaceGB,
    };
  }
}

export default new DeviceTelemetryService();
