import { FormEvent, useState } from 'react';

interface Props {
  onDetect: (employeeId: string, teamId: string, textInput: string) => Promise<void>;
  loading: boolean;
}

export default function DetectionPanel({ onDetect, loading }: Props) {
  const [employeeId, setEmployeeId] = useState('emp-001');
  const [teamId, setTeamId] = useState('team-alpha');
  const [textInput, setTextInput] = useState('I feel focused but slightly tired after meetings.');

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    await onDetect(employeeId, teamId, textInput);
  };

  return (
    <section className="card dashboard-card">
      <h2 className="card-title blue-title">Live Detection</h2>
      <form onSubmit={submit} className="form-grid">
        <input value={employeeId} onChange={(e) => setEmployeeId(e.target.value)} placeholder="Employee ID" required />
        <input value={teamId} onChange={(e) => setTeamId(e.target.value)} placeholder="Team ID" required />
        <textarea
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          placeholder="Describe current mood and workload context"
          rows={4}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Scanning...' : 'Start Emotion Detection'}
        </button>
      </form>
    </section>
  );
}
