from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "1325ghtkendshthe"

# TODO: Fill in methods and routes
@app.route("/")
@app.route("/home", methods=["GET","POST"])
def home():
    #if user is logged in, this will change the navbar to "Logout" (used in every method)
    is_logged_in = "username" in session
    return render_template("home.html", is_logged_in=is_logged_in)

@app.route("/lunch", methods=["GET","POST"])
def lunch():
    #query all songs in Lunch playlist to print on the page
    songs = db_session.query(Song).where(Song.playlist_id == "Lunch").all()
    is_logged_in = "username" in session
    return render_template("playlist.html", name="Lunch", songs=songs, is_logged_in = is_logged_in)


@app.route("/ready", methods=["GET","POST"])
def ready():
    is_logged_in = "username" in session
    #query all songs in Getting Ready playlist to print on the page
    songs = db_session.query(Song).where(Song.playlist_id == "Ready").all()
    return render_template("playlist.html",  name="Getting Ready", songs=songs, is_logged_in=is_logged_in)

@app.route("/driving", methods=["GET","POST"])
def driving():
    is_logged_in = "username" in session
    #query all songs in Driving playlist to print on the page
    songs = db_session.query(Song).where(Song.playlist_id == "Driving").all()
    return render_template("playlist.html", name="Driving", songs=songs, is_logged_in=is_logged_in)

@app.route("/addasong", methods=["GET","POST"])
def add():
    is_logged_in = "username" in session
    if request.method == "GET":
        return render_template("addsong.html", name="Add a Song", is_logged_in=is_logged_in)
    elif request.method == "POST":
        title = request.form["title"]
        artist = request.form["artist"]
        playlist_id = request.form["playlist"]
        #create new song based on users inputs
        new_song = Song(user_id = session["username"], title=title, artist=artist, playlist_id=playlist_id)
        #add song to database
        db_session.add(new_song)
        #query playlist user added the song to 
        playlist = db_session.query(Playlist).filter(Playlist.title== playlist_id).first()
        #count number of songs already in playlist
        num_songs = db_session.query(Song).filter(Song.playlist_id == playlist_id).count()
        #update number of songs in playlist
        playlist.num_songs = num_songs
        db_session.commit()
        return redirect(url_for(playlist_id.lower()))

@app.route("/signup", methods=["GET","POST"])
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
    

@app.route("/login", methods=["GET","POST"])
def login():
    is_logged_in = "username" in session
    if request.method == "GET":
        return render_template("login.html", is_logged_in = is_logged_in)
    else:
        username = request.form["username"]
        password = request.form["password"]
        user = db_session.query(User).where((username == User.username) & (password == User.password)).first()
        #if user not in database, display error message 
        if user == None:
            flash("Invalid Username or Password", "info")
            return render_template("login.html")
        else:
            session["username"] = username
            return redirect(url_for("home"))


@app.route("/suggest", methods=["GET","POST"])
def suggest():
    is_logged_in = "username" in session
    if request.method == "GET":
        return render_template("suggest.html", name="Suggest a Song", is_logged_in=is_logged_in)
    else:
        title = request.form["title"]
        description = request.form["description"]
        suggest = PlaylistSuggestions(user_id=session["username"], title=title, description=description)
        db_session.add(suggest)
        db_session.commit()
        return redirect(url_for("home"))

@app.route("/logout", methods=["GET","POST"])
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
