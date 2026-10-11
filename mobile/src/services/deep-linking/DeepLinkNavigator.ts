// Deep Link Navigation Service
import { Linking, Platform, Alert } from 'react-native';

export const DEEP_LINK_ACTIONS = {
  ios: {
    wifi: 'App-Prefs:WIFI',
    bluetooth: 'App-Prefs:Bluetooth',
    cellular: 'App-Prefs:MOBILE_DATA',
    battery: 'App-Prefs:BATTERY_USAGE',
    storage: 'App-Prefs:General&path=STORAGE_MGMT',
    appPermissions: 'app-settings:',
    notifications: 'App-Prefs:NOTIFICATIONS_ID',
    location: 'App-Prefs:Privacy&path=LOCATION',
  },
  android: {
    wifi: 'android.settings.WIFI_SETTINGS',
    bluetooth: 'android.settings.BLUETOOTH_SETTINGS',
    cellular: 'android.settings.DATA_ROAMING_SETTINGS',
    battery: 'android.settings.BATTERY_SAVER_SETTINGS',
    storage: 'android.settings.INTERNAL_STORAGE_SETTINGS',
    appPermissions: 'android.settings.APPLICATION_DETAILS_SETTINGS',
    notifications: 'android.settings.APP_NOTIFICATION_SETTINGS',
    location: 'android.settings.LOCATION_SOURCE_SETTINGS',
    apps: 'android.settings.APPLICATION_SETTINGS',
  },
};

interface DeepLinkAction {
  action: keyof typeof DEEP_LINK_ACTIONS.ios | keyof typeof DEEP_LINK_ACTIONS.android;
  label: string;
  description: string;
}

class DeepLinkNavigator {
  /**
   * Open native settings page for a specific action
   */
  async openSettings(action: DeepLinkAction['action']): Promise<boolean> {
    try {
      if (Platform.OS === 'ios') {
        const url = DEEP_LINK_ACTIONS.ios[action as keyof typeof DEEP_LINK_ACTIONS.ios];
        if (!url) {
          console.warn(`iOS deep link not found for action: ${action}`);
          return false;
        }
        await Linking.openURL(url);
        return true;
      } else {
        const intentAction = DEEP_LINK_ACTIONS.android[
          action as keyof typeof DEEP_LINK_ACTIONS.android
        ];
        if (!intentAction) {
          console.warn(`Android intent not found for action: ${action}`);
          return false;
        }

        const url = `intent://#Intent;action=${intentAction};end`;
        await Linking.openURL(url);
        return true;
      }
    } catch (error) {
      console.error('Error opening settings:', error);
      return false;
    }
  }

  /**
   * Generate a deep link action card for the chat UI
   */
  generateActionCard(
    issue: string,
    action: DeepLinkAction['action']
  ): DeepLinkAction {
    const actionMap: Record<string, DeepLinkAction> = {
      wifi: {
        action: 'wifi',
        label: 'Open Wi-Fi Settings',
        description: 'Configure your Wi-Fi connection',
      },
      battery: {
        action: 'battery',
        label: 'Check Battery Settings',
        description: 'View battery usage and optimization options',
      },
      storage: {
        action: 'storage',
        label: 'Manage Storage',
        description: 'Free up space by deleting unused files',
      },
      appPermissions: {
        action: 'appPermissions',
        label: 'Review App Permissions',
        description: 'Grant necessary permissions for this app',
      },
    };

    return (
      actionMap[action] || {
        action,
        label: 'Open Settings',
        description: 'Navigate to relevant settings page',
      }
    );
  }

  /**
   * Validate if a deep link can be opened
   */
  async canOpenDeepLink(action: DeepLinkAction['action']): Promise<boolean> {
    try {
      const url =
        Platform.OS === 'ios'
          ? DEEP_LINK_ACTIONS.ios[action as keyof typeof DEEP_LINK_ACTIONS.ios]
          : `intent://#Intent;action=${
              DEEP_LINK_ACTIONS.android[action as keyof typeof DEEP_LINK_ACTIONS.android]
            };end`;

      if (!url) return false;
      return await Linking.canOpenURL(url);
    } catch {
      return false;
    }
  }

  /**
   * Open settings with user confirmation
   */
  async openWithConfirmation(
    action: DeepLinkAction['action'],
    message: string
  ): Promise<void> {
    Alert.alert(
      'Open Settings',
      message,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Open',
          onPress: async () => {
            const success = await this.openSettings(action);
            if (!success) {
              Alert.alert('Error', 'Could not open settings. Please navigate manually.');
            }
          },
        },
      ],
      { cancelable: true }
    );
  }
}

export default new DeepLinkNavigator();
