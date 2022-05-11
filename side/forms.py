
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from side.models import User


'''Bruges i html.
Classen gør det muligt for html og databasen at snakke sammen, så vi slipper for at døje 
med POST og GET. Disse erstatter submitfields i HTML'''
class RegistrationForm(FlaskForm): 
    '''Oprettelse af brugere, husk at alle brugere har admin privilegier, og kan slette/oprette events'''
    username=StringField("Brugernavn", validators=[DataRequired(), Length(min=2,max=20)], render_kw={"placeholder": "Brugernavn"})
    password=PasswordField("Adgangskode",render_kw={"placeholder": "Adgangskode"})
    confirm_password=PasswordField("Bekræft Adgangskode", validators=[DataRequired(),EqualTo("password")],render_kw={"placeholder": "Bekræft Adgangskode"})
    submit = SubmitField("Opret Bruger")
    def validate_username(self,username):
        #! Her tjekker vi om brugernanet allerede findes, hvis det gør så får de en besked.
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Brugernavn Taget")

class LoginForm(FlaskForm):
    #* Logind formen
    username = StringField("Brugernavn", validators=[DataRequired(), Length(min = 2, max = 20)], render_kw={"placeholder": "Brugernavn"})
    password = PasswordField("Adgangskode", validators=[DataRequired()], render_kw={"placeholder": "Adgangskode"})
    submit = SubmitField("Log ind")

# * Oprettelse af et event
class EventForm(FlaskForm):
    link = StringField("link", validators=[DataRequired()], render_kw={"placeholder": "YourTicket link"})
    pris=StringField("Pris")
    event_date = DateField("Dato")
    title = StringField("Overskrift", validators=[DataRequired()], render_kw={"placeholder": "Overskrift"})
    content = TextAreaField("Indhold", validators=[DataRequired()], render_kw={"placeholder": "Indhold"})
    thumbnail = FileField("Thumbnail billede", validators=[FileAllowed(["jpg", "png"])])
    event_picture = FileField("Event billede", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Opret event")
