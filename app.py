import os

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
from datetime import datetime
from credentials import API_KEY

from forms import UserAddForm, UserEditForm, ProjectForm, TagForm, LoginForm, GeocodeForm
from models import db, connect_db, User, Project, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///matchmaker'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


def browser_login(user):
    """ Adds the User instance to session and g variable """

    session['CURR_USER_KEY'] = user.id
    g.user = user


def browser_logout():
    """ Logs current user out of their account """

    session.clear()
    g.user = None


@app.before_request
def add_user_to_g():
    """ If we're logged in, add curr user to Flask global. """

    if 'CURR_USER_KEY' in session:
        g.user = User.query.get(session['CURR_USER_KEY'])
        if not g.user:
            session.pop('CURR_USER_KEY')
    else:
        g.user = None
        if 'GUEST_GEOCODE' in session:
            g.guest = session['GUEST_GEOCODE']


@app.before_request
def add_API_key():
    """ Adds API key to the global variable g """

    g.API_KEY = API_KEY


@app.route("/")
def landing_page():
    """ Render initial landing page for user or redirect to
    the search page if the user is already logged in previously """

    if 'CURR_USER_KEY' in session:
        return redirect("/search")

    return render_template("landing.html")


@app.route("/profile/new", methods = ["GET", "POST"])
def sign_up_page():
    """ Render the signup form or process the information """

    if 'CURR_USER_KEY' in session:
        flash("You are already logged into an account, please log out before creating a new account.", "danger")
        return redirect("/search")
    
    form = UserAddForm(prefix='form-user-signup-')

    if form.validate_on_submit():
        user_obj = {
            'first_name': form.first_name.data,
            'display_name': form.display_name.data,
            'email': form.email.data,
            'password': form.password.data,
            'profile_pic': request.form.get('profile_pic'),
            'lat': form.lat.data,
            'long': form.long.data,
            'privacy': request.form.get('privacy'),
            'seeking_project': request.form.get('seeking_project'),
            'seeking_help': request.form.get('seeking_help')
        }
        user_final = User.signup(user_obj)
        browser_login(user_final)

        flash("Signed up successfully", "success")
        return redirect("/search")

    return render_template("profile-new.html", form=form)


@app.route("/login", methods = ["GET", "POST"])
def login_page():
    """ Render the login form or process the information """

    if 'CURR_USER_KEY' in session:
        flash("You are already logged into an account.", "success")
        return redirect("/search")
    
    form = LoginForm(prefix='form-user-login-')

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_final = User.login(email, password)
        if user_final:
            browser_login(user_final)
            flash("Logged in successfully", "success")
            return redirect("/search")
        else: 
            flash("Logged in failed. Please double check your email and password combination.", "danger")
            return redirect("/login")
    return render_template("login.html", form=form)


@app.route("/logout", methods = ["POST"])
def logout():
    """ Logs current user out of their account """

    browser_logout()
    return redirect("/")


@app.route("/guest", methods = ["GET", "POST"])
def guest_page():
    """ Renders the guest access page and prepares user for
    the search page by collecting geocode data """

    if 'CURR_USER_KEY' in session:
        flash("You are already logged into an account.", "success")
        return redirect("/search") 

    form = GeocodeForm(prefix='form-user-guest-')

    if form.validate_on_submit():
        lat = form.lat.data
        long = form.long.data
        session['GUEST_GEOCODE'] = [lat, long]
        flash("Entering as a Guest. Some features are not displayed.", "success")
        return redirect("/search")

    return render_template("guest.html", form=form)


@app.route("/search")
def search_page():
    """ Renders the main search page """

    if ('GUEST_GEOCODE' not in session) and ('CURR_USER_KEY' not in session):
       flash("Please choose an option, before searching for projects","danger")
       return redirect("/") 

    if ('CURR_USER_KEY' in session):
        g.user = User.lookup_user(session['CURR_USER_KEY'])

    return render_template("search.html")


