from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager




app = Flask(__name__)
app.config["SECRET_KEY"]="1234"
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://nbfptvkuaepcpb:93e79606b53715be5bd8b0c2c86f8c40662c490eecbb9b5323129860752b4b22@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/d546vtlf0ekjsd"
#/app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:admin@localhost/dummyside"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from side import routes