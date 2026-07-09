import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAppContext } from '../context/AppContext.jsx'

export default function Login() {
  const { setUser } = useAppContext()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    // No real backend yet — this just marks the session as logged in
    // so the navbar and flows relying on `user` behave correctly.
    setUser({ name: email.split('@')[0] || 'Shopper', email })
    navigate('/')
  }

  return (
    <div className="auth-wrap soft-section">
      <div className="auth-card">
        <h2>Welcome back</h2>
        <p className="auth-sub">Log in to see your favorites and orders.</p>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="login-email">Email</label>
            <input
              id="login-email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
          </div>

          <div className="field">
            <label htmlFor="login-password">Password</label>
            <input
              id="login-password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />
          </div>

          <button type="submit" className="btn btn-primary btn-block">
            Log in
          </button>
        </form>

        <p className="auth-switch">
          New here? <Link to="/register">Create an account</Link>
        </p>
      </div>
    </div>
  )
}
