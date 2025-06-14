"""
Simple Data Collection Script for London Crime Analysis
Uses only standard library modules to fetch crime data from police.uk API
"""

import requests
import json
import csv
from datetime import datetime, timedelta
import time
import os

def fetch_london_crimes():
    """Fetch real London crime data from police.uk API"""
    print("Fetching London crime data from police.uk API...")
    
    # Key London coordinates
    london_locations = [
        {'name': 'Westminster', 'lat': 51.4975, 'lng': -0.1357},
        {'name': 'Camden', 'lat': 51.5290, 'lng': -0.1255},
        {'name': 'Tower Hamlets', 'lat': 51.5099, 'lng': -0.0059},
        {'name': 'Southwark', 'lat': 51.5024, 'lng': -0.0967},
        {'name': 'City of London', 'lat': 51.5156, 'lng': -0.0919},
    ]
    
    all_crimes = []
    base_url = "https://data.police.uk/api"
    
    # Get last 3 months of data
    end_date = datetime.now()
    dates = []
    for i in range(3):
        date = end_date - timedelta(days=30 * i)
        dates.append(date.strftime('%Y-%m'))
    
    print(f"Collecting data for dates: {dates}")
    
    for location in london_locations:
        print(f"\nFetching crimes for {location['name']}...")
        
        for date in dates:
            try:
                url = f"{base_url}/crimes-street/all-crime"
                params = {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'date': date
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    crimes = response.json()
                    
                    for crime in crimes:
                        crime['collection_location'] = location['name']
                        crime['collection_date'] = date
                        all_crimes.append(crime)
                    
                    print(f"  {date}: {len(crimes)} crimes")
                else:
                    print(f"  {date}: API error {response.status_code}")
                
                time.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                print(f"  {date}: Error - {str(e)}")
                continue
    
    print(f"\nTotal crimes collected: {len(all_crimes)}")
    
    # Save to CSV
    if all_crimes:
        os.makedirs('collected_data', exist_ok=True)
        
        # Write CSV
        csv_file = 'collected_data/london_crimes.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if all_crimes:
                fieldnames = all_crimes[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_crimes)
        
        print(f"Data saved to {csv_file}")
        
        # Write summary
        summary = {
            'total_records': len(all_crimes),
            'collection_date': datetime.now().isoformat(),
            'locations': [loc['name'] for loc in london_locations],
            'date_range': dates,
            'source': 'police.uk API'
        }
        
        with open('collected_data/summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("Collection summary saved")
        
        # Print sample data
        if all_crimes:
            print("\nSample crime record:")
            sample = all_crimes[0]
            for key, value in sample.items():
                print(f"  {key}: {value}")
    
    return all_crimes

if __name__ == "__main__":
    crimes = fetch_london_crimes()
    print(f"\nData collection complete! Collected {len(crimes)} records.")