'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import MapComponent from '@/components/MapComponent'
import RideBookingForm from '@/components/RideBookingForm'
import RideStatus from '@/components/RideStatus'
import { useAuth } from '@/hooks/useAuth'

export default function Home() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [activeRide, setActiveRide] = useState(null)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/sign-in')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <main className="min-h-screen">
      <div className="relative h-screen w-full">
        <MapComponent activeRide={activeRide} />
        <div className="absolute bottom-0 left-0 right-0 p-4">
          {activeRide ? (
            <RideStatus ride={activeRide} onRideComplete={() => setActiveRide(null)} />
          ) : (
            <RideBookingForm onRideCreated={setActiveRide} />
          )}
        </div>
      </div>
    </main>
  )
}


