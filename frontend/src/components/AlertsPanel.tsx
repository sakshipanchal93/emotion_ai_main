import { StressAlert } from '../types';

interface Props {
  alerts: StressAlert[];
}

export default function AlertsPanel({ alerts }: Props) {
  const latest = alerts[0];

  return (
    <section className="card dashboard-card alerts-card">
      <h2 className="card-title">Stress Management Alerts</h2>
      {alerts.length === 0 ? (
        <p className="ok-state">No stress alerts detected.</p>
      ) : (
        <ul className="alert-list">
          {alerts.map((alert) => (
            <li key={`${alert.employee_id}-${alert.created_at}`}>
              {new Date(alert.created_at).toLocaleString()} — {alert.employee_id} ({alert.team_id}): {alert.message}
            </li>
          ))}
        </ul>
      )}
      {latest && (
        <p className="result-text">
          Latest streak: <strong>{latest.streak_count}</strong>
        </p>
      )}
    </section>
  );
}
