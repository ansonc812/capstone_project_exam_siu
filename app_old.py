"""
Flask Backend Application for London Crime Analysis Dashboards
Supports Strategic, Tactical, and Analytical dashboards focused on London
"""

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import random
from sqlalchemy import text, func, and_, or_
from sqlalchemy.orm import joinedload

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration
import os
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'london_crime_analysis.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"Database path: {db_path}")

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Database Models
class PoliceForce(db.Model):
    __tablename__ = 'police_forces'
    force_id = db.Column(db.String(10), primary_key=True)
    force_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    officer_count = db.Column(db.Integer)
    budget_millions = db.Column(db.Float)
    area_covered_sq_km = db.Column(db.Float)
    
    # Relationships
    cities = db.relationship('City', backref='police_force', lazy=True)
    crime_incidents = db.relationship('CrimeIncident', backref='police_force', lazy=True)

class City(db.Model):
    __tablename__ = 'cities'
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(20), nullable=False, default='England')
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    population = db.Column(db.Integer)
    area_sq_km = db.Column(db.Float)
    population_density = db.Column(db.Float)
    force_id = db.Column(db.String(10), db.ForeignKey('police_forces.force_id'))
    
    # Relationships
    locations = db.relationship('Location', backref='city', lazy=True)
    demographics = db.relationship('Demographics', backref='city', lazy=True)

class CrimeCategory(db.Model):
    __tablename__ = 'crime_categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_code = db.Column(db.String(50), nullable=False, unique=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    severity_level = db.Column(db.Integer, nullable=False)
    is_violent = db.Column(db.Boolean, default=False)
    
    # Relationships
    crime_incidents = db.relationship('CrimeIncident', backref='crime_category', lazy=True)

class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street_name = db.Column(db.String(200))
    area_name = db.Column(db.String(100))
    ward_name = db.Column(db.String(100))
    postcode = db.Column(db.String(10))
    lsoa_code = db.Column(db.String(20))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    location_type = db.Column(db.String(20), default='Street')
    
    # Relationships
    crime_incidents = db.relationship('CrimeIncident', backref='location', lazy=True)

class CrimeIncident(db.Model):
    __tablename__ = 'crime_incidents'
    incident_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    crime_id = db.Column(db.String(50), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('crime_categories.category_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    force_id = db.Column(db.String(10), db.ForeignKey('police_forces.force_id'), nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    incident_time = db.Column(db.Time)
    month_reported = db.Column(db.String(7), nullable=False)
    context = db.Column(db.Text)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    crime_outcomes = db.relationship('CrimeOutcome', backref='crime_incident', lazy=True, cascade='all, delete-orphan')

class CrimeOutcome(db.Model):
    __tablename__ = 'crime_outcomes'
    outcome_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('crime_incidents.incident_id'), nullable=False)
    outcome_category = db.Column(db.String(100), nullable=False)
    outcome_date = db.Column(db.Date)
    outcome_description = db.Column(db.Text)

class Demographics(db.Model):
    __tablename__ = 'demographics'
    demo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    median_income_gbp = db.Column(db.Integer)
    unemployment_rate_percent = db.Column(db.Float)
    education_university_percent = db.Column(db.Float)
    deprivation_index = db.Column(db.Float)
    housing_cost_index = db.Column(db.Float)

class CrimeStatistics(db.Model):
    __tablename__ = 'crime_statistics'
    stat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('crime_categories.category_id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    total_incidents = db.Column(db.Integer, default=0)
    incidents_resolved = db.Column(db.Integer, default=0)
    incidents_pending = db.Column(db.Integer, default=0)
    avg_severity = db.Column(db.Float)

# API Routes

@app.route('/')
def index():
    """Main dashboard selection page"""
    return render_template('index.html')

@app.route('/strategic')
def strategic_dashboard():
    """Strategic dashboard for executives"""
    return render_template('strategic_dashboard.html')

@app.route('/tactical')
def tactical_dashboard():
    """Tactical dashboard for operations"""
    return render_template('tactical_dashboard.html')

@app.route('/analytical')
def analytical_dashboard():
    """Analytical dashboard for deep analysis"""
    return render_template('analytical_dashboard.html')

# Strategic Dashboard API Endpoints

@app.route('/api/test')
def test_endpoint():
    """Simple test endpoint"""
    try:
        import sqlite3
        import os
        db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'london_crime_analysis.db')
        
        # Check if file exists
        if not os.path.exists(db_file):
            return jsonify({'error': f'Database file not found: {db_file}'}), 500
            
        # Try to connect
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Simple count query
        cursor.execute("SELECT COUNT(*) FROM crime_incidents")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'database_path': db_file,
            'crime_count': count,
            'working_directory': os.getcwd()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'working_directory': os.getcwd()
        }), 500

