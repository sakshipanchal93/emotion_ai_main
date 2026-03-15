import { useState } from 'react';
import AlertsPanel from './components/AlertsPanel';
import DetectionPanel from './components/DetectionPanel';
import InsightsPanel from './components/InsightsPanel';
import LoginPage from './components/LoginPage';
import MoodHistoryChart from './components/MoodHistoryChart';
import ResultPanel from './components/ResultPanel';
import TeamAnalyticsChart from './components/TeamAnalyticsChart';
import { detectEmotion, getMoodHistory, getStressAlerts, getTeamAnalytics } from './services/api';
import { EmotionDetectionResponse, MoodHistoryItem, StressAlert, TeamAnalyticsResponse, Emotion } from './types';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem('task_optimizer_user') !== null);
  const [userEmail, setUserEmail] = useState(localStorage.getItem('task_optimizer_user') || '');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EmotionDetectionResponse | null>(null);
  const [history, setHistory] = useState<MoodHistoryItem[]>([]);
  const [analytics, setAnalytics] = useState<TeamAnalyticsResponse | null>(null);
  const [alerts, setAlerts] = useState<StressAlert[]>([]);
  const [emotionList, setEmotionList] = useState<Emotion[]>([]);

  const handleLogin = (email: string, password: string) => {
    if (email.toLowerCase() === 'demo@taskoptimizer.ai' && password === 'demo123') {
      localStorage.setItem('task_optimizer_user', email.toLowerCase());
      setUserEmail(email.toLowerCase());
      setIsAuthenticated(true);
      return true;
    }
    return false;
  };

  const handleLogout = () => {
    localStorage.removeItem('task_optimizer_user');
    setIsAuthenticated(false);
    setUserEmail('');
  };

  const runDetection = async (employeeId: string, teamId: string, textInput: string) => {
    setLoading(true);
    try {
      const detection = await detectEmotion({ employee_id: employeeId, team_id: teamId, text_input: textInput });
      setResult(detection);
      setEmotionList((prev) => [...prev, detection.detection.emotion]);
      const [historyData, analyticsData, alertsData] = await Promise.all([
        getMoodHistory(employeeId),
        getTeamAnalytics(teamId),
        getStressAlerts(),
      ]);
      setHistory(historyData);
      setAnalytics(analyticsData);
      setAlerts(alertsData);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />;
  }

  const recentScans = [...emotionList].slice(-4).reverse();

  return (
    <main className="app">
      <header className="topbar">
        <div className="topbar-left">
          <h1>Emotion AI</h1>
          <p className="topbar-subtitle">Intelligent mood-aware workflow assistant</p>
        </div>
        <div className="topbar-right">
          <span className="status-pill">{userEmail}</span>
          <button type="button" className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <section className="banner welcome-banner">
        <h2>Hello, Alex.</h2>
        <p>Monitor team mood in real time and balance workload with AI recommendations.</p>
      </section>

      <section className="recent-strip card-like">
        <p className="strip-title">Recent Scans</p>
        <div className="scan-list">
          {recentScans.length === 0 ? (
            <span className="scan-placeholder">No scans yet</span>
          ) : (
            recentScans.map((emotion, index) => (
              <span key={`${emotion}-${index}`} className={`scan-chip emotion-${emotion}`}>
                {emotion}
              </span>
            ))
          )}
        </div>
      </section>

      <div className="grid">
        <DetectionPanel onDetect={runDetection} loading={loading} />
        <ResultPanel result={result} />
        <MoodHistoryChart data={history} emotionList={emotionList} />
        <TeamAnalyticsChart analytics={analytics} />
        <AlertsPanel alerts={alerts} />
        <InsightsPanel result={result} analytics={analytics} alerts={alerts} />
      </div>
    </main>
  );
}
