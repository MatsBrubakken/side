from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




app = Flask(__name__)
app.config["SECRET_KEY"]="1234"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://bfafd66faf5a08:d7111510@eu-cdbr-west-02.cleardb.net/heroku_6e8715942acc2da?reconnect=true"
#/app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:admin@localhost/dummyside"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from side import routes