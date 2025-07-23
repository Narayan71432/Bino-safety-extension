import geocoder
import logging
from typing import Optional, Dict

class LocationService:
    @staticmethod
    def get_current_location() -> Optional[Dict[str, str]]:
        """
        Get the current location using IP-based geolocation.
        Returns a dictionary with 'address' and 'maps_link' or None if failed.
        """
        try:
            g = geocoder.ip('me')
            if g.ok:
                return {
                    'address': g.address,
                    'maps_link': f"https://www.google.com/maps?q={g.lat},{g.lng}"
                }
        except Exception as e:
            logging.error(f"Error getting location: {e}")
        return None

if __name__ == "__main__":
    # Test the location service
    location = LocationService.get_current_location()
    if location:
        print(f"Current Location: {location['address']}")
        print(f"Google Maps: {location['maps_link']}")
    else:
        print("Could not determine location.")
