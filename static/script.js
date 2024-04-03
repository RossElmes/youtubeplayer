// static/script.js
let player;
let timestamps = [];
console.log(1000)

function onYouTubeIframeAPIReady() {
    const videoId = 'I3rKOd4b6Os'
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: videoId
    });
}

// Assuming 'player' is the div that contains the YouTube player
const playerElement = document.getElementById('player');

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
    timestamps.push({ action: action, time: currentTime });
    updateClipsList();
}

// Function to update the list of clips
function updateClipsList() {
    const clipsList = document.getElementById('clips');
    clipsList.innerHTML = '';
    timestamps.forEach(timestamp => {
        const listItem = document.createElement('li');
        listItem.textContent = `${timestamp.action} - ${timestamp.time.toFixed(2)}s`;
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



// Example function to send timestamps to the server
function sendTimestampsToServer(timestamps) {
    fetch('/timestamps', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ timestamps: timestamps, match_id:match_id})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to save timestamps');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error(error.message);
    });
}
