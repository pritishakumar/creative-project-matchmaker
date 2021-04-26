from unittest import TestCase
from flask import session, g
from app import app
from models import db, User, Project, Tag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///matchmaker_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


user_data = {
  "first_name": 'Tester',
  "display_name": 'tester',
  "email": 'test@test.com',
  "password": '$2b$12$46DrbnRGb.he3uz138xWyuBbCG2zcPE8Y9dTJEi1OrB8zOvkGAJOC',
  "lat": 49.176662,
  "long": -123.080341,
  "profile_pic": "/static/images/junior-ferreira-profile.jpg",
  "privacy": False,
  "seeking_project": True,
  "seeking_help": True
}

user_data2 = {
  "first_name": 'Tester2',
  "display_name": 'tester2',
  "email": 'test2@test.com',
  "password": '$2b$12$46DrbnRGb.he3uz138xWyuBbCG2zcPE8Y9dTJEi1OrB8zOvkGAJOC',
  "lat": 49.176663,
  "long": -123.080342
}

project1 = {
	"name":'Stained Glass',
	"description":f"""I have a really boring window
	with a mediocre view! I would love to do a
	stained glass project of some sort
	with it? Does anyone have any expertise on
	this and be willing to help me?""",
	"contact_info_type":'email',
	"contact_info": user_data["email"],
	"pic_url1":'..\static\images\window-nicolas-solerieu-unsplash.jpg',
	"lat":user_data["lat"],
	"long":user_data["long"]
}

project2 = {
	"name":'Compost Bin',
	"description":f"""Anyone have metal welding equipment
				 and skills that they'd be helping to lend to my
				 project? I want to make a tumbler compost bin from
				 a metal food grade drum I have lying around!""",
	"contact_info_type":'email',
	"contact_info": user_data["email"],
	"lat":user_data["lat"],
	"long":user_data["long"]
}

class LandingTestCase(TestCase):
	"""Tests for landing page"""

	def test_landing(self):
		"""Tests rendering landing page"""

		with app.test_client() as client:
			resp = client.get("/")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("Welcome to <i>Creative Project Matchmaker", html)
			self.assertIn("An Existing Account?", html)
			self.assertIn("Proceed As A Guest?", html)
			self.assertIn("Guest Access!", html)
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertFalse(g.get('user', None))


