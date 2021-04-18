## Creative Project Matchmaker

A web app where users can create or find posts to meet like-minded individuals who are looking to collaborate on creative projects in their area. 

#### Tech Stack:

- OOP, Python, Flask, Jinja, WTForms, SQLAlchemy, Posgres SQL, JavaScript, AJAX, HTML5, CSS, Bootstrap, Google Maps Geocoding API and JavaScript API

#### To run:
- NOTE: You require a file in the the project root directory called `credentials.py` containing a variable with your Google Maps API key `API_KEY = ....`
- Create a virtual environment, and enter the venv -> in Command Line Interface (CLI) type `python -m venv venv` (Mac) or `. venv/scripts/activate` (Windows)
- install pip dependencies -> in CLI type `pip install -r requirements.txt`
- create database matchmaker -> in CLI type `createdb matchmaker`
- seed database with seed.py -> in CLI type `python seed.py`
- start the flask server -> in CLI type `flask run`
- go to URL given by CLI or `http://127.0.0.1:5000/`

#### Testing:
(In Progress) ~~~~~~~~************************************************************************************** 

#### Test user (In Progress)  ~~~~~~~~************************************************************************************** 
- Username: `test@test.com`
- Password: `password`

#### Routes

- GET - http://127.0.0.1:5000/ (/)
  - Landing Page
  - with options to sign up, log in, or continue as guest
  - only renders if user is not logged in during this session (Flask session is checked for data), otherwise redirects to Search page
  - authorization required: not logged in
  
- GET - http://127.0.0.1:5000/profile/new (/profile/new)
  - Sign Up Form
  - renders sign up form for user
  - only renders if user is not logged in during this session (Flask session is checked for data), otherwise redirects to Search page
  - authorization required: not logged in
- POST - http://127.0.0.1:5000/profile/new (/profile/new)
  - Process Sign Up Form
  - retrieves sign up form data from user and signs up user into the system
  - upon successful sign up, it logs in the user, and redirects to Search page
  - only executes logic if user is not logged in during this session (Flask session is checked for data), otherwise redirects to Search page
  - authorization required: not logged in
  
- GET - http://127.0.0.1:5000/login (/login)
  - Login Form
  - renders login form for user
  - only renders if user is not logged in during this session (Flask session is checked for data), otherwise redirects to Search page
  - authorization required: not logged in
- POST - http://127.0.0.1:5000/login (/login)
  - Process Login Form
  - retrieves login form data from user, logs user into the system and redirects to Search page
  - only renders if user is not logged in during this session (Flask session is checked for data), otherwise redirects to Search page
  - authorization required: not logged in
  
- POST - http://127.0.0.1:5000/logout (/logout)
  - Logs Out Registered User or Guest
  - clears Flask session
  - authorization required: logged in as Guest or Registered User
  
- GET - http://127.0.0.1:5000/guest (/guest)
  - Guest Form
  - renders guest form for user to choose geocode information
  - only renders if user is not logged in during this session (Flask session is checked for data), otherwise redirects to Search page
  - authorization required: not logged in
- POST - http://127.0.0.1:5000/guest (/guest)
  - Guest Form
  - processes guest geocode information, and redirects to the Search page
  - only executes logic if user is not logged in during this session (Flask session is checked for data), otherwise redirects to Search page
  - authorization required: not logged in
  
- GET - http://127.0.0.1:5000/search (/search)
  - Search Page
  - renders search page where user interactions use AJAX
  - only renders if user is logged in during this session (Flask session is checked for data), otherwise redirects to Landing page
  - authorization required: logged in as Guest or Registered User
  
- GET - http://127.0.0.1:5000/profile/edit (/profile/edit)
  - Registered User Profile Edit Form
  - renders profile edit form for a logged in user
  - only renders if user is logged in during this session as a Registered User (Flask session is checked for data), otherwise redirects to Search page (if logged in as a Guest) or Landing page (if not logged in at all)
  - authorization required: logged in as Registered User
- POST - http://127.0.0.1:5000/profile/edit (/profile/edit)
  - Registered User Profile Edit Form
  - processes profile edit form data for a logged in user, saves changes if user password matches and redirect to Search page
  - only executes logic if user is logged in during this session as a Registered User (Flask session is checked for data), otherwise redirects to Search page (if logged in as a Guest) or Landing page (if not logged in at all)
  - authorization required: logged in as Registered User
  
- POST - http://127.0.0.1:5000/profile/delete/<user_id> (/profile/delete/<user_id>)
  - Registered User Profile Edit Form
  - processes profile edit form data for a logged in user, saves changes if user password matches and redirect to Search page
  - only executes logic if user is logged in during this session as the same Registered User as the account being deleted (Flask session is checked for data), otherwise redirects to Search page (if logged in as a Guest) or Landing page (if not logged in at all)
  - authorization required: logged in as Registered User, same as one being deleted
  
- GET - http://127.0.0.1:5000/project/new (/project/new)
  - New Project Form
  - renders new project form for a logged in user
  - only renders if user is logged in during this session as a Registered User (Flask session is checked for data), otherwise redirects to Search page (if logged in as a Guest) or Landing page (if not logged in at all)
  - authorization required: logged in as Registered User
- POST - http://127.0.0.1:5000/project/new (/project/new)
  - Process New Project Form
  - processes new project form for a logged in user, creates project, and redirects to the newly created project detail page
  - only renders if user is logged in during this session as a Registered User (Flask session is checked for data), otherwise redirects to Search page (if logged in as a Guest) or Landing page (if not logged in at all)
  - authorization required: logged in as Registered User
  
- GET - http://127.0.0.1:5000/project/<project_id> (/project/<project_id>)
  - Project Detail Page
  - renders details of a specific project
  - authorization required: none
  
- GET - http://127.0.0.1:5000/project/<project_id>/edit (/project/<project_id>/edit)
  - Project Edit Form
  - renders form for editing a specific project
  - only renders if user is logged in during this session as the Registered User owner of the post (Flask session is checked for data), otherwise redirects to Project Detail page
  - authorization required: logged in as Registered User and owner of post
- POST - http://127.0.0.1:5000/project/<project_id>/edit (/project/<project_id>/edit)
  - Process Project Edit Form
  - processes form data for editing a specific project and redirects to the updated Project Detail page
  - only executes logic if user is logged in during this session as the Registered User owner of the post (Flask session is checked for data), otherwise redirects to Project Detail page
  - authorization required: logged in as Registered User and owner of post

- POST - http://127.0.0.1:5000/project/<project_id>/delete (/project/<project_id>/delete)
  - Delete Project
  - deletes a specific project
  - only executes logic if user is logged in during this session as the Registered User owner of the post (Flask session is checked for data), otherwise redirects to Project Detail page
  - authorization required: logged in as Registered User and owner of post

#### Backend Routes

- GET - http://127.0.0.1:5000/api/geocode?<address> (/project/api/geocode?<address>)
  - Geocoding API Data Submit
  - address = text, a URL safe address viable for the Google Maps Geocoding API
  - retrieves the address and makes a GET request, returning latitude and longitude
  - authorization required: ****************~~~~

- GET - http://127.0.0.1:5000/api/neighborhood?<north>&<south>&<east>&<west> (/project/api/neighborhood?<north>&<south>&<east>&<west>)
  - Retrieve Nearby Projects
  - retrieves the nearby projects using the latitude and longitude bounds of the user's viewpoint
  - authorization required: ****************~~~~

- GET - http://127.0.0.1:5000/api/tags (/api/tags)
  - Retrieve All Existing Tags List
  - retrieves a JSON list of all existing tags
  - authorization required: ****************~~~~
