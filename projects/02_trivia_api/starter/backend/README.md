# Backend - Full Stack Trivia API 

The current project is developed as backend of Udatrivia. It is using Python, sqlalchemy as ORM & flask as framework. With regard to the DB it is using postgres. It comes with everything built-in. It consists of some API endpoints that serve categories and their questions & answers. It also include endpoints to create and delete them. The most attractive part of the project is the use of CORS so that the requests can be made from outside the world.   
###Running the application

This project is thought to be run independently almost without any intervention from the executor/reviewer. Also, it is a firm candidate to be relased into Stagging env. It is using docker-compose under the hood. The backend, frontend & the database as well as the interaction between the pieces are already setup so that the only thing needed to run the application is:
```shell
cd ../projects/02_trivia_api/starter/
sh start.sh
```
The script above will install the dependencies setup env vars, secrets.

Once executed go to http://localhost:3000 and start playing

### Running test
```shell
sh test.sh
```
Once inside the container execute `python test_flaskr.py`. The database for testing is already up and running.

### List of endpoints

```
GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

DELETE /questions/id/
- Deletes a question given its id
- Parameters: id of the question
- Returns: An object on succeding
  {'success': True}
- Returns: An object on failing
{'success': False,
'error': 405,
'message': f'method not allowed: {error}'}


POST /questions/
- Inserts a question in the database 
- Parameters: question, answer, category, difficulty of the question
- Returns: An object on succeding
  {
    'success': True,
    'created': 1,
    'questions': ['question1', 'question2', 'question3'],
    'total_questions': 90
  }
- Returns: An object on failing
  {
     'success': False,
     'error': 422,
     'message': 'unable to process'
  }
  
GET /questions/search/?search_term=abcd
- Fetches all the questions that have a particular search_term in the question statement
- Parameters: search_term
- Returns: A list (could be empty) of questions which statement includes the search_term
  {
    'success': True,
    'questions': []
  }
- Returns: An object on failing
  {
    'success': False,
    'error': 422,
    'message': 'unable to process'
  }
  
  
GET /questions/list/?page=1
- Fetches all the questions that belong to the M page of N questions that belong to a particular category
- Parameters: page
- Returns: A list (could be empty) of questions which statement includes the search_term
  {
    'success': True,
    'questions': [],
    'total_questions': 10,
    'categories': [],
    'current_category': 1
  }
- Returns: An object on failing
  {
    'success': False,
    'error': 422,
    'message': 'unable to process'
  }
  
GET /categories/<id>/questions
- Fetches all the questions that belong to a particular category
- Parameters: id
- Returns: A list (could be empty) of questions that belong to that category
  {
    'success': True,
    'questions': [],
    'total_questions': 10,
    'current_category': 1
  }
- Returns: An object on failing
  {
    'success': False,
    'error': 422,
    'message': 'unable to process'
  }
  


GET /questions/play/?quiz_category=1&previous_questions=1,2,3
- Fetches the next question that belongs to a particular category without repeting the same question
- Parameters: quiz_category & previous_questions
- Returns: A question that belong to that category
  {
    'success': True,
    'question': question,
    'number_of_questions': 10,
    'answer': answer,
    'id': id
  }
- Returns: An object on failing. It could fail in case either or both parameters are missing from the URL
  {
    'success': False,
    'error': 422,
    'message': 'unable to process'
  }
```

## Steps needed without docker-compose: To run the tests, run
```
PGPASSWORD=${DB_TEST_PASSWORD} dropdb -h trivia_db_test -U trivia_test trivia_test
PGPASSWORD=${DB_TEST_PASSWORD} createdb -h trivia_db_test -U trivia_test trivia_test
PGPASSWORD=${DB_TEST_PASSWORD} psql -h trivia_db_test -U trivia_test trivia_test < trivia.psql
python test_flaskr.py
```

## Steps needed without docker-compose: Populate the DB
```
PGPASSWORD=${DB_PASSWORD} dropdb -h trivia_db -U trivia trivia
PGPASSWORD=${DB_PASSWORD} createdb -h trivia_db -U trivia trivia
PGPASSWORD=${DB_PASSWORD} psql -h trivia_db -U trivia trivia < trivia.psql
```
