from flask import Flask,flash,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import User, db
import uuid
import psycopg2
from sqlalchemy import create_engine,text
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager(app)
login_manager.login_view = "login_page"

with app.app_context():
    db.init_app(app)
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/player')
@login_required
def player():
    return render_template('player.html')

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_action():
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    email = request.form["email"]
    password = request.form["password"]
    if User.query.filter_by(email=email).first():
        flash(f"The username '{email}' is already taken")
        return redirect(url_for("register_page"))

    user = User(email=email, password=password,firstname=firstname,surname=surname)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash(f"Welcome {firstname}!")
    return redirect(url_for("index"))


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_action():
    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()
    if not user:
        flash(f"No such user '{email}'")
        return redirect(url_for("login_page"))
    if password != user.password:
        flash(f"Invalid password for the user '{email}'")
        return redirect(url_for("login_page"))
    login_user(user)
    flash(f"Welcome back, {email}!")
    return redirect(url_for("index"))

@app.route("/logout", methods=["GET"])
@login_required
def logout_page():
    return render_template("logout.html")

@app.route("/logout", methods=["POST"])
@login_required
def logout_action():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))  # TODO: Fix the 'next' functionality

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Generate a unique ID
        unique_id = str(uuid.uuid4())
        youtube_link = request.form.get('youtube_link')
        videoid = extract_video_id(youtube_link)
        venue = request.form.get('venue')
        home_team = request.form.get('home_team')
        away_team = request.form.get('away_team')
        home_team_score = request.form.get('home_team_score')
        away_team_score = request.form.get('away_team_score')
        uploaded_by = request.form.get('uploaded_by')
        date_of_match = request.form.get('date_of_match')

        # # Assuming redirection for simplicity
        # return redirect(url_for('showdetails', unique_id=unique_id, youtube_link=youtube_link, venue=venue,
        #                         home_team=home_team, away_team=away_team, home_team_score=home_team_score,
        #                         away_team_score=away_team_score, uploaded_by=uploaded_by, date_of_match=date_of_match,
        #                         videoid=videoid))

    # If it's a GET request, render the upload form
    return render_template('form.html')

@app.route('/showdetails')
def showdetails():
    # Extract query parameters
    details = {
        'unique_id': request.args.get('unique_id'),
        'youtube_link': request.args.get('youtube_link'),
        'venue': request.args.get('venue'),
        'home_team': request.args.get('home_team'),
        'away_team': request.args.get('away_team'),
        'home_team_score': request.args.get('home_team_score'),
        'away_team_score': request.args.get('away_team_score'),
        'uploaded_by': request.args.get('uploaded_by'),
        'date_of_match': request.args.get('date_of_match'),
        'videoid':request.args.get('videoid')
    }
    return render_template('details.html', details=details)

@app.route('/play', methods=['POST'])
def play_video():
    youtube_link = request.form['youtube_link']
    video_id = extract_video_id(youtube_link)  # You'll need to implement this function
    return render_template('index.html', video_id=video_id)


# Your Flask route for processing timestamps
@app.route('/timestamps', methods=['POST'])
def save_timestamps():
    new_timestamps = request.json.get('timestamps')
    existing_timestamps = Timestamp.query.all()
    
    # Extract existing timestamps from the database
    existing_timestamp_values = [timestamp.timestamp for timestamp in existing_timestamps]
    
    # Filter out duplicate timestamps
    unique_new_timestamps = [timestamp for timestamp in new_timestamps if timestamp not in existing_timestamp_values]
    
    # Insert the unique new timestamps into the database
    for timestamp_value in unique_new_timestamps:
        db_timestamp = Timestamp(timestamp=timestamp_value)
        db.session.add(db_timestamp)
    db.session.commit()
    
    return jsonify({'message': 'Timestamps saved successfully'}), 200



def extract_video_id(youtube_url):
    # Find the index of 'v=' in the URL
    index = youtube_url.find('v=')
    if index != -1:
        # Extract the substring starting from the index of 'v=' to the end of the URL
        video_id = youtube_url[index + 2:]
        
        # If there are additional parameters, remove them by finding the index of '&' and taking the substring before it
        ampersand_index = video_id.find('&')
        if ampersand_index != -1:
            video_id = video_id[:ampersand_index]
        
        return video_id
    
    # Return None if 'v=' is not found in the URL
    return None


if __name__ == '__main__':
    app.run(debug=True)

