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
    u3 = User(first_name='Tester',
              display_name='tester',
              email='test@test.com',
              password='$2b$12$46DrbnRGb.he3uz138xWyuBbCG2zcPE8Y9dTJEi1OrB8zOvkGAJOC',
              lat=49.176662,
              long=-123.080341)
    t1 = Tag(name='glass art')
    t2 = Tag(name='green living')
    t3 = Tag(name='hardware')
    db.session.add_all([u1, u2, u3, t1, t2, t3])
    db.session.commit()

    p1 = Project(name='Stained Glass',
                 description=f"""I have a really boring window
                 with a mediocre view! I would love to do a
                 stained glass project of some sort
                 with it? Does anyone have any expertise on
                 this and be willing to help me?""",
                 user_id=u1.id,
                 contact_info_type='email',
                 contact_info=u1.email,
                 pic_url1='..\static\images\window-nicolas-solerieu-unsplash.jpg',
                 lat=u1.lat,
                 long=u1.long)
    p2 = Project(name='Compost Bin',
                 description=f"""Anyone have metal welding equipment
                 and skills that they'd be helping to lend to my
                 project? I want to make a tumbler compost bin from
                 a metal food grade drum I have lying around!""",
                 user_id=u2.id,
                 contact_info_type='email',
                 contact_info=u2.email,
                 lat=u2.lat,
                 long=u2.long)
    p3 = Project(name='Wooden Pallet useful for you?',
                 description=f"""I've got old wooden pallets, anyone
                 want to make a fun project with them? I'd love to
                 hear some ideas!""",
                 user_id=u3.id,
                 contact_info_type='email',
                 contact_info=u3.email,
                 pic_url1='..\static\images\wooden_pallet-reproductive-health-supplies-coalition-unsplash.jpg',
                 lat=u3.lat,
                 long=u3.long)
    db.session.add_all([p1, p2, p3])
    db.session.commit()

    p1.tags = [t1]
    p2.tags = [t2, t3]
    p3.tags = [t2]
    db.session.commit()


seed_database()
