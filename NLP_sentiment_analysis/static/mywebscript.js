let RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value.trim();
    const responseDiv = document.getElementById("system_response");
    const analyzeBtn = document.getElementById("analyzeBtn");

    // Validate input
    if (!textToAnalyze) {
        responseDiv.innerHTML = `
            <div class="alert alert-warning" role="alert">
                <strong>Warning:</strong> Please enter some text to analyze.
            </div>
        `;
        return;
    }

    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm mr-2"></span>Analyzing...';
    responseDiv.innerHTML = `
        <div class="loading">
            <div class="spinner-border text-primary" role="status">
                <span class="sr-only">Loading...</span>
            </div>
            <p class="mt-2">Analyzing sentiment...</p>
        </div>
    `;

    // Encode the text for URL
    const encodedText = encodeURIComponent(textToAnalyze);
    
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            // Reset button state
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = 'Run Sentiment Analysis';
            
            if (this.status == 200) {
                responseDiv.innerHTML = xhttp.responseText;
            } else {
                responseDiv.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        <strong>Error:</strong> Failed to analyze sentiment. Status code: ${this.status}
                        <br><small>Please check your connection and try again.</small>
                    </div>
                `;
            }
        }
    };
    
    xhttp.onerror = function() {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Run Sentiment Analysis';
        responseDiv.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <strong>Error:</strong> Network error occurred. Please check your connection and try again.
            </div>
        `;
    };
    
    xhttp.open("GET", "sentimentAnalyzer?textToAnalyze=" + encodedText, true);
    xhttp.send();
}
