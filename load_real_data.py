"""
Load real London crime data directly into SQLite database
Uses the 12,186 real crime records from police.uk API
"""

import sqlite3
import csv
import json
from datetime import datetime

def create_database_schema():
    """Create the database schema"""
    conn = sqlite3.connect('london_crime_analysis.db')
    cursor = conn.cursor()
    
    # Create tables based on app.py models
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS police_forces (
            force_id TEXT PRIMARY KEY,
            force_name TEXT NOT NULL,
            region TEXT NOT NULL,
            officer_count INTEGER,
            budget_millions REAL,
            area_covered_sq_km REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL,
            region TEXT NOT NULL,
            country TEXT NOT NULL DEFAULT 'England',
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            population INTEGER,
            area_sq_km REAL,
            population_density REAL,
            force_id TEXT,
            FOREIGN KEY (force_id) REFERENCES police_forces (force_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crime_categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_code TEXT NOT NULL UNIQUE,
            category_name TEXT NOT NULL,
            description TEXT,
            severity_level INTEGER NOT NULL,
            is_violent BOOLEAN DEFAULT FALSE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            street_name TEXT,
            area_name TEXT,
            ward_name TEXT,
            postcode TEXT,
            lsoa_code TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            city_id INTEGER,
            location_type TEXT DEFAULT 'Street',
            FOREIGN KEY (city_id) REFERENCES cities (city_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crime_incidents (
            incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
            crime_id TEXT NOT NULL UNIQUE,
            category_id INTEGER NOT NULL,
            location_id INTEGER NOT NULL,
            force_id TEXT NOT NULL,
            incident_date DATE NOT NULL,
            incident_time TIME,
            month_reported TEXT NOT NULL,
            context TEXT,
            status TEXT DEFAULT 'Open',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES crime_categories (category_id),
            FOREIGN KEY (location_id) REFERENCES locations (location_id),
            FOREIGN KEY (force_id) REFERENCES police_forces (force_id)
        )
    ''')
    
    conn.commit()
    return conn

def load_reference_data(conn):
    """Load police forces, boroughs, and crime categories"""
    cursor = conn.cursor()
    
    # Add Metropolitan Police
    cursor.execute('''
        INSERT OR REPLACE INTO police_forces 
        (force_id, force_name, region, officer_count, budget_millions, area_covered_sq_km)
        VALUES ('metropolitan', 'Metropolitan Police Service', 'London', 31000, 3200.0, 1572.0)
    ''')
    
    # Add London boroughs based on our data collection areas
    boroughs = [
        ('Westminster', 51.4975, -0.1357, 261000),
        ('Camden', 51.5290, -0.1255, 270000),
        ('Tower Hamlets', 51.5099, -0.0059, 324000),
        ('Southwark', 51.5024, -0.0967, 318000),
        ('City of London', 51.5156, -0.0919, 9000)
    ]
    
    for name, lat, lng, pop in boroughs:
        cursor.execute('''
            INSERT OR REPLACE INTO cities 
            (city_name, region, country, latitude, longitude, population, force_id)
            VALUES (?, 'London', 'England', ?, ?, ?, 'metropolitan')
        ''', (name, lat, lng, pop))
    
    # Add crime categories based on real API data
    categories = [
        ('anti-social-behaviour', 'Anti-social Behaviour', 'Behaviour that causes harassment, alarm or distress', 2, False),
        ('burglary', 'Burglary', 'Illegal entry with intent to commit theft', 4, False),
        ('robbery', 'Robbery', 'Theft involving force or threat of force', 5, True),
        ('vehicle-crime', 'Vehicle Crime', 'Theft of or from vehicles', 3, False),
        ('violent-crime', 'Violent Crime', 'Offences against the person involving violence', 5, True),
        ('theft-from-the-person', 'Theft from Person', 'Theft directly from a person', 3, False),
        ('criminal-damage-arson', 'Criminal Damage & Arson', 'Intentional damage to property', 3, False),
        ('drugs', 'Drugs', 'Drug-related offences', 4, False),
        ('public-order', 'Public Order', 'Offences affecting public peace', 3, False),
        ('shoplifting', 'Shoplifting', 'Theft from retail premises', 2, False),
        ('other-theft', 'Other Theft', 'Theft not covered by other categories', 3, False),
        ('possession-of-weapons', 'Possession of Weapons', 'Illegal possession of weapons', 4, True),
        ('other-crime', 'Other Crime', 'Crimes not covered by other categories', 2, False),
        ('bicycle-theft', 'Bicycle Theft', 'Theft of bicycles', 2, False)
    ]
    
    for code, name, desc, severity, violent in categories:
        cursor.execute('''
            INSERT OR REPLACE INTO crime_categories 
            (category_code, category_name, description, severity_level, is_violent)
            VALUES (?, ?, ?, ?, ?)
        ''', (code, name, desc, severity, violent))
    
    conn.commit()
    print("Reference data loaded successfully")

def load_crime_data(conn):
    """Load the real crime data from CSV"""
    cursor = conn.cursor()
    
    # Read the real crime data
    with open('collected_data/london_crimes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        crimes = list(reader)
    
    print(f"Loading {len(crimes)} real crime records...")
    
    # Process locations and crimes
    location_cache = {}
    crimes_loaded = 0
    
    for crime in crimes:
        try:
            # Parse location data
            location_str = crime['location']
            if location_str.startswith("{'") or location_str.startswith('{"'):
                # Parse the location dictionary
                location_str = location_str.replace("'", '"')
                location_data = json.loads(location_str)
                
                lat = float(location_data['latitude'])
                lng = float(location_data['longitude']) 
                street_info = location_data.get('street', {})
                street_name = street_info.get('name', 'Unknown Street')
            else:
                continue  # Skip malformed location data
            
            # Determine borough
            borough_id = get_borough_id(cursor, lat, lng, crime['collection_location'])
            if not borough_id:
                continue
            
            # Create location key
            loc_key = f"{lat:.6f},{lng:.6f}"
            
            if loc_key not in location_cache:
                # Insert location
                cursor.execute('''
                    INSERT INTO locations (street_name, latitude, longitude, city_id, location_type)
                    VALUES (?, ?, ?, ?, 'Street')
                ''', (street_name, lat, lng, borough_id))
                
                location_id = cursor.lastrowid
                location_cache[loc_key] = location_id
            else:
                location_id = location_cache[loc_key]
            
            # Get category ID
            cursor.execute('SELECT category_id FROM crime_categories WHERE category_code = ?', 
                         (crime['category'],))
            category_result = cursor.fetchone()
            if not category_result:
                continue
            category_id = category_result[0]
            
            # Parse date
            crime_date = datetime.strptime(crime['month'], '%Y-%m').date()
            
            # Determine status
            status = 'Closed' if crime.get('outcome_status') and crime['outcome_status'] != 'None' else 'Open'
            
            # Insert crime
            cursor.execute('''
                INSERT INTO crime_incidents 
                (crime_id, category_id, location_id, force_id, incident_date, month_reported, context, status)
                VALUES (?, ?, ?, 'metropolitan', ?, ?, ?, ?)
            ''', (
                f"REAL-{crime['id']}", 
                category_id, 
                location_id, 
                crime_date,
                crime['month'],
                crime.get('context', ''),
                status
            ))
            
            crimes_loaded += 1
            
        except Exception as e:
            print(f"Error processing crime: {e}")
            continue
    
    conn.commit()
    print(f"Successfully loaded {crimes_loaded} real crime records")
    return crimes_loaded

def get_borough_id(cursor, lat, lng, collection_location):
    """Get borough ID based on coordinates or collection location"""
    # First try to match by collection location name
    cursor.execute('SELECT city_id FROM cities WHERE city_name = ?', (collection_location,))
    result = cursor.fetchone()
    if result:
        return result[0]
    
    # Fallback to coordinate-based matching
    cursor.execute('SELECT city_id FROM cities ORDER BY ((latitude - ?) * (latitude - ?) + (longitude - ?) * (longitude - ?)) LIMIT 1', 
                  (lat, lat, lng, lng))
    result = cursor.fetchone()
    return result[0] if result else None

def main():
    """Main function to load all real data"""
    print("Loading real London crime data into database...")
    
    # Create database and schema
    conn = create_database_schema()
    print("Database schema created")
    
    # Load reference data
    load_reference_data(conn)
    
    # Load real crime data
    crimes_count = load_crime_data(conn)
    
    # Get summary statistics
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM crime_incidents')
    total_crimes = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM locations')
    total_locations = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT city_id) FROM locations')
    total_boroughs = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"\nDatabase loaded successfully!")
    print(f"- {total_crimes} real crime incidents")
    print(f"- {total_locations} unique locations")
    print(f"- {total_boroughs} London boroughs")
    print("Ready to run dashboard!")

if __name__ == "__main__":
    main()