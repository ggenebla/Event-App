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


@app.route('/login')
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email'].one())

        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            return render_template('home.html')

        login_form.password.errors = ["Incorrect username or password"]
        return render_template("userLog.html", form=login_form)
    else:
        return render_template('userLog.html')


@app.route('/new')
def new_event():
    return render_template('newEvent.html')


@app.route('/delete')
def delete_event():
    return render_template('delete.html')


#@app.route('/event/edit/<event_id>')
#def edit_event():

#    return render_template('edit.html')


#@app.route('/event/list/<event_id>')
#def list_event():
#    return render_template('list.html')


#@app.route('/event/list/<event_id>')
#def view_event():
#    return render_template('view.html')


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# routes for the pages
# http://127.0.0.1:5000/home
# http://127.0.0.1:5000/register
# http://127.0.0.1:5000/login
