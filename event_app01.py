import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('userReg.html')


@app.route('/login')
def login():
    return render_template('userLog.html')


@app.route('/new')
def new_event():
    return render_template('newEvent.html')


@app.route('/delete')
def delete_event():
    return render_template('delete.html')


@app.route('/event/edit/<event_id>')
def edit_event():

    return render_template('edit.html')


@app.route('event/list/<event_id>')
def list_event():
    return render_template('list.html')


@app.route('event/list/<event_id>')
def view_event():
    return render_template('view.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# routes for the pages
# http://127.0.0.1:5000/home
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/login
