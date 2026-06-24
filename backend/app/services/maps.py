import googlemaps
from typing import Dict, Tuple, Optional
from app.core.config import settings

_gmaps_client: Optional[googlemaps.Client] = None


def _get_gmaps_client() -> googlemaps.Client:
    global _gmaps_client
    if _gmaps_client is None:
        if not settings.GOOGLE_MAPS_API_KEY:
            raise ValueError("GOOGLE_MAPS_API_KEY is not configured")
        _gmaps_client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    return _gmaps_client


def calculate_distance_and_duration(
    origin: Tuple[float, float],
    destination: Tuple[float, float]
) -> Dict:
    try:
        gmaps = _get_gmaps_client()
        result = gmaps.distance_matrix(
            origins=[f"{origin[0]},{origin[1]}"],
            destinations=[f"{destination[0]},{destination[1]}"],
            mode="driving",
            units="metric"
        )
        
        if result["status"] == "OK":
            element = result["rows"][0]["elements"][0]
            if element["status"] == "OK":
                distance_meters = element["distance"]["value"]
                duration_secs = element["duration"]["value"]
                
                base_fare = 2.50
                per_km_rate = 1.50
                per_minute_rate = 0.25
                
                distance_km = distance_meters / 1000
                duration_minutes = duration_secs / 60
                
                fare_estimate = base_fare + (distance_km * per_km_rate) + (duration_minutes * per_minute_rate)
                
                return {
                    "distance_meters": distance_meters,
                    "duration_secs": duration_secs,
                    "fare_estimate": round(fare_estimate, 2),
                }
        
        return {
            "distance_meters": 0,
            "duration_secs": 0,
            "fare_estimate": 0.0,
        }
    
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return {
            "distance_meters": 0,
            "duration_secs": 0,
            "fare_estimate": 0.0,
        }


def get_address_from_coordinates(lat: float, lng: float) -> str:
    try:
        gmaps = _get_gmaps_client()
        result = gmaps.reverse_geocode((lat, lng))
        if result:
            return result[0]["formatted_address"]
        return f"{lat}, {lng}"
    except Exception:
        return f"{lat}, {lng}"
