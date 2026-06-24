import { useState, useEffect } from 'react'
import { useUser, useAuth as useClerkAuth } from '@clerk/nextjs'

export function useAuth() {
  const { user, isLoaded } = useUser()
  const { getToken } = useClerkAuth()
  const [authToken, setAuthToken] = useState<string | null>(null)

  useEffect(() => {
    if (user && getToken) {
      getToken().then((token) => {
        if (token) {
          setAuthToken(token)
          localStorage.setItem('auth_token', token)
        }
      })
    } else {
      localStorage.removeItem('auth_token')
      setAuthToken(null)
    }
  }, [user, getToken])

  return {
    user: user ? {
      id: user.id,
      email: user.primaryEmailAddress?.emailAddress,
      name: user.fullName || user.firstName || 'User',
      imageUrl: user.imageUrl,
    } : null,
    loading: !isLoaded,
    token: authToken,
  }
}
