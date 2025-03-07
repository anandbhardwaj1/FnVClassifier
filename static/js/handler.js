/**
 * Switch back to camera view to retake photo
 */
function retake() {
    document.getElementById('preview-ui').style.display = 'none';
    document.getElementById('camera-ui').style.display = 'flex';
}

/**
 * Process the captured image and send to backend
 */
function proceed() {
    document.getElementById('preview-ui').style.display = 'none';
    document.getElementById('analysis-ui').style.display = 'flex';

    // Stop the camera
    stopCamera();

    // Get the base64 image from the preview
    const imageData = document.getElementById('preview').src;
    
    // Convert base64 to blob
    fetch(imageData)
        .then(res => res.blob())
        .then(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'image.jpg');

            // Send to backend
            fetch('/analyze', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('analysis-ui').innerHTML = `
                    <div class="analysis-container">
                        <div class="title">Analysis Result</div>
                        <pre style="text-align: left; white-space: pre-wrap;">${data.analysis}</pre>
                    </div>
                `;
            })
            .catch(error => {
                document.getElementById('analysis-ui').innerHTML = `
                    <div class="analysis-container">
                        <div class="title">Error</div>
                        <div class="subtitle">${error.message}</div>
                    </div>
                `;
            });
        });
}

// Export functions for use in HTML
window.retake = retake;
window.proceed = proceed;