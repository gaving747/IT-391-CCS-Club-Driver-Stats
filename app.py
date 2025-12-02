# type: ignore
from flask import Flask
import os
import mysql.connector
import logging
from classes.MySQLRepository import *
from classes.Requestor import Requestor,WeatherRequestor
from classes.EventPageScraper import EventPageScraper
from datetime import datetime
from logging.handlers import RotatingFileHandler




# Import blueprints
from blueprints.accounts import api_accounts, init_account_routes
from blueprints.events import api_events, init_event_routes
from blueprints.locations import api_locations, init_location_routes
from blueprints.cars import api_cars, init_car_routes
from blueprints.weather import api_weather, init_weather_routes
from blueprints.sessions import api_sessions, init_session_routes
from blueprints.runs import api_runs, init_run_routes
from blueprints.web import web_routes, init_web_routes
from blueprints.scraping import api_scrape, init_scrape_routes

app = Flask(__name__)
app.secret_key = 'asdasdsadsadsa'



#Initiating logger
os.makedirs('logs',exist_ok=True)

logger = app.logger
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler('application.log', maxBytes=1024 * 1024 * 10, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)



logging.basicConfig(level=logging.DEBUG,handlers=[file_handler,stream_handler])

# -------------------------
# Database Configuration
# -------------------------
db_config = {
    'host': "10.111.21.71",          # VM IP over VPN
    'user': "admin",                 # admin can connect remotely
    'password': 'admin#ab12cd34',
    'database': "ccsccDB"
}

# Initialize database connection and repositories
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


#Initialize scraping utilities
requestor = Requestor(allowed_requests=200)
weather_requestor = WeatherRequestor('FakeKey, Not needed', allowed_requests=200)
event_page_scraper = EventPageScraper(requestor)

# -------------------------
# Initialize Blueprints
# -------------------------

# Initialize route handlers in blueprints
init_account_routes(account_repo)
init_event_routes(event_repo, event_chair_repo, event_session_repo) 
init_location_routes(location_repo)
init_car_routes(car_repo)
init_weather_routes(weather_repo)
init_session_routes(session_raw_repo, session_pax_repo, session_final_repo)
init_run_routes(run_repo)
init_web_routes(account_repo, event_chair_repo,location_repo,event_repo,event_session_repo,weather_repo,car_repo,session_raw_repo,session_pax_repo,session_final_repo,run_repo, db)
init_scrape_routes(weather_requestor, event_page_scraper, event_chair_repo,location_repo,event_repo,event_session_repo,weather_repo,car_repo,session_raw_repo,session_pax_repo,session_final_repo,run_repo)

# Register blueprints
app.register_blueprint(api_accounts)
app.register_blueprint(api_events)
app.register_blueprint(api_locations)
app.register_blueprint(api_cars)
app.register_blueprint(api_weather)
app.register_blueprint(api_sessions)
app.register_blueprint(api_runs)
app.register_blueprint(web_routes)
app.register_blueprint(api_scrape)

# -------------------------
# Run Flask Application
# -------------------------

if __name__ == '__main__':
    app.run(debug=True)
