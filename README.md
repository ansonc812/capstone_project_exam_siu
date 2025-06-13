# UK Police Crime Rate Analysis - Capstone Project

A comprehensive crime data analysis system featuring three specialized dashboards for strategic, tactical, and analytical decision-making support for UK police forces.

## Project Overview

This capstone project implements a complete data analytics solution for UK police crime data, supporting decision-making at multiple organizational levels:

- **Strategic Dashboard**: Executive-level insights for resource planning and performance evaluation
- **Tactical Dashboard**: Operational command support for real-time incident management
- **Analytical Dashboard**: Deep analysis tools for crime pattern investigation and research

## Features

### Data Collection & Processing
- Multiple data source integration (Police API, public datasets, web scraping)
- 15,000+ crime records with 20+ attributes
- Comprehensive data cleaning and validation
- 10-entity database schema with proper relationships

### Dashboard Capabilities

#### Strategic Dashboard
- Regional crime comparison and ranking
- Budget efficiency analysis
- Performance benchmarking
- Crime trend visualization
- Resource allocation insights

#### Tactical Dashboard
- Real-time incident monitoring
- Crime hotspot identification
- Resource deployment optimization
- Hourly pattern analysis
- Interactive mapping

#### Analytical Dashboard
- Crime correlation analysis
- Demographic factor analysis
- Seasonal pattern decomposition
- Geographic clustering
- Statistical modeling and export

## Technical Stack

- **Backend**: Flask with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite (MySQL schema provided)
- **Visualization**: Chart.js, D3.js, Leaflet.js
- **Styling**: Bootstrap 5

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd capstone_project_exam
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
capstone_project_exam/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── case_study_justification.md     # Project case study documentation
├── dashboard_planning.md           # Dashboard specifications
├── physical_erd_description.md     # Database design documentation
├── database_schema.sql            # MySQL database schema
├── populate_sample_data.sql       # Sample data population script
├── data_collection.py             # Data collection utilities
├── data_cleaning.py               # Data cleaning and processing
├── templates/                     # HTML templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Dashboard selection page
│   ├── strategic_dashboard.html   # Strategic dashboard
│   ├── tactical_dashboard.html    # Tactical dashboard
│   └── analytical_dashboard.html  # Analytical dashboard
├── static/                        # Static assets
│   ├── css/                       # Custom stylesheets
│   └── js/                        # Custom JavaScript
└── cleaned_data/                  # Processed datasets (generated)
```

## Database Schema

The database implements a comprehensive 10-entity schema:

1. **Police Forces** - Force information and resources
2. **Cities** - Geographic regions and demographics
3. **Crime Categories** - Classification hierarchy
4. **Locations** - Specific crime locations
5. **Crime Incidents** - Main fact table
6. **Crime Outcomes** - Case resolutions
7. **Demographics** - Socioeconomic data
8. **Police Stations** - Infrastructure data
9. **Time Dimension** - Temporal analysis support
10. **Crime Statistics** - Aggregated metrics

## API Endpoints

### Strategic Dashboard APIs
- `GET /api/strategic/overview` - High-level KPIs
- `GET /api/strategic/regional-comparison` - Regional performance data
- `GET /api/strategic/trends` - Crime trend analysis

### Tactical Dashboard APIs
- `GET /api/tactical/active-incidents` - Current active incidents
- `GET /api/tactical/hotspots` - Crime hotspot analysis
- `GET /api/tactical/hourly-patterns` - Time-based patterns

### Analytical Dashboard APIs
- `GET /api/analytical/correlation-matrix` - Crime correlations
- `GET /api/analytical/demographic-correlation` - Demographic analysis
- `GET /api/analytical/seasonal-patterns` - Seasonal trends

## Data Sources

1. **Police API** (data.police.uk)
   - Official UK police crime data
   - Street-level incident information
   - Police force boundaries and details

2. **Public Datasets**
   - ONS demographic statistics
   - Local government socioeconomic data
   - Population and geographic information

3. **Generated Mock Data**
   - Realistic sample data for demonstration
   - Statistically valid distributions
   - Comprehensive coverage for analysis

## Usage Guide

### Strategic Dashboard
1. Access via main navigation or direct link `/strategic`
2. Use filters to adjust time period and region scope
3. Analyze KPI cards for high-level performance metrics
4. Review regional comparison charts and efficiency analysis
5. Examine performance ranking table for detailed insights

### Tactical Dashboard
1. Navigate to `/tactical` for operational view
2. Monitor real-time incident alerts and active cases
3. Use map controls to switch between incidents, hotspots, and patrols
4. Analyze hourly patterns for resource deployment
5. Review priority queue for high-priority incidents

### Analytical Dashboard
1. Access via `/analytical` for deep analysis
2. Select analysis type and configure parameters
3. Run correlation analysis and review statistical summaries
4. Explore geographic clustering and demographic relationships
5. Export results and generate reports

## Development Notes

### Adding New Visualizations
1. Extend the appropriate API endpoint in `app.py`
2. Add Chart.js or D3.js visualization in the HTML template
3. Implement data processing in the JavaScript section
4. Update the dashboard layout as needed

### Database Extensions
1. Modify the SQLAlchemy models in `app.py`
2. Update the MySQL schema in `database_schema.sql`
3. Create migration scripts for existing data
4. Update API endpoints to handle new data structures

### Performance Optimization
1. Implement database indexing for frequently queried fields
2. Add caching for expensive calculations
3. Use pagination for large datasets
4. Optimize chart rendering for large data volumes

## Security Considerations

- Input validation on all API endpoints
- SQL injection prevention through ORM usage
- CORS configuration for cross-origin requests
- Environment-specific configuration management
- Data anonymization for sensitive information

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure SQLite database is created: Run database initialization
   - Check file permissions in the project directory

2. **Missing Dependencies**
   - Verify virtual environment activation
   - Reinstall requirements: `pip install -r requirements.txt`

3. **Port Conflicts**
   - Change port in `app.py`: `app.run(port=5001)`
   - Kill existing processes on port 5000

4. **JavaScript Errors**
   - Check browser console for specific errors
   - Verify all CDN resources are loading correctly
   - Clear browser cache and reload

## Future Enhancements

- Real-time data streaming integration
- Machine learning predictive models
- Advanced geographic analysis (heat maps, density clustering)
- Mobile-responsive design improvements
- Multi-user authentication and role-based access
- Automated report generation and scheduling
- Integration with external police systems

## Contributors

This project was developed as part of a capstone project demonstration, showcasing comprehensive data analytics capabilities for law enforcement decision support.

## License

This project is for educational and demonstration purposes. Crime data used is either publicly available or generated for demonstration purposes.