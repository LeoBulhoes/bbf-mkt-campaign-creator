'use client'

import { useState, useEffect } from 'react'
import { format } from 'date-fns'
import { AlertCircle, CheckCircle, Info, RefreshCw } from 'lucide-react'

type LogEntry = {
    id: string
    timestamp: string
    level: 'info' | 'success' | 'error' | 'warning'
    agent: string
    message: string
}

export default function LogsPage() {
    const [logs, setLogs] = useState<LogEntry[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // In production, this would fetch from GCP Cloud Logging via a Next.js API route
        setTimeout(() => {
            setLogs([
                { id: '1', timestamp: new Date().toISOString(), level: 'info', agent: 'Publisher', message: 'Triggered new publisher run from Cloud Scheduler.' },
                { id: '2', timestamp: new Date(Date.now() - 5000).toISOString(), level: 'success', agent: 'Publisher', message: 'Successfully published "Test Image" to Meta Ads.' },
                { id: '3', timestamp: new Date(Date.now() - 15000).toISOString(), level: 'error', agent: 'AI CMO', message: 'Failed to find ROAS target in database.' },
                { id: '4', timestamp: new Date(Date.now() - 60000).toISOString(), level: 'warning', agent: 'ETL Pipeline', message: 'Shopify API rate limit approaching.' },
                { id: '5', timestamp: new Date(Date.now() - 120000).toISOString(), level: 'success', agent: 'Image Gen', message: 'Generated 5 new assets and uploaded to GCS.' },
            ])
            setLoading(false)
        }, 800)
    }, [])

    const getLogIcon = (level: string) => {
        switch (level) {
            case 'info': return <Info size={18} color="var(--primary)" />
            case 'success': return <CheckCircle size={18} color="var(--success)" />
            case 'error': return <AlertCircle size={18} color="var(--danger)" />
            case 'warning': return <AlertCircle size={18} color="var(--warning)" />
            default: return <Info size={18} />
        }
    }

    return (
        <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1 className="text-gradient" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Agent Logs</h1>
                    <p className="text-muted">Live activity stream for your marketing bots.</p>
                </div>

                <button className="glass-button" disabled={loading}>
                    <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
                    Refresh Stream
                </button>
            </header>

            <div className="glass-panel" style={{ overflow: 'hidden' }}>
                {loading ? (
                    <div style={{ padding: '3rem', textAlign: 'center' }} className="text-muted">
                        Connecting to Log Stream...
                    </div>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        {logs.map((log, i) => (
                            <div
                                key={log.id}
                                style={{
                                    display: 'flex',
                                    alignItems: 'flex-start',
                                    gap: '1.5rem',
                                    padding: '1.25rem 1.5rem',
                                    borderBottom: i === logs.length - 1 ? 'none' : '1px solid var(--surface-border)',
                                    backgroundColor: 'rgba(0,0,0,0.1)'
                                }}
                            >
                                <div style={{ marginTop: '0.2rem' }}>
                                    {getLogIcon(log.level)}
                                </div>

                                <div style={{ flex: 1 }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                        <span style={{ fontWeight: 600, color: 'var(--foreground)' }}>[{log.agent}]</span>
                                        <span className="text-muted" style={{ fontSize: '0.85rem' }}>
                                            {format(new Date(log.timestamp), 'MMM d, HH:mm:ss')}
                                        </span>
                                    </div>
                                    <p style={{ color: log.level === 'error' ? 'var(--danger)' : '#e2e8f0', lineHeight: 1.5 }}>
                                        {log.message}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

        </div>
    )
}