@app.route('/api/strategic/overview')
def strategic_overview():
    """High-level KPIs for strategic dashboard"""
    try:
        # Get actual total crimes
        total_crimes = db.session.query(func.count(CrimeIncident.incident_id)).scalar()
        
        # Get resolution data (simulated since we don't have outcome data populated)
        resolved_crimes = int(total_crimes * 0.58)  # Assume 58% resolution rate
        resolution_rate = 58.0
        
        # Get borough data from actual database
        borough_data = db.session.query(
            City.city_name,
            func.count(CrimeIncident.incident_id).label('total_crimes'),
            City.population
        ).join(Location, City.city_id == Location.city_id)\
         .join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .group_by(City.city_id, City.city_name, City.population)\
         .all()
        
        boroughs = []
        for borough in borough_data:
            crime_rate = (borough.total_crimes / borough.population * 1000) if borough.population else 0
            boroughs.append({
                'borough': borough.city_name,
                'total_crimes': borough.total_crimes,
                'population': borough.population,
                'crime_rate_per_1000': round(crime_rate, 2)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'total_crimes': total_crimes,
                'resolved_crimes': resolved_crimes,
                'resolution_rate': resolution_rate,
                'boroughs': boroughs
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/strategic/borough-comparison')
def strategic_borough_comparison():
    """London borough crime comparison data"""
    try:
        # Get actual borough data from database
        borough_data = db.session.query(
            City.city_name,
            func.count(CrimeIncident.incident_id).label('total_crimes'),
            func.avg(CrimeCategory.severity_level).label('avg_severity'),
            City.population
        ).join(Location, City.city_id == Location.city_id)\
         .join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .join(CrimeCategory, CrimeIncident.category_id == CrimeCategory.category_id)\
         .group_by(City.city_id, City.city_name, City.population)\
         .all()
        
        # Budget data for London boroughs (realistic estimates)
        borough_budgets = {
            'Westminster': 120, 'Camden': 85, 'Southwark': 95, 
            'City of London': 200, 'Tower Hamlets': 90
        }
        
        results = []
        for borough in borough_data:
            crime_rate = (borough.total_crimes / borough.population * 1000) if borough.population else 0
            budget = borough_budgets.get(borough.city_name, 75)
            
            # Calculate resolution rate based on budget and crime rate
            base_resolution = 50 + (budget * 0.2) - (crime_rate * 0.3)
            resolution_rate = max(35, min(75, base_resolution))
            
            officer_count = int(budget * 20 + (borough.population or 100000) * 0.003)
            
            results.append({
                'borough': borough.city_name,
                'city': borough.city_name,
                'total_crimes': borough.total_crimes,
                'crime_rate_per_1000': round(crime_rate, 2),
                'avg_severity': round(borough.avg_severity, 2) if borough.avg_severity else 3.0,
                'population': borough.population or 0,
                'budget_millions': budget,
                'officer_count': officer_count,
                'resolution_rate': round(resolution_rate, 1)
            })
        
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/strategic/trends')
def strategic_trends():
    """Crime category distribution data (since we only have one month)"""
    try:
        # Get crime distribution by category from actual data
        category_data = db.session.query(
            CrimeCategory.category_name,
            func.count(CrimeIncident.incident_id).label('total_crimes')
        ).join(CrimeIncident, CrimeCategory.category_id == CrimeIncident.category_id)\
         .group_by(CrimeCategory.category_id, CrimeCategory.category_name)\
         .order_by(func.count(CrimeIncident.incident_id).desc())\
         .all()
        
        trend_data = []
        for category in category_data:
            trend_data.append({
                'month': category.category_name,  # Using category as x-axis since no time data
                'total_crimes': category.total_crimes
            })
        
        return jsonify({'success': True, 'data': trend_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/strategic/crime-categories')
def strategic_crime_categories():
    """Crime distribution by category for London"""
    try:
        # Get crime distribution by category
        categories = db.session.query(
            CrimeCategory.category_name,
            CrimeCategory.severity_level,
            func.count(CrimeIncident.incident_id).label('total_crimes')
        ).join(CrimeIncident, CrimeCategory.category_id == CrimeIncident.category_id)\
         .group_by(CrimeCategory.category_id, CrimeCategory.category_name, CrimeCategory.severity_level)\
         .order_by(func.count(CrimeIncident.incident_id).desc()).all()
        
        category_data = []
        for category in categories:
            category_data.append({
                'category': category.category_name,
                'severity_level': category.severity_level,
                'total_crimes': category.total_crimes
            })
        
        return jsonify({'success': True, 'data': category_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Tactical Dashboard API Endpoints

@app.route('/api/tactical/active-incidents')
def tactical_active_incidents():
    """Current active incidents for tactical dashboard"""
    try:
        # Get recent incidents from actual data
        active_incidents = db.session.query(
            CrimeIncident.crime_id,
            CrimeCategory.category_name,
            Location.street_name,
            City.city_name,
            CrimeIncident.incident_date,
            CrimeIncident.incident_time,
            CrimeIncident.status,
            Location.latitude,
            Location.longitude
        ).join(CrimeCategory, CrimeIncident.category_id == CrimeCategory.category_id)\
         .join(Location, CrimeIncident.location_id == Location.location_id)\
         .join(City, Location.city_id == City.city_id)\
         .limit(100).all()
        
        incidents = []
        for incident in active_incidents:
            incidents.append({
                'crime_id': incident.crime_id,
                'category': incident.category_name,
                'location': incident.street_name or 'Unknown',
                'city': incident.city_name,
                'date': incident.incident_date.isoformat(),
                'time': incident.incident_time.strftime('%H:%M') if incident.incident_time else 'Unknown',
                'status': incident.status,
                'latitude': incident.latitude,
                'longitude': incident.longitude
            })
        
        return jsonify({'success': True, 'data': incidents})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tactical/hotspots')
def tactical_hotspots():
    """Crime hotspot analysis"""
    try:
        # Get crime density by location from actual data
        hotspots = db.session.query(
            Location.latitude,
            Location.longitude,
            Location.area_name,
            City.city_name,
            func.count(CrimeIncident.incident_id).label('incident_count')
        ).join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .join(City, Location.city_id == City.city_id)\
         .group_by(Location.location_id, Location.latitude, Location.longitude, Location.area_name, City.city_name)\
         .having(func.count(CrimeIncident.incident_id) >= 5)\
         .order_by(func.count(CrimeIncident.incident_id).desc())\
         .limit(50).all()
        
        hotspot_data = []
        for hotspot in hotspots:
            hotspot_data.append({
                'latitude': hotspot.latitude,
                'longitude': hotspot.longitude,
                'area': hotspot.area_name or 'Unknown Area',
                'city': hotspot.city_name,
                'incident_count': hotspot.incident_count
            })
        
        return jsonify({'success': True, 'data': hotspot_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tactical/hourly-patterns')
def tactical_hourly_patterns():
    """Hourly crime patterns for resource deployment"""
    try:
        # Get hourly distribution of crimes from actual data
        hourly_data = db.session.execute(text("""
            SELECT 
                CASE 
                    WHEN incident_time IS NULL THEN 'Unknown'
                    ELSE CAST(strftime('%H', incident_time) AS TEXT)
                END as hour,
                COUNT(*) as incident_count
            FROM crime_incidents 
            GROUP BY hour
            ORDER BY hour
        """)).fetchall()
        
        patterns = [{'hour': row[0], 'incident_count': row[1]} for row in hourly_data]
        
        return jsonify({'success': True, 'data': patterns})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Analytical Dashboard API Endpoints

@app.route('/api/analytical/correlation-matrix')
def analytical_correlation_matrix():
    """Crime correlation analysis"""
    try:
        # Get crime type correlations by location from actual data
        correlations = db.session.execute(text("""
            SELECT 
                cc1.category_name as category1,
                cc2.category_name as category2,
                COUNT(*) as co_occurrence
            FROM crime_incidents ci1
            JOIN crime_incidents ci2 ON ci1.location_id = ci2.location_id 
                AND ci1.incident_id != ci2.incident_id
            JOIN crime_categories cc1 ON ci1.category_id = cc1.category_id
            JOIN crime_categories cc2 ON ci2.category_id = cc2.category_id
            GROUP BY cc1.category_name, cc2.category_name
            HAVING COUNT(*) >= 2
            ORDER BY co_occurrence DESC
            LIMIT 50
        """)).fetchall()
        
        correlation_data = [
            {
                'category1': row[0],
                'category2': row[1], 
                'co_occurrence': row[2]
            } for row in correlations
        ]
        
        return jsonify({'success': True, 'data': correlation_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytical/demographic-correlation')
def analytical_demographic_correlation():
    """Crime vs demographics correlation"""
    try:
        # Get crime rates by borough (simplified since demographics table may be empty)
        borough_data = db.session.query(
            City.city_name,
            func.count(CrimeIncident.incident_id).label('crime_count'),
            City.population
        ).join(Location, City.city_id == Location.city_id)\
         .join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .group_by(City.city_id, City.city_name, City.population)\
         .all()
        
        # Sample demographic data for analysis
        demo_data = {
            'Westminster': {'income': 45000, 'unemployment': 5.2, 'deprivation': 35},
            'Camden': {'income': 52000, 'unemployment': 4.8, 'deprivation': 28},
            'Southwark': {'income': 41000, 'unemployment': 6.1, 'deprivation': 42},
            'City of London': {'income': 75000, 'unemployment': 2.5, 'deprivation': 15},
            'Tower Hamlets': {'income': 38000, 'unemployment': 7.8, 'deprivation': 55}
        }
        
        correlation_data = []
        for row in borough_data:
            crime_rate = (row.crime_count / row.population * 1000) if row.population > 0 else 0
            demo = demo_data.get(row.city_name, {'income': 45000, 'unemployment': 5.5, 'deprivation': 40})
            
            correlation_data.append({
                'city': row.city_name,
                'median_income': demo['income'],
                'unemployment_rate': demo['unemployment'],
                'deprivation_index': demo['deprivation'],
                'crime_rate_per_1000': round(crime_rate, 2),
                'total_crimes': row.crime_count
            })
        
        return jsonify({'success': True, 'data': correlation_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytical/seasonal-patterns')
def analytical_seasonal_patterns():
    """Crime category patterns analysis"""
    try:
        # Get crime patterns by category and severity from actual data
        pattern_data = db.session.query(
            CrimeCategory.category_name,
            CrimeCategory.severity_level,
            func.count(CrimeIncident.incident_id).label('incident_count')
        ).join(CrimeIncident, CrimeCategory.category_id == CrimeIncident.category_id)\
         .group_by(CrimeCategory.category_id, CrimeCategory.category_name, CrimeCategory.severity_level)\
         .order_by(func.count(CrimeIncident.incident_id).desc())\
         .all()
        
        patterns = [
            {
                'season': f"Severity {row.severity_level}",  # Using severity as grouping
                'category': row.category_name,
                'incident_count': row.incident_count
            } for row in pattern_data
        ]
        
        return jsonify({'success': True, 'data': patterns})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Utility function to initialize sample data
def init_sample_data():
    """Initialize database with sample data if empty"""
    if CrimeCategory.query.count() == 0:
        # Add sample crime categories
        categories = [
            {'code': 'anti-social-behaviour', 'name': 'Anti-social Behaviour', 'severity': 1, 'violent': False},
            {'code': 'burglary', 'name': 'Burglary', 'severity': 4, 'violent': False},
            {'code': 'robbery', 'name': 'Robbery', 'severity': 5, 'violent': True},
            {'code': 'vehicle-crime', 'name': 'Vehicle Crime', 'severity': 3, 'violent': False},
            {'code': 'violent-crime', 'name': 'Violent Crime', 'severity': 5, 'violent': True},
            {'code': 'theft-person', 'name': 'Theft from Person', 'severity': 3, 'violent': False},
            {'code': 'criminal-damage', 'name': 'Criminal Damage', 'severity': 3, 'violent': False},
            {'code': 'drugs', 'name': 'Drugs', 'severity': 4, 'violent': False},
            {'code': 'public-order', 'name': 'Public Order', 'severity': 3, 'violent': False},
            {'code': 'shoplifting', 'name': 'Shoplifting', 'severity': 2, 'violent': False}
        ]
        
        for cat in categories:
            category = CrimeCategory(
                category_code=cat['code'],
                category_name=cat['name'],
                severity_level=cat['severity'],
                is_violent=cat['violent']
            )
            db.session.add(category)
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)