"""
Flask Backend Application for UK Crime Analysis Dashboards
Supports Strategic, Tactical, and Analytical dashboards
"""

from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from sqlalchemy import text, func, and_, or_
from sqlalchemy.orm import joinedload

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uk_crime_analysis.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/api/strategic/overview')
def strategic_overview():
    """High-level KPIs for strategic dashboard"""
    try:
        # Calculate key metrics
        total_crimes = db.session.query(func.count(CrimeIncident.incident_id)).scalar()
        resolved_crimes = db.session.query(func.count(CrimeIncident.incident_id)).filter(
            CrimeIncident.status == 'Closed'
        ).scalar()
        
        resolution_rate = (resolved_crimes / total_crimes * 100) if total_crimes > 0 else 0
        
        # Get regional breakdown
        regional_data = db.session.query(
            City.region,
            func.count(CrimeIncident.incident_id).label('total_crimes'),
            func.sum(City.population).label('total_population')
        ).join(Location, City.city_id == Location.city_id)\
         .join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .group_by(City.region).all()
        
        regions = []
        for region, crimes, population in regional_data:
            crime_rate = (crimes / population * 1000) if population > 0 else 0
            regions.append({
                'region': region,
                'total_crimes': crimes,
                'population': population,
                'crime_rate_per_1000': round(crime_rate, 2)
            })
        
        return jsonify({
            'success': True,
            'data': {
                'total_crimes': total_crimes,
                'resolved_crimes': resolved_crimes,
                'resolution_rate': round(resolution_rate, 2),
                'regions': regions
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/strategic/regional-comparison')
def strategic_regional_comparison():
    """Regional crime comparison data"""
    try:
        # Get data for last 12 months
        cutoff_date = datetime.now() - timedelta(days=365)
        
        query = db.session.query(
            City.city_name,
            City.region,
            PoliceForce.force_name,
            func.count(CrimeIncident.incident_id).label('total_crimes'),
            func.count(func.nullif(CrimeIncident.status == 'Closed', False)).label('resolved_crimes'),
            City.population,
            PoliceForce.budget_millions,
            PoliceForce.officer_count
        ).join(Location, City.city_id == Location.city_id)\
         .join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .join(PoliceForce, City.force_id == PoliceForce.force_id)\
         .filter(CrimeIncident.incident_date >= cutoff_date.date())\
         .group_by(City.city_id, City.city_name, City.region, PoliceForce.force_name, City.population, PoliceForce.budget_millions, PoliceForce.officer_count)\
         .all()
        
        results = []
        for row in query:
            resolution_rate = (row.resolved_crimes / row.total_crimes * 100) if row.total_crimes > 0 else 0
            crime_rate = (row.total_crimes / row.population * 1000) if row.population > 0 else 0
            
            results.append({
                'city': row.city_name,
                'region': row.region,
                'force': row.force_name,
                'total_crimes': row.total_crimes,
                'resolution_rate': round(resolution_rate, 2),
                'crime_rate_per_1000': round(crime_rate, 2),
                'budget_millions': row.budget_millions,
                'officer_count': row.officer_count
            })
        
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/strategic/trends')
def strategic_trends():
    """Crime trend data over time"""
    try:
        # Get monthly trends for last 24 months
        trends = db.session.query(
            CrimeIncident.month_reported,
            func.count(CrimeIncident.incident_id).label('total_crimes')
        ).filter(
            CrimeIncident.incident_date >= (datetime.now() - timedelta(days=730)).date()
        ).group_by(CrimeIncident.month_reported)\
         .order_by(CrimeIncident.month_reported).all()
        
        trend_data = [{'month': month, 'total_crimes': count} for month, count in trends]
        
        return jsonify({'success': True, 'data': trend_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Tactical Dashboard API Endpoints

@app.route('/api/tactical/active-incidents')
def tactical_active_incidents():
    """Current active incidents for tactical dashboard"""
    try:
        # Get incidents from last 7 days that are still active
        cutoff_date = datetime.now() - timedelta(days=7)
        
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
         .filter(
             and_(
                 CrimeIncident.incident_date >= cutoff_date.date(),
                 CrimeIncident.status.in_(['Open', 'Under Investigation'])
             )
         ).limit(100).all()
        
        incidents = []
        for incident in active_incidents:
            incidents.append({
                'crime_id': incident.crime_id,
                'category': incident.category_name,
                'location': incident.street_name,
                'city': incident.city_name,
                'date': incident.incident_date.isoformat(),
                'time': incident.incident_time.strftime('%H:%M') if incident.incident_time else None,
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
        # Get crime density by location for last 30 days
        cutoff_date = datetime.now() - timedelta(days=30)
        
        hotspots = db.session.query(
            Location.latitude,
            Location.longitude,
            Location.area_name,
            City.city_name,
            func.count(CrimeIncident.incident_id).label('incident_count')
        ).join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .join(City, Location.city_id == City.city_id)\
         .filter(CrimeIncident.incident_date >= cutoff_date.date())\
         .group_by(Location.location_id, Location.latitude, Location.longitude, Location.area_name, City.city_name)\
         .having(func.count(CrimeIncident.incident_id) >= 5)\
         .order_by(func.count(CrimeIncident.incident_id).desc())\
         .limit(50).all()
        
        hotspot_data = []
        for hotspot in hotspots:
            hotspot_data.append({
                'latitude': hotspot.latitude,
                'longitude': hotspot.longitude,
                'area': hotspot.area_name,
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
        # Get hourly distribution of crimes
        hourly_data = db.session.execute(text("""
            SELECT 
                CASE 
                    WHEN incident_time IS NULL THEN 'Unknown'
                    ELSE CAST(strftime('%H', incident_time) AS TEXT)
                END as hour,
                COUNT(*) as incident_count
            FROM crime_incidents 
            WHERE incident_date >= date('now', '-30 days')
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
        # Get crime type correlations by location
        correlations = db.session.execute(text("""
            SELECT 
                cc1.category_name as category1,
                cc2.category_name as category2,
                COUNT(*) as co_occurrence
            FROM crime_incidents ci1
            JOIN crime_incidents ci2 ON ci1.location_id = ci2.location_id 
                AND ci1.incident_id != ci2.incident_id
                AND DATE(ci1.incident_date) = DATE(ci2.incident_date)
            JOIN crime_categories cc1 ON ci1.category_id = cc1.category_id
            JOIN crime_categories cc2 ON ci2.category_id = cc2.category_id
            WHERE ci1.incident_date >= date('now', '-365 days')
            GROUP BY cc1.category_name, cc2.category_name
            HAVING COUNT(*) >= 5
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
        # Correlate crime rates with demographic factors
        correlations = db.session.query(
            City.city_name,
            Demographics.median_income_gbp,
            Demographics.unemployment_rate_percent,
            Demographics.deprivation_index,
            func.count(CrimeIncident.incident_id).label('crime_count'),
            City.population
        ).join(Location, City.city_id == Location.city_id)\
         .join(CrimeIncident, Location.location_id == CrimeIncident.location_id)\
         .join(Demographics, City.city_id == Demographics.city_id)\
         .filter(Demographics.year == 2024)\
         .group_by(City.city_id, City.city_name, Demographics.median_income_gbp, 
                  Demographics.unemployment_rate_percent, Demographics.deprivation_index, City.population)\
         .all()
        
        correlation_data = []
        for row in correlations:
            crime_rate = (row.crime_count / row.population * 1000) if row.population > 0 else 0
            correlation_data.append({
                'city': row.city_name,
                'median_income': row.median_income_gbp,
                'unemployment_rate': row.unemployment_rate_percent,
                'deprivation_index': row.deprivation_index,
                'crime_rate_per_1000': round(crime_rate, 2),
                'total_crimes': row.crime_count
            })
        
        return jsonify({'success': True, 'data': correlation_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytical/seasonal-patterns')
def analytical_seasonal_patterns():
    """Seasonal crime pattern analysis"""
    try:
        # Get seasonal patterns
        seasonal_data = db.session.execute(text("""
            SELECT 
                CASE 
                    WHEN CAST(strftime('%m', incident_date) AS INTEGER) IN (12, 1, 2) THEN 'Winter'
                    WHEN CAST(strftime('%m', incident_date) AS INTEGER) IN (3, 4, 5) THEN 'Spring'
                    WHEN CAST(strftime('%m', incident_date) AS INTEGER) IN (6, 7, 8) THEN 'Summer'
                    ELSE 'Autumn'
                END as season,
                cc.category_name,
                COUNT(*) as incident_count
            FROM crime_incidents ci
            JOIN crime_categories cc ON ci.category_id = cc.category_id
            WHERE ci.incident_date >= date('now', '-365 days')
            GROUP BY season, cc.category_name
            ORDER BY season, incident_count DESC
        """)).fetchall()
        
        patterns = [
            {
                'season': row[0],
                'category': row[1],
                'incident_count': row[2]
            } for row in seasonal_data
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