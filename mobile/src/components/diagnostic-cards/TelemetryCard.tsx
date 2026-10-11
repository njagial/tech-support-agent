// Telemetry Card Component
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card, ProgressBar, Button } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { DeviceTelemetry } from '../types';

interface TelemetryCardProps {
  telemetry: DeviceTelemetry;
  showCollectionButton?: boolean;
  onCollect?: () => void;
}

export const TelemetryCard: React.FC<TelemetryCardProps> = ({
  telemetry,
  showCollectionButton = false,
  onCollect,
}) => {
  const getStorageColor = () => {
    if (telemetry.storage.usedPercentage > 90) return '#FF3B30';
    if (telemetry.storage.usedPercentage > 75) return '#FF9500';
    return '#34C759';
  };

  const getBatteryColor = () => {
    if (telemetry.battery.level < 20) return '#FF3B30';
    if (telemetry.battery.level < 50) return '#FF9500';
    return '#34C759';
  };

  return (
    <Card style={styles.card} elevation={2}>
      <Card.Content>
        <Text style={styles.cardTitle}>Device Health</Text>

        {/* Battery Status */}
        <View style={styles.metricRow}>
          <View style={styles.metricHeader}>
            <Icon name="battery" size={20} color={getBatteryColor()} />
            <Text style={styles.metricLabel}>Battery</Text>
          </View>
          <Text style={styles.metricValue}>
            {telemetry.battery.level}%
            {telemetry.battery.isCharging && ' (Charging)'}
          </Text>
        </View>

        {/* Storage Status */}
        <View style={styles.metricRow}>
          <View style={styles.metricHeader}>
            <Icon name="harddisk" size={20} color={getStorageColor()} />
            <Text style={styles.metricLabel}>Storage</Text>
          </View>
          <Text style={styles.metricValue}>
            {telemetry.storage.freeSpace}GB free
          </Text>
          <ProgressBar
            progress={telemetry.storage.usedPercentage / 100}
            color={getStorageColor()}
            style={styles.progressBar}
          />
        </View>

        {/* Memory Status */}
        <View style={styles.metricRow}>
          <View style={styles.metricHeader}>
            <Icon name="memory" size={20} color="#007AFF" />
            <Text style={styles.metricLabel}>RAM</Text>
          </View>
          <Text style={styles.metricValue}>
            {telemetry.memory.totalRAM}GB total
          </Text>
        </View>

        {/* Network Status */}
        <View style={styles.metricRow}>
          <View style={styles.metricHeader}>
            <Icon
              name={telemetry.network.isConnected ? 'wifi' : 'wifi-off'}
              size={20}
              color={telemetry.network.isConnected ? '#34C759' : '#FF3B30'}
            />
            <Text style={styles.metricLabel}>Network</Text>
          </View>
          <Text style={styles.metricValue}>
            {telemetry.network.type.toUpperCase()}
            {telemetry.network.ssid && ` (${telemetry.network.ssid})`}
          </Text>
        </View>

        {showCollectionButton && (
          <Button mode="text" onPress={onCollect} style={styles.refreshButton}>
            <Icon name="refresh" size={18} color="#007AFF" />
            <Text style={styles.refreshText}>Refresh Telemetry</Text>
          </Button>
        )}
      </Card.Content>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginVertical: 8,
    marginHorizontal: 12,
    borderRadius: 12,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 16,
    color: '#1F1F1F',
  },
  metricRow: {
    marginBottom: 16,
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  metricLabel: {
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
    color: '#333',
  },
  metricValue: {
    fontSize: 14,
    color: '#666',
    marginLeft: 28,
  },
  progressBar: {
    marginTop: 8,
    marginLeft: 28,
    height: 6,
    borderRadius: 3,
  },
  refreshButton: {
    marginTop: 16,
    padding: 0,
    minHeight: 0,
  },
  refreshText: {
    marginLeft: 4,
    color: '#007AFF',
  },
});
