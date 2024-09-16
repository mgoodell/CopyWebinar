# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime
import pytz
import src.get_webinar_id
import src.copy_webinar
import src.get_webinar_info
import src.date_to_iso_format

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random 24-character secret key

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        webinar_key = request.form.get('webinarKey')
        api_key = request.form.get('apiKey')
        api_secret = request.form.get('apiSecret')

        # Get Webinar ID
        webinar_id = src.get_webinar_id.fetch_all_webinar_data(webinar_key, api_key, api_secret)

        if webinar_id:
            session['webinar_id'] = webinar_id
            session['api_key'] = api_key  # Store API credentials
            session['api_secret'] = api_secret  # Store API credentials
            return redirect(url_for('copy'))
        else:
            session.pop('_flashes', None)
            flash('Webinar not found. Please check your credentials.', 'error')

    return render_template('home.html')

@app.route('/copy', methods=['GET', 'POST'])
def copy():
    # Retrieve webinar_id and credentials from the session
    webinar_id = session.get('webinar_id', None)
    api_key = session.get('api_key', None)
    api_secret = session.get('api_secret', None)

    if request.method == 'POST':
        action = request.form.get('action', 'copy')  # Check which action was triggered

        if action == 'cancel':
            # Clear flash messages and redirect to home page
            session.pop('_flashes', None)
            return redirect(url_for('home'))
        elif action == 'copy':
            if webinar_id:
                # Gather form data
                title = request.form.get('title')
                source = request.form.get('source')
                schedule_type = request.form.get('type')
                schedule_start = request.form.get('start')
                schedule_end = request.form.get('end')
                time_zone = request.form.get('timeZone')
                copy_media = request.form.get('copyMedia') == 'Yes'  # Convert to boolean

                # Convert start and end times to ISO 8601 format
                try:
                    schedule_start_iso, schedule_end_iso = src.date_to_iso_format.convert_to_iso_format(schedule_start,
                                                                                                        schedule_end,
                                                                                                        time_zone)
                except ValueError:
                    flash('Invalid date or time format. Please use the correct format (YYYY-MM-DDTHH:MM).', 'error')
                    return redirect(url_for('copy'))

                # Call the function to copy the webinar
                success, message = src.copy_webinar.webinar_copy(webinar_id, api_key, api_secret, title, source,
                                                                 schedule_type, schedule_start_iso, schedule_end_iso,
                                                                 time_zone, copy_media)

                if success:
                    # Redirect to the webinar page with the new webinar ID
                    return redirect(url_for('webinar'))
                else:
                    flash(message, 'error')
            else:
                flash('Webinar ID not found. Please try again.', 'error')
            return redirect(url_for('home'))

    return render_template('copy.html')

@app.route('/webinar', methods=['GET'])
def webinar():
    # Retrieve webinar_id and credentials from the session
    new_webinar_id = session.get('new_webinar_id', None)
    api_key = session.get('api_key', None)
    api_secret = session.get('api_secret', None)

    if not new_webinar_id:
        flash('New webinar ID not found. Please try again.', 'error')
        return redirect(url_for('home'))

    # Fetch webinar details
    details = src.get_webinar_info.fetch_webinar_details(new_webinar_id, api_key, api_secret)

    # Format the Start Date/Time
    formatted_start = src.date_to_iso_format.format_datetime(details['webinar']['latestSchedule']['start'])
    details['webinar']['formatted_start'] = formatted_start

    if not details:
        flash('Failed to retrieve webinar details.', 'error')
        return redirect(url_for('home'))

    return render_template('webinar.html', details=details)

@app.route('/clear_flash_and_return')
def clear_flash_and_return():
    # Clear flash messages
    session.pop('_flashes', None)
    # Redirect to the home page
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
