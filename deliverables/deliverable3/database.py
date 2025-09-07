"""
Database helper functions for Community Connect application
Week 3 Deliverable: Advanced Queries, Evaluation, and Reporting
Author: Daniel Bai
Date: 2025
Description: Enhanced SQLite database connectivity with advanced queries for complex reporting
"""

import sqlite3
import os
from datetime import datetime

DATABASE_NAME = 'community_connect.db'

def get_db_connection():
    """
    Create and return a database connection with proper settings
    Returns: sqlite3.Connection object with row factory enabled
    """
    try:
        # Get the absolute path to the database file
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATABASE_NAME)
        
        # Create connection
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        
        # Enable foreign key constraints
        conn.execute('PRAGMA foreign_keys = ON')
        
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """
    Execute a SQL query with optional parameters
    
    Args:
        query (str): SQL query to execute
        params (tuple): Optional parameters for the query
        fetch (bool): Whether to fetch results (True for SELECT, False for INSERT/UPDATE/DELETE)
    
    Returns:
        For SELECT: List of results or None if error
        For INSERT/UPDATE/DELETE: Number of affected rows or None if error
    """
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            results = cursor.fetchall()
            conn.close()
            return results
        else:
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected
            
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
        conn.close()
        return None

# ====================================
# VOLUNTEER CRUD OPERATIONS
# ====================================

