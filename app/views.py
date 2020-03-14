"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, Flask, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import UserProfile
from app import app
from werkzeug.utils import secure_filename
from .forms import LoginForm
import datetime

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

def format_date_joined(date_joined):
    return date_joined.strftime("%B %d, %Y")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html',form=form)

    if request.method == 'POST' and form.validate_on_submit():
        date_joined = datetime.datetime.now()
        file = request.files['photo'] 
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = UserProfile(request.form['firstname'],request.form['lastname'],request.form['gender'],request.form['email'],request.form['location'],request.form['biography'],filename,format_date_joined(date_joined))
        db.session.add(user)
        db.session.commit()
        flash('Profile added successfully') 
        return redirect(url_for('profiles',pics = get_uploaded_images())) 
    else:
        flash_errors(form)
        return render_template('login.html', form=form) 

import os
def get_uploaded_images():
    a=[]
    rootdir = os.getcwd()
    print (rootdir)
    for subdir, dirs, files in os.walk(rootdir + app.config['UPLOAD_FOLDER']):
        for file in files:
            a.append(file)
    return a

@app.route("/profiles")
def profiles():  
    users = UserProfile.query.all() 
    return render_template('profiles.html',pics = get_uploaded_images(),users=users)

@app.route("/profile/<int:userid>")
def pro(userid):   
    user=UserProfile.query.filter_by(id=userid).first()
    return render_template('userid.html',user=user)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
