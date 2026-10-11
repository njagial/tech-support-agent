import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Text, Button, Chip, ActivityIndicator, List } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useQuery } from 'react-query';
import DeviceTelemetryService from '../services/telemetry/DeviceTelemetryService';
import NetworkDiagnostics from '../services/telemetry/NetworkDiagnostics';
import { DeviceTelemetry } from '../types';
import { TelemetryCard } from '../components/diagnostic-cards/TelemetryCard';
import { NetworkTestCard } from '../components/diagnostic-cards/NetworkTestCard';

export default function DiagnosticDashboard() {
  const [manualRefresh, setManualRefresh] = useState(false);

  const { data: telemetry, isLoading: telemetryLoading } = useQuery(
    'device-telemetry',
    () => DeviceTelemetryService.collectTelemetry(),
    {
      staleTime: 1000 * 60 * 5, // 5 minutes
    }
  );

  const { data: networkResults, isLoading: networkLoading } = useQuery(
    'network-diagnostics',
    () => NetworkDiagnostics.runDiagnostics(),
    {
      staleTime: 1000 * 60 * 1, // 1 minute
      enabled: !!telemetry?.network.isConnected,
    }
  );

  const handleRefresh = async () => {
    setManualRefresh(true);
    await Promise.all([
      queryClient.invalidateQueries('device-telemetry'),
      queryClient.invalidateQueries('network-diagnostics'),
    ]);
    setManualRefresh(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.content}>
        <View style={styles.header}>
          <Text variant="headlineMedium">Device Diagnostics</Text>
          <Text variant="bodyMedium" style={styles.subtitle}>
            Real-time system status and health
          </Text>
        </View>

        <Button
          icon="refresh"
          mode="contained-tonal"
          onPress={handleRefresh}
          style={styles.refreshButton}
          loading={manualRefresh}
        >
          Refresh Diagnostics
        </Button>

        {telemetryLoading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" />
            <Text style={styles.loadingText}>Collecting device information...</Text>
          </View>
        ) : telemetry ? (
          <TelemetryCard telemetry={telemetry} />
        ) : null}

        {telemetry?.network.isConnected && (
          <NetworkTestCard
            network={telemetry.network}
            results={networkResults}
            isLoading={networkLoading}
          />
        )}

        <View style={styles.storageSection}>
          <Text variant="titleMedium" style={styles.sectionTitle}>
            Storage Health
          </Text>
          {telemetry && <StorageHealthCard telemetry={telemetry} />}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function StorageHealthCard({ telemetry }: { telemetry: DeviceTelemetry }) {
  const isCritical = telemetry.storage.usedPercentage > 90;
  const isWarning = telemetry.storage.usedPercentage > 75;

  return (
    <Card style={styles.storageCard}>
      <Card.Content>
        <View style={styles.storageHeader}>
          <Text variant="titleMedium">Storage</Text>
          <Chip
            icon={isCritical ? 'alert' : isWarning ? 'alert-outline' : 'check-circle'}
            mode="flat"
            textColor={isCritical ? '#FF3B30' : isWarning ? '#FF9500' : '#34C759'}
          >
            {isCritical ? 'Critical' : isWarning ? 'Warning' : 'Healthy'}
          </Chip>
        </View>

        <ProgressBar
          progress={telemetry.storage.usedPercentage / 100}
          color={isCritical ? '#FF3B30' : isWarning ? '#FF9500' : '#34C759'}
          style={styles.progressBar}
        />

        <View style={styles.storageStats}>
          <Text variant="bodyMedium">
            Used: {(telemetry.storage.totalSpace - telemetry.storage.freeSpace).toFixed(1)} GB
          </Text>
          <Text variant="bodyMedium">
            Free: {telemetry.storage.freeSpace.toFixed(1)} GB
          </Text>
        </View>

        {isCritical && (
          <List.Item
            title="Free Up Space"
            description="Remove unused apps and media files"
            left={(props) => <List.Icon {...props} icon="delete-forever" />}
            onPress={() => {}}
            style={styles.actionItem}
          />
        )}
      </Card.Content>
    </Card>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    padding: 16,
  },
  header: {
    marginBottom: 24,
  },
  subtitle: {
    color: '#666',
    marginTop: 4,
  },
  refreshButton: {
    marginBottom: 24,
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 48,
  },
  loadingText: {
    marginTop: 16,
    color: '#666',
  },
  storageSection: {
    marginTop: 16,
  },
  sectionTitle: {
    marginBottom: 16,
  },
  storageCard: {
    borderRadius: 12,
  },
  storageHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  progressBar: {
    height: 8,
    borderRadius: 4,
    marginBottom: 16,
  },
  storageStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionItem: {
    backgroundColor: '#FFF8E1',
    borderRadius: 8,
    marginTop: 12,
  },
});
