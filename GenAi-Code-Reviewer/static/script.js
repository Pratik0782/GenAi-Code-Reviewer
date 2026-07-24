async function reviewCode() {

    const code = document.getElementById("code").value;
    const language = document.getElementById("language").value;

    const result = document.getElementById("result");
    const status = document.getElementById("status");
    const button = document.getElementById("reviewButton");


    if (code.trim() === "") {

        alert("Please enter some code.");

        return;
    }


    // Show loading state

    status.textContent = "AI is analyzing your code...";

    result.textContent =
        "Analyzing bugs, security, performance and code quality...";

    button.disabled = true;

    button.textContent = "Reviewing...";


    try {

        const response = await fetch("/review", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                code: code,
                language: language
            })
        });


        const data = await response.json();


        if (!response.ok) {

            result.textContent =
                data.error || "Something went wrong.";

            status.textContent = "Analysis failed";

            return;
        }


      result.innerHTML = formatReview(data.review);

        status.textContent = "Analysis completed";


    } catch (error) {

        console.error(error);

        result.textContent =
            "Unable to connect to the server.";

        status.textContent =
            "Connection error";

    } finally {

        button.disabled = false;

        button.textContent = "Review Code";
    }
}
function clearCode() {
    document.getElementById("code").value = "";

    document.getElementById("result").innerHTML =
    'Enter your code and click "Review Code" to start the AI analysis.';

    document.getElementById("status").textContent =
        "Ready for analysis";
}
function formatReview(review) {

    // Protect HTML characters coming from generated code
    let formatted = review
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Format code blocks
    formatted = formatted.replace(
        /```(?:\w+)?\n([\s\S]*?)```/g,
        "<pre class='code-block'><code>$1</code></pre>"
    );

    // Format numbered section headings
    formatted = formatted.replace(
        /(\d+\.\s+(?:BUGS|CODE QUALITY|SECURITY|PERFORMANCE|RECOMMENDATIONS|IMPROVED CODE))/g,
        "<h3>$1</h3>"
    );

    // Main report heading
    formatted = formatted.replace(
        /CODE REVIEW REPORT/g,
        "<h2>CODE REVIEW REPORT</h2>"
    );

    // Line breaks
    formatted = formatted.replace(/\n/g, "<br>");

    return formatted;
}   