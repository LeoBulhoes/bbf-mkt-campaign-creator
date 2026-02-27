import { NextResponse, NextRequest } from 'next/server'

export function middleware(req: NextRequest) {
    const basicAuth = req.headers.get('authorization')
    const url = req.nextUrl

    // Require auth on all routes in production
    if (process.env.NODE_ENV === 'production') {
        if (basicAuth) {
            const authValue = basicAuth.split(' ')[1]
            const [user, pwd] = atob(authValue).split(':')

            // Very simple basic auth check mapped to a PORTAL_PASSWORD env variable.
            // If none is set, default to "bluebullfly". User is always "admin".
            const portalUser = process.env.PORTAL_USER || 'admin'
            const portalPassword = process.env.PORTAL_PASSWORD || 'bluebullfly'

            if (user === portalUser && pwd === portalPassword) {
                return NextResponse.next()
            }
        }
        url.pathname = '/api/basicauth'

        return new NextResponse('Auth required', {
            status: 401,
            headers: {
                'WWW-Authenticate': 'Basic realm="Secure Portal"',
            },
        })
    }
}

export const config = {
    matcher: '/(.*)',
}
