import React, { useState, useEffect, useRef } from 'react';
import { View, StyleSheet, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { Card, Text, Avatar, Button, Chip, ProgressBar, ActivityIndicator } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useChatStore } from '../store/chatStore';
import { ChatMessage, DiagnosticCardAction } from '../types';
import { ChatMessageBubble } from '../components/chat/ChatMessage';
import { TelemetryCard } from '../components/diagnostic-cards/TelemetryCard';
import { DeepLinkActionCard } from '../components/diagnostic-cards/DeepLinkActionCard';
import { ScreenshotAnalysisCard } from '../components/diagnostic-cards/ScreenshotAnalysisCard';
import { ChatInput } from '../components/chat/ChatInput';

export default function ChatScreen() {
  const { messages, sendMessage, isTyping, loadSession, deviceTelemetry } = useChatStore();
  const [inputText, setInputText] = useState('');
  const [showTelemetry, setShowTelemetry] = useState(false);
  const flatListRef = useRef<FlatList>(null);
  const messagesEndRef = useRef<View>(null);

  useEffect(() => {
    loadSession();
  }, [loadSession]);

  useEffect(() => {
    if (messages.length > 0) {
      flatListRef.current?.scrollToEnd({ animated: true });
    }
  }, [messages, isTyping]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;
    await sendMessage(text);
    setInputText('');
  };

  const handleTelemetryCollection = async () => {
    // Triggers telemetry collection via store action
  };

  const renderMessage = ({ item }: { item: ChatMessage }) => {
    if (item.metadata?.action === 'request_telemetry') {
      return (
        <Card style={styles.card}>
          <Card.Content>
            <Text>Collecting device information...</Text>
            <Button onPress={handleTelemetryCollection} mode="text">
              Allow
            </Button>
          </Card.Content>
        </Card>
      );
    }

    if (item.role === 'user') {
      return <ChatMessageBubble message={item} isUser={true} />;
    }

    return <ChatMessageBubble message={item} isUser={false} />;
  };

  const renderDiagnosticCards = () => {
    const lastAssistantMessage = messages
      .slice()
      .reverse()
      .find((m) => m.role === 'assistant' && m.metadata?.actions);

    if (!lastAssistantMessage?.metadata?.actions?.length) return null;

    return lastAssistantMessage.metadata.actions.map((action, index) => {
      if (action.type === 'telemetry') {
        return (
          <TelemetryCard key={index} telemetry={deviceTelemetry!} showCollectionButton />
        );
      }
      if (action.type === 'deep_link') {
        return (
          <DeepLinkActionCard key={index} action={action} />
        );
      }
      if (action.type === 'screenshot_analysis') {
        return (
          <ScreenshotAnalysisCard key={index} action={action} />
        );
      }
      return null;
    });
  };

  return (
    <SafeAreaView style={styles.container} edges={['bottom']}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.content}
      >
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={renderMessage}
          onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
          ListHeaderComponent={
            <>
              {renderDiagnosticCards()}
              {deviceTelemetry && <TelemetryCard telemetry={deviceTelemetry} />}
            </>
          }
          style={styles.messageList}
        />

        {isTyping && (
          <View style={styles.typingIndicator}>
            <ActivityIndicator size="small" color="#007AFF" />
            <Text style={styles.typingText}>Thinking...</Text>
          </View>
        )}

        <ChatInput
          value={inputText}
          onChangeText={setInputText}
          onSend={handleSendMessage}
          disabled={isTyping}
        />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
  },
  messageList: {
    flex: 1,
  },
  card: {
    margin: 12,
    borderRadius: 12,
  },
  typingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  typingText: {
    marginLeft: 8,
    color: '#666',
  },
});
