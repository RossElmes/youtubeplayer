from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import  models
import uuid
import psycopg2
from sqlalchemy import create_engine,text

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    return render_template('index.html')

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

