from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class Project_Tag(db.Model):
    """ Project_Tag Model """

    __tablename__ = "project_tags"

    id = db.Column(db.Integer,
        primary_key = True)
    project_id = db.Column(db.Integer,
        db.ForeignKey('projects.id', ondelete='CASCADE'),
        nullable=False,
        index=True)
    tag_name = db.Column(db.String(15),
        db.ForeignKey('tags.name', ondelete='CASCADE'),
        nullable=False)

    def __repr__(self):
        """ Show more useful info on Project_Tag """
        return f"<Project_Tag {self.project_id} {self.tag_name}>"


class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    id = db.Column(db.Integer,
        primary_key = True)
    email = db.Column(db.String(260),
        nullable = False,
        unique = True,
        index=True)
    password = db.Column(db.String(100),
        nullable = False)
    display_name = db.Column(db.String(20),
        nullable = False,
        unique = True)
    first_name = db.Column(db.String(20),
        nullable = False)
    profile_pic = db.Column(db.String(2000),
        nullable = True,
        default = "/static/images/junior-ferreira-profile.jpg")
    privacy = db.Column(db.Boolean,
        nullable = False,
        default = False)
    lat = db.Column(db.Float,
        nullable = False)
    long = db.Column(db.Float,
        nullable = False)
    seeking_project = db.Column(db.Boolean,
        nullable = False,
        default = True)
    seeking_help = db.Column(db.Boolean,
        nullable = False,
        default = True)

    projects = db.relationship("Project")

    def __repr__(self):
        """ Show more useful info on User """
        return f"<User {self.display_name} {self.first_name}>"

    @classmethod
    def signup(cls, user_obj):
        """ Signs up new User with required info """
        optional_params = ['profile_pic', 'privacy', 'seeking_project', 'seeking_help']

        hashed_password = bcrypt.generate_password_hash(user_obj['password']).decode('UTF-8')
        user = cls(
            first_name= user_obj['first_name'],
            display_name= user_obj['display_name'],
            email= user_obj['email'],
            password=hashed_password,
            lat= user_obj['lat'],
            long= user_obj['long']
        )
        db.session.add(user)
        db.session.commit()

        for each in optional_params:
            if user_obj[each] != None:
                user.each = user_obj[each]
        db.session.commit()

        return user

    @classmethod
    def login(cls, email, password):
        """ Authenticates User with required info """

        user = cls.query.filter_by(email=email).first()   
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    @classmethod
    def lookup_user(cls, id):
        """ Looks up User instance and returns it """
        user = cls.query.get_or_404(id)
        return user

class Project(db.Model):
    """ Project Model """

    __tablename__ = "projects"

    id = db.Column(db.Integer,
        primary_key = True)
    name = db.Column(db.String(30),
        nullable = False)
    description = db.Column(db.Text,
        nullable = False)
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False)
    contact_info_type = db.Column(db.String(20),
        nullable = False)
    contact_info = db.Column(db.String(260),
        nullable = False)
    lat = db.Column(db.Float,
        nullable = False,
        index=True)
    long = db.Column(db.Float,
        nullable = False,
        index=True)
    time_posted = db.Column(db.DateTime,
        nullable=False,
        default=datetime.utcnow())
    inquiry_deadline = db.Column(db.Date,
        nullable = True)
    work_start = db.Column(db.Date,
        nullable = True)
    work_end = db.Column(db.Date,
        nullable = True)
    pic_url1 = db.Column(db.String(2000),
        nullable = True)
    pic_url2 = db.Column(db.String(2000),
        nullable = True)

    user = db.relationship("User")

    tags = db.relationship(
        "Tag",
        secondary = "project_tags"
    )

    def __repr__(self):
        """ Show more useful info on Project """
        return f"<Project {self.name}>"

    @classmethod
    def create_project(cls, project_obj):
        """ Creates a new project instance by the current
        user """
        optional_params = ['inquiry_deadline', 'work_start', 'work_end', 'pic_url1', 'pic_url2']

        project = cls(
            name= project_obj['name'],
            description= project_obj['description'],
            user_id= project_obj['user_id'],
            contact_info_type= project_obj['contact_info_type'],
            contact_info= project_obj['contact_info'],
            lat= project_obj['lat'],
            long= project_obj['long'],
            inquiry_deadline= project_obj['inquiry_deadline'] or None,
            work_start= project_obj['work_start'] or None,
            work_end= project_obj['work_end'] or None,
            pic_url1= project_obj['pic_url1'] or None,
            pic_url2= project_obj['pic_url2'] or None
        )
        db.session.add(project)
        db.session.commit()

        return project

    @classmethod
    def lookup_project(cls, project_id):
        """ Queries for a specific project """
        project = cls.query.get_or_404(project_id)
        return project

    @classmethod
    def query_neighborhood(cls, north, south, east, west):
        """ Queries for projects within specific lat&long bounds """
        neighborhood = cls.query.filter(Project.lat < north,
            Project.lat > south, 
            Project.long > west, 
            Project.long < east).all()
        return neighborhood

class Tag(db.Model):
    """ Tag Model """

    __tablename__ = "tags"
    
    name = db.Column(db.String(15),
        nullable = False,
        unique= True,
        primary_key = True)

    projects = db.relationship(
        "Project",
        secondary = "project_tags"
    )

    def __repr__(self):
        """ Show more useful info on Tag """
        return f"<Tag {self.name}>"

    @classmethod
    def create_tag(cls, name):
        """ Creates a tag instance given a name """
        tag = cls(name = name)
        db.session.add(tag)
        db.session.commit()
        return tag

    @classmethod
    def list_all(cls):
        """ Creates a list of all existing tags """
        object_list = cls.query.all()
        return [tag.name for tag in object_list]

    @classmethod
    def lookup_tag(cls, name):
        """ Looks up tag object based on name and returns it """
        tag = cls.query.filter_by(name=name).first()
        return tag