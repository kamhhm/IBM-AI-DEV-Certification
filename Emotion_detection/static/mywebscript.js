async function analyzeEmotion() {
    const textToAnalyze = document.getElementById("textToAnalyze").value.trim();
    const resultsDiv = document.getElementById("results");
    const errorDiv = document.getElementById("errorMessage");
    const loadingDiv = document.getElementById("loading");
    const btn = document.querySelector(".btn");

    resultsDiv.classList.remove("visible");
    errorDiv.classList.remove("visible");
    resetBars();

    if (!textToAnalyze) {
        errorDiv.classList.add("visible");
        return;
    }

    loadingDiv.classList.add("visible");
    btn.disabled = true;

    try {
        const response = await fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`);
        const data = await response.json();

        loadingDiv.classList.remove("visible");
        btn.disabled = false;

        if (data.error) {
            errorDiv.classList.add("visible");
            return;
        }

        updateResults(data);
        resultsDiv.classList.add("visible");

    } catch (error) {
        loadingDiv.classList.remove("visible");
        btn.disabled = false;
        errorDiv.classList.add("visible");
    }
}

function updateResults(data) {
    const emotions = data.emotions;
    const dominant = data.dominant_emotion;

    document.getElementById("dominantText").textContent = dominant.charAt(0).toUpperCase() + dominant.slice(1);

    Object.keys(emotions).forEach(emotion => {
        const score = emotions[emotion];
        const percentage = score * 100;

        document.getElementById(`${emotion}Score`).textContent = score.toFixed(4);
        
        setTimeout(() => {
            document.getElementById(`${emotion}Bar`).style.width = `${percentage}%`;
        }, 50);

        const item = document.getElementById(`${emotion}Item`);
        item.classList.toggle("dominant", emotion === dominant);
    });
}

function resetBars() {
    document.querySelectorAll(".emotion-item").forEach(item => item.classList.remove("dominant"));
    document.querySelectorAll(".emotion-bar").forEach(bar => bar.style.width = "0%");
}
