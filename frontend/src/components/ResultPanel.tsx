import { EmotionDetectionResponse } from '../types';

interface Props {
  result: EmotionDetectionResponse | null;
}

export default function ResultPanel({ result }: Props) {
  if (!result) {
    return (
      <section className="card dashboard-card">
        <h2 className="card-title">Detection Result</h2>
        <p className="result-text">Run live detection to view emotion confidence and task suggestions.</p>
      </section>
    );
  }

  const topTask = result.recommendations[0];

  return (
    <section className="card dashboard-card">
      <h2 className="card-title">Detection Result</h2>
      <div className="result-block">
        <p className="result-label">Emotion Detected</p>
        <p className="result-emotion">{result.detection.emotion} <span>(Confidence: {Math.round(result.detection.confidence * 100)}%)</span></p>
        <p className="result-text">Source: {result.detection.source} | Sentiment: {result.detection.sentiment_score}</p>
      </div>
      <div className="result-block">
        <p className="result-label">Recommended Task</p>
        <p className="result-task">{topTask?.task_title}</p>
        <p className="result-text">{topTask?.task_type} • Priority: {topTask?.priority}</p>
      </div>
      <p className="result-text">
        Stress streak: <strong>{result.current_stress_streak ?? 0}</strong>
        {result.stress_streak_threshold ? ` / ${result.stress_streak_threshold}` : ''}
      </p>
      {result.alert_triggered && <p className="alert-inline">Stress alert triggered due to consecutive stressed entries.</p>}
    </section>
  );
}
