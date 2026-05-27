import os  # <-- Built into Python to read your laptop's hidden environment settings
import google.generativeai as genai
from flask import Flask, request, render_template
import markdown
from dotenv import load_dotenv  # <-- Our new security tool!

# 1. Load the variables from your hidden .env file into your computer's memory
load_dotenv()

# 2. Grab the key securely from memory so it's never written in plain text
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_text = request.form['text']
    
    prompt = f"Summarize this text into 3 clean bullet points and create 2 practice quiz questions based on it:\n\n{user_text}"
    
    response = model.generate_content(prompt)
    
    formatted_html = markdown.markdown(response.text)
    
    return render_template('result.html', output=formatted_html)

if __name__ == '__main__':
    app.run(debug=True)