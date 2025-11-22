import requests
import time
import re
from typing import Dict, List, Optional, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
CONFIG = {
    'NOMINATIM_URL': 'https://nominatim.openstreetmap.org/search',
    'OPENMETEO_URL': 'https://api.open-meteo.com/v1/forecast',
    'OVERPASS_URL': 'https://overpass-api.de/api/interpreter',
    'REQUEST_DELAY': 1
}

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self):
        self.request_delay = float(CONFIG.get('REQUEST_DELAY', 1))
    
    def make_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Make HTTP request with rate limiting"""
        try:
            time.sleep(self.request_delay)
            headers = {
                'User-Agent': 'TourismAgent/1.0 (https://github.com/yourusername/tourism-agent)'
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error for {url}: {e}")
            return None

class GeocodingService:
    """Service to get coordinates for a place using Nominatim API"""
    
    def get_coordinates(self, place: str) -> Optional[Tuple[float, float]]:
        """Get latitude and longitude for a place"""
        params = {
            'q': place,
            'format': 'json',
            'limit': 1
        }
        
        headers = {
            'User-Agent': 'TourismAgent/1.0 (https://github.com/yourusername/tourism-agent)'
        }
        
        try:
            response = requests.get(CONFIG['NOMINATIM_URL'], params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                print(f"📍 Found coordinates for {place}: {lat}, {lon}")
                return (lat, lon)
            else:
                print(f"❌ No coordinates found for {place}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Geocoding error: {e}")
            return None
        except (KeyError, ValueError) as e:
            print(f"Data parsing error: {e}")
            return None

class WeatherAgent(BaseAgent):
    """Agent responsible for fetching weather information"""
    
    def execute(self, place: str, coordinates: Tuple[float, float]) -> str:
        """Get current weather and forecast"""
        lat, lon = coordinates
        
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,precipitation_probability,weather_code',
            'timezone': 'auto'
        }
        
        data = self.make_request(CONFIG['OPENMETEO_URL'], params)
        
        if not data:
            return f"Unable to fetch weather data for {place}."
        
        try:
            current = data.get('current', {})
            temp = current.get('temperature_2m', 'N/A')
            precip_prob = current.get('precipitation_probability', 0)
            
            # Handle cases where precipitation might be None
            if precip_prob is None:
                precip_prob = 0
                
            return f"In {place} it's currently {temp}°C with a chance of {precip_prob}% to rain."
            
        except Exception as e:
            return f"Error processing weather data: {e}"

class PlacesAgent(BaseAgent):
    """Agent responsible for fetching tourist attractions"""
    
    def execute(self, place: str, coordinates: Tuple[float, float]) -> str:
        """Get tourist attractions using Overpass API"""
        lat, lon = coordinates
        
        # Overpass QL query to find tourist attractions within 20km radius
        # Prioritize specific tourism types: attraction, museum, monument, gallery, etc.
        query = f"""
        [out:json][timeout:25];
        (
          node["tourism"~"^(attraction|museum|monument|gallery|theme_park|zoo|aquarium|artwork|viewpoint|information)$"](around:20000,{lat},{lon});
          way["tourism"~"^(attraction|museum|monument|gallery|theme_park|zoo|aquarium|artwork|viewpoint|information)$"](around:20000,{lat},{lon});
          relation["tourism"~"^(attraction|museum|monument|gallery|theme_park|zoo|aquarium|artwork|viewpoint|information)$"](around:20000,{lat},{lon});
          node["historic"](around:20000,{lat},{lon});
          way["historic"](around:20000,{lat},{lon});
          relation["historic"](around:20000,{lat},{lon});
          node["leisure"~"^(park|nature_reserve|garden)$"](around:20000,{lat},{lon});
          way["leisure"~"^(park|nature_reserve|garden)$"](around:20000,{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """
        
        try:
            response = requests.post(CONFIG['OVERPASS_URL'], 
                                   data={'data': query}, 
                                   timeout=30)
            response.raise_for_status()
            data = response.json()
            
            places = self._extract_place_names(data)
            
            if places:
                # Format: "In {place} these are the places you can go," (comma, no bullets for single query)
                places_list = "\n\n".join([place for place in places[:5]])
                return f"In {place} these are the places you can go,\n\n{places_list}"
            else:
                return f"No tourist attractions found for {place}."
                
        except requests.exceptions.RequestException as e:
            return f"Error fetching places data: {e}"
        except Exception as e:
            return f"Error processing places data: {e}"
    
    def _is_english_name(self, name: str) -> bool:
        """Check if a name is primarily in English (ASCII characters)"""
        if not name:
            return False
        # Count ASCII characters (English) vs non-ASCII characters
        ascii_count = sum(1 for c in name if ord(c) < 128 and c.isprintable())
        total_chars = len([c for c in name if c.isprintable()])
        if total_chars == 0:
            return False
        # Consider it English if at least 70% of characters are ASCII
        return (ascii_count / total_chars) >= 0.7
    
    def _get_english_name(self, tags: Dict) -> Optional[str]:
        """Get English name from tags, preferring name:en, then checking name"""
        # First try name:en (English name tag)
        if 'name:en' in tags:
            name = tags['name:en']
            if name and len(name.strip()) > 0:
                return name.strip()
        
        # Then try name:en:official or name:en:short
        for key in ['name:en:official', 'name:en:short', 'official_name:en']:
            if key in tags:
                name = tags[key]
                if name and len(name.strip()) > 0:
                    return name.strip()
        
        # Finally check regular name, but only if it's English
        if 'name' in tags:
            name = tags['name']
            if name and self._is_english_name(name):
                return name.strip()
        
        return None
    
    def _extract_place_names(self, data: Dict) -> List[str]:
        """Extract place names from Overpass API response with prioritization"""
        places = []
        place_scores = {}  # Dictionary to score and rank places
        
        # Tourism type priority (higher = better)
        tourism_priority = {
            'attraction': 10,
            'museum': 9,
            'monument': 9,
            'gallery': 8,
            'theme_park': 8,
            'zoo': 8,
            'aquarium': 8,
            'artwork': 7,
            'viewpoint': 7,
            'information': 6,
            'historic': 9,
            'park': 7,
            'nature_reserve': 7,
            'garden': 6
        }
        
        # Words to exclude (generic or non-tourist places)
        exclude_words = [
            'residency', 'hotel', 'hostel', 'restaurant', 'cafe', 'bank',
            'atm', 'parking', 'toilet', 'bench', 'waste', 'cross', 'junction',
            'signal', 'traffic', 'bus stop', 'metro', 'station', 'mall',
            'shop', 'store', 'market', 'commercial', 'office', 'building',
            'apartment', 'residential', 'house', 'home', 'holiday home'
        ]
        
        for element in data.get('elements', []):
            if 'tags' not in element:
                continue
            
            # Get English name (prefer name:en, fallback to name if English)
            name = self._get_english_name(element['tags'])
            if not name or len(name) == 0 or len(name) > 50:
                continue
            
            # Skip if name contains exclude words
            name_lower = name.lower()
            if any(exclude_word in name_lower for exclude_word in exclude_words):
                continue
            
            # Calculate score based on tourism type
            score = 0
            tourism_type = element['tags'].get('tourism', '')
            historic_type = element['tags'].get('historic', '')
            leisure_type = element['tags'].get('leisure', '')
            
            if tourism_type in tourism_priority:
                score = tourism_priority[tourism_type]
            elif historic_type:
                score = tourism_priority.get('historic', 5)
            elif leisure_type in tourism_priority:
                score = tourism_priority[leisure_type]
            else:
                score = 3  # Default score for other tourism types
            
            # Bonus for having additional relevant tags
            if 'wikidata' in element['tags'] or 'wikipedia' in element['tags']:
                score += 2  # More likely to be well-known
            
            # Bonus for having name:en (official English name)
            if 'name:en' in element['tags']:
                score += 1
            
            if name not in place_scores or place_scores[name] < score:
                place_scores[name] = score
        
        # Sort by score (descending) and return top places
        sorted_places = sorted(place_scores.items(), key=lambda x: x[1], reverse=True)
        places = [place[0] for place in sorted_places[:10]]  # Get top 10, then return top 5
        
        # If we don't have enough high-quality places, try a broader search
        if len(places) < 3:
            # Fallback: include any tourism place that has an English name
            for element in data.get('elements', []):
                if 'tags' not in element:
                    continue
                name = self._get_english_name(element['tags'])
                if (name and len(name.strip()) > 0 and 
                    name not in places and 
                    len(name) < 50):
                    name_lower = name.lower()
                    # Still exclude obvious non-tourist places
                    if not any(exclude_word in name_lower for exclude_word in ['residency', 'holiday home', 'bank', 'cross']):
                        places.append(name)
                        if len(places) >= 5:
                            break
        
        return places[:5]

class TourismAIAgent:
    """Parent agent that orchestrates the tourism system"""
    
    def __init__(self):
        self.geocoding_service = GeocodingService()
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
    
    def extract_place(self, user_input: str) -> Optional[str]:
        """Extract place name from user input"""
        input_lower = user_input.lower()
        
        # Enhanced patterns for place extraction (order matters - more specific first)
        patterns = [
            r"going to go to\s+([^,\.!?]+)",  # "I'm going to go to Bangalore"
            r"going to\s+([^,\.!?]+)",        # "I'm going to Bangalore"
            r"go to\s+([^,\.!?]+)",           # "go to Bangalore"
            r"in\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",  # "in Bangalore" or "in New York"
            r"visit\s+([^,\.!?]+)",           # "visit Paris"
            r"to\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",  # "to Tokyo"
            r"at\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)",  # "at London"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                potential_place = match.group(1).strip()
                # Clean up the place name - remove common question words and verbs
                potential_place = re.sub(
                    r'\b(?:going|to|visit|travel|trip|plan|what|where|how|is|are|the|there|and|can|i|my|me|let\'s|lets)\b', 
                    '', 
                    potential_place, 
                    flags=re.IGNORECASE
                ).strip()
                
                # Remove trailing punctuation and extra words
                potential_place = re.sub(r'[,\.!?].*$', '', potential_place).strip()
                
                # Split and take the first significant word(s) as place name
                words = potential_place.split()
                if words:
                    # Take up to 3 words (for places like "New York" or "Los Angeles")
                    place = ' '.join(words[:3]).strip()
                    if len(place) > 1:
                        return place.title()
        
        # Fallback: Look for capitalized words that might be place names
        words = user_input.split()
        capitalized_words = []
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word and clean_word[0].isupper() and len(clean_word) > 2:
                capitalized_words.append(clean_word)
        
        if capitalized_words:
            # Return the longest capitalized word (likely the place name)
            return max(capitalized_words, key=len).title()
        
        return None
    
    def analyze_intent(self, user_input: str) -> Dict[str, bool]:
        """Analyze user intent from input"""
        input_lower = user_input.lower()
        
        # Weather-related keywords
        weather_keywords = [
            'temperature', 'temp', 'weather', 'rain', 'forecast', 
            'hot', 'cold', 'warm', 'cool', 'humid', 'precipitation',
            'climate', 'sunny', 'cloudy', 'rainy'
        ]
        
        # Places-related keywords (more specific phrases to avoid false positives)
        places_phrases = [
            'places to', 'place to', 'places i can', 'places you can',
            'what places', 'which places', 'what are the places',
            'attractions', 'tourist', 'sightseeing', 'sights',
            'where to go', 'where to visit', 'what to see', 'what to visit',
            'things to do', 'destinations', 'can visit', 'can go',
            'should visit', 'should see', 'places i can visit',
            'places can visit', 'places can go'
        ]
        
        # Single word keywords (only if not part of "going to")
        places_single_words = ['visit', 'see']
        
        # Check for weather intent
        has_weather = any(keyword in input_lower for keyword in weather_keywords)
        
        # Check for places intent - use phrases first (more reliable)
        has_places = any(phrase in input_lower for phrase in places_phrases)
        
        # Also check single words, but exclude if they're part of "going to" pattern
        if not has_places:
            for word in places_single_words:
                if word in input_lower:
                    # Make sure it's not part of "going to [place]"
                    pattern = rf'going\s+to\s+[^,\.!?]*\b{word}\b'
                    if not re.search(pattern, input_lower):
                        has_places = True
                        break
        
        # Special case: "plan my trip" or "plan trip" strongly indicates places
        if 'plan' in input_lower and ('trip' in input_lower or 'visit' in input_lower):
            has_places = True
        
        # Check for combined intent
        has_both = has_weather and has_places
        
        return {
            'weather': has_weather,
            'places': has_places,
            'both': has_both
        }
    
    def process_request(self, user_input: str) -> str:
        """Main method to process user request"""
        print(f"🔍 Processing: {user_input}")
        
        # Extract place from input
        place = self.extract_place(user_input)
        
        if not place:
            return "I couldn't determine which place you're interested in. Please specify a location like 'Paris' or 'What to see in London?'"
        
        print(f"📍 Identified place: {place}")
        
        # Get coordinates for the place
        coordinates = self.geocoding_service.get_coordinates(place)
        
        if not coordinates:
            return f"It doesn't know this place exist."
        
        # Analyze user intent
        intent = self.analyze_intent(user_input)
        print(f"🎯 Detected intent: {intent}")
        
        # Execute appropriate agents based on intent
        results = []
        weather_result = None
        places_result = None
        
        # If no specific intent detected, check for trip planning keywords
        if not any([intent['weather'], intent['places'], intent['both']]):
            # Check if it's a general trip planning query
            input_lower = user_input.lower()
            if any(phrase in input_lower for phrase in ['plan', 'trip', 'going to go to']):
                print("🔍 Detected trip planning query, fetching places...")
                places_result = self.places_agent.execute(place, coordinates)
                results.append(places_result)
            else:
                # Default: fetch both
                print("🔍 No specific intent detected, fetching both weather and places...")
                weather_result = self.weather_agent.execute(place, coordinates)
                places_result = self.places_agent.execute(place, coordinates)
                results.extend([weather_result, places_result])
        else:
            # Handle specific intents
            if intent['weather'] or intent['both']:
                print("🌤️ Fetching weather data...")
                weather_result = self.weather_agent.execute(place, coordinates)
                results.append(weather_result)
            
            if intent['places'] or intent['both']:
                print("🏛️ Fetching tourist places...")
                places_result = self.places_agent.execute(place, coordinates)
                results.append(places_result)
        
        # Format the response based on the examples
        if intent['both'] or (weather_result and places_result):
            # Combined response format: "In X it's... And these are the places..."
            if weather_result and places_result:
                # For combined queries, format with bullets and colon
                if f"In {place} these are the places you can go," in places_result:
                    # Extract places list (remove the header)
                    places_text = places_result.replace(f"In {place} these are the places you can go,\n\n", "")
                    # Format with bullets for combined query
                    places_lines = [line.strip() for line in places_text.split("\n\n") if line.strip()]
                    places_list = "\n".join([f"• {p}" for p in places_lines[:5]])
                    places_formatted = f"And these are the places you can go:\n{places_list}"
                else:
                    places_formatted = places_result
                
                # Combine with proper spacing
                return f"{weather_result} {places_formatted}"
        
        # Return single result or combined results
        return " ".join(results)

def main():
    """Main application loop"""
    agent = TourismAIAgent()
    
    print("🌍 Welcome to the Multi-Agent Tourism System!")
    print("=" * 50)
    print("You can ask about weather, tourist places, or both!")
    print("\n💡 Examples:")
    print("• 'I'm going to Bangalore, what's the temperature?'")
    print("• 'What places can I visit in Paris?'")
    print("• 'Tell me about Tokyo'")
    print("• 'Weather in New York'")
    print("• 'Sightseeing in London'")
    print("• Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n🔹 Enter your query: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\nThank you for using the Tourism System! 👋")
                break
            
            if not user_input:
                print("Please enter a valid query.")
                continue
            
            # Process the request
            print("\n" + "=" * 50)
            response = agent.process_request(user_input)
            print(f"\n🤖 {response}")
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Tourism System! 👋")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again with a different query.")

if __name__ == "__main__":
    main()