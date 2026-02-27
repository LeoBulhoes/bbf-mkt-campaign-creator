import type { Metadata } from 'next'
import './globals.css'
import Navigation from './Navigation'

export const metadata: Metadata = {
  title: 'BlueBullFly | Content Command Center',
  description: 'AI Marketing Pipeline and Ad Management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="page-container">
          <Navigation />
          <main className="main-content">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
