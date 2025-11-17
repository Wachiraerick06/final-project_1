import os
import json
import openai

# Load API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def review_code_ai(code: str) -> dict:
    """
    Review code using GPT-4. Falls back to stub output if API fails or key missing.
    """

    # Fallback stub
    fallback = {
        "quality_score": 75,
        "bugs": ["Possible variable misalignment"],
        "security_issues": ["No input validation detected"],
        "suggestions": ["Add type hints", "Use try/except blocks"],
        "docstring": "This function performs a task but needs optimization."
    }

    # If no API key, return stub immediately
    if not openai.api_key:
        return fallback

    prompt = f"""
You are an expert Python code reviewer. Analyze the following code:

{code}

Provide:
- A quality score (0-100)
- List of bugs
- List of security issues
- Suggestions to improve
- A concise docstring describing the function

Return ONLY a JSON object.
"""

    try:
        # GPT-4 API call with timeout
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            request_timeout=10  # timeout in seconds
        )

        content = response.choices[0].message.content

        # Attempt to parse JSON
        return json.loads(content)

    except Exception as e:
        print("OpenAI API error:", e)
        # Always return fallback to keep backend responsive
        return fallback
