import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Emotion, MoodHistoryItem } from '../types';

interface Props {
  data: MoodHistoryItem[];
  emotionList: Emotion[];
}

const emotionScoreMap: Record<Emotion, number> = {
  happy: 1,
  neutral: 0.35,
  stressed: -0.35,
  sad: -0.7,
  angry: -1,
};

export default function MoodHistoryChart({ data, emotionList }: Props) {
  const persisted = [...data]
    .reverse()
    .map((item, index) => ({
      point: `#${index + 1}`,
      mood: emotionScoreMap[item.emotion],
      emotion: item.emotion,
    }));

  const fallback = emotionList.map((emotion, index) => ({
    point: `#${index + 1}`,
    mood: emotionScoreMap[emotion],
    emotion,
  }));

  const chartData = persisted.length > 0 ? persisted : fallback;

  return (
    <section className="card dashboard-card">
      <h2 className="card-title">Mood History</h2>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 12, left: 0, bottom: 18 }}>
            <CartesianGrid stroke="#e7edf8" strokeDasharray="4 4" />
            <XAxis dataKey="point" interval="preserveStartEnd" minTickGap={20} tickMargin={10} />
            <YAxis domain={[-1, 1]} tickMargin={8} tickCount={5} />
            <Tooltip formatter={(value) => [value, 'Mood Score']} />
            <Line
              type="monotone"
              dataKey="mood"
              stroke="#4b93db"
              strokeWidth={3}
              dot={{ r: 3, strokeWidth: 2, fill: '#ffffff' }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      {chartData.length > 0 && (
        <p className="legend-line">
          Latest emotion: <strong>{chartData[chartData.length - 1].emotion}</strong>
        </p>
      )}
    </section>
  );
}
