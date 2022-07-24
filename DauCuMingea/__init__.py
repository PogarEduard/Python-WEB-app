from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import socket
import os



app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tt8546496@gmail.com'
app.config['MAIL_PASSWORD'] = 'xgspfffujdwijevt'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SECRET_KEY'] = '8942408b86aa144b7a2c5a6a'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from DauCuMingea import routes



