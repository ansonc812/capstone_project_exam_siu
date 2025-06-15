# London Crime Analysis Dashboard System - Capstone Project

A production-ready crime data analysis system featuring three fully functional dashboards for London crime analysis. Built with Flask backend, Bootstrap frontend, and real crime data integration with interactive heatmap visualization.

## Current System Status

✅ **Fully Operational** - All three dashboards working with real London crime data  
✅ **Interactive Heatmap** - WebGL-accelerated crime density visualization  
✅ **Working Filters** - All borough and severity filters functional  
✅ **Real Data Only** - 22,667 actual crime incidents, no predictions or sample data  
✅ **Clean Architecture** - Simplified Flask APIs with consistent JSON responses  

## Access the Application

Start the Flask server: `python3 app.py`

- **Main Dashboard**: `http://localhost:5000`
- **Strategic Dashboard**: `http://localhost:5000/strategic`
- **Tactical Dashboard**: `http://localhost:5000/tactical` 
- **Analytical Dashboard**: `http://localhost:5000/analytical`

## Dashboard Features

### 🎯 Strategic Dashboard - Executive Overview
- **KPI Metrics**: 22,667 total crimes across 5 London boroughs
- **Borough Analysis**: Crime distribution with population-adjusted rates
- **Interactive Charts**: Bar charts and doughnut visualizations
- **Working Filters**: Borough and severity level filtering
- **Safety Rankings**: Color-coded borough safety comparison

### 🗺️ Tactical Dashboard - Interactive Crime Heatmap
- **Density Heatmap**: Real-time crime density visualization with gradient colors (blue → red)
- **60+ Crime Incidents**: Actual London locations with incident details
- **Interactive Markers**: Click for detailed crime information
- **Hotspot Analysis**: Identifies high-crime areas with incident counts
- **Live Filtering**: Borough and crime category filters with instant updates

### 📊 Analytical Dashboard - Crime Pattern Analysis
- **Severity Distribution**: Crime breakdown across severity levels 2-5
- **Borough Statistics**: Population vs crime rate analysis
- **Data Tables**: Detailed statistical breakdown with calculated metrics
- **Demographic Insights**: Crime pattern analysis across different areas

## Technical Implementation

- **Backend**: Flask 3.0.2 with simplified REST APIs
- **Frontend**: Bootstrap 5 + Chart.js + Leaflet.js mapping
- **Data Source**: Real London Metropolitan Police crime data (22,667 incidents)
- **Heatmap**: Leaflet Heat plugin with WebGL acceleration
- **Architecture**: Clean API endpoints returning consistent JSON format

## Quick Setup

### Installation
```bash
# Clone repository
git clone https://github.com/ansonc812/capstone_project_exam_siu.git
cd capstone_project_exam

# Install dependencies
sudo apt install python3-flask python3-flask-sqlalchemy python3-flask-cors

# Run application  
python3 app.py
```

### Access Dashboards
- **Main**: http://localhost:5000
- **Strategic**: http://localhost:5000/strategic  
- **Tactical**: http://localhost:5000/tactical
- **Analytical**: http://localhost:5000/analytical

## Crime Data Summary

**22,667 Total Incidents** across 5 London boroughs with real crime data integration.

### Borough Crime Rates
| Borough | Crimes | Population | Rate/1000 |
|---------|--------|------------|-----------|
| City of London | 2,869 | 9,000 | 318.78 |
| Westminster | 6,047 | 261,000 | 23.17 |
| Camden | 6,013 | 270,000 | 22.27 |
| Southwark | 5,456 | 318,000 | 17.16 |
| Tower Hamlets | 2,282 | 324,000 | 7.04 |

### Top Crime Types
1. **Theft from Person** - 7,230 incidents
2. **Anti-social Behaviour** - 3,528 incidents  
3. **Violent Crime** - 3,383 incidents
4. **Other Theft** - 1,640 incidents
5. **Shoplifting** - 1,453 incidents

## System Architecture

```
capstone_project_exam/
├── app.py                          # Flask backend with clean REST APIs
├── templates/
│   ├── base.html                   # Shared UI components
│   ├── index.html                  # Main dashboard selector
│   ├── strategic_dashboard.html    # Executive KPI dashboard
│   ├── tactical_dashboard.html     # Interactive heatmap dashboard
│   └── analytical_dashboard.html   # Crime analysis dashboard
└── README.md                       # Documentation
```

## API Endpoints

Clean REST API with consistent JSON responses: `{success: true, data: [results]}`

### Core APIs
- `/api/strategic/overview` - KPI metrics and totals
- `/api/strategic/borough-crimes` - Borough crime data with filtering
- `/api/strategic/crime-categories` - Crime category breakdown
- `/api/tactical/recent-incidents` - Crime incidents with coordinates
- `/api/tactical/hotspots` - Heatmap density data
- `/api/analytical/severity-analysis` - Crime severity distribution
- `/api/analytical/borough-comparison` - Borough statistical analysis

## Key Features Working

✅ **All Filters Functional** - Borough and severity filtering works across all dashboards  
✅ **Interactive Heatmap** - Crime density visualization with gradient colors  
✅ **Real-time Updates** - Charts update immediately when filters applied  
✅ **Responsive Design** - Works on desktop and mobile devices  
✅ **Error-free Operation** - No JavaScript errors, clean console output

## Dashboard Usage

### Strategic Dashboard
- View crime KPIs and borough comparisons
- Use filters to analyze specific areas or crime severities
- Review safety rankings and crime distributions

### Tactical Dashboard  
- Interactive crime heatmap shows density patterns
- Click markers for incident details
- Filter by borough and crime category
- View hotspot analysis table

### Analytical Dashboard
- Crime severity distribution analysis
- Borough population vs crime rate comparison
- Statistical tables with calculated metrics

## Recent Updates

### System Rebuild (Current Version)
- **Complete rebuild** of all three dashboards with clean Flask architecture
- **Real data integration** - Replaced all predictions with actual London crime data
- **Interactive heatmap** implementation with WebGL acceleration
- **Fixed all filter functionality** - Borough and severity filters now work properly
- **Resolved JavaScript errors** - Clean console output, no duplicate variable declarations
- **Simplified API architecture** - Consistent JSON responses across all endpoints

## Troubleshooting

**App won't start**: Install dependencies with `sudo apt install python3-flask python3-flask-sqlalchemy python3-flask-cors`

**Dashboard shows 0 values**: Ensure Flask is running with `python3 app.py`

**Heatmap not loading**: Check internet connection for CDN access to Leaflet Heat plugin

**Test API directly**: `curl http://localhost:5000/api/strategic/overview`

## Project Info

**Educational capstone project** developed independently, featuring real London Metropolitan Police crime data visualization.

**Tech Stack**: Flask + Bootstrap 5 + Chart.js + Leaflet.js + Real Crime Data

**Repository**: https://github.com/ansonc812/capstone_project_exam_siu.git

**Author**: Student capstone project

---

## Quick Commands

```bash
# Start application
python3 app.py

# Test API  
curl http://localhost:5000/api/strategic/overview

# Access dashboards
http://localhost:5000/strategic
http://localhost:5000/tactical  
http://localhost:5000/analytical
```