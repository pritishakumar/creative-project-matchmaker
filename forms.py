from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, TextAreaField, BooleanField#, DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional


class LoginForm(FlaskForm):
    """Form for logging in"""
    email = StringField("Email Address", 
        validators = [InputRequired(), Length(max=260), Email()])
    password = PasswordField("Password", 
        validators = [InputRequired(), Length(max=30)])

class GeocodeForm(FlaskForm):
    """ Form for guests to enter geocode data and accept rules of
    the website """

    lat = StringField("Approx User Latitude", 
        validators = [InputRequired()])
    long = StringField("Approx User Longitude", 
        validators = [InputRequired()])
    accept_rules = BooleanField("Have you read and accepted the rules for this website?",
        validators = [InputRequired()])

class UserAddForm(FlaskForm):
    """Form for adding users"""

    first_name = StringField("First Name", 
        validators = [InputRequired(), Length(max=20)])
    display_name = StringField("Display Name", 
        validators = [InputRequired(), Length(max=20)])
    email = StringField("Email Address", 
        validators = [InputRequired(), Length(max=260), Email()])
    password = PasswordField("Password", 
        validators = [InputRequired(), Length(max=30)])
    confirm_password = PasswordField("Confirm Your Password", 
        validators = [InputRequired(), Length(max=30), EqualTo("password", message='Passwords must match')])
    profile_pic = StringField("Profile Picture URL (optional)",
        validators = [Optional()])
    lat = StringField("Default Approx User Latitude", 
        validators = [InputRequired()])
    long = StringField("Default Approx User Longitude", 
        validators = [InputRequired()])
    privacy = BooleanField("Profile Hidden from Search")
    seeking_project = BooleanField("Open to Finding New Projects to Help")
    seeking_help = BooleanField("Seeking Help on Your Projects")
    accept_rules = BooleanField("Have you read and accepted the rules for this website?",
        validators = [InputRequired()])

class UserEditForm(FlaskForm):
    """Form for editing users"""

    first_name = StringField("First Name", 
        validators = [InputRequired(), Length(max=20)])
    display_name = StringField("Display Name", 
        validators = [InputRequired(), Length(max=20)])
    email = StringField("Email Address", 
        validators = [InputRequired(), Length(max=260), Email()])
    password = PasswordField("Password", 
        validators = [InputRequired(), Length(max=30)])
    profile_pic = StringField("Profile Picture URL (optional)",
        validators = [Optional()])
    lat = StringField("Default Approx User Latitude", 
        validators = [InputRequired()])
    long = StringField("Default Approx User Longitude", 
        validators = [InputRequired()])
    privacy = BooleanField("Profile Hidden from Search")
    seeking_project = BooleanField("Open to Finding New Projects to Help")
    seeking_help = BooleanField("Seeking Help on Your Projects")

class ProjectForm(FlaskForm):
    """Form for adding/editing projects"""

    name = StringField("Project Name", 
        validators = [InputRequired(), Length(max=30)])
    description = TextAreaField("Project Description", 
        validators = [InputRequired()])
    contact_info_type = StringField("Contact Info Type", 
        validators = [InputRequired(), Length(max=20)])
    contact_info = StringField("Contact Info", 
        validators = [InputRequired(), Length(max=260)])
    lat = StringField("Default Approx Project Latitude", 
        validators = [InputRequired()])
    long = StringField("Default Approx Project Longitude", 
        validators = [InputRequired()])
    inquiry_deadline = DateField("Deadline for Receiving Inquiries (Optional)", 
        validators = [Optional()], format='%Y-%m-%d')
    work_start = DateField("Proposed Project Start Date (Optional)", 
        validators = [Optional()], format='%Y-%m-%d')
    work_end = DateField("Proposed Project End Date (Optional)", 
        validators = [Optional()], format='%Y-%m-%d')
    pic_url1 = StringField("Project Picture 1 (Optional)",
        validators = [Length(max=2000), Optional()])
    pic_url2 = StringField("Project Picture 2 (Optional)",
        validators = [Length(max=2000), Optional()])
    tags = HiddenField("Tags",
        validators = [Optional()])


class TagForm(FlaskForm):
    """Form for adding/edit custom tags"""

    name = StringField("Tag Name", 
        validators = [InputRequired(), Length(max=15)])

