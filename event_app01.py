import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('userReg.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# routes for the pages
# http://127.0.0.1:5000/home
# http://127.0.0.1:5000/register