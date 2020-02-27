from flask import Flask, request, redirect, url_for, render_template, session
from models import get_posts
app = Flask(__name__)

@app.route('/')
def index():
    role = 'author'
    posts = get_posts()
    return render_template('index.html', role=role, posts=posts)

if __name__ == '__main__':
    app.run(debug=True)