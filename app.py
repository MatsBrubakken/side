from ast import Sub
from crypt import methods
from email.policy import default
from tokenize import String
from flask import Flask, render_template, url_for, redirect, abort
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_required, login_user, LoginManager, current_user, logout_user
import pymysql
import secrets
import os
from PIL import Image



app = Flask(__name__)
app.config["SECRET_KEY"]="1234"
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:admin@localhost/dummyside"
db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    thumbnail = db.Column(db.String(20))
    event_picture = db.Column(db.String(20))
    user_id= db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

    def __repr__(self):
        return f"User('{self.title}, {self.date_posted}, {self.thumbnail}, {self.event_picture}')"


class RegistrationForm(FlaskForm):
    username=StringField("Brugernavn", validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder": "Brugernavn"})
    password=PasswordField("Adgangskode", validators=[DataRequired()],render_kw={"placeholder": "Adgangskode"})
    confirm_password=PasswordField("Bekræft Adgangskode", validators=[DataRequired(),EqualTo("password")],render_kw={"placeholder": "Bekræft Adgangskode"})
    submit = SubmitField("Opret Bruger")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Brugernavn Taget")

class LoginForm(FlaskForm):
    username = StringField("Brugernavn", validators=[DataRequired(), Length(min = 2, max = 20)], render_kw={"placeholder": "Brugernavn"})
    password = PasswordField("Adgangskode", validators=[DataRequired()], render_kw={"placeholder": "Adgangskode"})
    submit = SubmitField("Log ind")


class EventForm(FlaskForm):
    title = StringField("Overskrift", validators=[DataRequired()], render_kw={"placeholder": "Overskrift"})
    content = TextAreaField("Indhold", validators=[DataRequired()], render_kw={"placeholder": "Indhold"})
    thumbnail = FileField("Thumbnail billede", validators=[FileAllowed(["jpg", "png"])])
    event_picture = FileField("Event billede", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Opret event")


@app.route("/home")
@app.route('/')
def home():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template("home.html",title="Hjem", posts=posts)

@app.route('/opret', methods=['GET', 'POST'])
def opret():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("opret.html",title="Opret",form=form)

@app.route("/logind", methods=["POST", "GET"])
def logind():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.query.filter_by(password=form.password.data).first():
            login_user(user)
            return redirect(url_for('home'))
    return render_template("logind.html", form=form)


@app.route("/logud")
def logout():
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def save_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    output_size = (250,250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn




@app.route("/opret_event", methods=["POST", "GET"])
def opret_event():
    form = EventForm()
    if form.validate_on_submit():
        thumbnail_pic = None
        event_pic = None
        if form.thumbnail.data:
            thumbnail_pic = save_picture(form.thumbnail.data)
        if form.event_picture.data:
            event_pic = save_picture(form.event_picture.data)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, thumbnail=thumbnail_pic, event_picture=event_pic)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("opret_event.html", form=form)



@app.route("/omos")
def omos():
    return render_template("omos.html")


@app.route("/event/<int:event_id>")
def event(event_id):
    post = Post.query.get_or_404(event_id)
    return render_template("event.html", title=post.title, post=post)


@app.route("/event/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_post(event_id):
    post = Post.query.get_or_404(event_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

