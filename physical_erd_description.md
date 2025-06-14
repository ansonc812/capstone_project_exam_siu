# London Crime Analysis System - Physical Entity Relationship Diagram

## Database Schema Overview

The London Crime Analysis Dashboard System employs a relational database design with **8 core entities** optimized for crime data analysis, geographic mapping, and multi-level dashboard reporting. The schema follows third normal form (3NF) principles to ensure data integrity while maintaining query performance for real-time dashboard operations.

### Core Entities

#### 1. **Police Forces** (Dimension Table)
- **Primary Key**: force_id (VARCHAR)
- **Purpose**: Stores information about UK police forces
- **Key Attributes**: force_name, region, officer_count, budget_millions, area_covered_sq_km
- **Relationships**: One-to-Many with Cities, Crime Incidents, Police Stations

#### 2. **Cities** (Dimension Table) 
- **Primary Key**: city_id (AUTO_INCREMENT)
- **Purpose**: Geographic regions and population data
- **Key Attributes**: city_name, region, country, latitude, longitude, population, population_density
- **Relationships**: Many-to-One with Police Forces, One-to-Many with Locations, Demographics, Police Stations

#### 3. **Crime Categories** (Dimension Table)
- **Primary Key**: category_id (AUTO_INCREMENT) 
- **Purpose**: Classification system for different crime types
- **Key Attributes**: category_code, category_name, severity_level, is_violent, parent_category_id (self-referencing)
- **Relationships**: One-to-Many with Crime Incidents, hierarchical self-relationship

#### 4. **Locations** (Dimension Table)
- **Primary Key**: location_id (AUTO_INCREMENT)
- **Purpose**: Specific geographic locations where crimes occur
- **Key Attributes**: street_name, ward_name, postcode, lsoa_code, latitude, longitude, location_type
- **Relationships**: Many-to-One with Cities, One-to-Many with Crime Incidents

#### 5. **Crime Incidents** (Fact Table - Central Entity)
- **Primary Key**: incident_id (AUTO_INCREMENT)
- **Purpose**: Main fact table storing individual crime occurrences
- **Key Attributes**: crime_id, persistent_id, incident_date, incident_time, month_reported, context, status
- **Relationships**: Many-to-One with Categories, Locations, Police Forces; One-to-Many with Crime Outcomes

#### 6. **Crime Outcomes** (Fact Table)
- **Primary Key**: outcome_id (AUTO_INCREMENT)
- **Purpose**: Results and resolutions of crime incidents
- **Key Attributes**: outcome_category, outcome_date, court_case_reference, outcome_description
- **Relationships**: Many-to-One with Crime Incidents

#### 7. **Demographics** (Dimension/Fact Table)
- **Primary Key**: demo_id (AUTO_INCREMENT)
- **Purpose**: Socioeconomic data for correlation analysis
- **Key Attributes**: median_income_gbp, unemployment_rate_percent, education_university_percent, deprivation_index
- **Relationships**: Many-to-One with Cities (includes year for temporal analysis)

#### 8. **Police Stations** (Dimension Table)
- **Primary Key**: station_id (AUTO_INCREMENT)
- **Purpose**: Police infrastructure and resource allocation
- **Key Attributes**: station_name, address, station_type, operational_hours, officer_capacity
- **Relationships**: Many-to-One with Police Forces and Cities

#### 9. **Time Dimension** (Dimension Table)
- **Primary Key**: time_id (AUTO_INCREMENT)
- **Purpose**: Comprehensive temporal analysis support
- **Key Attributes**: date_value, year, quarter, month, day_of_week, season, is_weekend, is_holiday
- **Relationships**: Used for temporal joins with fact tables

#### 10. **Crime Statistics** (Aggregated Fact Table)
- **Primary Key**: stat_id (AUTO_INCREMENT)
- **Purpose**: Pre-calculated summaries for dashboard performance
- **Key Attributes**: total_incidents, incidents_resolved, incidents_pending, avg_severity
- **Relationships**: Many-to-One with Cities and Crime Categories

### Relationship Matrix

| Entity | Police Forces | Cities | Crime Categories | Locations | Crime Incidents | Crime Outcomes | Demographics | Police Stations | Time Dimension | Crime Statistics |
|--------|---------------|--------|------------------|-----------|-----------------|----------------|--------------|-----------------|----------------|------------------|
| **Police Forces** | - | 1:M | - | - | 1:M | - | - | 1:M | - | - |
| **Cities** | M:1 | - | - | 1:M | - | - | 1:M | 1:M | - | 1:M |
| **Crime Categories** | - | - | 1:M (self) | - | 1:M | - | - | - | - | 1:M |
| **Locations** | - | M:1 | - | - | 1:M | - | - | - | - | - |
| **Crime Incidents** | M:1 | - | M:1 | M:1 | - | 1:M | - | - | M:1 (implicit) | - |
| **Crime Outcomes** | - | - | - | - | M:1 | - | - | - | - | - |
| **Demographics** | - | M:1 | - | - | - | - | - | - | - | - |
| **Police Stations** | M:1 | M:1 | - | - | - | - | - | - | - | - |
| **Time Dimension** | - | - | - | - | - | - | - | - | - | - |
| **Crime Statistics** | - | M:1 | M:1 | - | - | - | - | - | - | - |

### Key Design Features

#### **Normalization Level**: 3NF (Third Normal Form)
- Eliminates transitive dependencies
- Reduces data redundancy
- Maintains referential integrity

#### **Indexing Strategy**
- Primary keys: Clustered indexes
- Foreign keys: Non-clustered indexes  
- Geographic coordinates: Spatial indexes
- Date fields: Temporal indexes
- Composite indexes for common query patterns

#### **Data Types Optimization**
- **Geographic**: DECIMAL(10,6) for latitude, DECIMAL(11,6) for longitude
- **Temporal**: DATE for dates, TIME for times, TIMESTAMP for audit trails
- **Identifiers**: VARCHAR for external IDs, AUTO_INCREMENT for internal PKs
- **Flags**: BOOLEAN for binary attributes, ENUM for controlled vocabularies

#### **Scalability Features**
- Partitioning ready (by date/region)
- Materialized views (Crime Statistics table)
- Stored procedures for data loading
- Optimized for both OLTP and OLAP workloads

#### **Business Rules Enforcement**
- Foreign key constraints ensure referential integrity
- CHECK constraints validate data ranges
- UNIQUE constraints prevent duplicates
- NOT NULL constraints ensure data completeness

### Dashboard Support

#### **Strategic Dashboard** (Executive Level)
- Uses: Cities, Police Forces, Crime Statistics, Demographics
- Aggregation: City/Region level
- Time Granularity: Monthly/Quarterly

#### **Tactical Dashboard** (Operational Level) 
- Uses: Crime Incidents, Locations, Crime Categories, Police Stations
- Aggregation: Daily/Weekly patterns
- Geographic Granularity: Ward/Station level

#### **Analytical Dashboard** (Investigation Level)
- Uses: All entities for detailed drill-down
- Supports: Pattern analysis, correlation studies
- Flexibility: Ad-hoc queries and filtering

This ERD design supports both current reporting needs and future analytical requirements while maintaining performance and data integrity.