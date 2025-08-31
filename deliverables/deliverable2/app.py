"""
Community Connect Flask Web Application
Week 2 Deliverable: Database Implementation and Basic Application
Author: Daniel Bai
Date: 2025
Description: Flask web application implementing CRUD operations for the Community Connect system
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    create_volunteer, get_all_volunteers, get_volunteer_by_id, update_volunteer_phone,
    get_all_organisations, get_all_events, get_event_by_id, delete_event,
    validate_email, validate_phone, test_database_connection
)
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'community_connect_secret_key_2025'  # For flash messages

# ====================================
# HOME AND NAVIGATION ROUTES
# ====================================

@app.route('/')
def index():
    """
    Home page showing system overview and navigation options
    """
    # Test database connection
    db_status = test_database_connection()
    
    # Get counts for dashboard
    volunteers = get_all_volunteers()
    organisations = get_all_organisations()
    events = get_all_events()
    
    volunteer_count = len(volunteers) if volunteers else 0
    organisation_count = len(organisations) if organisations else 0
    event_count = len(events) if events else 0
    
    return render_template('index.html', 
                         db_status=db_status,
                         volunteer_count=volunteer_count,
                         organisation_count=organisation_count,
                         event_count=event_count)

# ====================================
# CREATE OPERATIONS
# ====================================

@app.route('/volunteers/new', methods=['GET', 'POST'])
def new_volunteer():
    """
    CREATE Operation: Form to add a new volunteer to the database
    """
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        date_of_birth = request.form.get('date_of_birth', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        # Validation
        errors = []
        if not first_name:
            errors.append("First name is required")
        if not last_name:
            errors.append("Last name is required")
        if not date_of_birth:
            errors.append("Date of birth is required")
        if not email or not validate_email(email):
            errors.append("Valid email address is required")
        if not phone or not validate_phone(phone):
            errors.append("Valid phone number is required")
        if not address:
            errors.append("Address is required")
        
        # Check date of birth is not in the future
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
            if dob.date() >= datetime.now().date():
                errors.append("Date of birth must be in the past")
        except ValueError:
            errors.append("Invalid date format")
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('new_volunteer.html', 
                                 first_name=first_name, last_name=last_name,
                                 date_of_birth=date_of_birth, email=email,
                                 phone=phone, address=address)
        
        # Create volunteer
        volunteer_id = create_volunteer(first_name, last_name, date_of_birth, email, phone, address)
        
        if volunteer_id:
            flash(f'Volunteer {first_name} {last_name} created successfully!', 'success')
            return redirect(url_for('view_volunteers'))
        else:
            flash('Error creating volunteer. Please check your input and try again.', 'error')
            return render_template('new_volunteer.html', 
                                 first_name=first_name, last_name=last_name,
                                 date_of_birth=date_of_birth, email=email,
                                 phone=phone, address=address)
    
    # GET request - show form
    return render_template('new_volunteer.html')

# ====================================
# READ OPERATIONS
# ====================================

@app.route('/organisations')
def view_organisations():
    """
    READ Operation: Display all organisations from the database
    """
    organisations = get_all_organisations()
    
    if organisations is None:
        flash('Error retrieving organisations from database', 'error')
        organisations = []
    
    return render_template('view_organisations.html', organisations=organisations)

@app.route('/volunteers')
def view_volunteers():
    """
    Additional READ Operation: Display all volunteers (for navigation)
    """
    volunteers = get_all_volunteers()
    
    if volunteers is None:
        flash('Error retrieving volunteers from database', 'error')
        volunteers = []
    
    return render_template('view_volunteers.html', volunteers=volunteers)

# ====================================
# UPDATE OPERATIONS
# ====================================

@app.route('/volunteers/<int:volunteer_id>/update_phone', methods=['GET', 'POST'])
def update_volunteer_contact(volunteer_id):
    """
    UPDATE Operation: Form to update a volunteer's contact number
    """
    # Get volunteer details
    volunteer = get_volunteer_by_id(volunteer_id)
    if not volunteer:
        flash('Volunteer not found', 'error')
        return redirect(url_for('view_volunteers'))
    
    if request.method == 'POST':
        new_phone = request.form.get('phone', '').strip()
        
        # Validation
        if not new_phone:
            flash('Phone number is required', 'error')
            return render_template('update_volunteer_phone.html', volunteer=volunteer, new_phone=new_phone)
        
        if not validate_phone(new_phone):
            flash('Please enter a valid phone number', 'error')
            return render_template('update_volunteer_phone.html', volunteer=volunteer, new_phone=new_phone)
        
        # Update phone number
        rows_affected = update_volunteer_phone(volunteer_id, new_phone)
        
        if rows_affected and rows_affected > 0:
            flash(f'Phone number updated successfully for {volunteer["first_name"]} {volunteer["last_name"]}', 'success')
            return redirect(url_for('view_volunteers'))
        else:
            flash('Error updating phone number. Please try again.', 'error')
            return render_template('update_volunteer_phone.html', volunteer=volunteer, new_phone=new_phone)
    
    # GET request - show form
    return render_template('update_volunteer_phone.html', volunteer=volunteer)

# ====================================
# DELETE OPERATIONS
# ====================================

@app.route('/events')
def view_events():
    """
    Display all events (needed for delete operation)
    """
    events = get_all_events()
    
    if events is None:
        flash('Error retrieving events from database', 'error')
        events = []
    
    return render_template('view_events.html', events=events)

@app.route('/events/<int:event_id>/delete', methods=['POST'])
def delete_event_route(event_id):
    """
    DELETE Operation: Remove a specific event from the database
    """
    # Get event details for confirmation
    event = get_event_by_id(event_id)
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('view_events'))
    
    # Delete the event
    rows_affected = delete_event(event_id)
    
    if rows_affected and rows_affected > 0:
        flash(f'Event "{event["event_name"]}" deleted successfully', 'success')
    else:
        flash('Error deleting event. Please try again.', 'error')
    
    return redirect(url_for('view_events'))

# API endpoints removed for basic CRUD implementation

# ====================================
# ERROR HANDLERS
# ====================================

@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors
    """
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Handle 500 errors
    """
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

# Template filters removed for basic implementation

# ====================================
# APPLICATION STARTUP
# ====================================

if __name__ == '__main__':
    # Test database connection on startup
    if not test_database_connection():
        print("⚠️  WARNING: Database connection test failed!")
        print("   Make sure 'community_connect.db' exists in the same directory")
    else:
        print("✓ Database connection successful!")
    
    # Run Flask application
    print("Starting Community Connect web application...")
    print("Visit http://localhost:5000 to view the application")
    
    # Run in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)