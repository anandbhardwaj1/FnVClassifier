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
                let percentage = parseInt(data.Percentage.replace('%', ''));
                let isPassed = percentage <= 20;
                 debugger
                // Create result UI based on QC pass/fail
                document.getElementById('analysis-ui').innerHTML = `
                    <div class="analysis-container">
                        
                        <div class="result-icon ${isPassed ? 'pass' : 'fail'}">
                            ${isPassed ? 
                                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3">'+
                                '<path d="M5 12l5 5 9-9" /></svg>' : 
                                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3">'+
                                '<path d="M6 18L18 6M6 6l12 12" /></svg>'
                            }
                        </div>
                        
                        <div class="result-title">
                            ${isPassed ? 'Yay! QC Passed' : 'Uh-Oh! QC Failed'}
                        </div>
                        
                        <div class="insights-section">
                            <div class="insights-title f-w-700">Insights</div>
                            
                            <div class="insight-row">
                                <div>Item Detected</div>
                                <div>${data.Item || 'Unknown'}</div>
                            </div>
                            
                            <div class="insight-row">
                                <div>Bad Quality</div>
                                <div>${data.Percentage || 'NA'}</div>
                            </div>
                            
                            <div class="insight-row">
                                <div>Shelf Life</div>
                                <div>${data.ShelfLife || 'NA'}</div>
                            </div>
                        </div>
                        
                        ${data.Judgement ? `
                            <div class="instructions-box" style="margin-left: 0px; margin-right: 0px;">
                                ${data.Judgement
                                .map(instruction => 
                                    `<div class="instruction-item">• ${instruction}</div>`
                                ).join('')}
                            </div>
                        ` : ''}
                        
                        <div class="action-buttons" style="width: 100%">
                            <button class="button button-secondary" onclick="window.location.reload()">Cancel</button>
                            <button class="button" onclick="window.location.reload()">Proceed</button>
                        </div>
                    </div>
                `;
                
                // Add these styles dynamically if not already in your CSS
                if (!document.getElementById('results-styles')) {
                    const styleEl = document.createElement('style');
                    styleEl.id = 'results-styles';
                    styleEl.textContent = `
                        .analysis-container { text-align: center; padding: 20px; }
                        .result-icon { width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 20px auto; }
                        .result-icon.pass { background-color: #4CAF50; }
                        .result-icon.fail { background-color: #F44336; }
                        .result-title { font-size: 24px; color: #4CAF50; margin-bottom: 30px; font-weight: 500; }
                        .result-icon.fail + .result-title { color: #F44336; }
                        .insights-section { margin-bottom: 20px; width: 100%; }
                        .insights-title { font-weight: 500; text-align: left; margin-bottom: 10px; }
                        .insight-row { display: flex; justify-content: space-between; margin-bottom: 10px; }
                        .instructions-box { background-color: #FFF8E1; border-radius: 8px; padding: 15px; margin-bottom: 20px; text-align: left; }
                        .instruction-item { color: #FF9800; margin-bottom: 8px; }
                        .action-buttons { display: flex; gap: 10px; margin-top: 20px; }
                        .action-buttons .button { flex: 1; }
                    `;
                    document.head.appendChild(styleEl);
                }
            })
            .catch(error => {
                console.log("error", error)
                document.getElementById('analysis-ui').innerHTML = `
                    <div class="analysis-container">
                        <div class="error-icon">
                            <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#F44336" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12" y2="16"></line>
                            </svg>
                        </div>
                        <div class="title" style="color: #F44336; margin-top: 15px;">Unable to Analyze Image</div>
                        <div class="subtitle" style="margin: 15px 0; text-align: center;">
                            We couldn't analyze this image properly. This might be due to poor lighting, 
                            blurry image, or the item is not FnV.
                        </div>
                        <div class="subtitle" style="margin-bottom: 20px; font-size: 14px; color: #757575;">
                            Please try again with a clearer image.
                        </div>
                        <button class="button" onclick="window.location.reload()" style="min-width: 120px;">Try Again</button>
                    </div>
                `;
            })
        });
}

// Export functions for use in HTML
window.retake = retake;
window.proceed = proceed;