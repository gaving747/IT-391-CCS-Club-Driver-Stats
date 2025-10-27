# type: ignore
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
import os
from classes.Repository import *
from classes.MySQLRepository import *


app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']  # Needed for flash messages


# -------------------------
# MySQL connection
# -------------------------
db_config = {
   'host': "10.111.21.71",          # VM IP over VPN
   'user': "admin",                 # admin can connect remotely
   'password': os.environ['ADMIN_PASS'],
   'database': "ccsccDB"
}

conn = MySQLConnection(db_config)
db = mysql.connector.connect(**db_config)

# Initialize repositories
account_repo = MySQLAccountRepo(conn)
event_chair_repo = MySQLEventChairRepo(conn)
location_repo = MySQLLocationRepo(conn)
event_repo = MySQLEventRepo(conn)
event_session_repo = MySQLEventSessionRepo(conn)
weather_repo = MySQLWeatherDataRepo(conn)
car_repo = MySQLCarRepo(conn)
session_raw_repo = MySQLSessionRawRepo(conn)
session_pax_repo = MySQLSessionPAXRepo(conn)
session_final_repo = MySQLSessionFinalRepo(conn)
run_repo = MySQLRunRepo(conn)

# -------------------------
# API ROUTES
# -------------------------

# Account routes
@app.route('/api/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        data = request.json
        account_id = account_repo.create_account(
            data['username'],
            data['drivername'],
            data['email'],
            data['password']
        )
        return jsonify({'id': account_id}), 201
    else:
        accounts = account_repo.get_accounts()
        return jsonify(accounts)

@app.route('/api/accounts/<email>', methods=['GET', 'PUT', 'DELETE'])
def account(email):
    if request.method == 'GET':
        account = account_repo.get_account_by_email(email)
        if account:
            return jsonify(account)
        return {'error': 'Account not found'}, 404
    elif request.method == 'PUT':
        account_repo.update_account(email, request.json)
        return '', 204
    else:  # DELETE
        account_repo.delete_account(email)
        return '', 204

# Event Chair routes
@app.route('/api/event-chairs', methods=['GET', 'POST'])
def event_chairs():
    if request.method == 'POST':
        data = request.json
        chair_id = event_chair_repo.create_event_chair(
            data['event_id'],
            data['chair_name']
        )
        return jsonify({'id': chair_id}), 201
    else:
        chairs = event_chair_repo.get_all_event_chairs()
        return jsonify(chairs)

@app.route('/api/event-chairs/<int:event_id>', methods=['GET', 'PUT', 'DELETE'])
def event_chair(event_id):
    if request.method == 'GET':
        chair = event_chair_repo.get_event_chair(event_id)
        if chair:
            return jsonify(chair)
        return {'error': 'Event chair not found'}, 404
    elif request.method == 'PUT':
        event_chair_repo.update_event_chair(event_id, request.json['chair_name'])
        return '', 204
    else:  # DELETE
        event_chair_repo.delete_event_chair(event_id)
        return '', 204

# Location routes
@app.route('/api/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        data = request.json
        location_id = location_repo.create_location(
            data['lat'],
            data['lon'],
            data.get('surface_type'),
            data.get('course_map_url')
        )
        return jsonify({'id': location_id}), 201
    else:
        locations = location_repo.get_locations()
        return jsonify(locations)

@app.route('/api/locations/<int:location_id>', methods=['GET', 'PUT', 'DELETE'])
def location(location_id):
    if request.method == 'GET':
        location = location_repo.get_location(location_id)
        if location:
            return jsonify(location)
        return {'error': 'Location not found'}, 404
    elif request.method == 'PUT':
        location_repo.update_location(location_id, request.json)
        return '', 204
    else:  # DELETE
        location_repo.delete_location(location_id)
        return '', 204

# Event routes
@app.route('/api/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        data = request.json
        event_id = event_repo.create_event(
            data['event_name'],
            data['event_link'],
            data.get('event_notes'),
            data.get('location_id')
        )
        return jsonify({'id': event_id}), 201
    else:
        events = event_repo.get_events()
        return jsonify(events)

@app.route('/api/events/<int:event_id>', methods=['GET', 'PUT', 'DELETE'])
def event(event_id):
    if request.method == 'GET':
        event = event_repo.get_event(event_id)
        if event:
            return jsonify(event)
        return {'error': 'Event not found'}, 404
    elif request.method == 'PUT':
        event_repo.update_event(event_id, request.json)
        return '', 204
    else:  # DELETE
        event_repo.delete_event(event_id)
        return '', 204

# Event Session routes
@app.route('/api/event-sessions', methods=['GET', 'POST'])
def event_sessions():
    if request.method == 'POST':
        data = request.json
        session_date = datetime.strptime(data['evt_session_date'], '%Y-%m-%d').date()
        session_id = event_session_repo.create_event_session(
            session_date,
            data['event_id']
        )
        return jsonify({'id': session_id}), 201
    else:
        event_id = request.args.get('event_id', type=int)
        sessions = event_session_repo.get_event_sessions(event_id)
        return jsonify(sessions)

@app.route('/api/event-sessions/<int:session_id>', methods=['GET', 'PUT', 'DELETE'])
def event_session(session_id):
    if request.method == 'GET':
        session = event_session_repo.get_event_session(session_id)
        if session:
            return jsonify(session)
        return {'error': 'Event session not found'}, 404
    elif request.method == 'PUT':
        event_session_repo.update_event_session(session_id, request.json)
        return '', 204
    else:  # DELETE
        event_session_repo.delete_event_session(session_id)
        return '', 204

# Weather Data routes
@app.route('/api/weather', methods=['POST'])
def create_weather():
    data = request.json
    weather_id = weather_repo.create_weather(
        data['cloud_cover'],
        data['humidity'],
        data['precip'],
        data['high_temp'],
        data['low_temp'],
        data['pressure'],
        data['wind_speed'],
        data['wind_dir'],
        data['event_session_id']
    )
    return jsonify({'id': weather_id}), 201

@app.route('/api/weather/<int:weather_id>', methods=['GET', 'PUT', 'DELETE'])
def weather_data(weather_id):
    if request.method == 'GET':
        weather = weather_repo.get_weather(weather_id)
        if weather:
            return jsonify(weather)
        return {'error': 'Weather data not found'}, 404
    elif request.method == 'PUT':
        weather_repo.update_weather(weather_id, request.json)
        return '', 204
    else:  # DELETE
        weather_repo.delete_weather(weather_id)
        return '', 204

@app.route('/api/weather/session/<int:session_id>', methods=['GET'])
def session_weather(session_id):
    weather = weather_repo.get_weather_for_session(session_id)
    return jsonify(weather)

# Car routes
@app.route('/api/cars', methods=['GET', 'POST'])
def cars():
    if request.method == 'POST':
        data = request.json
        car_id = car_repo.create_car(
            data['car_driver_name'],
            data['car_year'],
            data['car_make'],
            data['car_model'],
            data.get('wheelbase'),
            data.get('mods'),
            data.get('tire_description'),
            data.get('weight')
        )
        return jsonify({'id': car_id}), 201
    else:
        cars = car_repo.get_cars()
        return jsonify(cars)

@app.route('/api/cars/<int:car_id>', methods=['GET', 'PUT', 'DELETE'])
def car(car_id):
    if request.method == 'GET':
        car = car_repo.get_car(car_id)
        if car:
            return jsonify(car)
        return {'error': 'Car not found'}, 404
    elif request.method == 'PUT':
        car_repo.update_car(car_id, request.json)
        return '', 204
    else:  # DELETE
        car_repo.delete_car(car_id)
        return '', 204

# Session Raw Data routes
@app.route('/api/session-raw', methods=['POST'])
def create_session_raw():
    data = request.json
    session_id = session_raw_repo.create_session_raw(
        data['session_class_abrv'],
        data['session_car_num'],
        data['sr_raw_time'],
        data['car_id'],
        data['event_session_id']
    )
    return jsonify({'id': session_id}), 201

@app.route('/api/session-raw/<int:session_id>', methods=['GET', 'PUT', 'DELETE'])
def session_raw(session_id):
    if request.method == 'GET':
        session = session_raw_repo.get_session_raw(session_id)
        if session:
            return jsonify(session)
        return {'error': 'Raw session data not found'}, 404
    elif request.method == 'PUT':
        session_raw_repo.update_session_raw(session_id, request.json)
        return '', 204
    else:  # DELETE
        session_raw_repo.delete_session_raw(session_id)
        return '', 204

@app.route('/api/session-raw/event/<int:event_session_id>', methods=['GET'])
def session_raw_by_event(event_session_id):
    sessions = session_raw_repo.get_session_raw_by_event(event_session_id)
    return jsonify(sessions)

# Session PAX Data routes
@app.route('/api/session-pax', methods=['POST'])
def create_session_pax():
    data = request.json
    session_id = session_pax_repo.create_session_pax(
        data['session_class_abrv'],
        data['session_car_num'],
        data['sp_raw_time'],
        data['sp_pax_factor'],
        data['sp_pax_time'],
        data['car_id'],
        data['event_session_id']
    )
    return jsonify({'id': session_id}), 201

@app.route('/api/session-pax/<int:session_id>', methods=['GET', 'PUT', 'DELETE'])
def session_pax(session_id):
    if request.method == 'GET':
        session = session_pax_repo.get_session_pax(session_id)
        if session:
            return jsonify(session)
        return {'error': 'PAX session data not found'}, 404
    elif request.method == 'PUT':
        session_pax_repo.update_session_pax(session_id, request.json)
        return '', 204
    else:  # DELETE
        session_pax_repo.delete_session_pax(session_id)
        return '', 204

@app.route('/api/session-pax/event/<int:event_session_id>', methods=['GET'])
def session_pax_by_event(event_session_id):
    sessions = session_pax_repo.get_session_pax_by_event(event_session_id)
    return jsonify(sessions)

# Session Final Data routes
@app.route('/api/session-final', methods=['POST'])
def create_session_final():
    data = request.json
    session_id = session_final_repo.create_session_final(
        data['session_class_abrv'],
        data['session_car_num'],
        data['sf_has_trophy'],
        data['sf_car_color'],
        data['car_id'],
        data['event_session_id']
    )
    return jsonify({'id': session_id}), 201

@app.route('/api/session-final/<int:session_id>', methods=['GET', 'PUT', 'DELETE'])
def session_final(session_id):
    if request.method == 'GET':
        session = session_final_repo.get_session_final(session_id)
        if session:
            return jsonify(session)
        return {'error': 'Final session data not found'}, 404
    elif request.method == 'PUT':
        session_final_repo.update_session_final(session_id, request.json)
        return '', 204
    else:  # DELETE
        session_final_repo.delete_session_final(session_id)
        return '', 204

@app.route('/api/session-final/event/<int:event_session_id>', methods=['GET'])
def session_final_by_event(event_session_id):
    sessions = session_final_repo.get_session_final_by_event(event_session_id)
    return jsonify(sessions)

# Run routes
@app.route('/api/runs', methods=['POST'])
def create_run():
    data = request.json
    run_id = run_repo.create_run(
        data['run_time'],
        data['is_dnf'],
        data['num_penalties'],
        data['fsession_id']
    )
    return jsonify({'id': run_id}), 201

@app.route('/api/runs/<int:run_id>', methods=['GET', 'PUT', 'DELETE'])
def run(run_id):
    if request.method == 'GET':
        run = run_repo.get_run(run_id)
        if run:
            return jsonify(run)
        return {'error': 'Run not found'}, 404
    elif request.method == 'PUT':
        run_repo.update_run(run_id, request.json)
        return '', 204
    else:  # DELETE
        run_repo.delete_run(run_id)
        return '', 204

@app.route('/api/runs/session/<int:fsession_id>', methods=['GET'])
def runs_by_session(fsession_id):
    runs = run_repo.get_runs_by_final_session(fsession_id)
    return jsonify(runs)

# -------------------------
# Web Routes
# -------------------------

@app.route('/')
def home():
    """Driver stats home page"""
    return render_template('driver_status_home.html')

@app.route('/schedule_race')
def schedule_race():
    return render_template('schedule_race.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/home_logged_in')
def home_logged_in():
    return render_template('driver_status_logged_in_home.html')

@app.route('/schedule_race_logged_in')
def schedule_race_logged_in():
    return render_template('schedule_race_logged_in.html')

@app.route('/stats_logged_in')
def stats_logged_in():
    return render_template('logged_in_stats.html')

@app.route('/personal_stats')
def personal_stats():
    return render_template('personal_stats.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/profile')
def profile():
    user = {
        'email': session['email'],
        'username': session['username'],
        'drivername': session['drivername']
    }
    return render_template('profile.html', user=user)

'''
@app.route('/garage')
def garage():
    cursor = db.cursor(dictionary=True)
    user_driver_name = session.get('drivername')  # consistent key
     # fetch cars for logged-in user
    cursor.execute(
        "SELECT * FROM Car WHERE car_driver_name = %s ORDER BY car_ID DESC",
        (user_driver_name,)
    )
    cars = cursor.fetchall()

    return render_template('garage.html')
'''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login form submission"""
    if request.method == 'POST':
        email = request.form['username']  # matches HTML input name
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT verify_login(%s, %s)", (email, password))
        result = cursor.fetchone()

        if result and result[0]:  # True if login successful
            flash("Login successful!", "success")
            print("account found")
            return redirect(url_for('home_logged_in'))  # redirect to driver_status_home page
        else:
            flash("Invalid email or password.", "danger")
            print("account not found")
            return redirect(url_for('login'))

    # GET request → show login page
    return render_template('login.html')

'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']  # form input for email
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT verify_login(%s, %s)", (email, password))
        result = cursor.fetchone()

        if result and result[0]:  # True if login successful
            # Fetch the user's details from Account table
            cursor.execute("SELECT act_email, act_username, act_drivername FROM Account WHERE act_email = %s", (email,))
            user = cursor.fetchone()

            # Store info in Flask session (NOT password)
            session['email'] = user[0]
            session['username'] = user[1]
            session['drivername'] = user[2]

            flash("Login successful!", "success")
            print("account found")
            return redirect(url_for('home_logged_in'))
        else:
            flash("Invalid email or password.", "danger")
            print("account not found")
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle account creation form submission"""
    if request.method == 'POST':
        username = request.form['username']
        drivername = request.form['drivername']
        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.callproc('create_account', (username, drivername, email, password))
        db.commit()

        flash("Account created (if email was unique). Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/garage', methods=['GET', 'POST'])
def garage():
    cursor = db.cursor(dictionary=True)
    user_driver_name = session.get('drivername')

    if request.method == 'POST':
        car_year = request.form['car_year']
        car_make = request.form['car_make']
        car_model = request.form['car_model']
        wheelbase = request.form.get('wheelbase', None)
        mods = request.form.get('mods', None)
        tire_description = request.form.get('tire_description', None)
        weight = request.form.get('weight', None)

        cursor.callproc('add_car', (
            user_driver_name, car_year, car_make, car_model,
            wheelbase, mods, tire_description, weight
        ))
        db.commit()
        flash("Car successfully added!", "success")

    # Fetch cars for logged-in user
    cursor.execute(
        "SELECT * FROM Car WHERE car_driver_name = %s ORDER BY car_ID DESC",
        (user_driver_name,)
    )
    cars = cursor.fetchall()

    return render_template('garage.html', cars=cars)



# -------------------------
# RUN FLASK
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
