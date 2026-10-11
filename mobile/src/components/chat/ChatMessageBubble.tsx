import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Card, Button } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { ChatMessage } from '../types';

interface ChatMessageBubbleProps {
  message: ChatMessage;
  isUser: boolean;
}

export const ChatMessageBubble: React.FC<ChatMessageBubbleProps> = ({ message, isUser }) => {
  return (
    <View
      style={[
        styles.container,
        isUser ? styles.userContainer : styles.assistantContainer,
      ]}
    >
      <View
        style={[
          styles.bubble,
          isUser ? styles.userBubble : styles.assistantBubble,
        ]}
      >
        {isUser && (
          <View style={styles.userHeader}>
            <Text style={styles.userLabel}>You</Text>
          </View>
        )}
        <Text style={isUser ? styles.userText : styles.assistantText}>
          {message.content}
        </Text>
        {message.metadata?.actions && message.metadata.actions.length > 0 && (
          <View style={styles.actionsContainer}>
            {message.metadata.actions.map((action, index) => (
              <ActionChip key={index} action={action} />
            ))}
          </View>
        )}
        <Text style={styles.timestamp}>
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </Text>
      </View>
    </View>
  );
};

function ActionChip({ action }: { action: any }) {
  return (
    <View style={styles.chipContainer}>
      <Icon name={action.icon || 'lightbulb'} size={16} color="#007AFF" />
      <Text style={styles.chipText}>{action.label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    padding: 4,
  },
  userContainer: {
    justifyContent: 'flex-end',
    alignItems: 'flex-end',
  },
  assistantContainer: {
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
  },
  bubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
  },
  userBubble: {
    backgroundColor: '#007AFF',
    borderBottomRightRadius: 4,
  },
  assistantBubble: {
    backgroundColor: '#fff',
    borderBottomLeftRadius: 4,
    elevation: 1,
  },
  userHeader: {
    marginBottom: 4,
    marginLeft: 4,
  },
  userLabel: {
    color: 'rgba(255,255,255,0.7)',
    fontSize: 12,
  },
  userText: {
    color: '#fff',
    fontSize: 15,
    lineHeight: 20,
  },
  assistantText: {
    color: '#1F1F1F',
    fontSize: 15,
    lineHeight: 20,
  },
  actionsContainer: {
    marginTop: 8,
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  chipContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0,122,255,0.1)',
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 12,
  },
  chipText: {
    color: '#007AFF',
    fontSize: 13,
    fontWeight: '600',
    marginLeft: 4,
  },
  timestamp: {
    marginTop: 6,
    fontSize: 11,
    color: '#999',
    textAlign: 'right',
  },
});
