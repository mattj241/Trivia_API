# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql --> Max/Unix
psql -U <username> -d trivia_test -a -f trivia.psql --> windows bash
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions(?page=1)'
POST '/questions'
DELETE '/questions/<int:id>'
POST '/quizzes'

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

GET '/questions(?page=1)'
- Fetches a dictionary that contains most of the data used by the trivia app. Automatically considers pagination up to the first 10 units. See below request args if data following the first 10 units is desired.
- Request Args: "page", type: int, default=1. 
- Returns: All the questions specified in the initial request, the amount of those questions, as well as all the categories they all fall into.
Request Example: '/questions?page=2'
Response Example: 
{ 
    "categories": {'1' : "Science",
                '2' : "Art",
                '3' : "Geography",
                '4' : "History",
                '5' : "Entertainment",
                '6' : "Sports"}
    "questions": [
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
        },
        ...
    ],
    "total_questions" : 24
}

DELETE '/questions/<int:id>'
- Attempts to remove the question from the trivia board specified by the question identifier within the URL
- Request args: One arg defined as a URL parameter to indicate unique key of the question targetted to delete
- Returns: Upon successful deletion, the entire new set of questions are sent back to the client. If the ID specified could not be found, a 404 will be sent back to the client:
Request Example: '/questions/20'
Response Example: 
Successful:
{
    "categories": {'1' : "Science",
                '2' : "Art",
                '3' : "Geography",
                '4' : "History",
                '5' : "Entertainment",
                '6' : "Sports"}
    "questions": [
                {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        ...
    ],
    "total_questions" : 23
}
Unsuccessful:
{
        "error": 404,
        "message": "Data was not found."
}

POST '/questions'
- Endpoint capable of adding a new question formatted by the user. It is also capable of forming a search request to filter for certain questions. Since search activity takes priority, if the search term parameter is found in the HTTP message body, it will take priority over adding a question.
- Request Args: 
A)
All necessary info for adding questions shall be configured within the BODY of the HTTP request. 4 total parameters: "question", "answer", "difficulty" (1-5, 1 being easy and being difficult), and "category"

B)
One field is required to search for a question, called "searchTerm"

- Returns: 
A) If the addition request was formatted correctly, the client will receive 201 back from the server indicating the data was written into the trivia database. If the request is formatted incorrect, an error will occur (like 422 Unprocessable Entity)

B) The search function shall return all questions that contain the "searchTerm" content within the "question" attribute 

Request Example A): '/questions'
                    Body: 
                    {
                        "question" : "What production vehicle holds the world record for fasted 0-60 mph time?",
                        "answer" : "Tesla Model S Plaid",
                        "category" : 4,
                        "Difficulty" : 2
                    }
Request Example B): '/questions'
                    Body: 
                    {
                        "searchTerm" : "Cassius Clay"
                    }

Response Examples A):
Successful:
{
    "message" : "201 Question successfully created"
}
Unsuccessful:
{
    "error": 422,
    "message": "The request was well-formed but was unable to be followed due to semantic errors."
}

Response Examples B):
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Science",
    "questions": [
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "total_questions": 1
}

POST '/quizzes'
- This endpoint is responsible for controlling the trivia game. The trivia game can be played for all defined categories or one specific category. Successive calls of this endpoint occur through the entire game, keeping track of what questions were previously asked until no more remain. 
- Request Args: A list of previously asked questions (defined below as "Current_Question"), and the selected category for the trivia quiz. Category ID 0 is considered all categories!
- Response: Ultimately, every call of this endpoint will return a random question from the remaining question set.

Current_Question format:
{
    "question": {
        "question" : "yyy",
        "answer" : "zzz",
        "id" : 20,
        "category": : 1
    }
}
Request Example: /quizzes
                 Body:
                {
                    "previous_questions" : [20, 21],
                    "quiz_category" : {
                        "type": "Science",
                        "id": "1"
                    }
                }
Response Example (Current_Question format):
{
    "question": 
    {
        "answer":"Alexander Fleming",
        "category":1,
        "difficulty":3,
        "id":21,
        "question":"Who discovered penicillin?",
        "category": : 1}
    }
}




## Testing
To run the tests, cd to ./backend and run

```
dropdb trivia_test
createdb trivia_test
psql -U <username> -d trivia_test -a -f trivia.psql
python test_flaskr.py
```
