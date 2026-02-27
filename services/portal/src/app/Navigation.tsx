'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Activity, BarChart3, Settings, Rocket } from 'lucide-react'

export default function Navigation() {
    const pathname = usePathname()

    const links = [
        { name: 'Dashboard', href: '/', icon: BarChart3 },
        { name: 'Agent Logs', href: '/logs', icon: Activity },
        { name: 'Settings', href: '/settings', icon: Settings },
    ]

    return (
        <nav className="sidebar animate-fade-in">
            <div style={{ padding: '0 1rem', marginBottom: '2rem' }}>
                <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--foreground)' }}>
                    <Rocket size={24} color="var(--primary)" />
                    <span>BlueBullFly AI</span>
                </h2>
                <p className="text-muted" style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>Marketing Command Center</p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {links.map((link) => {
                    const Icon = link.icon
                    const isActive = pathname === link.href
                    return (
                        <Link
                            key={link.name}
                            href={link.href}
                            className={`nav-item ${isActive ? 'active' : ''}`}
                        >
                            <Icon size={20} />
                            {link.name}
                        </Link>
                    )
                })}
            </div>
        </nav>
    )
}
