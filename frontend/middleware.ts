import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { authMiddleware } from '@clerk/nextjs'

const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY ?? ''
const clerkConfigured =
  publishableKey.startsWith('pk_') &&
  !publishableKey.includes('placeholder') &&
  !publishableKey.includes('your_key')

const clerkMiddleware = authMiddleware({
  publicRoutes: ['/sign-in', '/sign-up'],
})

export default function middleware(request: NextRequest) {
  if (!clerkConfigured) {
    return NextResponse.next()
  }
  return clerkMiddleware(request, {} as any)
}

export const config = {
  matcher: ['/((?!.+\\.[\\w]+$|_next).*)', '/', '/(api|trpc)(.*)'],
}
