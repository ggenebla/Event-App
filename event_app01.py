import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Functionality Check"


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
