import axios from 'axios';
import {
  EmotionDetectionResponse,
  MoodHistoryItem,
  StressAlert,
  TeamAnalyticsResponse,
} from '../types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
});

export const detectEmotion = async (payload: {
  employee_id: string;
  team_id: string;
  text_input: string;
}): Promise<EmotionDetectionResponse> => {
  const { data } = await api.post<EmotionDetectionResponse>('/emotion/detect', payload);
  return data;
};

export const getMoodHistory = async (employeeId: string): Promise<MoodHistoryItem[]> => {
  const { data } = await api.get<MoodHistoryItem[]>(`/employees/${employeeId}/mood-history`);
  return data;
};

export const getTeamAnalytics = async (teamId: string): Promise<TeamAnalyticsResponse> => {
  const { data } = await api.get<TeamAnalyticsResponse>(`/teams/${teamId}/analytics`);
  return data;
};

export const getStressAlerts = async (): Promise<StressAlert[]> => {
  const { data } = await api.get<StressAlert[]>('/alerts');
  return data;
};
