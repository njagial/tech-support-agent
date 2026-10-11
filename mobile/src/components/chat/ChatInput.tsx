import React, { useState } from 'react';
import { View, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

interface ChatInputProps {
  value: string;
  onChangeText: (text: string) => void;
  onSend: (text: string) => void | Promise<void>;
  disabled?: boolean;
  placeholder?: string;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  value,
  onChangeText,
  onSend,
  disabled = false,
  placeholder = 'Describe your issue...',
}) => {
  const [isFocused, setIsFocused] = useState(false);

  const handleSend = async () => {
    if (value.trim() && !disabled) {
      await onSend(value.trim());
    }
  };

  const handleKeyPress = (e: any) => {
    if (e.nativeEvent.key === 'Enter' && !e.nativeEvent.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <View
      style={[
        styles.container,
        isFocused && styles.containerFocused,
        disabled && styles.containerDisabled,
      ]}
    >
      <TextInput
        style={styles.input}
        value={value}
        onChangeText={onChangeText}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        onKeyPress={handleKeyPress}
        placeholder={placeholder}
        placeholderTextColor="#999"
        multiline
        numberOfLines={1}
        maxLines={4}
        returnKeyType="send"
        editable={!disabled}
      />
      <TouchableOpacity
        style={[
          styles.sendButton,
          (!value.trim() || disabled) && styles.sendButtonDisabled,
        ]}
        onPress={handleSend}
        disabled={!value.trim() || disabled}
        activeOpacity={0.8}
      >
        <Icon
          name="send"
          size={20}
          color={!value.trim() || disabled ? '#ccc' : '#fff'}
        />
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  containerFocused: {
    backgroundColor: '#f9f9f9',
    borderTopColor: '#e0e0e0',
  },
  containerDisabled: {
    opacity: 0.7,
  },
  input: {
    flex: 1,
    maxHeight: 100,
    fontSize: 16,
    lineHeight: 21,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#f0f0f0',
    paddingHorizontal: 12,
    marginRight: 8,
  },
  sendButton: {
    width: 40,
    height: 40,
    backgroundColor: '#007AFF',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#e0e0e0',
  },
});
