-- Sample Data Population Script for UK Crime Analysis Database
-- This script populates the database with realistic sample data

-- Sample Cities Data
INSERT INTO cities (city_name, region, country, latitude, longitude, population, area_sq_km, force_id) VALUES
('London', 'London', 'England', 51.5074, -0.1278, 8982000, 1572, 'MET'),
('Manchester', 'North West', 'England', 53.4808, -2.2426, 2720000, 630, 'GMP'),
('Birmingham', 'West Midlands', 'England', 52.4862, -1.8904, 1141000, 267, 'WMP'),
('Leeds', 'Yorkshire', 'England', 53.8008, -1.5491, 793000, 487, 'WYP'),
('Glasgow', 'Scotland', 'Scotland', 55.8642, -4.2518, 635000, 175, 'PS'),
('Liverpool', 'North West', 'England', 53.4084, -2.9916, 498000, 199, 'GMP'),
('Newcastle', 'North East', 'England', 54.9783, -1.6178, 300000, 180, 'NP'),
('Sheffield', 'Yorkshire', 'England', 53.3811, -1.4701, 584000, 368, 'SYP'),
('Bristol', 'South West', 'England', 51.4545, -2.5879, 463000, 110, 'ASP'),
('Cardiff', 'Wales', 'Wales', 51.4816, -3.1791, 364000, 140, 'SWP');

-- Update population density
UPDATE cities SET population_density = population / area_sq_km;

-- Additional Police Forces
INSERT INTO police_forces (force_id, force_name, region, officer_count, budget_millions) VALUES
('NP', 'Northumbria Police', 'North East', 3500, 285.0),
('SYP', 'South Yorkshire Police', 'Yorkshire', 2800, 245.0),
('ASP', 'Avon and Somerset Police', 'South West', 3200, 312.0),
('SWP', 'South Wales Police', 'Wales', 3000, 278.0);

-- Sample Police Stations
INSERT INTO police_stations (station_name, address, postcode, latitude, longitude, force_id, city_id, station_type, officer_capacity) VALUES
('New Scotland Yard', 'Broadway, Westminster', 'SW1H 0BG', 51.4994, -0.1358, 'MET', 1, 'Main', 1000),
('Manchester Central', 'Chester House, Boyer Street', 'M16 0RE', 53.4669, -2.2658, 'GMP', 2, 'Main', 500),
('Birmingham Central', 'Steelhouse Lane', 'B4 6NE', 52.4853, -1.8936, 'WMP', 3, 'Main', 400),
('Leeds District HQ', 'Elland Road', 'LS11 8BU', 53.7767, -1.5728, 'WYP', 4, 'Main', 350),
('Glasgow HQ', 'Pitt Street', 'G2 4JS', 55.8609, -4.2514, 'PS', 5, 'Main', 800),
('Liverpool Central', 'Canning Place', 'L1 8JX', 53.4002, -2.9665, 'GMP', 6, 'Divisional', 300),
('Newcastle Central', 'Market Street', 'NE1 6XE', 54.9719, -1.6103, 'NP', 7, 'Main', 250),
('Sheffield Central', 'Snig Hill', 'S3 8LY', 53.3856, -1.4659, 'SYP', 8, 'Main', 280),
('Bristol Central', 'Nelson Street', 'BS1 2LE', 51.4516, -2.5906, 'ASP', 9, 'Main', 320),
('Cardiff Central', 'King Edward VII Avenue', 'CF10 3NN', 51.4758, -3.1778, 'SWP', 10, 'Main', 300);

-- Sample Demographics Data (for last 3 years)
INSERT INTO demographics (city_id, year, median_income_gbp, unemployment_rate_percent, education_university_percent, deprivation_index, housing_cost_index) VALUES
-- London
(1, 2022, 39000, 4.2, 52.3, 15.8, 142.5),
(1, 2023, 41000, 3.8, 53.1, 15.2, 148.3),
(1, 2024, 42500, 3.5, 54.2, 14.9, 151.2),
-- Manchester  
(2, 2022, 28500, 5.8, 38.7, 28.4, 95.2),
(2, 2023, 29800, 5.2, 39.9, 27.1, 98.7),
(2, 2024, 31200, 4.9, 41.2, 26.3, 102.1),
-- Birmingham
(3, 2022, 26800, 6.7, 35.4, 32.1, 88.3),
(3, 2023, 28200, 6.1, 36.8, 30.9, 91.5),
(3, 2024, 29600, 5.8, 38.1, 29.7, 94.2),
-- Leeds
(4, 2022, 27900, 5.3, 42.6, 24.7, 89.6),
(4, 2023, 29100, 4.9, 43.8, 23.8, 92.4),
(4, 2024, 30400, 4.6, 45.1, 22.9, 95.1),
-- Glasgow
(5, 2022, 26200, 6.8, 41.2, 31.6, 78.4),
(5, 2023, 27400, 6.3, 42.4, 30.2, 81.7),
(5, 2024, 28600, 5.9, 43.6, 29.1, 84.3);