class UserViewsTestCase(TestCase):
	"""Tests for user profile related views"""

	def setUp(self):
		"""Make demo data."""

		db.drop_all()
		db.create_all()
		user = User(**user_data)
		db.session.add(user)
		db.session.commit()
		self.user = user

	def tearDown(self):
		"""Clean up fouled transactions."""

		db.session.rollback()

	def test_signup_get(self):
		"""Tests the get request that renders the form"""
		with app.test_client() as client:
			resp = client.get("/profile/new")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Make A New Account", html)
			self.assertIn("Add New User", html)
			self.assertIn("Go Back to Options", html)
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertFalse(g.get('user', None))

	def test_signup_post(self):
		"""Ensures Post request redirects after processing data"""
		
		with app.test_client() as client:
			resp = client.post(
				"/profile/new", data={
					'form-user-signup-first_name': user_data2['first_name'],
					'form-user-signup-display_name': user_data2['display_name'] ,
					'form-user-signup-email': user_data2['email'],
					'form-user-signup-password': 'password',
					'form-user-signup-confirm_password': 'password',
					'form-user-signup-lat': user_data2['lat'],
					'form-user-signup-long': user_data2['long'],
					'form-user-signup-accept_rules': True
				})

			self.assertEqual(resp.status_code,302)
			self.assertEqual(resp.location, "http://localhost/search")
			
	
	def test_signup_post_redirected(self):
		"""Ensure Post request loads redirected page correctly"""

		with app.test_client() as client:
			resp = client.post(
				"/profile/new", data={
					'form-user-signup-first_name': user_data2['first_name'],
					'form-user-signup-display_name': user_data2['display_name'] ,
					'form-user-signup-email': user_data2['email'],
					'form-user-signup-password': 'password',
					'form-user-signup-confirm_password': 'password',
					'form-user-signup-lat': user_data2['lat'],
					'form-user-signup-long': user_data2['long'],
					'form-user-signup-accept_rules': True
				},
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Signed up successfully", html)
			self.assertIn("Log out</button>", html)
			self.assertIn("Edit Profile", html)	
			self.assertTrue(session['CURR_USER_KEY'])
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertTrue(g.get('user', None))
			

	def test_login_get(self):
		""" Tests rendering the form via Get request"""
		with app.test_client() as client:
			resp = client.get("/login")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Log In!", html)
			self.assertIn("Login", html)
			self.assertIn("Go Back to Options", html)
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertFalse(g.get('user', None))

	def test_login_post(self):
		"""Ensures Post request processes data and redirects"""
		
		with app.test_client() as client:
			resp = client.post(
				"/login", data={
					'form-user-login-email': user_data['email'],
					'form-user-login-password': 'password',
				})

			self.assertEqual(resp.status_code,302)
			self.assertEqual(resp.location, "http://localhost/search")
	
	def test_login_post_redirected(self):
		"""Ensures redirected page renders correctly after Post 
		request data is processed"""
		with app.test_client() as client:
			resp = client.post(
				"/login", data={
					'form-user-login-email': user_data['email'],
					'form-user-login-password': 'password',
				},
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Logged in successfully", html)
			self.assertIn("Log out</button>", html)
			self.assertIn("Edit Profile", html)	
			self.assertTrue(session['CURR_USER_KEY'])
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertTrue(g.get('user', None))

	def test_guest_get(self):
		"""Ensures Guest form renders correctly"""
		with app.test_client() as client:
			resp = client.get("/guest")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Guest Access!", html)
			self.assertIn("Enter Search Page", html)
			self.assertIn("Go Back to Options", html)
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertFalse(g.get('user', None))

	def test_guest_post(self):
		"""Ensures Guest Post request directs after submitting data"""
		
		with app.test_client() as client:
			resp = client.post(
				"/guest", data={
					'form-user-guest-lat': user_data2['lat'],
					'form-user-guest-long': user_data2['long'],
					'form-user-guest-accept_rules': True
				})

			self.assertEqual(resp.status_code,302)
			self.assertEqual(resp.location, "http://localhost/search")
	
	def test_guest_post_redirected(self):
		"""Ensure redirected page renders correctly after Post request"""
		with app.test_client() as client:
			resp = client.post(
				"/guest", data={
					'form-user-guest-lat': user_data2['lat'],
					'form-user-guest-long': user_data2['long'],
					'form-user-guest-accept_rules': True
				},
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Log out of Guest Mode", html)
			self.assertIn("Entering as a Guest. Some features are not displayed.", html)
			self.assertTrue(session['GUEST_GEOCODE'])
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
			self.assertFalse(g.get('user', None))

	def test_logout(self):
		"""Ensures user log out redirects"""
		
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = 999
			resp = client.post("/logout")

			self.assertEqual(resp.status_code,302)
			self.assertEqual(resp.location, "http://localhost/")

	def test_logout_redirected(self):
		"""Ensures user log out renders landing page correctly"""
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = 999
			resp = client.post("/logout", follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Successfully logged out.", html)
			self.assertIn("Welcome to <i>Creative Project Matchmaker", html)
			self.assertIn("An Existing Account?", html)
			self.assertIn("Proceed As A Guest?", html)
			self.assertIn("Guest Access!", html)
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertFalse(g.get('user', None))

	def test_user_edit_get(self):
		"""Ensures user profile edit form renders"""
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.get("/profile/edit")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Update Your User Profile!", html)
			self.assertIn("To confirm any profile changes, enter your current password:", html)
			self.assertIn(self.user.email, html)
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']

	def test_user_edit_post(self):
		"""Ensures user profile edit Post request redirects after processing data"""
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				"/profile/edit", data={
					'form-user-edit-first_name': user_data['first_name'],
					'form-user-edit-display_name': user_data['display_name'] ,
					'form-user-edit-email': user_data['email'],
					'form-user-edit-password': 'password',
					'form-user-edit-profile_pic': "#",
					'form-user-edit-lat': user_data['lat'],
					'form-user-edit-long': user_data['long'],
					'form-user-edit-privacy': False,
					'form-user-edit-seeking_project': True,
					'form-user-edit-seeking_help': True
				})

			self.assertEqual(resp.status_code,302)
			self.assertEqual(resp.location, "http://localhost/search")

	def test_user_edit_post_redirected(self):
		"""Ensures redirected page renders correctly after correctly processing
		Post request data"""
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				"/profile/edit", data={
					'form-user-edit-first_name': user_data['first_name'],
					'form-user-edit-display_name': user_data['display_name'] ,
					'form-user-edit-email': user_data['email'],
					'form-user-edit-password': 'password',
					'form-user-edit-profile_pic': "#",
					'form-user-edit-lat': user_data['lat'],
					'form-user-edit-long': user_data['long'],
					'form-user-edit-privacy': False,
					'form-user-edit-seeking_project': True,
					'form-user-edit-seeking_help': True
				},
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("<h2>Search</h2>", html)
			self.assertIn("Profile edited successfully.", html)
			self.assertIn('img src="#"', html)
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertTrue(session['CURR_USER_KEY'])

	def test_user_delete_post(self):
		"""Ensures user account deletion redirects"""
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(f"/profile/delete/{self.user.id}")

			self.assertEqual(resp.status_code,302)
			self.assertEqual(resp.location, "http://localhost/")

	def test_user_delete_post_redirected(self):
		"""Ensures user account deletion occurs"""
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				f"/profile/delete/{self.user.id}",
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Welcome to <i>Creative Project Matchmaker</i>", html)
			self.assertIn("Profile deleted successfully.", html)
			self.assertIn('An Existing Account?', html)
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']

class SearchViewTestCase(TestCase):
	"""Tests for search related views"""

	def setUp(self):
		"""Make demo data."""

		db.drop_all()
		db.create_all()
		user = User(**user_data)
		db.session.add(user)
		db.session.commit()
		self.user = user

	def tearDown(self):
		"""Clean up fouled transactions."""

		db.session.rollback()

	def test_search_get_user(self):
		"""
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			resp = client.get("/search")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Log out</button>", html)
			self.assertIn("<h2>Search</h2>", html)
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']

	def test_search_get_guest(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['GUEST_GEOCODE'] = 99
			resp = client.get("/search")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Log out of Guest Mode", html)
			self.assertIn("<h2>Search</h2>", html)
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']

class ProjectViewsTestCase(TestCase):
	"""Tests for project related views"""

	def setUp(self):
		"""Make demo data."""

		db.drop_all()
		db.create_all()
		user = User(**user_data)
		t1 = Tag(name='glass art')
		db.session.add_all([user, t1])
		db.session.commit()
		self.user = user
		self.tag1 = t1

		p1 = Project(
			**project1,
			user_id =user.id,
		)
		db.session.add(p1)
		db.session.commit()
		self.project1_id = p1.id
		p1.tags = [t1]
		db.session.commit()
		

	def tearDown(self):
		"""Clean up fouled transactions."""

		db.session.rollback()

	def test_project_detail_get(self):
		with app.test_client() as client:
			resp = client.get(f"/project/{self.project1_id}")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn(f"<h2>{project1['name']}</h2>", html)
			self.assertIn('<p>Tags: glass art</p>', html)
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			with self.assertRaises(KeyError):
				session['CURR_USER_KEY']
	
	def test_project_new_get(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			resp = client.get("/project/new")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Log out</button>", html)
			self.assertIn("<h2>New Project</h2>", html)
			self.assertIn('<option value="glass art" />', html)
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']

	def test_project_new_post(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				"/project/new", data={
					'form-project-new-name': project2['name'],
					'form-project-new-description': project2['description'],
					'form-project-new-contact_info_type': project2['contact_info_type'],
					'form-project-new-contact_info': project2['contact_info'],
					'form-project-new-lat': project2['lat'],
					'form-project-new-long': project2['long'],
				})

			self.assertEqual(resp.status_code,302)
	
	def test_project_new_post_redirected(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				"/project/new", data={
					'form-project-new-name': project2['name'],
					'form-project-new-description': project2['description'],
					'form-project-new-contact_info_type': project2['contact_info_type'],
					'form-project-new-contact_info': project2['contact_info'],
					'form-project-new-lat': project2['lat'],
					'form-project-new-long': project2['long'],
				},
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Project created successfully", html)
			self.assertIn(f"<h2>{project2['name']}</h2>", html)
			self.assertIn("Edit this Project", html)	
			self.assertTrue(session['CURR_USER_KEY'])
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertTrue(g.get('user', None))

	def test_project_edit_get(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			resp = client.get(f"/project/{self.project1_id}/edit")

			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Log out</button>", html)
			self.assertIn(" <h2>Edit Your Post</h2>", html)
			self.assertIn('Stained Glass', html)
			self.assertIn("Update Project", html)
			self.assertIn("Delete Project", html)
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertTrue(g.get('user', None))

	def test_project_edit_post(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				f"/project/{self.project1_id}/edit", data={
					'form-project-edit-name': project2['name'],
					'form-project-edit-description': "#",
					'form-project-edit-contact_info_type': project2['contact_info_type'],
					'form-project-edit-contact_info': project2['contact_info'],
					'form-project-edit-lat': project2['lat'],
					'form-project-edit-long': project2['long'],
					'form-project-edit-tags': "",
				})

			self.assertEqual(resp.status_code,302)
	
	def test_project_edit_post_redirected(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				f"/project/{self.project1_id}/edit", data={
					'form-project-edit-name': project2['name'],
					'form-project-edit-description': "#",
					'form-project-edit-contact_info_type': project2['contact_info_type'],
					'form-project-edit-contact_info': project2['contact_info'],
					'form-project-edit-lat': project2['lat'],
					'form-project-edit-long': project2['long'],
					'form-project-edit-tags': "",
				},
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Project edited successfully.", html)
			self.assertIn(f"<h2>{project2['name']}</h2>", html)
			self.assertIn("<p><i>#</i></p>", html)
			self.assertIn("Edit this Project", html)	
			self.assertTrue(session['CURR_USER_KEY'])
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertTrue(g.get('user', None))

	def test_project_delete_post(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(f"/project/{self.project1_id}/delete")

			self.assertEqual(resp.status_code,302)
			self.assertEqual(resp.location, "http://localhost/search")
	
	def test_project_delete_post_redirected(self):
		with app.test_client() as client:
			with client.session_transaction() as change_session:
				change_session['CURR_USER_KEY'] = self.user.id
			g = {"user": user_data}
			resp = client.post(
				f"/project/{self.project1_id}/delete",
				follow_redirects=True
			)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code,200)
			self.assertIn("Log out</button>", html)
			self.assertIn("Project deleted successfully.", html)
			self.assertIn("<h2>Search</h2>", html)
			self.assertTrue(session['CURR_USER_KEY'])
			with self.assertRaises(KeyError):
				session['GUEST_GEOCODE']
			self.assertTrue(g.get('user', None))

class APIGeocodeTestCase(TestCase):
	"""Tests for API geocode"""

	def test_api_geocode(self):
		with app.test_client() as client:
			resp = client.get("/api/geocode?address=3211%20Grant%20McConachie")

			self.assertEqual(resp.status_code, 200)

			data = resp.json
			self.assertEqual(data['results'][0]['address_components'][0]['long_name'], "3211")

class APINeighbourhoodTestCase(TestCase):
	"""Tests for api neighbourhood"""

	def setUp(self):
		"""Make demo data."""

		db.drop_all()
		db.create_all()
		user = User(**user_data)
		t1 = Tag(name='glass art')
		db.session.add_all([user, t1])
		db.session.commit()
		self.user = user
		self.tag1 = t1

		p1 = Project(
			**project1,
			user_id =user.id,
		)
		db.session.add(p1)
		db.session.commit()
		self.project1_id = p1.id
		p1.tags = [t1]
		db.session.commit()
		

	def tearDown(self):
		"""Clean up fouled transactions."""

		db.session.rollback()

	def test_api_neighborhood(self):
		with app.test_client() as client:
			resp = client.get("""api/neighborhood?north=49.376019219200614&south=49.107045276672984&east=-122.75234442225093&west=-123.5310004281103""")

			self.assertEqual(resp.status_code, 200)
			data = resp.json
			self.assertEqual(data['projects'][0]['name'], project1['name'] )

class APITagsTestCase(TestCase):
	"""Tests for api tags"""

	def setUp(self):
		"""Make demo data."""

		db.drop_all()
		db.create_all()
		t1 = Tag(name='glass art')
		t2 = Tag(name='renovations')
		db.session.add_all([t1, t2])
		db.session.commit()

	def tearDown(self):
		"""Clean up fouled transactions."""

		db.session.rollback()

	def test_api_neighborhood(self):
		with app.test_client() as client:
			resp = client.get("/api/tags")

			self.assertEqual(resp.status_code, 200)
			data = resp.json
			self.assertEqual(data, ['glass art', 'renovations'] )