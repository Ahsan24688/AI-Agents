import os
from flask import Flask, request, render_template_string
from groq import Groq
from dotenv import load_dotenv 


load_dotenv()

app = Flask(__name__)


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Study Chat</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
        .chat-container { width: 450px; background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); overflow: hidden; display: flex; flex-direction: column; height: 600px; }
        .chat-header { background: #667eea; color: white; padding: 15px; text-align: center; font-weight: bold; }
        .messages { flex: 1; padding: 20px; overflow-y: auto; background: #e5ddd5; display: flex; flex-direction: column; gap: 10px; }
        .msg { padding: 10px; border-radius: 10px; max-width: 80%; }
        .user { align-self: flex-end; background: #dcf8c6; }
        .ai { align-self: flex-start; background: white; }
        .input-area { padding: 15px; border-top: 1px solid #ddd; }
        input, select { width: 100%; padding: 8px; margin-bottom: 5px; border: 1px solid #ccc; border-radius: 5px; }
        button { width: 100%; padding: 10px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
        pre { white-space: pre-wrap; font-family: inherit; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">AI Study Assistant</div>
        <div class="messages" id="chat">
            <div class="msg ai">Hello! Subjects aur hours likhein study plan ke liye.</div>
            {% if user_input %}
                <div class="msg user"><b>Subjects:</b> {{user_input.subjects}}<br><b>Hours:</b> {{user_input.hours}}</div>
            {% endif %}
            {% if plan %}
                <div class="msg ai"><pre>{{ plan }}</pre></div>
            {% endif %}
        </div>
        <div class="input-area">
            <form method="post">
                <input type="text" name="subjects" placeholder="Subjects" required>
                <input type="number" name="hours" placeholder="Daily Hours" required>
                <select name="level"><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select>
                <button type="submit">Generate Plan</button>
            </form>
        </div>
    </div>
    <script>var c = document.getElementById("chat"); c.scrollTop = c.scrollHeight;</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    study_plan = None
    user_input = None
    if request.method == "POST":
        subjects = request.form["subjects"]
        hours = request.form["hours"]
        level = request.form["level"]
        user_input = {"subjects": subjects, "hours": hours}
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Create 7-day study plan: {subjects}, {hours} hrs/day, Level: {level}"}]
            )
            study_plan = response.choices[0].message.content
        except Exception as e:
            study_plan = f"Error: {str(e)}"
            
    return render_template_string(HTML_TEMPLATE, plan=study_plan, user_input=user_input)

app = app