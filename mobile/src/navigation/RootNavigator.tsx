import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// Screens
import ChatScreen from '../screens/ChatScreen';
import DiagnosticDashboard from '../screens/DiagnosticDashboard';
import SettingsScreen from '../screens/SettingsScreen';

type RootTabParamList = {
  Chat: undefined;
  Diagnostics: undefined;
  Settings: undefined;
};

const Tab = createBottomTabNavigator<RootTabParamList>();

export default function RootNavigator() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName: string;

            switch (route.name) {
              case 'Chat':
                iconName = 'chat';
                break;
              case 'Diagnostics':
                iconName = 'health-icons';
                break;
              case 'Settings':
                iconName = 'cog';
                break;
              default:
                iconName = 'help-circle';
            }

            return <Icon name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#007AFF',
          tabBarInactiveTintColor: 'gray',
          headerShown: false,
        })}
      >
        <Tab.Screen
          name="Chat"
          component={ChatScreen}
          options={{ title: 'Tech Support' }}
        />
        <Tab.Screen
          name="Diagnostics"
          component={DiagnosticDashboard}
          options={{ title: 'Diagnostics' }}
        />
        <Tab.Screen
          name="Settings"
          component={SettingsScreen}
          options={{ title: 'Settings' }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