@app.route("/profile/edit", methods = ["GET", "POST"])
def profile_edit():
    """ Renders form to edit the profile or process the information """

    if not 'CURR_USER_KEY' in session:
        flash("Unauthorized access. Account needed to edit profile.", "danger")
        if 'GUEST_GEOCODE' in session:
            return redirect("/search")
        else:
            return redirect("/")
    
    form = UserEditForm(obj = g.user, prefix='form-user-edit-')

    if form.validate_on_submit():
        user = User.login(form.email.data, form.password.data)
        if (user.id == g.user.id):
            user.first_name = form.first_name.data
            user.display_name = form.display_name.data
            user.profile_pic = form.profile_pic.data
            user.lat = form.lat.data
            user.long = form.long.data
            user.privacy = form.privacy.data
            user.seeking_project = form.seeking_project.data
            user.seeking_help = form.seeking_help.data
            db.session.commit()
                
            flash("Profile edited successfully.", "success")
            return redirect("/search")
        else:
            flash("Incorrect password. Profile changes not made", "danger")
            return redirect("/profile/edit")
    return render_template("profile-edit.html", form=form)


@app.route("/profile/delete/<user_id>", methods = ["POST"])
def profile_delete(user_id):
    """ Deletes the currently logged in user """

    if not 'CURR_USER_KEY' in session or int(user_id) != g.user.id:
        flash("Unauthorized access. Correct account needed to delete profile.", "danger")
        if 'GUEST_GEOCODE' in session:
            return redirect("/search")
        else:
            return redirect("/")

    user = User.lookup_user(user_id)
    db.session.delete(user)
    db.session.commit()
    
    browser_logout()
    flash("Profile deleted successfully.", "success")
    return redirect("/")


@app.route("/project/new", methods = ["GET", "POST"])
def project_new():
    """ Renders form to create new project or process the form """

    if not 'CURR_USER_KEY' in session:
        flash("Unauthorized access. Account needed to create.", "danger")
        if 'GUEST_GEOCODE' in session:
            return redirect("/search")
        else:
            return redirect("/")

    form = ProjectForm(prefix='form-project-new-')
    tags_full_list = Tag.list_all()

    if form.validate_on_submit():
        optional_date_keys = ['inquiry_deadline', 'work_start', 'work_end']
        optional_date_values = []
        for each in optional_date_keys:
            try:
                y, m, d = request.form.get(each).split('-')
                print(y,m,d,'out of if')
                if y and m and d:
                    date = datetime(int(y), int(m), int(d))
                    optional_date_values.append(date)
                    print(date, 'in if', optional_date_values)
            except ValueError:
                optional_date_values.append(None)
                print('caught value error', optional_date_values)
            except AttributeError:
                optional_date_values.append(None)
                print('caught value error', optional_date_values)
        inquiry_deadline_date, work_start_date, work_end_date = optional_date_values

        project_obj = {
            'name': form.name.data,
            'description': form.description.data,
            'user_id': g.user.id,
            'contact_info_type': form.contact_info_type.data,
            'contact_info': form.contact_info.data,
            'lat': form.lat.data,
            'long': form.long.data,
            'inquiry_deadline': inquiry_deadline_date,
            'work_start': work_start_date,
            'work_end': work_end_date,
            'pic_url1': request.form.get('pic_url1'),
            'pic_url2': request.form.get('pic_url2'),
        }
        project_final = Project.create_project(project_obj)

        tags = request.form.get('tags')
        if tags:
            tags = tags.split('|')
            tag_objs = []
            if (len(tags) > 0):
                for name in tags:
                    tag_obj = Tag.lookup_tag(name)
                    if not tag_obj:
                        tag_obj = Tag.create_tag(name)

                    tag_objs.append(tag_obj)
                project_final.tags = tag_objs
                db.session.commit()

        flash("Project created successfully", "success")
        return redirect(f"/project/{project_final.id}")

    return render_template("project-new.html", form=form, tags_full_list = tags_full_list)


@app.route("/project/<project_id>")
def project_detail(project_id):
    """ Renders page for a specific project """

    project = Project.lookup_project(project_id)
    tags = ', '.join([tag.name for tag in project.tags])

    return render_template("project-detail.html", project=project, tags=tags)


