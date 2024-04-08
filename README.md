# Rugby Video Analyis Application

[App on Render] (https://youtubeplayer-app.onrender.com/)  
Code on [GIT](https://github.com/RossElmes/youtubeplayer)    
Dummy User: johndoe@gmail.com  
Dummy Password: password12345  
Dummy Unlisted Video: https://www.youtube.com/watch?v=zrpOyIhk1VQ&list=PLxX3BcKr3Cbftg3K8IP3kY0vmxT4Xbdjw&index=3 that can be used to test Match Details upload.  


## Background
I used to work previously for a professional rugby team as a video analyst.  This is a big market across all sports world wide.  The main software that is used in called Sportcode by [HUDL](https://www.hudl.com/en_gb/products/sportscode).  A pro license for Hudl costs thousands of pounds an year which for amatuer sports teams is un realistic sum of money to expected to pay to complete analysis. I wanted to create an app that replicates what we can do on hudl to a small scale. 

## Simple Functionality 
The MVP for this app needs to be able to do the following 
- Create a USER
- Login
- Logout
- Upload Match Details
- Take timestamps of certain actions from within the video
- CREATE DELETE match clips from the database
- Seek to a certain part of the match based on a timestamp

## Data Model 
Below is the data model for the project. 
![ERD](static/datamodel.png)


## How to Run Locally
Follow the following steps to run locally.
- Download and unzip the project
- Create a virtualenv using `python -m venv venv`
- Activate it source venv/bin/activate
- You would need to update the `DB_URL` env variable to point to a local instance of a database.
- Run the local application with running `pyhton run app.py`

## Creating the Database on Render
To create the database on render I followed [PostgreSQL on Render](https://docs.render.com/databases)

## How I connected to render with Github
To host my application I followed the documents on [Render's Docs](https://docs.render.com/github).  I had two challenges here. I needed to update the start command to `$ guinicorn app::app` instead of `$ guinicorn run::app` as the file in my repo in app.py not run.py.  The second challenge I needed to troubleshoot here was the access Render had to my GIT account.  I had to give access to the repo on the applications settings page on github.  You'll find your personal one [here](github.com/settings/installations)

## Leverage the Youtube API
Storing video files is expensive traditionally.  Amaturer clubs will host videos of there games in youtube in unlisted files for post game/match reviews.  This is why I chose tho leverage the youtube IFrame Player API. More info what is possible with the API can be found in the [documentation](https://developers.google.com/youtube/iframe_api_reference).  The player object has lots of possible functionality that can be levergaed with Javascript.  I need to leverage this functionality to capture current time on the video and also seek to certain time on the video. 

## Learning Outcomes 
I think I learned a great deal completing this project. Below are some of the highlights 

- Leveraging a database within my application 
- Sending data to flask then to the database from the browser
- Retriving data from database to flask and then sending data from flask to browser which I could then use javascript on
- Using SQLAlchemy to generate models 
- Developing an application locally and setting up a local sever instance of postgreSQL database
- Creating a enviormental variable within a virtual environment.  This was different to how I would usually create a variable. 
- Integrating basic CRUD opperations


## Further development

Below are some further elements I'd like to create 

- Be able to review same type of clips from different games.  It would be great to have for example, all try clips from three or four games that we could review.
- Be able to add clips to a playlist based on `browswer_id` and save down commentary within the playlist.  This would allow for analysis week on week
- Have Possesion pill that you can change possession across the different teams and stamp the time for the change. 
- Create a export that anyone can download a CSV of all the data.  This is an important step.  Clip level data is something that sportscode doesn't offer cleanly. 
- Work on the styling.  I've leanred that the design and styling of a website is not something that I am good and and not something I think I would want to work on.  I enjoy building the functionality of the app rather than the UI design.  However I need to be able to complete it to a basic standard to make apps functional and more appealing that if there was no styling. 


## Checklist for Assignment 
- [x] A Flask Env     
- [x] B Create Flask Application Files  
- [x] C Create HTML Files  
- [x] D Apply CSS Styling  
- [x] E Implement JavaScript Functionality  
- [x] G Define Flask Routes and Render HTML Files  
- [x] H Integrate PostgrSQL Database with Flask  
- [x] I Test and Run the Flask Application  
- [x] J Hosting the Web App on Render.com  