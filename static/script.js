// Assuming 'player' is the div that contains the YouTube player
let playerElement = document.getElementById('player');
let videoId = playerElement.getAttribute('data-video-id');
let matchId = playerElement.getAttribute('data-match-id');
let timestamps = []

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
    clip = {code:action,time:currentTime,browser_id:myuuid,match_id:matchId}
    sendDataToFlask(clip)
    timestamps.push({ code: action, time: currentTime,browser_id:myuuid,match_id:matchId});
    updateClipsList();
}

// Function to update the list of clips
function updateClipsList() {
    const clipsList = document.getElementById('clips');
    clipsList.innerHTML = '';
    timestamps.forEach(timestamp => {
        const listItem = document.createElement('div');
        listItem.setAttribute('class','clip-item')
        // Create a new button element
        const del_button = document.createElement('button');
        del_button.textContent = 'Delete Clips'
        del_button.setAttribute('class','clip-btn delete')

        // Add event listener to the button if needed
        del_button.addEventListener('click', () => {
            deleteclip(timestamp.browser_id)
            del_button.parentNode.remove();
            console.log('Delete Clip')
        });


        const seekto_button = document.createElement('button');
        seekto_button.textContent = 'Seek to Clip'
        seekto_button.setAttribute('class','clip-btn seek-to')

        seekto_button.addEventListener('click', function() {
            seekToTimestamp(timestamp.time);
        });

        listItem.textContent = `${timestamp.code} - ${parseFloat(timestamp.time).toFixed(0)}s`;
        listItem.appendChild(seekto_button)
        listItem.appendChild(del_button)

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




const url = `/api/clips?match_id=${matchId}`;

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



// Function to delete timestamp from array
function deleteTimestamp(browserId) {
    const index = timestamps.findIndex(timestamp => timestamp.browser_id === browserId);
    if (index !== -1) {
        timestamps.splice(index, 1); // Remove the object at the found index
        console.log(`Timestamp with browser_id ${browserId} deleted`);
        console.log(timestamps)
    }
}

function deleteclip(browser_id) {

    const url = `/api/deleteclip?browser_id=${browser_id}`;

    fetch(url,{
        method:'DELETE'
    })
    .then(response => {
        if(response.ok){
            console.log(`Match clip with ID ${browser_id} deleted successfully`);
            deleteTimestamp(browser_id)
        }else {
            console.error(`Failed to delete match clip with ID ${browser_id}`);
        }
    }) .catch(error => {
            console.error('Error fetching clips data:', error);
        });
}

