import { FormEvent, useState } from 'react';

interface Props {
  onLogin: (email: string, password: string) => boolean;
}

export default function LoginPage({ onLogin }: Props) {
  const [email, setEmail] = useState('demo@taskoptimizer.ai');
  const [password, setPassword] = useState('demo123');
  const [error, setError] = useState('');

  const submit = (event: FormEvent) => {
    event.preventDefault();
    const ok = onLogin(email, password);
    if (!ok) {
      setError('Invalid credentials. Use demo@taskoptimizer.ai / demo123');
      return;
    }
    setError('');
  };

  return (
    <main className="auth-shell">
      <div className="auth-float-layer" aria-hidden="true">
        <span className="float-emoji d1">✨</span>
        <span className="float-emoji d2">😊</span>
        <span className="float-emoji d3">&#128514;</span>
        <span className="float-emoji d4">&#128526;</span>
        <span className="float-emoji d5">&#x1F60E;</span>
      </div>
      <section className="login-card">
        <div className="hero-mask" aria-hidden="true">
          <span className="hero-emoji">&#128521;</span>
        </div>
        <div className="login-brand">
          <h1>Emotion AI </h1>
        </div>
        <p className="login-subtitle">Understand emotions in real time and improve productivity.</p>
        <form onSubmit={submit} className="form-grid">
          <label className="input-label">
            Email
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="name@company.com"
              required
            />
          </label>
          <label className="input-label">
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>
          {error && <p className="auth-error">{error}</p>}
          <button type="submit">Login</button>
        </form>
        <p className="login-hint">Demo login: demo@taskoptimizer.ai / demo123</p>
      </section>
    </main>
  );
}
