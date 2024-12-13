from typing import List, Tuple
import requests
from datetime import datetime

class Hospital:
    def __init__(self, name: str, address: str, distance: float, 
                 location: Tuple[float, float], phone: str = None):
        self.name = name
        self.address = address
        self.distance = distance  # in kilometers
        self.location = location  # (latitude, longitude)
        self.phone = phone

class LocationService:
    def __init__(self):
        self.overpass_url = 'https://overpass-api.de/api/interpreter'
    
    def get_nearby_hospitals(self, location: str, radius: int = 5000) -> List[Hospital]:
        """
        Find nearby hospitals within specified radius (in meters)
        Args:
            location: Location name (e.g., "Kampala, Uganda")
            radius: Search radius in meters (default 5km)
        Returns:
            List of Hospital objects sorted by distance
        """
        try:
            # First get the coordinates for the location
            nominatim_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
            location_data = requests.get(nominatim_url).json()
            
            if not location_data:
                raise ValueError(f"Could not find location: {location}")
            
            lat = float(location_data[0]['lat'])
            lon = float(location_data[0]['lon'])
            
            # Create Overpass query for hospitals
            overpass_query = f"""
            [out:json];
            (
              node["amenity"="hospital"](around:{radius},{lat},{lon});
              way["amenity"="hospital"](around:{radius},{lat},{lon});
              relation["amenity"="hospital"](around:{radius},{lat},{lon});
            );
            out center body;
            """
            
            response = requests.get(self.overpass_url, params={'data': overpass_query})
            data = response.json()
            
            hospitals = []
            for element in data.get('elements', []):
                # Get coordinates based on element type
                if element['type'] == 'node':
                    hospital_lat = element['lat']
                    hospital_lon = element['lon']
                else:  # way or relation
                    hospital_lat = element.get('center', {}).get('lat')
                    hospital_lon = element.get('center', {}).get('lon')
                
                if hospital_lat and hospital_lon:
                    # Calculate straight-line distance
                    distance = self._calculate_distance(
                        (lat, lon),
                        (hospital_lat, hospital_lon)
                    )
                    
                    hospital = Hospital(
                        name=element.get('tags', {}).get('name', 'Unknown Hospital'),
                        address=element.get('tags', {}).get('addr:full', ''),
                        distance=distance,
                        location=(hospital_lat, hospital_lon),
                        phone=element.get('tags', {}).get('phone', '')
                    )
                    hospitals.append(hospital)
            
            return sorted(hospitals, key=lambda x: x.distance)
            
        except Exception as e:
            print(f"Error finding nearby hospitals: {str(e)}")
            return []
    
    def _calculate_distance(self, origin: Tuple[float, float], 
                          destination: Tuple[float, float]) -> float:
        """Calculate straight-line distance between two points in kilometers"""
        from math import sin, cos, sqrt, atan2, radians
        
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = radians(origin[0]), radians(origin[1])
        lat2, lon2 = radians(destination[0]), radians(destination[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return distance

def validate_uganda_location(location: str, gmaps=None) -> bool:
    """Validate if the given location is in Uganda"""
    return "uganda" in location.lower()

def main():
    # Initialize the service
    location_service = LocationService()
    
    # Get user input for Uganda location
    while True:
        location = input("Enter location in Uganda (e.g., 'Kampala, Uganda'): ").strip()
        if not location:
            location = "Kampala, Uganda"  # Default to Kampala if no input
        
        if validate_uganda_location(location):
            break
        print("Please enter a valid location in Uganda.")

    radius = int(input("Enter search radius in meters (default 5000): ") or "5000")

    print(f"\nSearching for hospitals near {location} within {radius}m radius...")
    
    # Fetch nearby hospitals
    hospitals = location_service.get_nearby_hospitals(location, radius)

    if not hospitals:
        print("No hospitals found in the specified area.")
        return

    # Display the hospitals
    print(f"\nFound {len(hospitals)} hospitals in Uganda:")
    print("-" * 80)
    
    for i, hospital in enumerate(hospitals, 1):
        print(f"{i}. {hospital.name}")
        print(f"   Address: {hospital.address}")
        print(f"   Distance: {hospital.distance:.2f} km")
        print(f"   Phone: {hospital.phone or 'N/A'}")
        print("-" * 80)

    # Rest of the code remains the same...

if __name__ == "__main__":
    main() 