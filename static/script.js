// static/script.js

// Assuming 'player' is the div that contains the YouTube player
let playerElement = document.getElementById('player');
let videoId = playerElement.getAttribute('data-video-id');
let matchId = playerElement.getAttribute('data-match-id');

let player;

function onYouTubeIframeAPIReady() {
player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: videoId,
    events: {
        'onReady': onPlayerReady,
        'onStateChange': onPlayerStateChange
    }
});
}

function onPlayerReady(event) {
event.target.playVideo();
}

function onPlayerStateChange(event) {
if (event.data == YT.PlayerState.PLAYING) {
    // Video is playing
}
}


// Function to request full screen
function requestFullScreen(element) {
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.mozRequestFullScreen) { /* Firefox */
        element.mozRequestFullScreen();
    } else if (element.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
        element.webkitRequestFullscreen();
    } else if (element.msRequestFullscreen) { /* IE/Edge */
        element.msRequestFullscreen();
    }
}

// Function to seek to a timestamp
function seekToTimestamp(timestamp) {
    player.seekTo(timestamp);
}


// Function to mark an action and timestamp
function markAction(action) {
    const currentTime = player.getCurrentTime();
    let myuuid = crypto.randomUUID()
    timestamps.push({ action: action, time: currentTime,browser_id:myuuid,match_id:matchId});
    updateClipsList();
    console.log(timestamps)
}

// Function to update the list of clips
function updateClipsList() {
    const clipsList = document.getElementById('clips');
    clipsList.innerHTML = '';
    timestamps.forEach(timestamp => {
        const listItem = document.createElement('li');
        listItem.textContent = `${timestamp.code} - ${timestamp.time}s`;
        listItem.addEventListener('click', function() {
            seekToTimestamp(timestamp.time);
        });
        clipsList.appendChild(listItem);
    });
}


// Example usage: Mark an action when a button is clicked
document.querySelectorAll('.mark-action').forEach(button => {
    button.addEventListener('click', function() {
        const action = button.dataset.action;
        markAction(action);
    });
});



function sendDataToFlask(data) {
    fetch('/timestamps', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data sent to Flask:', data);
        // Optionally handle the response from Flask
    })
    .catch(error => {
        console.error('Error sending data to Flask:', error);
        // Optionally handle errors
    });
}


document.getElementById('saveButton').addEventListener('click', function() {
    // Call the function to send data to Flask
    body = JSON.stringify(timestamps)
    console.log(body)
    sendDataToFlask(timestamps);
});



// Construct the URL with the match ID as a query parameter
let playerElement2 = document.getElementById('player');
let matchId2 = playerElement2.getAttribute('data-match-id');
let timestamps = []

const url = `/api/clips?match_id=${matchId2}`;

fetch(url)
    .then(response => response.json())
    .then(data => {
        // Handle the received clips data
        timestamps = data
        updateClipsList(timestamps)

    })
    .catch(error => {
        console.error('Error fetching clips data:', error);
    });


