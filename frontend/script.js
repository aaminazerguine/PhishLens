const analyzeButton = document.getElementById("analyzeButton");
const analyzeTab = document.getElementById("analyzeTab");
const historyTab = document.getElementById("historyTab");

const analyzeSection = document.getElementById("analyzeSection");
const resultCard = document.getElementById("resultCard");
const historySection = document.getElementById("historySection");

const result = document.getElementById("result");
const history = document.getElementById("history");


analyzeButton.addEventListener("click", async () => {

    const sender = document.getElementById("sender").value;
    const subject = document.getElementById("subject").value;
    const body = document.getElementById("body").value;

    result.innerHTML = "<p>Analyzing...</p>";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                sender: sender,
                subject: subject,
                body: body
            })
        });

        const data = await response.json();

        result.innerHTML = `
            <p><strong>Risk:</strong> ${data.risk}</p>
            <p><strong>Score:</strong> ${data.score}</p>
            <p><strong>Indicators:</strong></p>
            <ul>
                ${data.indicators.map(indicator => `<li>${indicator}</li>`).join("")}
            </ul>
        `;

    } catch (error) {
        result.innerHTML = "<p>Could not connect to the PhishLens API.</p>";
        console.error(error);
    }
});


historyTab.addEventListener("click", async () => {

    analyzeSection.style.display = "none";
    resultCard.style.display = "none";
    historySection.style.display = "block";

    history.innerHTML = "<p>Loading history...</p>";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyses");

        const data = await response.json();

        if (data.length === 0) {
            history.innerHTML = "<p>No analyses yet.</p>";
            return;
        }

        history.innerHTML = data.map(analysis => `
            <div class="history-item">
                <p><strong>Sender:</strong> ${analysis.sender}</p>
                <p><strong>Subject:</strong> ${analysis.subject}</p>
                <p><strong>Score:</strong> ${analysis.score}</p>
                <p><strong>Risk:</strong> ${analysis.risk}</p>
                <p><strong>Date:</strong> ${analysis.created_at ?? "Old analysis"}</p>
            </div>
        `).join("");

    } catch (error) {
        history.innerHTML = "<p>Could not load history.</p>";
        console.error(error);
    }
});


analyzeTab.addEventListener("click", () => {

    analyzeSection.style.display = "block";
    resultCard.style.display = "block";
    historySection.style.display = "none";
});