def create_volunteer(first_name, last_name, date_of_birth, email, phone, address):
    """
    Insert a new volunteer into the database
    
    Returns:
        int: volunteer_id if successful, None if failed
    """
    query = """
    INSERT INTO VOLUNTEER (first_name, last_name, date_of_birth, email, phone, address)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (first_name, last_name, date_of_birth, email, phone, address))
        volunteer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return volunteer_id
    except sqlite3.Error as e:
        print(f"Error creating volunteer: {e}")
        conn.close()
        return None

def get_all_volunteers():
    """
    Retrieve all volunteers from the database
    
    Returns:
        List of volunteer records or None if error
    """
    query = """
    SELECT volunteer_id, first_name, last_name, date_of_birth, email, phone, address, registration_date
    FROM VOLUNTEER
    ORDER BY last_name, first_name
    """
    return execute_query(query, fetch=True)

def get_volunteer_by_id(volunteer_id):
    """
    Retrieve a specific volunteer by ID
    
    Returns:
        Single volunteer record or None if not found/error
    """
    query = """
    SELECT volunteer_id, first_name, last_name, date_of_birth, email, phone, address, registration_date
    FROM VOLUNTEER
    WHERE volunteer_id = ?
    """
    results = execute_query(query, (volunteer_id,), fetch=True)
    return results[0] if results else None

def update_volunteer_phone(volunteer_id, new_phone):
    """
    Update a volunteer's phone number
    
    Returns:
        Number of rows affected or None if error
    """
    query = """
    UPDATE VOLUNTEER
    SET phone = ?
    WHERE volunteer_id = ?
    """
    return execute_query(query, (new_phone, volunteer_id))

# ====================================
# ORGANISATION CRUD OPERATIONS
# ====================================

def get_all_organisations():
    """
    Retrieve all organisations from the database
    
    Returns:
        List of organisation records or None if error
    """
    query = """
    SELECT org_id, org_name, contact_email, phone, address, org_type, description
    FROM ORGANISATION
    ORDER BY org_name
    """
    return execute_query(query, fetch=True)

def get_organisation_by_id(org_id):
    """
    Retrieve a specific organisation by ID
    
    Returns:
        Single organisation record or None if not found/error
    """
    query = """
    SELECT org_id, org_name, contact_email, phone, address, org_type, description
    FROM ORGANISATION
    WHERE org_id = ?
    """
    results = execute_query(query, (org_id,), fetch=True)
    return results[0] if results else None

# ====================================
# EVENT CRUD OPERATIONS
# ====================================

def get_all_events():
    """
    Retrieve all events with organisation information
    
    Returns:
        List of event records with organisation names or None if error
    """
    query = """
    SELECT e.event_id, e.event_name, e.description, e.start_date, e.end_date, 
           e.location, e.max_volunteers, o.org_name
    FROM EVENT e
    JOIN ORGANISATION o ON e.org_id = o.org_id
    ORDER BY e.start_date
    """
    return execute_query(query, fetch=True)

def get_event_by_id(event_id):
    """
    Retrieve a specific event by ID with organisation information
    
    Returns:
        Single event record or None if not found/error
    """
    query = """
    SELECT e.event_id, e.event_name, e.description, e.start_date, e.end_date, 
           e.location, e.max_volunteers, o.org_name, o.org_id
    FROM EVENT e
    JOIN ORGANISATION o ON e.org_id = o.org_id
    WHERE e.event_id = ?
    """
    results = execute_query(query, (event_id,), fetch=True)
    return results[0] if results else None

def delete_event(event_id):
    """
    Delete a specific event from the database
    
    Returns:
        Number of rows affected or None if error
    """
    query = """
    DELETE FROM EVENT
    WHERE event_id = ?
    """
    return execute_query(query, (event_id,))

# ====================================
# ADVANCED QUERIES (WEEK 3)
# ====================================

def search_volunteers_by_skill(skill_name):
    """
    Search for volunteers who possess a specific skill
    
    Args:
        skill_name (str): Name of the skill to search for
        
    Returns:
        List of volunteer records with skill information or None if error
    """
    query = """
    SELECT DISTINCT v.volunteer_id, v.first_name, v.last_name, v.email, v.phone,
           vs.proficiency_level, vs.years_experience
    FROM VOLUNTEER v
    JOIN VOLUNTEER_SKILL vs ON v.volunteer_id = vs.volunteer_id
    JOIN SKILL s ON vs.skill_id = s.skill_id
    WHERE s.skill_name LIKE ?
    ORDER BY vs.proficiency_level DESC, vs.years_experience DESC
    """
    return execute_query(query, (f'%{skill_name}%',), fetch=True)

def get_volunteers_for_organisation_events(org_id):
    """
    Get all volunteers signed up for events from a specific organisation
    Requires INNER JOIN across 3+ tables: VOLUNTEER, VOLUNTEER_EVENT, EVENT
    
    Args:
        org_id (int): Organisation ID
        
    Returns:
        List of volunteer records with event details or None if error
    """
    query = """
    SELECT v.volunteer_id, v.first_name, v.last_name, v.email, v.phone,
           e.event_name, e.start_date, e.location,
           ve.registration_date, ve.attendance_status,
           o.org_name
    FROM VOLUNTEER v
    INNER JOIN VOLUNTEER_EVENT ve ON v.volunteer_id = ve.volunteer_id
    INNER JOIN EVENT e ON ve.event_id = e.event_id
    INNER JOIN ORGANISATION o ON e.org_id = o.org_id
    WHERE o.org_id = ?
    ORDER BY e.start_date, v.last_name, v.first_name
    """
    return execute_query(query, (org_id,), fetch=True)

def get_event_statistics():
    """
    Get aggregate statistics for events using COUNT and GROUP BY
    Shows volunteer count per event and average event duration
    
    Returns:
        List of event statistics or None if error
    """
    query = """
    SELECT e.event_name, o.org_name,
           COUNT(ve.volunteer_id) as volunteer_count,
           e.max_volunteers,
           e.start_date, e.end_date,
           CAST((julianday(e.end_date) - julianday(e.start_date)) AS INTEGER) as duration_days,
           CASE 
               WHEN COUNT(ve.volunteer_id) >= e.max_volunteers THEN 'Full'
               WHEN COUNT(ve.volunteer_id) > 0 THEN 'Partial'
               ELSE 'Empty'
           END as status
    FROM EVENT e
    JOIN ORGANISATION o ON e.org_id = o.org_id
    LEFT JOIN VOLUNTEER_EVENT ve ON e.event_id = ve.event_id
    GROUP BY e.event_id, e.event_name, o.org_name, e.max_volunteers, e.start_date, e.end_date
    ORDER BY volunteer_count DESC
    """
    return execute_query(query, fetch=True)

def get_volunteers_with_calculated_fields():
    """
    Display volunteers with concatenated full name and calculated age
    Uses aliases for calculated fields
    
    Returns:
        List of volunteer records with calculated fields or None if error
    """
    query = """
    SELECT volunteer_id,
           (first_name || ' ' || last_name) as full_name,
           email, phone, address,
           date_of_birth,
           CAST((julianday('now') - julianday(date_of_birth)) / 365.25 AS INTEGER) as age,
           registration_date
    FROM VOLUNTEER
    ORDER BY full_name
    """
    return execute_query(query, fetch=True)

def get_skill_distribution():
    """
    Get distribution of skills among volunteers using aggregate functions
    
    Returns:
        List of skill distribution statistics or None if error
    """
    query = """
    SELECT s.skill_name, s.skill_category,
           COUNT(vs.volunteer_id) as volunteer_count,
           AVG(vs.years_experience) as avg_experience,
           MAX(vs.years_experience) as max_experience,
           MIN(vs.years_experience) as min_experience
    FROM SKILL s
    LEFT JOIN VOLUNTEER_SKILL vs ON s.skill_id = vs.skill_id
    GROUP BY s.skill_id, s.skill_name, s.skill_category
    HAVING COUNT(vs.volunteer_id) > 0
    ORDER BY volunteer_count DESC, s.skill_category
    """
    return execute_query(query, fetch=True)

def get_organisation_event_summary():
    """
    Summary of events and volunteer engagement per organisation
    
    Returns:
        List of organisation statistics or None if error
    """
    query = """
    SELECT o.org_name, o.org_type,
           COUNT(DISTINCT e.event_id) as total_events,
           COUNT(DISTINCT ve.volunteer_id) as unique_volunteers,
           COUNT(ve.volunteer_id) as total_registrations,
           AVG(e.max_volunteers) as avg_event_capacity
    FROM ORGANISATION o
    LEFT JOIN EVENT e ON o.org_id = e.org_id
    LEFT JOIN VOLUNTEER_EVENT ve ON e.event_id = ve.event_id
    GROUP BY o.org_id, o.org_name, o.org_type
    ORDER BY total_events DESC, unique_volunteers DESC
    """
    return execute_query(query, fetch=True)

def get_all_skills():
    """
    Retrieve all skills for search functionality
    
    Returns:
        List of skill records or None if error
    """
    query = """
    SELECT skill_id, skill_name, skill_description, skill_category
    FROM SKILL
    ORDER BY skill_category, skill_name
    """
    return execute_query(query, fetch=True)

# ====================================
# UTILITY FUNCTIONS
# ====================================

def validate_email(email):
    """
    Basic email validation
    
    Returns:
        bool: True if email appears valid, False otherwise
    """
    return '@' in email and '.' in email.split('@')[-1]

def validate_phone(phone):
    """
    Basic Australian phone number validation
    
    Returns:
        bool: True if phone appears valid, False otherwise
    """
    # Remove common separators and spaces
    clean_phone = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    
    # Check if it's all digits and appropriate length
    return clean_phone.isdigit() and len(clean_phone) >= 10

def test_database_connection():
    """
    Test the database connection and basic functionality
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    conn = get_db_connection()
    if conn is None:
        return False
    
    try:
        # Test query to verify database structure
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        expected_tables = {'VOLUNTEER', 'ORGANISATION', 'SKILL', 'EVENT', 'VOLUNTEER_EVENT', 'VOLUNTEER_SKILL', 'EVENT_SKILL'}
        actual_tables = {table[0] for table in tables}
        
        conn.close()
        return expected_tables.issubset(actual_tables)
        
    except sqlite3.Error as e:
        print(f"Database test error: {e}")
        conn.close()
        return False

if __name__ == "__main__":
    # Test database connection when run directly
    if test_database_connection():
        print("✓ Database connection successful!")
        
        # Show some sample data
        volunteers = get_all_volunteers()
        print(f"✓ Found {len(volunteers) if volunteers else 0} volunteers in database")
        
        organisations = get_all_organisations()
        print(f"✓ Found {len(organisations) if organisations else 0} organisations in database")
        
        events = get_all_events()
        print(f"✓ Found {len(events) if events else 0} events in database")
        
    else:
        print("✗ Database connection failed!")