"""
Database helper functions for Community Connect application
Week 2 Deliverable: Database Implementation
Author: Daniel Bai
Date: 2025
Description: SQLite database connectivity and helper functions for CRUD operations
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