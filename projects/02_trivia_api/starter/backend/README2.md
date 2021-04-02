# Full Stack Trivia

This project is a trivia game web application for Udacity employees and students. All users have configuration privileges to add new trivia content (questions, answers, and difficulty level), configure the answers to show or be hidden, search for specific questions, and delete questions from the game. When the configurations are set and the game is initiated, then the trivia game application will randomize the questions within a specific category or no categories for game play.

As part of the Full Stack Nanodegree program, the trivia game application provides students the opportunity to apply the concepts learned in Course 2: API Development and Documentation. The front end software has been implemented by Udacity and provided as a baseline for students to immediately implement the back end of the application and documentation. By completing this project, students will have a solid foundation of unit testing, backend endpoints concepts, and web API documentation.
The code in this application adheres to the PEP 8 style guide and follows common best practices. 





## Getting Started
 
### Development Environment: 
- Verify git is installed by checking the version. If not, install git.
  
```bash
  $ git --version
  $ git clone https://github.com/alvaroandresgarayromero/FSND.git
```
- In the terminal create a virtual environment in the .../02_trivia_api project directory

```bash  
  $ python3 -m venv env
  $ source env/bin/activate
```

### Backend:

- In the virtual environment, go to ..../02_trivia_api/starter/backend to see, and install the dependencies

```bash  
$ pip install -r requirements.txt
```

 
- To run the application run the following commands in the backend path:

```bash  
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

- The application is run on http://127.0.0.1:5000/ by default  

### Frontend:

- Verify node and npm is already installed in your system. If not, download and install the software from Node.js

```bash 
$ node -v
$ npm -v
```

- In the virtual environment, go to ..../02_trivia_api/starter/frontend and install Bootstrap3

```bash 
$ npm init -y
$ npm install bootstrap@3
```

- To run the application run the following command in the frontend path:

```bash
$ npm start
```

- The application is run on http://127.0.0.1:3000/ by default  

### Test:
- See STP requirements in the “Backend Requirements” section.


## Backend Requirements:

### System Requirement Specification (SRD)

- SRD_01 - Context:
  - A trivia record is composed of a question, answer, difficulty, and category

- SRD_02 - Requirement:
  - The software shall provide the client a method to get recorded trivia records.  
- SRD_03 - Requirement:
  - The software shall perform pagination when getting recorded trivia records.
- SRD_04 - Requirement:
  - The software shall provide the client a method to get all categories
- SRD_05 - Requirement:
  - The software shall provide the client a method to delete trivia records that persist once deleted
- SRD_06 - Requirement:
  - The software shall provide the client a method to create trivia records that persist once created
- SRD_07 - Requirement:
  - The software shall provide the client a method to get trivia records based on category
- SRD_08 - Requirement:
  - The software shall provide the client a method to get trivia records based on a search term found in the question content.
- SRD_09 - Requirement:
  - The software shall provide the client a method to get non-repeating randomized trivia records by category or all categories during play mode.
- SRD_10 - Requirement
  - The software shall provide the client with useful information when an assert occurs

### Software Requirements Specification (SRS)
- SRS_01 - Requirement: 
  - Satisfies: SRD_02, SRD_03, SRD_10
  - The software shall get a minimum of 10 or less (whichever is smallest) trivia records per page scroll during ‘/questions?page=value’ GET request commands
  - Rational: A page scroll is a moving window that traverses the records at a rate of 10 records per page where the 1st page points to the start of the records.
- SRS_02 - Requirement: 
  - Satisfies: SRD_02, SRD_03, SRD_10
  - The software shall respond with a list of questions, number of total questions, current category, list of categories during ‘/questions?page=value’ GET request commands
- SRS_03 - Requirement: 
  - Satisfies: SRD_04
  - The software shall respond with a list of all categories during ‘/categories’ GET request commands
- SRS_04 - Requirement: 
  - Satisfies: SRD_06, SRD_10
  - The software shall create trivia records during ‘/questions POST request commands
- SRS_05 - Requirement: 
  - Satisfies: SRD_05, SRD_10
  - The software shall delete trivia records during ‘/questions/<int:value> DELETE request commands
- SRS_06 - Requirement: 
  - Satisfies: SRD_07, SRD_10
  - The software shall respond with a list of questions related to the requested category including the number of total questions during ‘/categories/<int:id_value>/questions’ GET request commands
- SRS_07 - Requirement: 
  - Satisfies: SRD_08, SRD_10
  - The software shall respond with a list of questions related to the requested search term including the number of total questions during ‘/questions’ POST request commands
- SRS_08 - Requirement: 
  - Satisfies: SRD_09, SRD_10
  - The software shall get a single trivia record related to the current category or all categories during ‘/quizzes POST request commands in accordance to the following conditions:
    - The trivia record is randomized  
    - The trivia record does not repeat itself during a play session
- SRD_09 - Requirement:
  - The software shall provide the client a method to get non-repeating randomized trivia records by category or all categories during play mode.


### Software Test Specification (STP)	
- STP_00 - Context
  - A test must complete the test suite with no errors in order to be considered a PASS. A test suite that does not complete the entirety of the test is considered a FAILURE.
  - Complete the instructions in ‘The Getting Started’ section
  - Verify postgresSQL is installed in the test system. If not, install the latest on the test system
    - psql --version
    - Go to .../02_trivia_api/starter/backend and create a test database:
```bash
$ dropdb trivia_test
$ createdb trivia_test
$ psql trivia_test < trivia.psql
```
  - Go to .../02_trivia_api/starter/backend where the test_flaskr.py unit test is located 
  - To run individual tests, follow the ‘STP_00 - Requirement’ instructions. Otherwise, to execute all tests run:
```bash
$ python test_flaskr.py
```

- STP_01 - Requirement
  - Satisfies: SRS_01
  - Verify that the software can paginate a minimum of 10 or less trivia records per page during ‘questions?page=value’ GET request commands 
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_01
    - Pass/Fail results will be displayed on the command line
- STP_02 - Requirement
  - Satisfies: SRS_01, SRS_02
  - Verify that the software asserts when there are no trivia records to paginate during a ‘questions?page=value’ GET request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_02
    - Pass/Fail results will be displayed on the command line
- STP_03 - Requirement
  - Satisfies: SRS_02
  - Verify that the software outputs the expected field names and datatype during ‘questions?page=value’ GET request commands.
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_03
    - Pass/Fail results will be displayed on the command line
- STP_04 - Requirement
  - Satisfies: SRS_03
  - Verify that the software outputs the expected field names and datatype during ‘/categories’ GET request commands.
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_04
    - Pass/Fail results will be displayed on the command line
- STP_05 - Requirement
  - Satisfies: SRS_04
  - Verify that the software creates a trivia record during ‘/questions’ POST request commands.
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_05
    - Pass/Fail results will be displayed on the command line
- STP_06 - Requirement
  - Satisfies: SRS_04
  - Verify that the software asserts when an invalid trivia record fails to create during ‘/questions’ POST request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_06
    - Pass/Fail results will be displayed on the command line
- STP_07 - Requirement
  - Satisfies: SRS_05
  - Verify that the software deletes a trivia record during ‘/questions/<int:value> DELETE request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_07
    - Pass/Fail results will be displayed on the command line
- STP_08 - Requirement
  - Satisfies: SRS_05
  - Verify that the software asserts on undefined trivia records during ‘/questions/<int:value> DELETE request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_08
    - Pass/Fail results will be displayed on the command line
- STP_09 - Requirement
  - Satisfies: SRS_06
  - Verify that the software can paginate a minimum of 10 or less trivia records per page during ‘/categories/<int:id_value>/questions’ GET request commands 
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_09
    - Pass/Fail results will be displayed on the command line
- STP_10 - Requirement
  - Satisfies: SRS_06
  - Verify that the software asserts when there are no trivia records to paginate during a ‘/categories/<int:id_value>/questions’ GET request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_10
    - Pass/Fail results will be displayed on the command line
- STP_11 - Requirement
  - Satisfies: SRS_06
  - Verify that the software asserts when the category requested does not exist during a ‘/categories/<int:id_value>/questions’ GET request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_11
    - Pass/Fail results will be displayed on the command line
- STP_12 - Requirement
  - Satisfies: SRS_06
  - Verify that the software outputs the expected field names and datatype during ‘/categories/<int:id_value>/questions’ GET request commands.
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_12
    - Pass/Fail results will be displayed on the command line
- STP_13 - Requirement
  - Satisfies: SRS_07
  - Verify that the software can paginate a minimum of 10 or less trivia records per page during ‘/questions’ search POST request commands 
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_13
    - Pass/Fail results will be displayed on the command line
- STP_14 - Requirement
  - Satisfies: SRS_07
  - Verify that the software searches the expected trivia records during ‘/questions’ search POST request commands 
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_14
    - Pass/Fail results will be displayed on the command line
- STP_15 - Requirement
  - Satisfies: SRS_07
  - Verify that the software asserts when there are no trivia records to paginate during ‘/questions’ search POST request commands 
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_15
    - Pass/Fail results will be displayed on the command line
- STP_16 - Requirement
  - Satisfies: SRS_07
  - Verify that the software outputs the expected field names and datatype during ‘/questions’ search POST request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_16
    - Pass/Fail results will be displayed on the command line
- STP_17 - Requirement
  - Satisfies: SRS_08
  - Verify that the software gets a random single trivia record by category, and by all categories during ‘/quizzes POST request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_17
    - Pass/Fail results will be displayed on the command line
- STP_18 - Requirement
  - Satisfies: SRS_08
  - Verify that the software does not get a trivia record that has been previously retrieved during ‘/quizzes POST request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_18
    - Pass/Fail results will be displayed on the command line
- STP_19 - Requirement
  - Satisfies: SRS_08
  - Verify that the software asserts for undefined requests during ‘/quizzes POST request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_19
    - Pass/Fail results will be displayed on the command line
- STP_20 - Requirement
  - Satisfies: SRS_08
  - Verify that the software outputs the expected field names and datatype  during ‘/quizzes POST request commands
  - Description:
    - Execute steps in STP_00 to configure the test system for testing
    - Run 
    - $: python3 -m unittest test_flaskr.TriviaTestCase.STP_20
    - Pass/Fail results will be displayed on the command line
  
## API Reference:

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/ and frontend app is hotels at the default, http://127.0.0.1:3000
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
- Errors are returned as JSON objects in the following format:
```bash
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

