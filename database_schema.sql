-- UK Crime Analysis Database Schema
-- Physical ERD Implementation with 8+ entities

-- 1. Police Forces Entity
CREATE TABLE police_forces (
    force_id VARCHAR(10) PRIMARY KEY,
    force_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    headquarters_address VARCHAR(200),
    phone VARCHAR(20),
    website VARCHAR(100),
    established_year INT,
    officer_count INT,
    civilian_staff_count INT,
    budget_millions DECIMAL(10,2),
    area_covered_sq_km DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Cities/Locations Entity
CREATE TABLE cities (
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    country VARCHAR(20) NOT NULL DEFAULT 'England', -- England, Wales, Scotland, NI
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(11, 6) NOT NULL,
    population INT,
    area_sq_km DECIMAL(10,2),
    population_density DECIMAL(10,2),
    force_id VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (force_id) REFERENCES police_forces(force_id),
    INDEX idx_coordinates (latitude, longitude)
);

-- 3. Crime Categories Entity
CREATE TABLE crime_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_code VARCHAR(50) NOT NULL UNIQUE,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    severity_level INT NOT NULL, -- 1-5 scale
    is_violent BOOLEAN DEFAULT FALSE,
    parent_category_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_category_id) REFERENCES crime_categories(category_id),
    INDEX idx_severity (severity_level)
);

-- 4. Locations/Streets Entity  
CREATE TABLE locations (
    location_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    street_name VARCHAR(200),
    area_name VARCHAR(100),
    ward_name VARCHAR(100),
    postcode VARCHAR(10),
    lsoa_code VARCHAR(20), -- Lower Layer Super Output Area
    lsoa_name VARCHAR(100),
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(11, 6) NOT NULL,
    city_id INT,
    location_type ENUM('Street', 'Building', 'Park', 'Transport', 'Other') DEFAULT 'Street',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    INDEX idx_coordinates (latitude, longitude),
    INDEX idx_lsoa (lsoa_code),
    INDEX idx_postcode (postcode)
);

