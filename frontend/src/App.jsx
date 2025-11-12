import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [calls, setCalls] = useState([])
  const [loading, setLoading] = useState(true)
  const [copiedId, setCopiedId] = useState(null)

  // Fetch pending calls (no disposition)
  const fetchPendingCalls = async () => {
    try {
      const response = await fetch('/api/calls/pending/')
      const data = await response.json()
      setCalls(data.data || data.results || [])
      setLoading(false)
    } catch (error) {
      console.error('Error fetching calls:', error)
      setLoading(false)
    }
  }

  // Auto-refresh every 10 seconds
  useEffect(() => {
    fetchPendingCalls()
    const interval = setInterval(fetchPendingCalls, 10000)
    return () => clearInterval(interval)
  }, [])

  // Copy phone number to clipboard (only last 10 digits, without country code)
  const copyNumber = (number, id) => {
    // Remove country code (91) and get only 10 digits
    let cleanNumber = number.trim().replace(/\D/g, '') // Remove non-digits

    // If number starts with 91 and has more than 10 digits, remove 91
    if (cleanNumber.startsWith('91') && cleanNumber.length > 10) {
      cleanNumber = cleanNumber.substring(2) // Remove first 2 digits (91)
    }

    // Take only last 10 digits
    cleanNumber = cleanNumber.slice(-10)

    navigator.clipboard.writeText(cleanNumber)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  // Format time with exact call time
  const formatTime = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)

    // Get exact time
    const exactTime = date.toLocaleString('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })

    const exactDate = date.toLocaleString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    })

    if (diffMins < 1) return `Just now (${exactTime})`
    if (diffMins < 60) return `${diffMins} min ago (${exactTime})`
    if (diffHours < 24) return `${diffHours} hours ago (${exactTime})`

    return `${exactDate} at ${exactTime}`
  }

  // Count calls from same number
  const getCallCount = (number) => {
    return calls.filter(call => call.caller_number.trim() === number.trim()).length
  }

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading pending calls...</div>
      </div>
    )
  }

  return (
    <div className="container">
      <header className="header">
        <h1>📞 Missed Calls Dashboard</h1>
        <div className="stats">
          <span className="badge">{calls.length} Pending Calls</span>
          <button onClick={fetchPendingCalls} className="refresh-btn">
            🔄 Refresh
          </button>
        </div>
      </header>

      {calls.length === 0 ? (
        <div className="empty-state">
          <p>✅ No pending calls! All caught up.</p>
        </div>
      ) : (
        <div className="calls-list">
          {calls.map((call) => {
            const callCount = getCallCount(call.caller_number)
            return (
              <div key={call.id} className="call-card">
                <div className="call-info">
                  <div className="phone-section">
                    <h2 className="phone-number">{call.caller_number.trim()}</h2>
                    <button
                      onClick={() => copyNumber(call.caller_number, call.id)}
                      className={copiedId === call.id ? 'copy-btn copied' : 'copy-btn'}
                    >
                      {copiedId === call.id ? '✓ Copied!' : '📋 Copy'}
                    </button>
                  </div>

                  <div className="meta-info">
                    <span className="time">⏰ {formatTime(call.call_start_time)}</span>
                    {callCount > 1 && (
                      <span className="call-count">
                        🔔 {callCount} calls from this number
                      </span>
                    )}
                    {call.caller_name && (
                      <span className="caller-name">👤 {call.caller_name}</span>
                    )}
                  </div>

                  <div className="call-details">
                    <span>Duration: {call.call_duration_formatted || '0s'}</span>
                    <span>Status: {call.call_status}</span>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      <footer className="footer">
        <p>💡 Copy number → Call from Tata Dealer → Set disposition → Number will auto-remove</p>
      </footer>
    </div>
  )
}

export default App
