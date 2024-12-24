from flask import Flask, render_template

app = Flask(__name__)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# AI Dream Page
@app.route('/ai-dream')
def ai_dream():
    return render_template('ai_dream.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
