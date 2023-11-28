from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from celery.schedules import crontab
from flask_caching import Cache

# Resource, reqparse, abort, fields, marshal_with
# from flask_mail import Mail


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_mad2.sqlite3'  # using SQLite for simplicity
# sqlite:///kanaban.sqlite3

jwt = JWTManager(app)
db = SQLAlchemy(app)
api = Api(app)
CORS(app, methods=["GET", "POST", "PUT", "DELETE"])

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
    })  # Adjust URL as needed


# app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = '4912b49f78f45d'
# app.config['MAIL_PASSWORD'] = '38bef1d68e399b'
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '78576668ea1e25'
app.config['MAIL_PASSWORD'] = '0127d70e78b00a'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


app.config["CELERY_CONFIG"] = {
    "broker_url": "redis://localhost:6379/0", 
    "result_backend": "redis://localhost:6379/1",
    "beat_schedule":{
        'mail-every-40-seconds': {
            'task': 'backend.routes.send_email',
            'schedule':crontab(minute='*/10'),
            # 'schedule':crontab(hour='19'),
            # 'schedule':crontab(hour='23', minute='29'),
            # # 'args': (),
        },
        'mail-html-reports': {
            'task': 'backend.routes.send_reports_email',
            'schedule':crontab(minute='*/10'),
            # 'schedule': 20,
            # 'schedule':crontab(day_of_month='1'),
            # 'schedule':crontab(hour='23', minute='29'),
            # # 'args': (),
        },
    }
}

# from backend import create_admin
from backend import api_file, routes