- The API will return three error types when requests fail
```bash
400: Bad Request
404: Resource Not Found
422: Not Processable
500: Internal Server Error
```
 
### Resource endpoint library
- GET /categories
  - General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a list of categories id:category_strings (key:value) pairs.
    - Sample: curl http://127.0.0.1:5000/categories
```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```


- GET /questions?page=value
  - General:
    - Fetches a dictionary of questions that has a list of question objects where the list of questions are paginated up to 10 questions per page 
    - Request Argument:
      - page  [optional] : value is numerical integer 
    - Returns a list of available questions, categories, current category, and total questions.
    - Sample: curl http://127.0.0.1:5000/questions?page=1
```bash

 {
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": "NA", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ....
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "total_questions": 22
}
```

- DELETE /questions/<int:a_id>
  - General:
    - Removes a question record from the database
    - Request Argument:
      - a_id [integer]: id key value that represents the question record to be remove
    - Returns a dictionary with the question id that was removed from the database.  
    - Sample: curl -X DELETE http://127.0.0.1:5000/questions/2
```bash
{
  "question_id": 2
}
```

- POST /questions/ 
  - JSON searchTerm:
    - General:
      - Searches for question objects that have the keyword requested where the list of questions are paginated up to 10 questions per page 
      - Request Arguments:
        - searchTerm [json type] : String used for query search
      - Returns a dictionary, questions, with a list of question objects, the current category and number of total questions filtered
      - Sample: curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm":"title"}'
```bash

{
  "currentCategory": "None", 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
 	 "totalQuestions": 2
}
```

- JSON create new question:
  - General:
    - Creates a new question record 
    - Request Arguments:
      - question [json type] : String with question contents
      - answer [json type] : String with answer contents
      - category [json type] : Numerical category id string
    - Returns a dictionary, question, with information about the created question record, a dictionary with the id created and the new total number of questions records.
    - Sample: curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question":"new_question","answer":"new_answer","category":"2"}'
```bash
{
  "created": 28, 
  "question": {
    "answer": "new_answer", 
    "category": 2, 
    "difficulty": null, 
    "id": 28, 
    "question": "new_question"
  }, 
  "total_questions": 22
}
``` 
- GET /categories/<int:id_value>/questions
  - General:
    - Fetches a list of question records by category where the list of questions are paginated up to 10 questions per page 
    - Request Arguments:
      - id_value [integer] : Category id 
      - page [optional] : Pagination (.../questions?page=value) where value is an integer
    - Returns a dictionary, question, with information about the created question record, a dictionary with the current category, and the total number of questions filtered.
    - Sample: curl -X GET http://127.0.0.1:5000/categories/0/questions
```bash
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
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
  "total_questions": 3
}
```
- POST /quizzes/ 
  - General:
    - Fetches a random question record by category or no categories. If the question record has already been chosen, then it will not be repeated. 
    - Request Arguments:
      - previous_question [json parameter ] : List of category ids that should be ignored
      - quiz_category [json parameter] : Request category information
      - type [string]: Category string name where ‘click’ means all categories
      - id [integer]: Category key id  
    - Returns a dictionary, question, with information about the created question record, a dictionary with the current category, and the total number of questions filtered.
    - Sample: curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":"[]","quiz_category":{"type":"click", "id":"0"}}'
    - Sample (where question object id 4 will never be chosen): curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions":"[4]","quiz_category":{"type":"click", "id":"0"}}'
```bash
{
  "question": {
    "answer": "Agra", 
    "category": 3, 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }
}
```
## Authors
- Alvaro Garay - Unit Test, Backend endpoints implementations, documentation, requirement definitions
- Udacity employees - Unit Test, Backend, Frontend application baselines


## Acknowledgements
- Coach Caryn and Udacity Mentors



