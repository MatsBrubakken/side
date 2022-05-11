from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




app = Flask(__name__)
app.config["SECRET_KEY"]="1234"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:admin@localhost/dummyside"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from side import routes