'use client'

import { useEffect, useRef, useState } from 'react'
import { Loader } from '@googlemaps/js-api-loader'

interface MapComponentProps {
  activeRide: any
}

export default function MapComponent({ activeRide }: MapComponentProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const [map, setMap] = useState<google.maps.Map | null>(null)
  const [pickupMarker, setPickupMarker] = useState<google.maps.Marker | null>(null)
  const [dropMarker, setDropMarker] = useState<google.maps.Marker | null>(null)
  const [directionsRenderer, setDirectionsRenderer] = useState<google.maps.DirectionsRenderer | null>(null)

  useEffect(() => {
    const initMap = async () => {
      const loader = new Loader({
        apiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
        version: 'weekly',
        libraries: ['places', 'geometry'],
      })

      try {
        const { Map } = await loader.importLibrary('maps')
        const { Marker } = await loader.importLibrary('marker')
        const { DirectionsRenderer } = await loader.importLibrary('routes')

        if (mapRef.current) {
          const mapInstance = new Map(mapRef.current, {
            center: { lat: 37.7749, lng: -122.4194 }, // Default to San Francisco
            zoom: 13,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: true,
          })

          setMap(mapInstance)

          // Get user's current location
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
              (position) => {
                const userLocation = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude,
                }
                mapInstance.setCenter(userLocation)
                mapInstance.setZoom(15)
              },
              (error) => {
                console.error('Error getting location:', error)
              }
            )
          }
        }
      } catch (error) {
        console.error('Error loading Google Maps:', error)
      }
    }

    initMap()
  }, [])

  useEffect(() => {
    if (!map || !activeRide) return

    const { Marker } = google.maps
    const { DirectionsRenderer, DirectionsService } = google.maps

    // Clear existing markers
    if (pickupMarker) pickupMarker.setMap(null)
    if (dropMarker) dropMarker.setMap(null)
    if (directionsRenderer) directionsRenderer.setMap(null)

    // Create pickup marker
    const pickup = new Marker({
      position: { lat: activeRide.pickup_lat, lng: activeRide.pickup_lng },
      map,
      label: 'P',
      title: 'Pickup',
    })
    setPickupMarker(pickup)

    // Create drop marker
    const drop = new Marker({
      position: { lat: activeRide.drop_lat, lng: activeRide.drop_lng },
      map,
      label: 'D',
      title: 'Drop',
    })
    setDropMarker(drop)

    // Draw route
    const directionsService = new DirectionsService()
    const renderer = new DirectionsRenderer({
      map,
      suppressMarkers: true,
    })
    setDirectionsRenderer(renderer)

    directionsService.route(
      {
        origin: { lat: activeRide.pickup_lat, lng: activeRide.pickup_lng },
        destination: { lat: activeRide.drop_lat, lng: activeRide.drop_lng },
        travelMode: google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === 'OK' && result) {
          renderer.setDirections(result)
          const bounds = new google.maps.LatLngBounds()
          result.routes[0].legs.forEach((leg) => {
            bounds.extend(leg.start_location)
            bounds.extend(leg.end_location)
          })
          map.fitBounds(bounds)
        }
      }
    )
  }, [map, activeRide]) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div
      ref={mapRef}
      className="w-full h-full"
      style={{ minHeight: '100vh' }}
    />
  )
}


