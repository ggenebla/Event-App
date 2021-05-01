import os
import bcrypt
from flask import Flask
from flask import render_template
from flask import session
from flask import request
from flask import redirect, url_for
from flask_bootstrap import Bootstrap
from database import db
from models import User as User
from models import Event as Event
from forms import RegisterForm, LoginForm

app = Flask(__name__)
Bootstrap(app)

# creates file called 'note_app_data.db' in root directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_app.db'

# disables signalling application every time change is made
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['SECRET_KEY'] = 'SE3155'

# Bind SQLAlchemy db object to the app
db.init_app(app)

# setup models
with app.app_context():
    db.create_all()


@app.route('/home')
def home():
    if session.get('user'):
        return render_template('home.html', user=session['user'])
    return render_template("home.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('home'))

    # something went wrong - display register view
    return render_template('userReg.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('home'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("userLog.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("userLog.html", form=login_form)


@app.route('/events/new', methods=['POST', 'GET'])
def new_event():
    # check method used for request
    if session.get('user'):
        if request.method == 'POST':
            title = request.form.get('title')
            location = request.form.get('location')
            description = request.form.get('description')
            today = request.form.get('date')
            # today = today.strftime("%m-%d-%y")
            time = request.form.get('time')
            # time = time.strftime("%H:%M")
            event_rsvp = request.form.get('rsvp')
            rating = None
            new_record = Event(title, location, description, today, time, event_rsvp, rating, session['user_id'])
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('list_events'))
        else:
            return render_template('newEvent.html', user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/events/delete/<event_id>', methods=['POST', 'GET'])
def delete_event(event_id):
    if session.get('user'):
        my_event = db.session.query(Event).filter_by(id=event_id).one()
        db.session.delete(my_event)
        db.session.commit()

        return redirect(url_for('list_events'))
    else:
        return redirect(url_for('login'))


@app.route('/events/rsvp/<event_id>', methods=['GET', 'POST'])
def rsvp(event_id):
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            location = request.form['location']
            description = request.form['description']
            today = request.form['date']
            # today = today.strftime("%m-%d-%y")
            time = request.form['time']
            # time = time.strftime("%H:%M")
            event = db.session.query(Event).filter_by(id=event_id).one()
            event_rsvp = request.form['rsvp']
            event.title = title
            event.location = location
            event.description = description
            event.date = today
            event.time = time
            event.rsvp = event_rsvp
            db.session.add(event)
            db.session.commit()

            return redirect(url_for('list_events'))
        else:
            my_event = db.session.query(Event).filter_by(id=event_id).one()

        return render_template("editEvent.html", event=my_event, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/events/edit/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            location = request.form['location']
            description = request.form['description']
            today = request.form['date']
            # today = today.strftime("%m-%d-%y")
            time = request.form['time']
            # time = time.strftime("%H:%M")
            event_rsvp = request.form['rsvp']
            event = db.session.query(Event).filter_by(id=event_id).one()
            event.title = title
            event.location = location
            event.description = description
            event.date = today
            event.time = time
            event.rsvp = event_rsvp
            db.session.add(event)
            db.session.commit()

            return redirect(url_for('list_events'))
        else:
            my_event = db.session.query(Event).filter_by(id=event_id).one()

        return render_template("editEvent.html", event=my_event, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/events')
def list_events():
    if session.get('user'):
        my_events = db.session.query(Event).filter_by(user_id=session['user_id']).all()
        return render_template('list.html', events=my_events, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/events/view/<event_id>')
def view_event(event_id):
    if session.get('user'):
        my_event = db.session.query(Event).filter_by(id=event_id).one()

#        form = CommentForm()
        return render_template('viewEvent.html', event=my_event, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/events/view/<event_id>/rate',  methods=['GET', 'POST'])
def rate_event(event_id):
    if session.get('user'):
        if request.method == 'POST':
            my_event = db.session.query(Event).filter_by(id=event_id)
            my_event.rating = request.form.get('star')
            

            return redirect(url_for('list_events'))
        else:
            my_event = db.session.query(Event).filter_by(id=event_id).one()
            return render_template('rate.html', event=my_event, user=session['user'])
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('home'))


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# routes for the pages
# http://127.0.0.1:5000/home
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/login
# http://127.0.0.1:5000/rate
