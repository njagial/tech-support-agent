// Screenshot Analysis Card Component
import React from 'react';
import { View, Text, StyleSheet, Image } from 'react-native';
import { Card, Button, ActivityIndicator } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import PIIDetector from '../../services/pii-masking/PIIDetector';

interface ScreenshotAnalysisCardProps {
  action: {
    type: string;
    label: string;
    description: string;
    screenshotData?: {
      uri: string;
      isRedacted: boolean;
    };
    analysis?: {
      detectedErrors: string[];
      hypothesis: string;
    };
  };
}

export const ScreenshotAnalysisCard: React.FC<ScreenshotAnalysisCardProps> = ({ action }) => {
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [piiDetected, setPiiDetected] = React.useState(false);

  const handleAnalyze = async () => {
    if (!action.screenshotData?.uri) return;

    setIsAnalyzing(true);
    try {
      const result = await PIIDetector.detectInScreenshot(action.screenshotData.uri);
      setPiiDetected(result.hasPII);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSendUnredacted = () => {
    // Send to backend for analysis (with user warning)
  };

  return (
    <Card style={styles.card} elevation={2}>
      <Card.Content>
        <Text style={styles.cardTitle}>Screenshot Analysis</Text>

        {/* Screenshot Preview */}
        <View style={styles.imageContainer}>
          {action.screenshotData?.uri ? (
            <Image
              source={{ uri: action.screenshotData.uri }}
              style={styles.screenshot}
            />
          ) : (
            <View style={styles.placeholder}>
              <Icon name="camera-outline" size={48} color="#ccc" />
              <Text style={styles.placeholderText}>No screenshot</Text>
            </View>
          )}

          {/* PII Warning Overlay */}
          {piiDetected && (
            <View style={styles.piiWarning}>
              <Icon name="shield-alert" size={24} color="#FF9500" />
              <Text style={styles.piiWarningText}>
                PII detected and redacted
              </Text>
            </View>
          )}
        </View>

        {/* Analysis Results */}
        {action.analysis && (
          <View style={styles.analysisSection}>
            <View style={styles.analysisHeader}>
              <Icon name="lightbulb" size={20} color="#FF9500" />
              <Text style={styles.analysisLabel}>AI Analysis</Text>
            </View>
            <Text style={styles.hypothesis}>{action.analysis.hypothesis}</Text>
            {action.analysis.detectedErrors.length > 0 && (
              <View style={styles.errorsContainer}>
                {action.analysis.detectedErrors.map((error, idx) => (
                  <Text key={idx} style={styles.errorText}>
                    • {error}
                  </Text>
                ))}
              </View>
            )}
          </View>
        )}

        {/* Action Buttons */}
        <View style={styles.actionButtons}>
          <Button
            mode="contained-tonal"
            onPress={handleAnalyze}
            disabled={isAnalyzing || !action.screenshotData?.uri}
            style={styles.analyzeButton}
          >
            {isAnalyzing ? (
              <>
                <ActivityIndicator size="small" />
                <Text>Analyzing...</Text>
              </>
            ) : (
              'Re-analyze'
            )}
          </Button>

          {piiDetected && (
            <Button
              mode="outlined"
              onPress={handleSendUnredacted}
              style={styles.sendButton}
            >
              Send Unredacted (with warning)
            </Button>
          )}
        </View>
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
    marginBottom: 12,
    color: '#1F1F1F',
  },
  imageContainer: {
    position: 'relative',
    borderRadius: 8,
    overflow: 'hidden',
    marginBottom: 12,
  },
  screenshot: {
    width: '100%',
    height: 200,
    resizeMode: 'contain',
    backgroundColor: '#f0f0f0',
  },
  placeholder: {
    width: '100%',
    height: 200,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#f0f0f0',
  },
  placeholderText: {
    color: '#999',
    marginTop: 8,
  },
  piiWarning: {
    position: 'absolute',
    top: 8,
    right: 8,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    padding: 8,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
  },
  piiWarningText: {
    marginLeft: 4,
    color: '#FF9500',
    fontWeight: '600',
  },
  analysisSection: {
    marginTop: 12,
    padding: 12,
    backgroundColor: '#FFF8E1',
    borderRadius: 8,
  },
  analysisHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  analysisLabel: {
    marginLeft: 8,
    fontWeight: '600',
    color: '#333',
  },
  hypothesis: {
    fontSize: 14,
    color: '#1F1F1F',
    marginBottom: 8,
  },
  errorsContainer: {
    flexWrap: 'wrap',
  },
  errorText: {
    fontSize: 13,
    color: '#FF3B30',
  },
  actionButtons: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 12,
  },
  analyzeButton: {
    flex: 1,
  },
  sendButton: {
    flex: 1,
  },
});
