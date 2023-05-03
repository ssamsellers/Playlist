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
    return render_template("home.html")

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
        new_song = Songs(title=title, artist=artist, playlist_id = playlist)
        db_session.add(new_song)
        db_session.commit()

@app.route("/signup")
def signup():
    return render_template("signup.html", name="Signup")

@app.route("/login")
def login():
    return render_template("login.html", name="Login")

@app.route("/suggest")
def suggest():
    return render_template("suggest.html", name="Suggest a Song")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
