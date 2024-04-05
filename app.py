from flask import Flask,flash,render_template, request, redirect, url_for,jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from models import User, db,MatchDetails,MatchClips
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
@login_required
def index():
    match_details= MatchDetails.query.filter_by(author_id=current_user.id).all()
    return render_template("index.html",match_details=match_details)

@app.route('/api/clips')
def get_clips():
    match_id = request.args.get('match_id')
    # Fetch clips data from the database based on the match ID
    match_clips = MatchClips.query.filter_by(match_id = match_id).all()
    json_data = json.dumps([item.serialize() for item in match_clips])
    #Return the data as JSON
    return json_data


@app.route('/player/<matchid>')
@login_required
def player(matchid):
    match = MatchDetails.query.get_or_404(matchid)
    return render_template('player.html',match=match)

# @app.route('/player')
# @login_required
# def player():
#     return render_template('player.html')

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
    print(user.id)
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


@app.route("/form", methods=["GET"])
@login_required
def form_page():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
@login_required
def form_action():
    youtube_link = request.form['youtube_link']
    videoid = extract_video_id(youtube_link)
    venue = request.form['venue']
    home_team = request.form['home_team']
    away_team = request.form['away_team']
    home_team_score = request.form['home_team_score']
    away_team_score = request.form['away_team_score']
    match_date =  request.form['date_of_match']
    competition = request.form['competition']
    author=current_user

    print(type(home_team_score))

    match_detail = MatchDetails(
        youtube_link = youtube_link,
        videoid = videoid,
        venue = venue,
        home_team = home_team,
        away_team = away_team,
        home_score = home_team_score,
        away_score = away_team_score,
        match_date =  match_date,
        competition = competition,
        author=current_user,
    )

    db.session.add(match_detail)
    db.session.commit()
    return redirect(url_for("index"))


# @app.route('/play', methods=['POST'])
# def play_video():
#     youtube_link = request.form['youtube_link']
#     video_id = extract_video_id(youtube_link)  # You'll need to implement this function
#     return render_template('index.html', video_id=video_id)


# Your Flask route for processing timestamps
@app.route('/timestamps', methods=['POST'])
def save_timestamps():

    existing_brower_id = []
    new_timestamps = request.json
    print(new_timestamps)
    existing_timestamps = MatchClips.query.all()
    for clip in existing_timestamps:
        existing_brower_id.append(clip.browser_id)
    
    unique_new_timestamps = [item for item in new_timestamps if item['browser_id'] not in existing_brower_id]

    #Insert the unique new timestamps into the database
    for clip in unique_new_timestamps:
        db_newclip = MatchClips(code=clip['action'],timestamp=clip['time'],browser_id=clip['browser_id'],match_id = clip['match_id'])
        db.session.add(db_newclip)
    db.session.commit()
    
    return jsonify({'message': 'Timestamps saved successfully'})



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

