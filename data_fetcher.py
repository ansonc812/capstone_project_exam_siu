"""
Data Collection Script for London Crime Analysis
Fetches real crime data from police.uk API and other sources
"""

import requests
import json
import csv
import pandas as pd
from datetime import datetime, timedelta
import time
import os

class LondonCrimeDataFetcher:
    def __init__(self):
        self.base_url = "https://data.police.uk/api"
        self.london_forces = ['metropolitan', 'city-of-london']
        self.data_dir = "collected_data"
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_police_forces(self):
        """Get all police forces to identify London forces"""
        try:
            response = requests.get(f"{self.base_url}/forces")
            forces = response.json()
            
            london_forces = []
            for force in forces:
                if 'metropolitan' in force['id'].lower() or 'city-of-london' in force['id'].lower():
                    london_forces.append(force)
            
            print(f"Found {len(london_forces)} London police forces:")
            for force in london_forces:
                print(f"- {force['name']} ({force['id']})")
            
            return london_forces
        except Exception as e:
            print(f"Error fetching police forces: {e}")
            return []
    
    def get_neighbourhoods(self, force_id):
        """Get neighbourhoods for a specific police force"""
        try:
            response = requests.get(f"{self.base_url}/{force_id}/neighbourhoods")
            neighbourhoods = response.json()
            print(f"Found {len(neighbourhoods)} neighbourhoods for {force_id}")
            return neighbourhoods
        except Exception as e:
            print(f"Error fetching neighbourhoods for {force_id}: {e}")
            return []
    
    def get_neighbourhood_boundary(self, force_id, neighbourhood_id):
        """Get boundary coordinates for a neighbourhood"""
        try:
            response = requests.get(f"{self.base_url}/{force_id}/{neighbourhood_id}/boundary")
            boundary = response.json()
            return boundary
        except Exception as e:
            print(f"Error fetching boundary for {neighbourhood_id}: {e}")
            return []
    
    def get_crimes_at_location(self, lat, lng, date=None):
        """Get crimes at a specific location"""
        try:
            url = f"{self.base_url}/crimes-at-location"
            params = {
                'lat': lat,
                'lng': lng
            }
            if date:
                params['date'] = date
            
            response = requests.get(url, params=params)
            crimes = response.json()
            return crimes
        except Exception as e:
            print(f"Error fetching crimes at location {lat},{lng}: {e}")
            return []
    
    def get_street_crimes(self, lat, lng, date=None):
        """Get street-level crimes near a location"""
        try:
            url = f"{self.base_url}/crimes-street/all-crime"
            params = {
                'lat': lat,
                'lng': lng
            }
            if date:
                params['date'] = date
            
            response = requests.get(url, params=params)
            crimes = response.json()
            return crimes
        except Exception as e:
            print(f"Error fetching street crimes near {lat},{lng}: {e}")
            return []
    
    def collect_london_crime_data(self, months_back=6):
        """Collect comprehensive London crime data"""
        print("Starting London crime data collection...")
        
        # Key London locations (central areas)
        london_locations = [
            {'name': 'Westminster', 'lat': 51.4975, 'lng': -0.1357},
            {'name': 'Camden', 'lat': 51.5290, 'lng': -0.1255},
            {'name': 'Islington', 'lat': 51.5362, 'lng': -0.1033},
            {'name': 'Tower Hamlets', 'lat': 51.5099, 'lng': -0.0059},
            {'name': 'Southwark', 'lat': 51.5024, 'lng': -0.0967},
            {'name': 'Lambeth', 'lat': 51.4607, 'lng': -0.1163},
            {'name': 'Hackney', 'lat': 51.5450, 'lng': -0.0553},
            {'name': 'Greenwich', 'lat': 51.4892, 'lng': 0.0648},
            {'name': 'Lewisham', 'lat': 51.4611, 'lng': -0.0185},
            {'name': 'Newham', 'lat': 51.5077, 'lng': 0.0469},
            {'name': 'City of London', 'lat': 51.5156, 'lng': -0.0919},
            {'name': 'Kensington and Chelsea', 'lat': 51.4991, 'lng': -0.1938},
        ]
        
        all_crimes = []
        
        # Generate date range
        end_date = datetime.now()
        dates = []
        for i in range(months_back):
            date = end_date - timedelta(days=30 * i)
            dates.append(date.strftime('%Y-%m'))
        
        print(f"Collecting data for dates: {dates}")
        
        for location in london_locations:
            print(f"\nCollecting data for {location['name']}...")
            
            for date in dates:
                try:
                    # Get street crimes
                    crimes = self.get_street_crimes(location['lat'], location['lng'], date)
                    
                    for crime in crimes:
                        crime['collection_location'] = location['name']
                        crime['collection_date'] = date
                        all_crimes.append(crime)
                    
                    print(f"  {date}: {len(crimes)} crimes found")
                    time.sleep(0.5)  # Rate limiting
                    
                except Exception as e:
                    print(f"  Error for {date}: {e}")
                    continue
        
        print(f"\nTotal crimes collected: {len(all_crimes)}")
        
        # Save to CSV
        if all_crimes:
            df = pd.DataFrame(all_crimes)
            csv_file = os.path.join(self.data_dir, 'london_crimes_raw.csv')
            df.to_csv(csv_file, index=False)
            print(f"Data saved to {csv_file}")
            
            # Save summary
            summary = {
                'total_records': len(all_crimes),
                'collection_date': datetime.now().isoformat(),
                'locations_covered': [loc['name'] for loc in london_locations],
                'date_range': dates,
                'unique_categories': list(df['category'].unique()) if 'category' in df.columns else [],
                'data_sources': ['police.uk API']
            }
            
            summary_file = os.path.join(self.data_dir, 'collection_summary.json')
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            print(f"Summary saved to {summary_file}")
        
        return all_crimes
    
    def download_bulk_data(self):
        """Download bulk crime data from police.uk"""
        print("Downloading latest bulk crime data...")
        
        try:
            # Download latest archive
            archive_url = "https://data.police.uk/data/archive/latest.zip"
            response = requests.get(archive_url, stream=True)
            
            if response.status_code == 200:
                zip_file = os.path.join(self.data_dir, 'latest_crime_data.zip')
                with open(zip_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Bulk data downloaded to {zip_file}")
                return zip_file
            else:
                print(f"Failed to download bulk data: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error downloading bulk data: {e}")
            return None

def main():
    """Main function to collect London crime data"""
    fetcher = LondonCrimeDataFetcher()
    
    print("London Crime Data Collection")
    print("=" * 40)
    
    # Get police forces info
    forces = fetcher.get_police_forces()
    
    # Collect street-level crime data
    crimes = fetcher.collect_london_crime_data(months_back=12)
    
    print(f"\nData collection complete!")
    print(f"Collected {len(crimes)} crime records")
    print(f"Data saved in '{fetcher.data_dir}' directory")

if __name__ == "__main__":
    main()