-- 5. Crime Incidents Entity (Main fact table)
CREATE TABLE crime_incidents (
    incident_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    crime_id VARCHAR(50) NOT NULL UNIQUE, -- External API ID
    persistent_id VARCHAR(50),
    category_id INT NOT NULL,
    location_id BIGINT NOT NULL,
    force_id VARCHAR(10) NOT NULL,
    incident_date DATE NOT NULL,
    incident_time TIME,
    month_reported VARCHAR(7) NOT NULL, -- YYYY-MM format
    context TEXT,
    status ENUM('Open', 'Under Investigation', 'Closed', 'No Further Action') DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES crime_categories(category_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (force_id) REFERENCES police_forces(force_id),
    INDEX idx_date (incident_date),
    INDEX idx_month (month_reported),
    INDEX idx_category (category_id),
    INDEX idx_location (location_id),
    INDEX idx_status (status)
);

-- 6. Crime Outcomes Entity
CREATE TABLE crime_outcomes (
    outcome_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    incident_id BIGINT NOT NULL,
    outcome_category VARCHAR(100) NOT NULL,
    outcome_date DATE,
    person_id BIGINT NULL, -- Reference to persons involved
    court_case_reference VARCHAR(50),
    outcome_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (incident_id) REFERENCES crime_incidents(incident_id) ON DELETE CASCADE,
    INDEX idx_incident (incident_id),
    INDEX idx_outcome_date (outcome_date),
    INDEX idx_category (outcome_category)
);

-- 7. Demographics Entity (for socioeconomic analysis)
CREATE TABLE demographics (
    demo_id INT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    year INT NOT NULL,
    median_income_gbp INT,
    unemployment_rate_percent DECIMAL(5,2),
    education_university_percent DECIMAL(5,2),
    deprivation_index DECIMAL(5,2),
    housing_cost_index DECIMAL(5,2),
    population_age_0_15_percent DECIMAL(5,2),
    population_age_16_64_percent DECIMAL(5,2),
    population_age_65_plus_percent DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    UNIQUE KEY uk_city_year (city_id, year),
    INDEX idx_year (year)
);

-- 8. Police Stations Entity
CREATE TABLE police_stations (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    postcode VARCHAR(10),
    phone VARCHAR(20),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(11, 6),
    force_id VARCHAR(10) NOT NULL,
    city_id INT,
    station_type ENUM('Main', 'Divisional', 'Community', 'Specialist') DEFAULT 'Main',
    operational_hours VARCHAR(50),
    officer_capacity INT,
    is_operational BOOLEAN DEFAULT TRUE,
    opened_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (force_id) REFERENCES police_forces(force_id),
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    INDEX idx_coordinates (latitude, longitude),
    INDEX idx_postcode (postcode)
);

-- 9. Time Dimension Table (for temporal analysis)
CREATE TABLE time_dimension (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    date_value DATE NOT NULL UNIQUE,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    week_of_year INT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE,
    season ENUM('Spring', 'Summer', 'Autumn', 'Winter') NOT NULL,
    INDEX idx_date (date_value),
    INDEX idx_year_month (year, month),
    INDEX idx_season (season)
);

-- 10. Crime Statistics Summary (Materialized view as table for performance)
CREATE TABLE crime_statistics (
    stat_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    city_id INT NOT NULL,
    category_id INT NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    total_incidents INT NOT NULL DEFAULT 0,
    incidents_resolved INT NOT NULL DEFAULT 0,
    incidents_pending INT NOT NULL DEFAULT 0,
    avg_severity DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(city_id),
    FOREIGN KEY (category_id) REFERENCES crime_categories(category_id),
    UNIQUE KEY uk_city_category_period (city_id, category_id, year, month),
    INDEX idx_period (year, month),
    INDEX idx_totals (total_incidents)
);

-- Create Views for Dashboard Queries

-- Strategic Dashboard View - High-level KPIs
CREATE VIEW v_strategic_dashboard AS
SELECT 
    c.city_name,
    c.region,
    pf.force_name,
    COUNT(ci.incident_id) as total_crimes,
    COUNT(CASE WHEN ci.status = 'Closed' THEN 1 END) as resolved_crimes,
    ROUND(COUNT(CASE WHEN ci.status = 'Closed' THEN 1 END) * 100.0 / COUNT(ci.incident_id), 2) as resolution_rate,
    AVG(cc.severity_level) as avg_severity,
    c.population,
    ROUND(COUNT(ci.incident_id) * 1000.0 / c.population, 2) as crimes_per_1000_population
FROM cities c
LEFT JOIN crime_incidents ci ON c.city_id = (SELECT city_id FROM locations WHERE location_id = ci.location_id)
LEFT JOIN crime_categories cc ON ci.category_id = cc.category_id
LEFT JOIN police_forces pf ON c.force_id = pf.force_id
WHERE ci.incident_date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY c.city_id, c.city_name, c.region, pf.force_name, c.population;

-- Tactical Dashboard View - Operational metrics
CREATE VIEW v_tactical_dashboard AS
SELECT 
    c.city_name,
    cc.category_name,
    DATE_FORMAT(ci.incident_date, '%Y-%m') as period,
    COUNT(ci.incident_id) as incident_count,
    COUNT(CASE WHEN ci.status IN ('Open', 'Under Investigation') THEN 1 END) as active_cases,
    AVG(DATEDIFF(COALESCE(co.outcome_date, CURDATE()), ci.incident_date)) as avg_resolution_days,
    HOUR(ci.incident_time) as peak_hour
FROM crime_incidents ci
JOIN locations l ON ci.location_id = l.location_id
JOIN cities c ON l.city_id = c.city_id
JOIN crime_categories cc ON ci.category_id = cc.category_id
LEFT JOIN crime_outcomes co ON ci.incident_id = co.incident_id
WHERE ci.incident_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY c.city_name, cc.category_name, period, HOUR(ci.incident_time);

-- Insert Sample Data (Basic structure - would be populated by data cleaning script)

-- Sample Police Forces
INSERT INTO police_forces (force_id, force_name, region, officer_count, budget_millions) VALUES
('MET', 'Metropolitan Police', 'London', 31000, 3200.0),
('GMP', 'Greater Manchester Police', 'North West', 6500, 612.0),
('WMP', 'West Midlands Police', 'West Midlands', 7200, 515.0),
('WYP', 'West Yorkshire Police', 'Yorkshire', 5500, 428.0),
('PS', 'Police Scotland', 'Scotland', 17000, 1100.0);

-- Sample Crime Categories
INSERT INTO crime_categories (category_code, category_name, severity_level, is_violent) VALUES
('anti-social-behaviour', 'Anti-social Behaviour', 1, FALSE),
('burglary', 'Burglary', 4, FALSE),
('robbery', 'Robbery', 5, TRUE),
('vehicle-crime', 'Vehicle Crime', 3, FALSE),
('violent-crime', 'Violent Crime', 5, TRUE),
('theft-person', 'Theft from Person', 3, FALSE),
('criminal-damage', 'Criminal Damage and Arson', 3, FALSE),
('drugs', 'Drugs', 4, FALSE),
('public-order', 'Public Order', 3, FALSE),
('shoplifting', 'Shoplifting', 2, FALSE);

-- Populate time dimension for last 3 years
INSERT INTO time_dimension (date_value, year, quarter, month, month_name, week_of_year, day_of_month, day_of_week, day_name, is_weekend, season)
SELECT 
    DATE_ADD('2022-01-01', INTERVAL seq.seq DAY) as date_value,
    YEAR(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) as year,
    QUARTER(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) as quarter,
    MONTH(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) as month,
    MONTHNAME(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) as month_name,
    WEEK(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY), 1) as week_of_year,
    DAY(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) as day_of_month,
    DAYOFWEEK(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) as day_of_week,
    DAYNAME(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) as day_name,
    CASE WHEN DAYOFWEEK(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) IN (1,7) THEN TRUE ELSE FALSE END as is_weekend,
    CASE 
        WHEN MONTH(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) IN (12,1,2) THEN 'Winter'
        WHEN MONTH(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) IN (3,4,5) THEN 'Spring'
        WHEN MONTH(DATE_ADD('2022-01-01', INTERVAL seq.seq DAY)) IN (6,7,8) THEN 'Summer'
        ELSE 'Autumn'
    END as season
