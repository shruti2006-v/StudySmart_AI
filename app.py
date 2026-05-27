import google.generativeai as genai
from flask import Flask, request, render_template
import markdown  # <-- This is our new formatting tool!

# Connect to Google's AI
genai.configure(api_key="AIzaSyBTPu2t7V_AUMljMMJybjpAxcdULiMOD44")
model = genai.GenerativeModel('gemini-2.5-flash')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_text = request.form['text']
    
    # We tweak the prompt slightly to ask for clean formatting
    prompt = f"Summarize this text into 3 clean bullet points and create 2 practice quiz questions based on it:\n\n{user_text}"
    
    response = model.generate_content(prompt)
    
    # Convert the raw AI markdown text into beautiful HTML tags automatically
    formatted_html = markdown.markdown(response.text)
    
    # Pass that beautiful HTML layout straight into a results page template
    return render_template('result.html', output=formatted_html)

if __name__ == '__main__':
    app.run(debug=True)