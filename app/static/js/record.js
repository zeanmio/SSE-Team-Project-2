function analyzeText() {
    const userInput = document.getElementById("userInput").value;

    fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: userInput })
    })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            if (data.analysis) {
                resultDiv.innerHTML = `<b>Analysis:</b> ${data.analysis}`;
            } else {
                resultDiv.textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