FROM (
    SELECT (a.N + b.N * 10 + c.N * 100 + d.N * 1000) as seq
    FROM (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) a
    CROSS JOIN (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) b
    CROSS JOIN (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) c
    CROSS JOIN (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) d
) seq
WHERE DATE_ADD('2022-01-01', INTERVAL seq.seq DAY) <= '2024-12-31';

-- Create indexes for performance optimization
CREATE INDEX idx_incident_date_category ON crime_incidents(incident_date, category_id);
CREATE INDEX idx_location_city ON locations(city_id, latitude, longitude);
CREATE INDEX idx_outcome_incident ON crime_outcomes(incident_id, outcome_date);

-- Create stored procedures for data population (would be called by Python scripts)
DELIMITER //

CREATE PROCEDURE PopulateCrimeData(
    IN p_crime_id VARCHAR(50),
    IN p_category_code VARCHAR(50),
    IN p_latitude DECIMAL(10,6),
    IN p_longitude DECIMAL(11,6),
    IN p_incident_date DATE,
    IN p_city_name VARCHAR(100)
)
BEGIN
    DECLARE v_category_id INT;
    DECLARE v_location_id BIGINT;
    DECLARE v_city_id INT;
    DECLARE v_force_id VARCHAR(10);
    
    -- Get category ID
    SELECT category_id INTO v_category_id 
    FROM crime_categories 
    WHERE category_code = p_category_code;
    
    -- Get city and force info
    SELECT c.city_id, c.force_id INTO v_city_id, v_force_id
    FROM cities c 
    WHERE c.city_name = p_city_name;
    
    -- Insert or get location
    INSERT INTO locations (latitude, longitude, city_id) 
    VALUES (p_latitude, p_longitude, v_city_id)
    ON DUPLICATE KEY UPDATE location_id = LAST_INSERT_ID(location_id);
    
    SET v_location_id = LAST_INSERT_ID();
    
    -- Insert crime incident
    INSERT INTO crime_incidents (crime_id, category_id, location_id, force_id, incident_date, month_reported)
    VALUES (p_crime_id, v_category_id, v_location_id, v_force_id, p_incident_date, DATE_FORMAT(p_incident_date, '%Y-%m'));
    
END //

DELIMITER ;