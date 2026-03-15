export type Emotion = 'happy' | 'neutral' | 'stressed' | 'sad' | 'angry';

export interface DetectionResult {
  emotion: Emotion;
  sentiment_score: number;
  confidence: number;
  source: string;
}

export interface TaskSuggestion {
  task_title: string;
  task_type: string;
  priority: string;
}

export interface EmotionDetectionResponse {
  detection: DetectionResult;
  recommendations: TaskSuggestion[];
  alert_triggered: boolean;
  current_stress_streak?: number;
  stress_streak_threshold?: number;
}

export interface MoodHistoryItem {
  emotion: Emotion;
  sentiment_score: number;
  source: string;
  created_at: string;
}

export interface TeamAnalyticsResponse {
  team_id: string;
  total_records: number;
  emotion_distribution: Record<string, number>;
  average_sentiment: number;
  stress_index: number;
}

export interface StressAlert {
  employee_id: string;
  team_id: string;
  streak_count: number;
  message: string;
  created_at: string;
}
