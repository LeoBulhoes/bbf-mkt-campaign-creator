'use client'

export default function SettingsPage() {
    return (
        <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

            <header>
                <h1 className="text-gradient" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Configuration</h1>
                <p className="text-muted">Manage Portal Access and API connections.</p>
            </header>

            <div className="glass-panel" style={{ padding: '2rem' }}>
                <h3 style={{ marginBottom: '1.5rem', color: 'var(--foreground)' }}>Cloud Run Deployments</h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'var(--surface)', borderRadius: 'var(--radius-sm)' }}>
                        <div>
                            <p style={{ fontWeight: 500 }}>Publishing API Connector</p>
                            <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>services/publisher</p>
                        </div>
                        <span style={{ color: 'var(--success)', fontSize: '0.9rem', fontWeight: 500 }}>Active</span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'var(--surface)', borderRadius: 'var(--radius-sm)' }}>
                        <div>
                            <p style={{ fontWeight: 500 }}>Unified Data Warehouse ETL</p>
                            <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>services/data_warehouse</p>
                        </div>
                        <span style={{ color: 'var(--success)', fontSize: '0.9rem', fontWeight: 500 }}>Active</span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem', background: 'var(--surface)', borderRadius: 'var(--radius-sm)' }}>
                        <div>
                            <p style={{ fontWeight: 500 }}>AI CMO Agent</p>
                            <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>services/cmo</p>
                        </div>
                        <span style={{ color: 'var(--warning)', fontSize: '0.9rem', fontWeight: 500 }}>Pending</span>
                    </div>
                </div>

            </div>
        </div>
    )
}
