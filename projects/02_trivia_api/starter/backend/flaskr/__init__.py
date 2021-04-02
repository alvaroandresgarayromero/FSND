import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from collections import deque
from math import ceil
from models import setup_db, Question, Category
import re

QUESTIONS_PER_PAGE = 10
DEFAULT_PAGE = 1
MIN_PAGE = 1

'''
  Saturates value to be within bounds
  INPUT:
    value [int]: requested value
    min_value [int]: min bound value
    max_value [int]: max bound value
  OUTPUT
    value [int]: bounded between min_value <= value <= max_value
'''


def saturate(value, min_value, max_value):
    return min(max(value, min_value), max_value)


'''
  Paginate the number of question objects

  INPUT:
    selection [list]: question object list
    request: From flask.request to get page argument from client
  OUTPUT
    questions [dict]: list of formatted questions objects
'''


def paginate(selection, request):
    # saturate client page value
    selection = deque(selection)
    num_selection = len(selection)
    max_page = ceil(num_selection / QUESTIONS_PER_PAGE)

    client_page = request.args.get('page', DEFAULT_PAGE, type=int)
    client_page_sat = saturate(client_page,
                               MIN_PAGE,
                               max_page)

    if client_page != client_page_sat:
        # client_page is out of bounds
        raise Exception("Sorry, page is out of bounds")

    # pagination: rebase page_num
    # to base 0 for left circular shift
    num_shift = (client_page - 1) * QUESTIONS_PER_PAGE
    selection.rotate(-1 * num_shift)
    questions = [selection[n].format()
                 for n in range(min(num_selection - num_shift,
                                    QUESTIONS_PER_PAGE))]

    return questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. 
  Delete the sample route after completing the TODOs
  '''
    # any origin can access the api uri
    CORS(app,
         resources={r"/api/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    # after a request is received run this method
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection_c = Category.query.\
            order_by(Category.id).all()

        categories = {}
        for category in selection_c:
            categories[category.id] = category.type

        return jsonify({'categories': categories})

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom 
  of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions', methods=['GET'])
    def get_questions():

        try:
            selection = Question.query.\
                order_by(Question.id).all()
            questions = paginate(selection, request)

            selection_c = Category.query.\
                order_by(Category.id).all()
            categories = {}
            for category in selection_c:
                categories[category.id] = category.type

            return jsonify({'questions': questions,
                            'total_questions': len(selection),
                            'categories': categories,
                            'current_category': 'NA'})
        except:
            abort(404)

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to
   a question, the question will be removed.
  This removal will persist in the database
   and when you refresh the page. 
  '''

    @app.route('/questions/<int:a_id>', methods=['DELETE'])
    def delete_question(a_id):

        try:

            question = Question.query.get(a_id)

            if question is None:
                abort(404)
            else:
                Question.query.filter(Question.id == a_id).\
                    delete()
                db.session.commit()

                return jsonify({'question_id': a_id})

        except:
            abort(404)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear 
  at the end of the last page
  of the questions list in the "List" tab.  
  '''
    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route('/questions', methods=['POST'])
    def set_questions():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        new_search = body.get('searchTerm', None)

        try:

            if new_search:
                selection = Question.query. \
                    order_by(Question.id). \
                    filter(Question.question.
                           ilike('%{}%'.format(new_search)))
                questions = paginate(selection.all(), request)

                return jsonify({
                    'questions': questions,
                    'totalQuestions': len(selection.all()),
                    'currentCategory': 'None'})

            else:

                question = Question(question=new_question,
                                    answer=new_answer,
                                    difficulty=new_difficulty,
                                    category=new_category)
                question.insert()

                selection = Question.query.get(question.id)

                return jsonify({
                    'created': question.id,
                    'question': selection.format(),
                    'total_questions': len(Question.query.all())
                })

        except:
            abort(422)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:id_value>/questions', methods=['GET'])
    def get_questions_per_categories(id_value):

        try:
            selection = Question.query.\
                filter_by(category=id_value).all()

            questions = paginate(selection, request)

            category = Category.query.get(id_value)

            return jsonify({'questions': questions,
                            'total_questions': len(selection),
                            'current_category': category.type})
        except:
            abort(404)

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and 
  previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes', methods=['POST'])
    def play():

        try:
            body = request.get_json()

            previous_questions = body.get('previous_questions', None)
            new_quiz_category = body.get('quiz_category', None)

            new_type = new_quiz_category['type']
            new_id = int(new_quiz_category['id'])
            # {'type': 'Science', 'id': '0'}

            if new_type == 'click':
                selection = Question.query.\
                    order_by(Question.id).all()
            else:
                selection = Question.query.\
                    filter_by(category=new_id).all()

            # removes previous selections from the list
            if type(previous_questions) is str:
                previous_questions = list(map(int,
                                              re.findall(r'\d+',
                                               previous_questions)))

            for previous_id in previous_questions:
                previous_selection = Question.\
                    query.get(previous_id)
                selection.remove(previous_selection)

            questions = [element.format() for element in selection]

            if questions:
                random.shuffle(questions)
                result = questions[0]
            else:
                result = None

            return jsonify({'question': result})
        except:
            abort(422)

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(422)
    def not_found(error):
        return jsonify(({
            "success": False,
            "error": 422,
            "message": "Not Processable"
        })), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        })), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify(({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        })), 400

    @app.errorhandler(500)
    def not_found(error):
        return jsonify(({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        })), 500

    return app
