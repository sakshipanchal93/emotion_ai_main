import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';
import { TeamAnalyticsResponse } from '../types';

interface Props {
  analytics: TeamAnalyticsResponse | null;
}

export default function TeamAnalyticsChart({ analytics }: Props) {
  if (!analytics) {
    return (
      <section className="card dashboard-card">
        <h2 className="card-title blue-title">Team Mood Analytics</h2>
        <p>No team analytics available yet.</p>
      </section>
    );
  }

  const happy = analytics.emotion_distribution.happy ?? 0;
  const neutral = analytics.emotion_distribution.neutral ?? 0;
  const stressedRaw = analytics.emotion_distribution.stressed ?? 0;
  const stressed = stressedRaw + (analytics.emotion_distribution.sad ?? 0) + (analytics.emotion_distribution.angry ?? 0);
  const total = Math.max(analytics.total_records, 1);

  const happyPct = Math.round((happy / total) * 100);
  const neutralPct = Math.round((neutral / total) * 100);
  const stressedPct = Math.round((stressed / total) * 100);

  const chartData = [
    { name: 'Happy', value: happyPct, color: '#76d2b4' },
    { name: 'Neutral', value: neutralPct, color: '#60a5fa' },
    { name: 'Stressed', value: stressedPct, color: '#f87171' },
  ];

  return (
    <section className="card dashboard-card">
      <h2 className="card-title blue-title">Team Mood Analytics</h2>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Tooltip formatter={(value) => [`${value}%`, 'Share']} />
            <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={46} outerRadius={76} paddingAngle={3}>
              {chartData.map((entry) => (
                <Cell key={entry.name} fill={entry.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="analytics-row">
        <span>Happy: <strong>{happyPct}%</strong></span>
        <span>Neutral: <strong>{neutralPct}%</strong></span>
        <span>Stressed: <strong>{stressedPct}%</strong></span>
      </div>
    </section>
  );
}
