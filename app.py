from email.policy import default
from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
import pymysql




app = Flask(__name__)
app.config["SECRET_KEY"]="1234"

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:admin@localhost/dummyside"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author",lazy=True)

    def __repr__(self):
        return f"User('{self.username})"


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)


class RegistrationForm(FlaskForm):
    username=StringField("Brugernavn", validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder": "Brugernavn"})
    password=PasswordField("Adgangskode", validators=[DataRequired()],render_kw={"placeholder": "Adgangskode"})
    confirm_password=PasswordField("Bekræft Adgangskode", validators=[DataRequired(),EqualTo("password")],render_kw={"placeholder": "Bekræft Adgangskode"})
    submit = SubmitField("Opret Bruger")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Brugernavn Taget")


@app.route('/')
def home():
    return render_template("home.html",title="Hjem")

@app.route('/opret', methods=['GET', 'POST'])
def opret():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("opret.html",title="Opret",form=form)



if __name__ == "__main__":
    app.run(debug=True)

