from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "1325ghtkendshthe"

# TODO: Fill in methods and routes
@app.route("/")
@app.route("/home")
def home():
    if "username" in session:
        return render_template("home.html")
    else:
        return redirect(url_for('login'))

@app.route("/lunch")
def lunch():
    return render_template("playlist.html", name="Lunch")

@app.route("/ready")
def ready():
    return render_template("playlist.html",  name="Getting Ready")

@app.route("/drive")
def drive():
    return render_template("playlist.html", name="Driving")

@app.route("/addasong")
def add():
    if request.method == "GET":
        return render_template("addsong.html", name="Add a Song")
    elif request.method == "POST":
        title = request.form["title"]
        artist = request.form["artist"]
        playlist = request.form["playlist"]
        new_song = Song(title=title, artist=artist, playlist_id = playlist)
        db_session.add(new_song)
        db_session.commit()

@app.route("/signup")
def signup():
    if request.method == "GET":
        return render_template("signup.html", name="Signup")
    else:
        username = request.form["username"]
        password = request.form["password"]
        cpassword = request.form["cpassword"]
        if password != cpassword:
            flash('Passwords do not match. Try again', 'error')
            return render_template("signup.html")
        else:
            new_user = User(username=username, password=password)
            db_session.add(new_user)
            db_session.commit()
            session["username"] = username
            return redirect(url_for('home'))
    

@app.route("/login")
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        return redirect(url_for('home'))


@app.route("/suggest")
def suggest():
    return render_template("suggest.html", name="Suggest a Song")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
