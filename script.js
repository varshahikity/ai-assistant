const analyzeBtn = document.getElementById("analyzeBtn");
const codeInput = document.getElementById("codeInput");
const languageSelect = document.getElementById("language");
const statusMessage = document.getElementById("statusMessage");

const errorResult = document.getElementById("errorResult");
const suggestionsResult = document.getElementById("suggestionsResult");
const complexityResult = document.getElementById("complexityResult");
const documentationResult = document.getElementById("documentationResult");
const testCasesResult = document.getElementById("testCasesResult");

analyzeBtn.addEventListener("click", async () => {
    const code = codeInput.value.trim();
    const language = languageSelect.value;

    if (!code) {
        statusMessage.textContent = "Please paste code before analyzing.";
        return;
    }

    try {
        analyzeBtn.disabled = true;
        statusMessage.textContent = "Analyzing code...";

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ code, language }),
        });

        const data = await response.json();

        if (!response.ok) {
            statusMessage.textContent = data.error || "Analysis failed.";
            return;
        }

        renderResults(data);
        statusMessage.textContent = "Analysis completed successfully.";
    } catch (error) {
        statusMessage.textContent = "Unable to connect to backend server.";
    } finally {
        analyzeBtn.disabled = false;
    }
});

function renderResults(data) {
    const errorMessage = data.errors?.message || "No error information.";
    errorResult.textContent = errorMessage;

    renderList(suggestionsResult, data.suggestions || []);
    renderList(testCasesResult, data.test_cases || []);

    const complexity = data.complexity || {};
    complexityResult.innerHTML = `
        <p><strong>Lines:</strong> ${complexity.line_count ?? "-"}</p>
        <p><strong>Functions:</strong> ${complexity.function_count ?? "-"}</p>
        <p><strong>Loops:</strong> ${complexity.loop_count ?? "-"}</p>
        <p><strong>Conditions:</strong> ${complexity.condition_count ?? "-"}</p>
        <p><strong>Complexity Score:</strong> ${complexity.complexity_score ?? "-"}</p>
        <p><strong>Rating:</strong> ${complexity.rating ?? "-"}</p>
    `;

    documentationResult.textContent = data.documentation || "No documentation generated.";
}

function renderList(listElement, items) {
    listElement.innerHTML = "";

    if (!items.length) {
        const li = document.createElement("li");
        li.textContent = "No items available.";
        listElement.appendChild(li);
        return;
    }

    items.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        listElement.appendChild(li);
    });
}
