"""
Data Processing Script for London Crime Analysis
Processes real crime data from police.uk API into database format
"""

import csv
import json
import sqlite3
from datetime import datetime
import re

def clean_location_data(location_str):
    """Clean and parse location data from API response"""
    try:
        if isinstance(location_str, str):
            # Remove extra quotes and parse
            location_str = location_str.replace("'", '"')
            location = json.loads(location_str.replace("'", '"'))
        else:
            location = location_str
        
        lat = float(location.get('latitude', 0))
        lng = float(location.get('longitude', 0))
        street_name = location.get('street', {}).get('name', 'Unknown')
        
        return lat, lng, street_name
    except:
        return 0.0, 0.0, 'Unknown'

def map_crime_category(api_category):
    """Map API crime categories to our database categories"""
    category_mapping = {
        'anti-social-behaviour': 1,
        'burglary': 2,
        'robbery': 3,
        'vehicle-crime': 4,
        'violent-crime': 5,
        'theft-from-the-person': 6,
        'criminal-damage-arson': 7,
        'drugs': 8,
        'public-order': 9,
        'shoplifting': 10,
        'other-theft': 6,  # Map to theft-from-person
        'possession-of-weapons': 5,  # Map to violent-crime
        'other-crime': 1,  # Map to anti-social-behaviour
        'bicycle-theft': 4,  # Map to vehicle-crime
    }
    return category_mapping.get(api_category, 1)  # Default to anti-social-behaviour

def get_borough_from_coordinates(lat, lng):
    """Determine borough based on coordinates (simplified mapping)"""
    # Westminster: Central London
    if 51.49 <= lat <= 51.52 and -0.15 <= lng <= -0.11:
        return 1
    # Camden: North of Westminster
    elif 51.52 <= lat <= 51.56 and -0.15 <= lng <= -0.10:
        return 2
    # Tower Hamlets: East London
    elif 51.50 <= lat <= 51.54 and -0.02 <= lng <= 0.02:
        return 4
    # Southwark: South of Thames
    elif 51.48 <= lat <= 51.51 and -0.12 <= lng <= -0.05:
        return 5
    # City of London: Financial district
    elif 51.51 <= lat <= 51.52 and -0.10 <= lng <= -0.07:
        return 1  # Group with Westminster for now
    else:
        return 1  # Default to Westminster

def process_london_crime_data():
    """Process collected London crime data into database"""
    print("Processing London crime data...")
    
    # Connect to database
    conn = sqlite3.connect('london_crime_analysis.db')
    cursor = conn.cursor()
    
    # Read collected data
    crimes_data = []
    with open('collected_data/london_crimes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        crimes_data = list(reader)
    
    print(f"Processing {len(crimes_data)} crime records...")
    
    # Process each crime record
    processed_locations = {}
    processed_crimes = []
    location_id_counter = 1
    
    for i, crime in enumerate(crimes_data):
        try:
            # Parse location
            lat, lng, street_name = clean_location_data(crime['location'])
            
            # Create unique location key
            location_key = f"{lat:.4f},{lng:.4f}"
            
            if location_key not in processed_locations:
                city_id = get_borough_from_coordinates(lat, lng)
                
                processed_locations[location_key] = {
                    'location_id': location_id_counter,
                    'street_name': street_name,
                    'latitude': lat,
                    'longitude': lng,
                    'city_id': city_id
                }
                location_id_counter += 1
            
            # Process crime record
            category_id = map_crime_category(crime['category'])
            
            # Parse date
            crime_date = datetime.strptime(crime['month'], '%Y-%m').date()
            
            # Determine status
            status = 'Closed' if crime.get('outcome_status') else 'Open'
            
            processed_crime = {
                'crime_id': f"REAL-{crime['id']}",
                'category_id': category_id,
                'location_id': processed_locations[location_key]['location_id'],
                'force_id': 'MET001',
                'incident_date': crime_date,
                'month_reported': crime['month'],
                'context': crime.get('context', ''),
                'status': status
            }
            
            processed_crimes.append(processed_crime)
            
        except Exception as e:
            print(f"Error processing crime {i}: {e}")
            continue
    
    print(f"Processed {len(processed_crimes)} crimes and {len(processed_locations)} unique locations")
    
    # Insert locations into database
    print("Inserting locations...")
    for location in processed_locations.values():
        cursor.execute("""
            INSERT OR REPLACE INTO locations 
            (location_id, street_name, latitude, longitude, city_id, location_type)
            VALUES (?, ?, ?, ?, ?, 'Street')
        """, (
            location['location_id'],
            location['street_name'],
            location['latitude'], 
            location['longitude'],
            location['city_id']
        ))
    
    # Insert crimes into database
    print("Inserting crimes...")
    for crime in processed_crimes:
        cursor.execute("""
            INSERT OR REPLACE INTO crime_incidents 
            (crime_id, category_id, location_id, force_id, incident_date, month_reported, context, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            crime['crime_id'],
            crime['category_id'],
            crime['location_id'],
            crime['force_id'],
            crime['incident_date'],
            crime['month_reported'],
            crime['context'],
            crime['status']
        ))
    
    conn.commit()
    conn.close()
    
    print("Data processing complete!")
    print(f"Inserted {len(processed_locations)} locations and {len(processed_crimes)} crimes")
    
    return len(processed_crimes), len(processed_locations)

if __name__ == "__main__":
    crimes_count, locations_count = process_london_crime_data()
    print(f"\nDatabase updated with {crimes_count} crimes across {locations_count} locations")