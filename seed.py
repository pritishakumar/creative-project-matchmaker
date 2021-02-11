from app import db
from models import User, Project, Tag

db.drop_all()
db.create_all()

def seed_database():
    u1 = User(first_name='Pat',
            display_name='pat',
            email='pat@email.com',
            password='password',
            lat=49.28778937014537,
            long=-123.11413092334273)
    u2 = User(first_name='Jill',
            display_name='jill',
            email='jill@email.com',
            password='password',
            lat=49.191682433834714,
            long=-122.84534638593648)
    t1 = Tag(name='glass art')
    t2 = Tag(name='green living')
    t3 = Tag(name='hardware')
    db.session.add_all([u1, u2, t1, t2, t3])
    db.session.commit()

    p1 = Project(name='Stained Glass',
            description='Window, need help with it',
            user_id=u1.id,
            contact_info_type='email',
            contact_info=u1.email,
            lat= u1.lat,
            long=u1.long)
    p2 = Project(name='Compost Bin',
            description='Compost Bin, need help with it',
            user_id=u2.id,
            contact_info_type='email',
            contact_info=u2.email,
            lat= u2.lat,
            long=u2.long)
    db.session.add_all([p1, p2])
    db.session.commit()

    p1.tags = [t1]
    p2.tags = [t2, t3]
    db.session.commit()

seed_database()