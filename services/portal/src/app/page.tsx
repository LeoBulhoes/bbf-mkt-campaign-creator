'use client'

import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

export default function Dashboard() {
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // In a real implementation, this hits our Next.js API route 
    // which securely queries BigQuery using the service account credentials.
    async function fetchMetrics() {
      try {
        const response = await fetch('/api/metrics')
        if (response.ok) {
          const json = await response.json()
          setData(json.data || [])
        }
      } catch (err) {
        console.error('Failed to load metrics', err)
      } finally {
        setLoading(false)
      }
    }

    // For now, load dummy data if API isn't ready
    setTimeout(() => {
      setData([
        { date: 'Feb 21', meta_spend: 120, shopify_sales: 450, roas: 3.75 },
        { date: 'Feb 22', meta_spend: 150, shopify_sales: 600, roas: 4.0 },
        { date: 'Feb 23', meta_spend: 140, shopify_sales: 420, roas: 3.0 },
        { date: 'Feb 24', meta_spend: 200, shopify_sales: 900, roas: 4.5 },
        { date: 'Feb 25', meta_spend: 220, shopify_sales: 1100, roas: 5.0 },
        { date: 'Feb 26', meta_spend: 180, shopify_sales: 750, roas: 4.16 },
      ])
      setLoading(false)
    }, 1000)

  }, [])

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

      <header>
        <h1 className="text-gradient" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Overview</h1>
        <p className="text-muted">Monitor your AI marketing performance.</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 className="text-muted" style={{ fontSize: '0.9rem', marginBottom: '0.5rem' }}>Total Spend (7d)</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>$1,010.00</p>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', marginTop: '0.5rem', fontSize: '0.85rem', color: 'var(--success)' }}>
            <span className="status-dot status-success"></span> AI Recommended target achieved.
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 className="text-muted" style={{ fontSize: '0.9rem', marginBottom: '0.5rem' }}>Total Sales (7d)</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>$4,220.00</p>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', marginTop: '0.5rem', fontSize: '0.85rem', color: 'var(--success)' }}>
            <span className="status-dot status-success"></span> +12% vs previous period.
          </div>
        </div>

        <div className="glass-panel" style={{ padding: '1.5rem' }}>
          <h3 className="text-muted" style={{ fontSize: '0.9rem', marginBottom: '0.5rem' }}>Blended ROAS</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--primary)' }}>4.17x</p>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.25rem', marginTop: '0.5rem', fontSize: '0.85rem', color: 'var(--warning)' }}>
            <span className="status-dot status-warning"></span> Monitor Meta CPA closely.
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '2rem', height: '400px' }}>
        <h3 style={{ marginBottom: '2rem' }}>Spend vs. Revenue</h3>
        {loading ? (
          <div style={{ display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center' }}>
            <p className="text-muted">Loading BigQuery metrics...</p>
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="80%">
            <BarChart data={data} maxBarSize={40}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
              <XAxis dataKey="date" stroke="#94a3b8" tickLine={false} axisLine={false} />
              <YAxis yAxisId="left" orientation="left" stroke="#94a3b8" tickLine={false} axisLine={false} tickFormatter={(value) => `$${value}`} />
              <YAxis yAxisId="right" orientation="right" stroke="#ec4899" tickLine={false} axisLine={false} />
              <Tooltip
                cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                contentStyle={{ backgroundColor: 'rgba(13, 15, 23, 0.9)', border: '1px solid var(--surface-border)', borderRadius: '8px' }}
              />
              <Bar yAxisId="left" dataKey="meta_spend" name="Meta Spend" fill="var(--primary)" radius={[4, 4, 0, 0]} />
              <Bar yAxisId="left" dataKey="shopify_sales" name="Shopify Sales" fill="var(--success)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>

    </div>
  )
}
