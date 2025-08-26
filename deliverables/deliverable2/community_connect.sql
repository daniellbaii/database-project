-- Community Connect Database
-- Week 2 Deliverable: Database Implementation
-- Author: Daniel Bai
-- Date: 2025
-- Description: Complete SQL script to create and populate the Community Connect volunteer coordination database

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- ========================================
-- DROP EXISTING TABLES (if they exist)
-- ========================================
DROP TABLE IF EXISTS EVENT_SKILL;
DROP TABLE IF EXISTS VOLUNTEER_SKILL;
DROP TABLE IF EXISTS VOLUNTEER_EVENT;
DROP TABLE IF EXISTS EVENT;
DROP TABLE IF EXISTS SKILL;
DROP TABLE IF EXISTS VOLUNTEER;
DROP TABLE IF EXISTS ORGANISATION;

-- ========================================
-- CREATE TABLES
-- ========================================

-- Create VOLUNTEER table
CREATE TABLE VOLUNTEER (
    volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL CHECK(LENGTH(first_name) > 0),
    last_name TEXT NOT NULL CHECK(LENGTH(last_name) > 0),
    date_of_birth DATE NOT NULL,
    email TEXT NOT NULL UNIQUE CHECK(email LIKE '%@%.%'),
    phone TEXT NOT NULL CHECK(LENGTH(phone) >= 10),
    address TEXT NOT NULL CHECK(LENGTH(address) > 0),
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Create ORGANISATION table
CREATE TABLE ORGANISATION (
    org_id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_name TEXT NOT NULL UNIQUE CHECK(LENGTH(org_name) > 0),
    contact_email TEXT NOT NULL CHECK(contact_email LIKE '%@%.%'),
    phone TEXT NOT NULL CHECK(LENGTH(phone) >= 10),
    address TEXT NOT NULL CHECK(LENGTH(address) > 0),
    org_type TEXT NOT NULL CHECK(org_type IN ('Charity', 'Community Group', 'Non-Profit', 'Government', 'Educational')),
    description TEXT
);

-- Create SKILL table
CREATE TABLE SKILL (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL UNIQUE CHECK(LENGTH(skill_name) > 0),
    skill_description TEXT,
    skill_category TEXT NOT NULL CHECK(skill_category IN ('Medical', 'Administrative', 'Physical', 'Technical', 'Communication', 'Educational', 'Creative'))
);

-- Create EVENT table
CREATE TABLE EVENT (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id INTEGER NOT NULL,
    event_name TEXT NOT NULL CHECK(LENGTH(event_name) > 0),
    description TEXT NOT NULL CHECK(LENGTH(description) > 0),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL CHECK(end_date >= start_date),
    location TEXT NOT NULL CHECK(LENGTH(location) > 0),
    max_volunteers INTEGER NOT NULL CHECK(max_volunteers > 0),
    FOREIGN KEY (org_id) REFERENCES ORGANISATION(org_id) ON DELETE CASCADE
);

-- Create VOLUNTEER_EVENT junction table
CREATE TABLE VOLUNTEER_EVENT (
    volunteer_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    attendance_status TEXT NOT NULL DEFAULT 'Registered' CHECK(attendance_status IN ('Registered', 'Attended', 'No-Show', 'Cancelled')),
    PRIMARY KEY (volunteer_id, event_id),
    FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE CASCADE
);

-- Create VOLUNTEER_SKILL junction table
CREATE TABLE VOLUNTEER_SKILL (
    volunteer_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    proficiency_level TEXT NOT NULL CHECK(proficiency_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    years_experience INTEGER CHECK(years_experience >= 0),
    PRIMARY KEY (volunteer_id, skill_id),
    FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id) ON DELETE CASCADE
);

-- Create EVENT_SKILL junction table
CREATE TABLE EVENT_SKILL (
    event_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    skill_priority TEXT NOT NULL CHECK(skill_priority IN ('Essential', 'Preferred', 'Bonus')),
    minimum_proficiency TEXT NOT NULL CHECK(minimum_proficiency IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    PRIMARY KEY (event_id, skill_id),
    FOREIGN KEY (event_id) REFERENCES EVENT(event_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id) ON DELETE CASCADE
);

-- ========================================
-- INSERT SAMPLE DATA
-- ========================================

-- Insert Skills (8 skills across different categories)
INSERT INTO SKILL (skill_name, skill_description, skill_category) VALUES
('First Aid', 'Certified first aid and emergency response training', 'Medical'),
('CPR', 'Cardiopulmonary resuscitation certification', 'Medical'),
('Food Handling', 'Safe food preparation and hygiene practices', 'Physical'),
('Event Planning', 'Organizing and coordinating events and activities', 'Administrative'),
('Public Speaking', 'Confident communication to groups and audiences', 'Communication'),
('IT Support', 'Computer troubleshooting and technical assistance', 'Technical'),
('Teaching', 'Educational instruction and mentoring capabilities', 'Educational'),
('Photography', 'Digital photography and event documentation', 'Creative');

-- Insert Organisations (4 organisations)
INSERT INTO ORGANISATION (org_name, contact_email, phone, address, org_type, description) VALUES
('Red Cross Perth', 'contact@redcrossperth.org.au', '08-9225-8888', '110 Goderich Street, East Perth WA 6004', 'Charity', 'Humanitarian organisation providing emergency relief and community services'),
('Community Kitchen Network', 'info@ckn.org.au', '08-9328-4488', '25 Beaufort Street, Perth WA 6000', 'Community Group', 'Volunteer-run kitchens providing meals for those in need'),
('Perth Environmental Action', 'volunteers@pea.org.au', '08-9227-5522', '200 St Georges Terrace, Perth WA 6000', 'Non-Profit', 'Environmental conservation and sustainability advocacy group'),
('Rossmoyne Senior High School', 'admin@rossmoyne.wa.edu.au', '08-9351-8200', '1 Keith Road, Rossmoyne WA 6148', 'Educational', 'Secondary school community engagement programs');

-- Insert Volunteers (6 volunteers with diverse backgrounds)
INSERT INTO VOLUNTEER (first_name, last_name, date_of_birth, email, phone, address, registration_date) VALUES
('Sarah', 'Johnson', '1995-03-15', 'sarah.johnson@email.com', '0412-345-678', '45 River Road, Applecross WA 6153', '2025-01-15'),
('Michael', 'Chen', '1988-07-22', 'michael.chen@email.com', '0423-456-789', '12 Ocean Drive, Cottesloe WA 6011', '2025-01-20'),
('Emma', 'Williams', '1992-11-08', 'emma.williams@email.com', '0434-567-890', '78 Forest Street, Fremantle WA 6160', '2025-02-01'),
('David', 'Brown', '1985-09-12', 'david.brown@email.com', '0445-678-901', '33 Hill View Crescent, Mount Pleasant WA 6153', '2025-02-05'),
('Jessica', 'Taylor', '1998-04-30', 'jessica.taylor@email.com', '0456-789-012', '56 Park Avenue, Nedlands WA 6009', '2025-02-10'),
('Robert', 'Anderson', '1990-12-18', 'robert.anderson@email.com', '0467-890-123', '21 Beach Road, Scarborough WA 6019', '2025-02-15');

-- Insert Events (5 events with different dates and requirements)
INSERT INTO EVENT (org_id, event_name, description, start_date, end_date, location, max_volunteers) VALUES
(1, 'Blood Drive Campaign', 'Community blood donation drive with donor support and registration assistance', '2025-03-15', '2025-03-15', 'Red Cross Perth Centre, East Perth', 12),
(2, 'Weekly Community Dinner', 'Prepare and serve meals for community members in need', '2025-03-20', '2025-03-20', 'Community Kitchen Network, Perth', 8),
(3, 'River Cleanup Initiative', 'Environmental cleanup of Swan River foreshore and surrounding parklands', '2025-04-05', '2025-04-05', 'Swan River Foreshore, Perth', 20),
(4, 'School Career Fair', 'Support students with career guidance and university information sessions', '2025-04-12', '2025-04-12', 'Rossmoyne Senior High School', 15),
(1, 'Emergency Response Training', 'Community first aid and emergency preparedness workshop', '2025-04-25', '2025-04-25', 'Red Cross Perth Centre, East Perth', 10);

-- Insert Volunteer Skills (showing different proficiency levels)
INSERT INTO VOLUNTEER_SKILL (volunteer_id, skill_id, proficiency_level, years_experience) VALUES
(1, 1, 'Expert', 8),    -- Sarah: First Aid - Expert
(1, 2, 'Advanced', 6),  -- Sarah: CPR - Advanced
(1, 5, 'Intermediate', 4), -- Sarah: Public Speaking - Intermediate
(2, 6, 'Expert', 12),   -- Michael: IT Support - Expert
(2, 4, 'Advanced', 7),  -- Michael: Event Planning - Advanced
(3, 3, 'Intermediate', 3), -- Emma: Food Handling - Intermediate
(3, 7, 'Advanced', 5),  -- Emma: Teaching - Advanced
(3, 8, 'Beginner', 1),  -- Emma: Photography - Beginner
(4, 1, 'Advanced', 10), -- David: First Aid - Advanced
(4, 2, 'Expert', 8),    -- David: CPR - Expert
(5, 5, 'Expert', 6),    -- Jessica: Public Speaking - Expert
(5, 4, 'Intermediate', 2), -- Jessica: Event Planning - Intermediate
(6, 3, 'Advanced', 4),  -- Robert: Food Handling - Advanced
(6, 8, 'Expert', 9);    -- Robert: Photography - Expert

-- Insert Event Skill Requirements
INSERT INTO EVENT_SKILL (event_id, skill_id, skill_priority, minimum_proficiency) VALUES
(1, 1, 'Essential', 'Intermediate'), -- Blood Drive: First Aid
(1, 2, 'Preferred', 'Beginner'),     -- Blood Drive: CPR
(1, 5, 'Preferred', 'Beginner'),     -- Blood Drive: Public Speaking
(2, 3, 'Essential', 'Intermediate'), -- Community Dinner: Food Handling
(2, 5, 'Preferred', 'Beginner'),     -- Community Dinner: Public Speaking
(3, 1, 'Preferred', 'Beginner'),     -- River Cleanup: First Aid
(3, 5, 'Bonus', 'Beginner'),        -- River Cleanup: Public Speaking
(4, 5, 'Essential', 'Intermediate'), -- Career Fair: Public Speaking
(4, 7, 'Preferred', 'Intermediate'), -- Career Fair: Teaching
(4, 6, 'Bonus', 'Beginner'),        -- Career Fair: IT Support
(5, 1, 'Essential', 'Advanced'),     -- Emergency Training: First Aid
(5, 2, 'Essential', 'Advanced'),     -- Emergency Training: CPR
(5, 7, 'Preferred', 'Intermediate'); -- Emergency Training: Teaching

-- Insert Volunteer Event Registrations
INSERT INTO VOLUNTEER_EVENT (volunteer_id, event_id, registration_date, attendance_status) VALUES
(1, 1, '2025-02-20', 'Registered'),  -- Sarah -> Blood Drive
(1, 5, '2025-02-25', 'Registered'),  -- Sarah -> Emergency Training
(2, 4, '2025-02-22', 'Registered'),  -- Michael -> Career Fair
(3, 2, '2025-02-18', 'Registered'),  -- Emma -> Community Dinner
(3, 4, '2025-02-28', 'Registered'),  -- Emma -> Career Fair
(4, 1, '2025-02-21', 'Registered'),  -- David -> Blood Drive
(4, 5, '2025-02-26', 'Registered'),  -- David -> Emergency Training
(5, 4, '2025-02-24', 'Registered'),  -- Jessica -> Career Fair
(6, 2, '2025-02-19', 'Registered'),  -- Robert -> Community Dinner
(6, 3, '2025-02-27', 'Registered');  -- Robert -> River Cleanup

-- ========================================
-- VERIFICATION QUERIES
-- ========================================

-- These queries can be used to verify the database was created correctly

-- Count records in each table
-- SELECT 'VOLUNTEER' as table_name, COUNT(*) as record_count FROM VOLUNTEER
-- UNION SELECT 'ORGANISATION', COUNT(*) FROM ORGANISATION
-- UNION SELECT 'SKILL', COUNT(*) FROM SKILL
-- UNION SELECT 'EVENT', COUNT(*) FROM EVENT
-- UNION SELECT 'VOLUNTEER_EVENT', COUNT(*) FROM VOLUNTEER_EVENT
-- UNION SELECT 'VOLUNTEER_SKILL', COUNT(*) FROM VOLUNTEER_SKILL
-- UNION SELECT 'EVENT_SKILL', COUNT(*) FROM EVENT_SKILL;

-- Test referential integrity
-- SELECT v.first_name, v.last_name, e.event_name, o.org_name
-- FROM VOLUNTEER v
-- JOIN VOLUNTEER_EVENT ve ON v.volunteer_id = ve.volunteer_id
-- JOIN EVENT e ON ve.event_id = e.event_id
-- JOIN ORGANISATION o ON e.org_id = o.org_id
-- ORDER BY v.last_name;