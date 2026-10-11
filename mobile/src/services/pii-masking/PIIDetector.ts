// PII Detection and Masking Service
import * as ImageManipulator from 'expo-image-manipulator';

export interface PIIDetectionResult {
  hasPII: boolean;
  detectedTypes: PIIType[];
  redactionBoxes: RedactionBox[];
}

export type PIIType = 'email' | 'phone' | 'ssn' | 'creditCard' | 'password' | 'name';

export interface RedactionBox {
  x: number;
  y: number;
  width: number;
  height: number;
  type: PIIType;
}

class PIIDetector {
  private readonly patterns = {
    email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
    phone: /\b(\+?1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b/g,
    ssn: /\b\d{3}-\d{2}-\d{4}\b/g,
    creditCard: /\b(?:\d{4}[-\s]?){3}\d{4}\b/g,
    password: /\b(password|passwd|pwd)[:=\s]+\S+/gi,
  };

  /**
   * Detect PII in text content
   */
  detectInText(text: string): PIIDetectionResult {
    const detectedTypes: PIIType[] = [];
    const redactionBoxes: RedactionBox[] = [];

    for (const [type, pattern] of Object.entries(this.patterns)) {
      const matches = text.match(pattern);
      if (matches && matches.length > 0) {
        detectedTypes.push(type as PIIType);
      }
    }

    return {
      hasPII: detectedTypes.length > 0,
      detectedTypes,
      redactionBoxes,
    };
  }

  /**
   * Redact PII from text
   */
  redactText(text: string): string {
    let redacted = text;

    for (const pattern of Object.values(this.patterns)) {
      redacted = redacted.replace(pattern, '[REDACTED]');
    }

    return redacted;
  }

  /**
   * Analyze screenshot for PII
   * In production, this would use ML Kit or TensorFlow Lite
   */
  async detectInScreenshot(imageUri: string): Promise<PIIDetectionResult> {
    return {
      hasPII: false,
      detectedTypes: [],
      redactionBoxes: [],
    };
  }

  /**
   * Apply blur/redaction mask to image
   */
  async applyRedactionMask(
    imageUri: string,
    redactionBoxes: RedactionBox[]
  ): Promise<string> {
    // This would use expo-image-manipulator to blur specific regions
    // For now, return the original URI
    return imageUri;
  }

  /**
   * Check if image needs redaction
   */
  async needsRedaction(imageUri: string): Promise<boolean> {
    const result = await this.detectInScreenshot(imageUri);
    return result.hasPII;
  }
}

export default new PIIDetector();
