from app import app
from flask import  render_template, request, redirect, url_for

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])

def play_video():
    youtube_link = request.form['youtube_link']
    video_id = extract_video_id(youtube_link)  # You'll need to implement this function
    return render_template('index.html', video_id=video_id)


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
