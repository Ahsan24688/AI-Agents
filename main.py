import os
from flask import Flask, render_template_string, request
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# 1. Load environment variables
current_dir = Path(__file__).resolve().parent
env_path = current_dir / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print("✅ .env file found and loaded!")
else:
    print("⚠️ .env file missing!")

app = Flask(__name__)

# 2. API Key Setup (Security ke sath)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    api_key = "PASTE_YOUR_NEW_GROQ_KEY_HERE" 


client = Groq(api_key=api_key)

# 3. HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Study Planner</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .glass-card { background: rgba(255, 255, 255, 0.95); border-radius: 1.5rem; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
    </style>
</head>
<body class="py-12 px-4">
    <div class="max-w-3xl mx-auto glass-card p-10">
        <div class="text-center mb-8">
            <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-indigo-600">
                📚 AI Study Planner
            </h1>
        </div>

        <form method="POST" class="space-y-6">
            <input type="text" name="user_input" placeholder=" Enter your study topic or goal..." value="{{ user_input }}"
                   class="w-full p-4 border rounded-xl outline-none focus:ring-2 focus:ring-purple-500" required>
            <button type="submit" class="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-4 rounded-xl transition">
                Generate Plan ✨
            </button>
        </form>

        {% if plan %}
        <div class="mt-10 p-8 bg-white rounded-2xl border border-purple-100 shadow-inner">
            <h2 class="text-2xl font-bold text-purple-800 mb-4">📝 Your Plan:</h2>
            <div class="prose max-w-none text-gray-800 whitespace-pre-line text-left">
                {{ plan }}
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    study_plan = ""
    user_input = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        try:
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Create a study plan for: {user_input}"}],
                temperature=0.7,
            )
            study_plan = completion.choices[0].message.content
        except Exception as e:
            study_plan = f"Opps! Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, plan=study_plan, user_input=user_input)

if __name__ == "__main__":
    app.run(debug=True)