document.getElementById('search-btn').addEventListener('click', function() {
    var searchText = document.getElementById('search-input').value;
    searchYouTubeVideos(searchText);
    // Display a loading message
    document.getElementById('video-list').innerHTML = '<p>Searching...</p>';
});

function searchYouTubeVideos(searchText) {
    fetch(`/search?query=${encodeURIComponent(searchText)}`)
        .then(response => response.json())
        .then(videoUrls => {
            const videoList = document.getElementById('video-list');
            videoList.innerHTML = ''; // Clear the loading message or existing videos

            if (videoUrls.length === 0) {
                videoList.innerHTML = '<p>No results found.</p>';
                return;
            }

            videoUrls.forEach(url => {
                const videoItem = document.createElement('a');
                videoItem.href = url;
                videoItem.target = '_blank';
                videoItem.classList.add('video-item');
                videoItem.textContent = 'View Video'; // Changed text content for a cleaner look
                videoList.appendChild(videoItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('video-list').innerHTML = '<p>Error loading results.</p>';
        });
}

