'use client'

import { useState, useEffect } from 'react'
import { Clock, MapPin, CheckCircle } from 'lucide-react'
import { api } from '@/lib/api'

interface RideStatusProps {
  ride: any
  onRideComplete: () => void
}

export default function RideStatus({ ride, onRideComplete }: RideStatusProps) {
  const [rideData, setRideData] = useState(ride)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Poll for ride updates or use WebSocket
    const interval = setInterval(async () => {
      try {
        const updated = await api.getRide(ride.id)
        setRideData(updated)
        if (updated.status === 'completed') {
          clearInterval(interval)
        }
      } catch (error) {
        console.error('Error fetching ride status:', error)
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [ride.id])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'text-yellow-600'
      case 'accepted':
        return 'text-blue-600'
      case 'in_progress':
        return 'text-green-600'
      case 'completed':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">Ride Status</h2>
        <span className={`font-semibold ${getStatusColor(rideData.status)}`}>
          {rideData.status.replace('_', ' ').toUpperCase()}
        </span>
      </div>

      <div className="space-y-3">
        <div className="flex items-start gap-3">
          <MapPin className="w-5 h-5 text-primary-600 mt-0.5" />
          <div className="flex-1">
            <div className="text-sm text-gray-600">Pickup</div>
            <div className="font-medium">{rideData.pickup_address}</div>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <MapPin className="w-5 h-5 text-red-600 mt-0.5" />
          <div className="flex-1">
            <div className="text-sm text-gray-600">Drop</div>
            <div className="font-medium">{rideData.drop_address}</div>
          </div>
        </div>

        {rideData.fare_estimate && (
          <div className="flex items-center justify-between pt-3 border-t">
            <span className="font-semibold">Estimated Fare</span>
            <span className="text-lg font-bold text-primary-600">
              ${rideData.fare_estimate.toFixed(2)}
            </span>
          </div>
        )}

        {rideData.status === 'completed' && (
          <button
            onClick={onRideComplete}
            className="w-full mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <CheckCircle className="w-5 h-5 inline mr-2" />
            Complete & Pay
          </button>
        )}
      </div>
    </div>
  )
}