@app.route("/project/<project_id>/edit", methods = ["GET", "POST"])
def project_edit(project_id):
    """ Renders form to edit specific project or process the form """

    if not 'CURR_USER_KEY' in session:
        flash("Unauthorized access. Account needed to edit.", "danger")
        return redirect(f"/project/{project_id}")

    project = Project.lookup_project(project_id)
    project = Project.lookup_project(project_id)
    if g.user.id != project.user.id:
        flash("Unauthorized user. Correct user account needed.", "danger")
        return redirect(f"/project/{project_id}")

    form = ProjectForm(obj = project, prefix='form-project-edit-')

    tags_full_list = Tag.list_all()
    project_tags = [tag.name for tag in project.tags]
    tags_list_str = "|".join(project_tags)

    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.user_id = g.user.id
        project.contact_info_type = form.contact_info_type.data
        project.contact_info = form.contact_info.data
        project.lat = form.lat.data
        project.long = form.long.data
        project.pic_url1 = request.form.get('pic_url1')
        project.pic_url2 = request.form.get('pic_url2')

        tags = request.form.get('tags')
        if (tags):
            tags = tags.split('|')
        tag_objs = []
        if (tags and len(tags) > 0):
            for name in tags:
                tag_obj = Tag.lookup_tag(name)
                if not tag_obj:
                    tag_obj = Tag.create_tag(name)
                tag_objs.append(tag_obj)
        project.tags = tag_objs

        optional_date_keys = ['inquiry_deadline', 'work_start', 'work_end']
        optional_date_values = []
        for each in optional_date_keys:
            try:
                y, m, d = request.form.get(each).split('-')
                print(y,m,d,'out of if')
                if y and m and d:
                    date = datetime(int(y), int(m), int(d))
                    optional_date_values.append(date)
                    print(date, 'in if', optional_date_values)
            except ValueError:
                pass
                optional_date_values.append(None)
                print('caught value error', optional_date_values)
            except AttributeError:
                optional_date_values.append(None)
                print('caught value error', optional_date_values)
        project.inquiry_deadline, project.work_start, project.work_end = optional_date_values      
        db.session.commit()

        flash("Project edited successfully.", "success")
        return redirect(f"/project/{project_id}")

    return render_template("project-edit.html", form=form, project=project, tags_list_str=tags_list_str, tags_full_list=tags_full_list)


@app.route("/project/<project_id>/delete", methods = ["POST"])
def project_delete(project_id):
    """ Renders form to delete a specific project"""

    if not 'CURR_USER_KEY' in session:
        flash("Unauthorized access. Account needed to delete.", "danger")
        return redirect(f"/project/{project_id}")

    project = Project.lookup_project(project_id)
    if g.user.id != project.user.id:
        flash("Unauthorized user. Correct user account needed.", "danger")
        return redirect(f"/project/{project_id}")

    db.session.delete(project)
    db.session.commit()

    flash("Project deleted successfully.", "success")
    return redirect("/search")


@app.route("/api/geocode")
def api_geocode():
    """ Handle geocoding api get requests """

    address = request.args['address']
    url = "https://maps.googleapis.com/maps/api/geocode/json?" 
    resp = requests.get(url,
        params={"key": API_KEY, "address": address})
    json_data = resp.json()
    return jsonify(json_data)


@app.route("/api/neighborhood")
def api_neighborhood():
    """ Handle project querying in the map vicinity """

    north = request.args['north']
    south = request.args['south']
    east = request.args['east']
    west = request.args['west']

    neighborhood = Project.query_neighborhood(north, south, east, west)

    resp = { 'projects': []}
    for project in neighborhood:
        resp['projects'].append({'id': project.id,
        'name': project.name,
        'display_name': project.user.display_name,
        'lat': project.lat,
        'long': project.long,
        'tags': [tag.name for tag in project.tags]
        })
    return jsonify(resp)


@app.route("/api/tags")
def api_tag_list():
    """ Generate and return a json list of all existing tags """
    
    tags_full_list = Tag.list_all()
    return jsonify(tags_full_list)





