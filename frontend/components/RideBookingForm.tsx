'use client'

import { useState } from 'react'
import { MapPin, Navigation, DollarSign } from 'lucide-react'
import { api } from '@/lib/api'
import { geocodeAddress } from '@/lib/geocoding'

interface RideBookingFormProps {
  onRideCreated: (ride: any) => void
}

export default function RideBookingForm({ onRideCreated }: RideBookingFormProps) {
  const [pickup, setPickup] = useState('')
  const [drop, setDrop] = useState('')
  const [pickupCoords, setPickupCoords] = useState<{ lat: number; lng: number } | null>(null)
  const [dropCoords, setDropCoords] = useState<{ lat: number; lng: number } | null>(null)
  const [estimate, setEstimate] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [booking, setBooking] = useState(false)
  const [geocoding, setGeocoding] = useState(false)

  const handleGeocodePickup = async () => {
    if (!pickup.trim()) return
    setGeocoding(true)
    try {
      const coords = await geocodeAddress(pickup)
      if (coords) {
        setPickupCoords(coords)
        setEstimate(null)
      } else {
        alert('Could not find pickup location. Please enter a valid address.')
        setPickupCoords(null)
      }
    } finally {
      setGeocoding(false)
    }
  }

  const handleGeocodeDrop = async () => {
    if (!drop.trim()) return
    setGeocoding(true)
    try {
      const coords = await geocodeAddress(drop)
      if (coords) {
        setDropCoords(coords)
        setEstimate(null)
      } else {
        alert('Could not find drop location. Please enter a valid address.')
        setDropCoords(null)
      }
    } finally {
      setGeocoding(false)
    }
  }

  const handleEstimate = async () => {
    if (!pickupCoords || !dropCoords) {
      alert('Please enter and confirm pickup and drop locations')
      return
    }

    setLoading(true)
    try {
      const data = await api.estimateRide(pickupCoords, dropCoords)
      setEstimate(data)
    } catch (error) {
      console.error('Error estimating ride:', error)
      alert('Failed to get estimate')
    } finally {
      setLoading(false)
    }
  }

  const handleBookRide = async () => {
    if (!pickupCoords || !dropCoords || !estimate) return

    setBooking(true)
    try {
      const ride = await api.createRide({
        pickup_lat: pickupCoords.lat,
        pickup_lng: pickupCoords.lng,
        drop_lat: dropCoords.lat,
        drop_lng: dropCoords.lng,
        pickup_address: pickup,
        drop_address: drop,
      })
      onRideCreated({
        ...ride,
        pickup_lat: pickupCoords.lat,
        pickup_lng: pickupCoords.lng,
        drop_lat: dropCoords.lat,
        drop_lng: dropCoords.lng,
      })
    } catch (error) {
      console.error('Error booking ride:', error)
      alert('Failed to book ride')
    } finally {
      setBooking(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4">Book a Ride</h2>

      <div className="space-y-4">
        <div>
          <label className="flex items-center gap-2 text-sm font-medium mb-2">
            <MapPin className="w-4 h-4" />
            Pickup Location
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={pickup}
              onChange={(e) => {
                setPickup(e.target.value)
                setPickupCoords(null)
                setEstimate(null)
              }}
              onBlur={handleGeocodePickup}
              placeholder="Enter pickup address"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          {pickupCoords && (
            <p className="text-xs text-green-600 mt-1">Location confirmed</p>
          )}
        </div>

        <div>
          <label className="flex items-center gap-2 text-sm font-medium mb-2">
            <Navigation className="w-4 h-4" />
            Drop Location
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={drop}
              onChange={(e) => {
                setDrop(e.target.value)
                setDropCoords(null)
                setEstimate(null)
              }}
              onBlur={handleGeocodeDrop}
              placeholder="Enter drop address"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          {dropCoords && (
            <p className="text-xs text-green-600 mt-1">Location confirmed</p>
          )}
        </div>

        {geocoding && (
          <p className="text-sm text-gray-500">Looking up address...</p>
        )}

        {estimate && (
          <div className="bg-primary-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-5 h-5 text-primary-600" />
              <span className="font-semibold">Estimate</span>
            </div>
            <div className="text-sm space-y-1">
              <div>Distance: {(estimate.distance_meters / 1000).toFixed(2)} km</div>
              <div>Duration: {Math.round(estimate.duration_secs / 60)} min</div>
              <div className="text-lg font-bold text-primary-600">
                ${estimate.fare_estimate.toFixed(2)}
              </div>
            </div>
          </div>
        )}

        <div className="flex gap-2">
          <button
            onClick={handleEstimate}
            disabled={!pickupCoords || !dropCoords || loading || geocoding}
            className="flex-1 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Calculating...' : 'Get Estimate'}
          </button>

          {estimate && (
            <button
              onClick={handleBookRide}
              disabled={booking}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {booking ? 'Booking...' : 'Book Ride'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
