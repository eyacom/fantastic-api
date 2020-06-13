# fantastic-api
Fantastic-API  is a recruitment test to check the candidate performance on : 

* Ability to run a project following a poor documentation 
* Ability to implement a feature following a TDD approach
* Ability to git merge branches,  push commits and make a pull request 

## TODO

- Follow the instructions below to clone and run this project 
- Explore and make a proposal for the issues opened by @yurilaaziz 


## Installation

* Create a python3 virtualenv

`python3 -m venv venv`

* Source the virtual env

`source venv/bin/activate`

* Install the dependencies 

`pip install -r requirements.txt`

## Run 

* Start the developement server on default' Flask port 5000 

`python server.py`

* Browse the swagger UI and interact with the API on http://127.0.0.1:5000

## Tests

Install tests dependencies 

`pip install  tox pytest pytest-cov flake8`

Run tests 

`pytest`

Launch tests using tox 

`tox`

