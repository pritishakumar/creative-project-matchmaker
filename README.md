## Creative Project Matchmaker

* NOTE: You require a file in the the project root directory called `credentials.py` containing a variable with your Google Maps API key `API_KEY = ....`

* Create a virtual environment, and enter the venv ->  `python -m venv venv` &`. venv/scripts/activate`
* `pip install -r requirements.txt`
* create database matchmaker -> `createdb matchmaker`
* seed database with seed.py -> `python seed.py`
* `flask run`

* go to URL given by Command Line Interface 