-- Sample Location Data (Street level)
INSERT INTO locations (street_name, area_name, ward_name, postcode, lsoa_code, latitude, longitude, city_id, location_type) VALUES
-- London locations
('Oxford Street', 'Westminster', 'West End', 'W1C 1JN', 'E00087123', 51.5154, -0.1423, 1, 'Street'),
('Camden High Street', 'Camden', 'Camden Town', 'NW1 7JE', 'E00087456', 51.5392, -0.1426, 1, 'Street'),
('Brick Lane', 'Tower Hamlets', 'Spitalfields', 'E1 6QL', 'E00087789', 51.5223, -0.0712, 1, 'Street'),
('Kings Road', 'Kensington and Chelsea', 'Chelsea', 'SW3 4ND', 'E00088012', 51.4922, -0.1634, 1, 'Street'),
('Tottenham Court Road', 'Camden', 'Fitzrovia', 'W1T 7NE', 'E00088345', 51.5175, -0.1368, 1, 'Street'),

-- Manchester locations  
('Market Street', 'City Centre', 'Deansgate', 'M1 1WA', 'E00165234', 53.4808, -2.2426, 2, 'Street'),
('Curry Mile', 'Rusholme', 'Rusholme', 'M14 5LN', 'E00165567', 53.4442, -2.2190, 2, 'Street'),
('Northern Quarter', 'City Centre', 'Piccadilly', 'M1 2HF', 'E00165890', 53.4834, -2.2356, 2, 'Street'),
('Oldham Street', 'City Centre', 'Piccadilly', 'M1 1JQ', 'E00166123', 53.4825, -2.2364, 2, 'Street'),
('Canal Street', 'City Centre', 'Village', 'M1 3HZ', 'E00166456', 53.4764, -2.2354, 2, 'Street'),

-- Birmingham locations
('Bull Ring', 'City Centre', 'Ladywood', 'B5 4BP', 'E00054789', 52.4773, -1.8930, 3, 'Building'),
('Broad Street', 'City Centre', 'Ladywood', 'B1 2EA', 'E00055012', 52.4794, -1.9026, 3, 'Street'),
('Digbeth', 'City Centre', 'Bordesley Green', 'B5 6DR', 'E00055345', 52.4751, -1.8876, 3, 'Street'),
('Corporation Street', 'City Centre', 'Nechells', 'B2 4LP', 'E00055678', 'B2 4LP', 52.4833, -1.8967, 3, 'Street'),
('New Street', 'City Centre', 'Ladywood', 'B2 4QA', 'E00056001', 52.4794, -1.8983, 3, 'Street');

-- Generate sample crime incidents (15,000+ records)
-- This uses a stored procedure approach for better performance

DELIMITER //

