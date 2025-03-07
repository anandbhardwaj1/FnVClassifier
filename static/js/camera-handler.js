// Global variable to store camera stream
let cameraStream = null;

/**
 * Initialize and start the camera
 */
function startCamera() {
    document.getElementById('initial-ui').style.display = 'none';
    document.getElementById('camera-ui').style.display = 'flex';
    
    // Access camera
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then(stream => {
            // Store the stream reference
            cameraStream = stream;
            document.getElementById('video').srcObject = stream;
        })
        .catch(err => console.error(err));
}

/**
 * Stop all camera tracks and release resources
 */
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => {
            track.stop();
        });
        cameraStream = null;
    }
}

/**
 * Initialize camera event handlers
 */
function initCameraHandlers() {
    // Capture photo when video is clicked
    document.getElementById('video').onclick = function() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        
        document.getElementById('preview').src = canvas.toDataURL('image/jpeg');
        document.getElementById('camera-ui').style.display = 'none';
        document.getElementById('preview-ui').style.display = 'flex';
    };
}

// Initialize when the DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initCameraHandlers();
});

// Export functions for use in other files
window.startCamera = startCamera;
window.stopCamera = stopCamera;