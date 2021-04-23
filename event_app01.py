import os
import bcrypt
from flask import Flask
from flask import render_template
from flask import session
from flask import request
from flask import redirect, url_for
from database import db
from models import User as User
from forms import RegisterForm, LoginForm

app = Flask(__name__)

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
    return render_template('home.html')


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



@app.route('/new')
def new_event():
    return render_template('newEvent.html')


@app.route('/delete')
def delete_event():
    return render_template('delete.html')


@app.route('/event/edit/<event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if session.get('user'):
        if request.method == 'POST':
            event_title = request.form['event_title']
            event_description = request.form['event_description']
            event = db.session.query(Event).filter_by(id=event_id).one()
            event.event_title = event_title
            event.event_description = event_description
            db.session.add(event)
            db.session.commit()

            return redirect(url_for('edit_event'))
        else:
            my_event = db.session.query(Note).filter_by(id=event_id).one()
            return render_template("editEvent.html", event=my_event, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/event/list/<event_id>')
def list_event():
    if session.get('user'):
         my_event = db.session.query(Event).filter_by(id=event_id).one()

         form = CommentForm()
         return render_template('list.html', event=my_event, user=session['user'], form=form)
     else:
        return redirect(url_for('login'))

@app.route('/event/view/<event_id>')
def view_event():
    if session.get('event'):
        my_note = db.session.query(Note).filter_by(id=note_id).one()

        form = CommentForm()
        return render_template('viewEvent.html', event=my_event, user=session['user'], form=form)
    else:
        return redirect(url_for('login'))



app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# routes for the pages
# http://127.0.0.1:5000/home
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/login
