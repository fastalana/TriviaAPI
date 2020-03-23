# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Documentation

### Getting Started
* Backend Base URL: http://127.0.0.1:5000/
* Authentication: Authentication or API keys are not used in the project yet.

### Error Handling
Errors are returned in the following JSON format:
```
    {
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }
```
There are error handlers for 400, 404, 422, and 500 errors.

### Endpoints
#### GET /categories
_Retrieves all Categories_
* _Sample Request:_ `curl http://127.0.0.1:5000/categories`
* _Sample Response:_
```
{
  "category": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }
  ], 
  "success": true, 
  "total_categories": 2
}
```

#### GET /questions
_Retrieves all Questions_
* _Sample Request:_ `curl http://127.0.0.1:5000/questions`
* _Sample Response:_
```
{
  "question": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true, 
  "total_questions": 24
}
```

#### DELETE /questions/<int:question_id>
_Deletes a question_
* _Sample Request:_ `curl -X DELETE http://127.0.0.1:5000/questions/9`
* _Sample Response:_
```
{
  "deleted_question_id": 9, 
  "success": true, 
  "total_questions_remaining": 1
}
```

MORE
#### POST /questions
_Searches for a question OR creates a new question_
**Search for a question**
* _Sample Request:_ `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"search":"Who"}'`
* _Sample Response:_
```
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions_in_search": 3
}
```
**Creating a new question**
* _Sample Request:_ `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Which Williams sister has won more Grand Slam titles?", "answer":"Serena", "categeory":"6", "difficulty":"3"}'`
* _Sample Response:_
```
{
  "created": 5, 
  "success": true, 
  "total_questions": 3
}
```
#### GET /categories/<int:category_id>/questions>
_Gets questions based on a category._
* _Sample Request:_ `curl http://127.0.0.1:5000/categories/1/questions`
* _Sample Response:_
```
{
  "category": 1, 
  "questions": [
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions_in_category": 2
}
```
#### POST /quizzes
_Gets a question to play the quiz._
* _Sample Request:_ `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "Sport", "id": "6"}}'`
* _Sample Response:_
```
{
  "question": {
    "answer": "Uruguay", 
    "category": 6, 
    "difficulty": 4, 
    "id": 11, 
    "question": "Which country won the first ever soccer World Cup in 1930?"
  }, 
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```