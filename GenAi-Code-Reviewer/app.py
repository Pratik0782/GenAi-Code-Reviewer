import os

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference


# Load variables from .env
load_dotenv()

app = Flask(__name__)


# Get IBM credentials from .env
API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_URL = os.getenv("WATSONX_URL")


# Create IBM watsonx credentials
credentials = Credentials(
    api_key=API_KEY,
    url=WATSONX_URL
)


# Create AI model
model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID,
    params={
        "max_new_tokens": 1000,
        "temperature": 0.2
    }
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/review", methods=["POST"])
def review_code():

    data = request.get_json()

    code = data.get("code", "")
    language = data.get("language", "")

    if not code.strip():
        return jsonify({
            "error": "Please enter some code."
        }), 400

    prompt = f"""
You are a senior software engineer performing a professional code review.

Programming language: {language}

Review ONLY the code provided below.

CODE START
{code}
CODE END

Important rules:

- Do not invent problems.
- Only report issues that actually exist in the submitted code.
- Distinguish between actual bugs and optional style improvements.
- Do not criticize indentation unless indentation is actually incorrect.
- Do not treat grammar, wording, capitalization, or punctuation inside normal
  string literals as programming errors.
- Do not modify string contents unless they cause a programming problem.
- If code is valid, clearly state that no bugs were found.
- Do not call an issue Critical unless it can cause severe failure,
  security compromise, or data loss.
- Consider language-specific syntax and conventions.
- Keep explanations concise and technically accurate.

Return the review using this format:

CODE REVIEW REPORT

Language: {language}

1. BUGS
List actual bugs or runtime errors.
For each issue include:
Severity:
Problem:
Explanation:

If there are no bugs, write:
No bugs found.

2. CODE QUALITY
Mention only genuine readability, maintainability, or design issues.
Separate optional style suggestions from actual problems.

3. SECURITY
Report genuine security concerns.
If none exist, write:
No obvious security vulnerabilities found.

4. PERFORMANCE
Report genuine performance problems.
If none exist, write:
No significant performance issues found.

5. RECOMMENDATIONS
Provide useful improvements only when necessary.

6. IMPROVED CODE
Provide corrected code only if meaningful improvements are necessary.
Otherwise state:
No changes required.

Do not repeat these instructions in your response.
Do not include introductory text before CODE REVIEW REPORT.
"""

    try:

        review = model.generate_text(prompt=prompt)

        return jsonify({
            "review": review
        })

    except Exception as e:

        print("Watsonx error:", e)

        return jsonify({
            "error": "Unable to generate AI review. Check the terminal for details."
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

   # https://eu-de.ml.cloud.ibm.com
#BCmXbgsjbZfBz0B6QUWgLv3V5u2kEPw65UTHMq_4DZTW
#ApiKey-853a12df-c1aa-4913-980a-afc1e23cede4