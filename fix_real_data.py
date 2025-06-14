"""
Simple fix to load real London crime data with proper location parsing
"""

import sqlite3
import csv
import re
from datetime import datetime

def parse_location_string(location_str):
    """Parse the location string using regex instead of JSON"""
    try:
        # Extract latitude using regex
        lat_match = re.search(r"'latitude': '([^']+)'", location_str)
        lng_match = re.search(r"'longitude': '([^']+)'", location_str)
        name_match = re.search(r"'name': '([^']+)'", location_str)
        
        if lat_match and lng_match:
            lat = float(lat_match.group(1))
            lng = float(lng_match.group(1))
            street_name = name_match.group(1) if name_match else 'Unknown Street'
            return lat, lng, street_name
        else:
            return None, None, None
    except:
        return None, None, None

def quick_load_data():
    """Quick load of real data with minimal processing"""
    conn = sqlite3.connect('london_crime_analysis.db')
    cursor = conn.cursor()
    
    print("Loading real London crime data (simplified)...")
    
    # Read CSV and count valid records
    valid_crimes = 0
    location_cache = {}
    location_id = 1
    
    with open('collected_data/london_crimes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for crime in reader:
            try:
                # Parse location
                lat, lng, street_name = parse_location_string(crime['location'])
                if lat is None or lng is None:
                    continue
                
                # Get borough mapping
                borough_mapping = {
                    'Westminster': 1,
                    'Camden': 2, 
                    'Tower Hamlets': 4,
                    'Southwark': 5,
                    'City of London': 1  # Group with Westminster
                }
                
                city_id = borough_mapping.get(crime['collection_location'], 1)
                
                # Create location if not exists
                loc_key = f"{lat:.5f},{lng:.5f}"
                if loc_key not in location_cache:
                    cursor.execute('''
                        INSERT INTO locations (street_name, latitude, longitude, city_id, location_type)
                        VALUES (?, ?, ?, ?, 'Street')
                    ''', (street_name, lat, lng, city_id))
                    location_cache[loc_key] = location_id
                    location_id += 1
                else:
                    cursor.execute('SELECT location_id FROM locations WHERE street_name = ? AND latitude = ? AND longitude = ?',
                                 (street_name, lat, lng))
                    result = cursor.fetchone()
                    if result:
                        location_cache[loc_key] = result[0]
                
                # Map crime category
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
                    'other-theft': 6,
                    'possession-of-weapons': 5,
                    'other-crime': 1,
                    'bicycle-theft': 4
                }
                category_id = category_mapping.get(crime['category'], 1)
                
                # Parse date
                crime_date = datetime.strptime(crime['month'], '%Y-%m').date()
                
                # Insert crime (use OR IGNORE to handle duplicates)
                cursor.execute('''
                    INSERT OR IGNORE INTO crime_incidents 
                    (crime_id, category_id, location_id, force_id, incident_date, month_reported, status)
                    VALUES (?, ?, ?, 'metropolitan', ?, ?, 'Open')
                ''', (
                    f"REAL-{crime['id']}-{valid_crimes}",  # Make unique
                    category_id,
                    location_cache[loc_key],
                    crime_date,
                    crime['month']
                ))
                
                valid_crimes += 1
                
                if valid_crimes % 1000 == 0:
                    print(f"Processed {valid_crimes} crimes...")
                    conn.commit()
                
            except Exception as e:
                continue
    
    conn.commit()
    
    # Get final counts
    cursor.execute('SELECT COUNT(*) FROM crime_incidents')
    total_crimes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM locations')
    total_locations = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\nData loaded successfully!")
    print(f"- {total_crimes} crime incidents")
    print(f"- {total_locations} unique locations")
    print(f"- {valid_crimes} valid crimes processed")
    
    return total_crimes

if __name__ == "__main__":
    total = quick_load_data()
    print(f"\nDatabase ready with {total} real London crime records!")