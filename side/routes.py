from flask import render_template, url_for, redirect, abort, request
from side import app, db
from flask_login import login_user, login_required, current_user, logout_user
from side.forms import RegistrationForm, EventForm, LoginForm
from side.models import User, Post
from sqlalchemy import asc
import secrets
import os
from PIL import Image




# Route til homesiden
@app.route("/home")
@app.route('/')
def home():
    """Viser hovedsiden med alle posts fra DB"""
    page = request.args.get('page', 1, type=int)
    # Gemmer alle posts fra database i rækkefølgen de blev postet i posts variabel
    post = Post.query.order_by(Post.event_date.asc()).paginate(per_page=6,page=page)
    # Sender posts variablen ind i HTML filen home.html, sådan at den kan bruges der.
    return render_template("home.html",title="Hjem", post=post)


# Route til at oprette bruger. GET OG POST method fordi de skal loade hjemmesiden og kunne oprette
@app.route('/opret', methods=['GET', 'POST'])
def opret():
    """Opretter en bruger og gemmer i databasen"""
    form = RegistrationForm()
    # Tjekker om RegFormen kommer igennem validatorne der er sat og kører det er efterfølg er IF
    # hvis den validerer
    if form.validate_on_submit():
        # user variablen sætter info fra formen i de forskellige tabeller i database
        user = User(username=form.username.data, password=form.password.data)
        # add tilføjer infoen som skal ind i databasen
        db.session.add(user)
        # commit gemmer databasen
        db.session.commit()
        return redirect(url_for("home"))
    # form variablen sender RegFormen ind i HTML filen sådan at den kan blive brugt.
    return render_template("opret.html",title="Opret",form=form)


# Route til logind. POST og GET fordi man kan loade hjemmesiden og logge ind
@app.route("/logind", methods=["POST", "GET"])
def logind():
    """Tjekker om bruger eksisterer og logger ind hvis den gør"""
    # Hvis brugeren allerede er logget ind bliver man smidt til hovedsiden
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    # Sætter variable form = LoginForm så formen kan bruges
    form = LoginForm()
    # Tjekker om formen der bliver submittet kommer igennem de forskellige validatorer
    if form.validate_on_submit():
        # user variable søger databasen efter username der bliver skrevet ind i formen. 
        # username er unik så den tager den første den finder
        user = User.query.filter_by(username=form.username.data).first()
        # Hvis bruernavnet eksisterer tjekker den om koden tilsvarer brugerens kode i DB
        if user and User.query.filter_by(password=form.password.data).first():
            # Logger bruger ind hvis alt passer og sender dem til hovedsiden
            login_user(user)
            return redirect(url_for('home'))
    # formen LoginForm bliver sendt til HTML filen så den kan bruges. Dette er det første der sker
    # når en bruger besøger siden. Alt overstående sker hvis formen bliver submittet
    return render_template("logind.html", form=form)



@app.route("/logud")
def logout():
    """Logger brugeren ud"""
    logout_user()
    return redirect(url_for("home"))

def save_picture(form_picture):
    """Ændrer navn på billede og gemmer det"""
    # random_hex ændrer navnet på billede til 8 tilfældige tegn
    random_hex = secrets.token_hex(8)
    # splitter billedet op så navnet og fx .txt er splittet
    #  dvs. navnet på billedet bliver ændret til hex navnet. F.eks. hund.jpg --> kjd3hwqkh34h5.jpg
    _, f_ext = os.path.splitext(form_picture.filename)
    # picture_fn tager det tilfældige navn og sætter sammen med endelsen på billedet
    picture_fn = random_hex + f_ext
    # picture_path definerer stedet billedet bliver gemt
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    # gemmer billedet der bliver smidt ind i funktionen i stedet der er defineret i picture_path
    form_picture.save(picture_path)
    # returner navnet på billedet. Det nye navn som er givet.
    return picture_fn


def save_thumbnail(form_picture):
    """Gør det samme som overstående funktion, men reduserer billedets størrelse så det passer"""
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
    """Opretter et event og gemmer i databasen"""
    # Sætter form = EventForm sådan at den kan bruges i HTML filen.
    form = EventForm()
    # Tjekker om formen der blvier submitter kommer igennem de forskellige validatorer
    if form.validate_on_submit():
        # Sætter billederne  til None således at den kun kører if statements hvis der er et billede i formen. 
        thumbnail_pic = None
        event_pic = None
        # Hvis der er et billede i form.thumbnail kører den denne IF statement.
        if form.thumbnail.data:
            # Ændrer thumbnail_pic fra None. 
            # Tager billedet som bliver postet og sender den ind i funktionen save_picture. 
            # form.thumbnail.data er infoen som bliver sat ind for form_picture i funktionen save_picture.
            thumbnail_pic = save_picture(form.thumbnail.data)
        # Denne if statement gør samme som overstående men istedet for billedet til eventpostet. 
        if form.event_picture.data:
            event_pic = save_picture(form.event_picture.data)
        # post variablen gemmer alle informationer fra formen
        post = Post(event_date=form.event_date.data,title=form.title.data, content=form.content.data, author=current_user, thumbnail=thumbnail_pic, event_picture=event_pic, link=form.link.data, pris=form.pris.data)
        # tilføjer post info til DB. 
        db.session.add(post)
        # Gemmer infoen i databasen
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("opret_event.html", form=form)



@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")

@app.route("/tilkunstneren")
def tilkunstneren():
    return render_template("tilkunstneren.html")

@app.route("/galleri")
@app.route("/omos")
def omos():
    return render_template("tomside.html")

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


@app.route("/event/<int:event_id>/update", methods=["POST", "GET"])
@login_required
def update_event(event_id):
    post = Post.query.get_or_404(event_id)
    form = EventForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.link = form.link.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('event', event_id=post.id))
    return render_template('opret_event.html', form=form)



