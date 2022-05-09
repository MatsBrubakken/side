from flask_sqlalchemy  import SQLAlchemy
from side import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

'''Oprettelse af database + tabeller. Modellerne bruges så programmet ved hvor
de forskellige ting ligger i databasen.
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author",lazy=True)

    def __repr__(self):
        #! Det her returnerer brugerens brugernavn, som vi bruger et andet sted for at
        #! give dem adgang til det content de selv har oprettet på siden.
        return f"User('{self.username})"


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    link = db.Column(db.String(100), nullable=False)
    date_posted =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_date = db.Column(db.Date)
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255))
    thumbnail = db.Column(db.String(20))
    event_picture = db.Column(db.String(20))
    user_id= db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False) #! User ID referer til brugerens ID som har oprettet eventet

    def __repr__(self):
        #! returnerer kombineret info om hvilken bruger har oprettet eventet
        return f"User('{self.title}, {self.date_posted}, {self.thumbnail}, {self.event_picture}')"