CREATE PROCEDURE GenerateSampleCrimes()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE v_category_id INT;
    DECLARE v_location_id BIGINT;
    DECLARE v_force_id VARCHAR(10);
    DECLARE v_incident_date DATE;
    DECLARE v_incident_time TIME;
    DECLARE v_outcome_category VARCHAR(100);
    
    -- Crime outcomes for variety
    DECLARE outcomes CURSOR FOR 
        SELECT 'Investigation complete; no suspect identified' UNION ALL
        SELECT 'Unable to prosecute suspect' UNION ALL
        SELECT 'Offender given a caution' UNION ALL
        SELECT 'Offender charged' UNION ALL
        SELECT 'Court result unavailable' UNION ALL
        SELECT 'Offender fined' UNION ALL
        SELECT 'Community sentence' UNION ALL
        SELECT 'Suspended sentence' UNION ALL
        SELECT 'Awaiting court outcome' UNION ALL
        SELECT 'Under investigation';
    
    WHILE i <= 15000 DO
        -- Random category (1-10 for the crime categories we inserted)
        SET v_category_id = FLOOR(1 + RAND() * 10);
        
        -- Random location (1-15 for the locations we inserted)  
        SET v_location_id = FLOOR(1 + RAND() * 15);
        
        -- Get force_id based on location
        SELECT c.force_id INTO v_force_id 
        FROM locations l 
        JOIN cities c ON l.city_id = c.city_id 
        WHERE l.location_id = v_location_id;
        
        -- Random date in last 2 years
        SET v_incident_date = DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 730) DAY);
        
        -- Time based on crime type patterns
        IF v_category_id IN (3, 4) THEN -- Burglary, vehicle crime - more at night
            SET v_incident_time = TIME(CONCAT(FLOOR(RAND() * 6), ':', FLOOR(RAND() * 60), ':00'));
        ELSEIF v_category_id IN (1, 8, 9) THEN -- ASB, public order - more evening/night
            SET v_incident_time = TIME(CONCAT(18 + FLOOR(RAND() * 6), ':', FLOOR(RAND() * 60), ':00'));
        ELSE 
            SET v_incident_time = TIME(CONCAT(FLOOR(RAND() * 24), ':', FLOOR(RAND() * 60), ':00'));
        END IF;
        
        -- Insert crime incident
        INSERT INTO crime_incidents (
            crime_id, 
            category_id, 
            location_id, 
            force_id, 
            incident_date, 
            incident_time,
            month_reported,
            status
        ) VALUES (
            CONCAT('CRIME_', LPAD(i, 6, '0')),
            v_category_id,
            v_location_id,
            v_force_id,
            v_incident_date,
            v_incident_time,
            DATE_FORMAT(v_incident_date, '%Y-%m'),
            CASE 
                WHEN RAND() < 0.6 THEN 'Closed'
                WHEN RAND() < 0.8 THEN 'Under Investigation' 
                ELSE 'Open'
            END
        );
        
        -- Add outcome for closed cases (60% of incidents)
        IF RAND() < 0.6 THEN
            SET v_outcome_category = ELT(FLOOR(1 + RAND() * 10), 
                'Investigation complete; no suspect identified',
                'Unable to prosecute suspect',
                'Offender given a caution', 
                'Offender charged',
                'Court result unavailable',
                'Offender fined',
                'Community sentence',
                'Suspended sentence', 
                'Awaiting court outcome',
                'Under investigation'
            );
            
            INSERT INTO crime_outcomes (
                incident_id,
                outcome_category,
                outcome_date
            ) VALUES (
                LAST_INSERT_ID(),
                v_outcome_category,
                DATE_ADD(v_incident_date, INTERVAL FLOOR(1 + RAND() * 90) DAY)
            );
        END IF;
        
        SET i = i + 1;
    END WHILE;
END //

DELIMITER ;

-- Execute the procedure to generate sample data
CALL GenerateSampleCrimes();

-- Update crime statistics table with aggregated data
INSERT INTO crime_statistics (city_id, category_id, year, month, total_incidents, incidents_resolved, incidents_pending)
SELECT 
    l.city_id,
    ci.category_id,
    YEAR(ci.incident_date) as year,
    MONTH(ci.incident_date) as month,
    COUNT(*) as total_incidents,
    COUNT(CASE WHEN ci.status = 'Closed' THEN 1 END) as incidents_resolved,
    COUNT(CASE WHEN ci.status IN ('Open', 'Under Investigation') THEN 1 END) as incidents_pending
FROM crime_incidents ci
JOIN locations l ON ci.location_id = l.location_id
GROUP BY l.city_id, ci.category_id, YEAR(ci.incident_date), MONTH(ci.incident_date);

-- Update average severity in statistics
UPDATE crime_statistics cs
JOIN crime_categories cc ON cs.category_id = cc.category_id
SET cs.avg_severity = cc.severity_level;

-- Create some additional sample data for demonstration

-- Sample data export summary
SELECT 
    'Data Population Complete' as Status,
    COUNT(*) as Total_Crime_Records
FROM crime_incidents

UNION ALL

SELECT 
    'Cities Loaded',
    COUNT(*)
FROM cities

UNION ALL

SELECT
    'Police Stations Created', 
    COUNT(*)
FROM police_stations

UNION ALL

SELECT
    'Demographics Records',
    COUNT(*) 
FROM demographics

UNION ALL

SELECT
    'Locations Created',
    COUNT(*)
FROM locations;

-- Drop the temporary procedure
DROP PROCEDURE GenerateSampleCrimes;