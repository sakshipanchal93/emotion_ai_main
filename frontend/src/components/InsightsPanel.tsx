import { EmotionDetectionResponse, StressAlert, TeamAnalyticsResponse } from '../types';

interface Props {
  result: EmotionDetectionResponse | null;
  analytics: TeamAnalyticsResponse | null;
  alerts: StressAlert[];
}

export default function InsightsPanel({ result, analytics, alerts }: Props) {
  const emotion = result?.detection.emotion ?? 'neutral';
  const stressIndex = analytics?.stress_index ?? 0;

  const productivityTip =
    emotion === 'happy'
      ? 'Great time for creative planning and collaboration.'
      : emotion === 'stressed'
      ? 'Prioritize low-complexity tasks and take a short break.'
      : emotion === 'sad'
      ? 'Use structured checklist tasks and pair with a teammate.'
      : emotion === 'angry'
      ? 'Pause high-conflict work and shift to independent tasks.'
      : 'Maintain regular execution tasks with short focus blocks.';

  const teamStatus =
    stressIndex >= 55
      ? 'High stress trend detected for the team.'
      : stressIndex >= 30
      ? 'Moderate stress trend. Monitor workload balance.'
      : 'Healthy team mood trend.';

  return (
    <section className="card dashboard-card">
      <h2 className="card-title">AI Insights</h2>

      <div className="result-block">
        <p className="result-label">Current Focus Suggestion</p>
        <p className="result-text">{productivityTip}</p>
      </div>

      <div className="result-block">
        <p className="result-label">Team Well-Being Status</p>
        <p className="result-text">{teamStatus}</p>
      </div>

      <div className="result-block">
        <p className="result-label">Alert Snapshot</p>
        <p className="result-text">Open alerts in timeline: <strong>{alerts.length}</strong></p>
      </div>
    </section>
  );
}
