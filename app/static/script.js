// static/script.js
let player;
let timestamps = [];
console.log(1000)

function onYouTubeIframeAPIReady() {
    const videoId = 'I3rKOd4b6Os'
    player = new YT.Player('player', {
        height: '390',
        width: '640',
        videoId: videoId,
    });
}

document.getElementById('mark-timestamp').addEventListener('click', function() {
    const currentTime = player.getCurrentTime();
    timestamps.push(currentTime);
    updateTimestampsList();
});

function updateTimestampsList() {
    const list = document.getElementById('timestamps');
    list.innerHTML = '';
    timestamps.forEach(timestamp => {
        const item = document.createElement('li');
        item.textContent = `Timestamp: ${timestamp}`;
        item.onclick = () => { player.seekTo(timestamp); };
        list.appendChild(item);
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

// Example usage: Seek to a timestamp when a timestamp item is clicked
document.getElementById('timestamps').addEventListener('click', function(event) {
    if (event.target.tagName === 'LI') {
        const timestamp = parseFloat(event.target.dataset.timestamp);
        if (!isNaN(timestamp)) {
            seekToTimestamp(timestamp);
        }
    }
});
