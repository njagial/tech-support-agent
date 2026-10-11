// Deep Link Action Card Component
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Card, Button } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import DeepLinkNavigator from '../../services/deep-linking/DeepLinkNavigator';

interface DeepLinkActionCardProps {
  action: {
    type: string;
    label: string;
    description: string;
    deepLink?: string;
  };
}

export const DeepLinkActionCard: React.FC<DeepLinkActionCardProps> = ({ action }) => {
  const handlePress = async () => {
    if (action.deepLink) {
      await DeepLinkNavigator.openSettings(action.deepLink as any);
    }
  };

  return (
    <Card style={styles.card} elevation={2}>
      <Card.Content>
        <View style={styles.header}>
          <Icon name="cog-outline" size={24} color="#007AFF" />
          <Text style={styles.title}>{action.label}</Text>
        </View>
        <Text style={styles.description}>{action.description}</Text>
      </Card.Content>
      <Card.Actions>
        <Button mode="contained" onPress={handlePress} style={styles.button}>
          Open Settings
        </Button>
      </Card.Actions>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginVertical: 8,
    marginHorizontal: 12,
    borderRadius: 12,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
    color: '#1F1F1F',
  },
  description: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  button: {
    marginLeft: 'auto',
  },
});
