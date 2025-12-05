import google.generativeai as genai
import os
import json

class CodeGenerator:
    """Generates code and fixes bugs using a Gemini large language model (LLM)."""

    def __init__(self):
        # Configure the Gemini API client
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            raise EnvironmentError(f"Failed to configure Gemini API: {e}. Please ensure GEMINI_API_KEY is set.")

    def generate_code(self, prompt, language="python"):
        """Generates code based on a user request and language, returning a JSON response."""
        system_prompt = f"""You are an expert {language} programmer. Your task is to write a complete,
        working program that fulfills the user's request. For multi-file projects, return a JSON
        object with filenames as keys and code as values. For single files, return a JSON object
        with a single key, e.g., 'main.py' or 'index.js'.

        The entire response must be a valid JSON object. Do not include any other text or markdown
        outside of the JSON object.

        Example for multiple files:
        {{
            "main.py": "def main():\\n\\tprint('Hello from main')\\n\\nif __name__ == '__main__':\\n\\tmain()",
            "utils.py": "def helper():\\n\\treturn 'helper function'"
        }}
        """
        user_prompt = f"Create a {language} program that: {prompt}"

        response = self.model.generate_content(
            contents=[
                {"role": "user", "parts": [{"text": system_prompt}]},
                {"role": "model", "parts": [{"text": "OK. I understand the format. What is the task?"}]},
                {"role": "user", "parts": [{"text": user_prompt}]}
            ]
        )

        try:
            # Gemini's response is often in a single 'text' part. We assume it's JSON.
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Gemini API: {e}")
            print(f"Raw response was: {response.text}")
            # Fallback for a single file if JSON decoding fails
            return {"main.py": response.text}


    def fix_code(self, files_content, error_message, language="python"):
        """Analyzes existing code and an error message to generate a fix."""
        prompt = f"""The following {language} code has an error.

        Code:
        ---
        {json.dumps(files_content, indent=4)}
        ---

        Error Message:
        {error_message}

        Analyze the code and the error message. Provide the corrected code. For multi-file projects,
        return a JSON object with filenames as keys and corrected code as values. Only return the
        corrected code for the files that need changes. Do not return files that are already correct.

        The entire response must be a valid JSON object.
        """

        response = self.model.generate_content(prompt)

        try:
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Gemini API during debugging: {e}")
            print(f"Raw response was: {response.text}")
            # Fallback to single file if JSON decoding fails
            return {"main.py": response.text}
        