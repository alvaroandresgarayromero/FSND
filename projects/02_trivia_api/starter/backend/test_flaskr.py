import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        #self.database_path = "postgresql://postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test 
    for successful operation and for expected errors.
    """
    def STP_01(self):

        # test pagination page scroll
        pages = [1 , 2]
        result_ids = []
        questions_per_page = 10

        for page in pages:
            query = '/questions?page={}'.format(page)
            server_response = self.client().get(query)
            data = server_response.get_json()

            # Verify that the questions queried meet the pagination criteria
            # of 10 or less per page
            self.assertLessEqual(len(data['questions']), questions_per_page,
                                 'Number of questions queried did not '
                                 'meet pagination criteria')

            for question in data['questions']:
                result_ids.append(question['id'])


        # Verify pagination scroll does
        # not repeat same questions in other pages
        self.assertEqual(len(set(result_ids)), len(result_ids),
                         'The question ids queried are not unique, and have'
                         'been repeated in more than one page')

    def STP_02(self):

        # test out of bounds pagination
        page = 1000

        query = '/questions?page={}'.format(page)
        server_response = self.client().get(query)
        data = server_response.get_json()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource Not Found")


    def STP_03(self):

        # test '/questions?page=1' interface
        query = '/questions?page=1'
        server_response = self.client().get(query)
        data = server_response.get_json()

        # verify category + question package interface
        fieldnames = list(data.keys())
        self.assertEqual(fieldnames[0],'categories' )
        self.assertEqual(fieldnames[1],'current_category' )
        self.assertEqual(fieldnames[2],'questions' )
        self.assertEqual(fieldnames[3],'total_questions' )

        self.assertEqual(type(data['categories']), dict )
        self.assertEqual(type(data['current_category']), str)
        self.assertEqual(type(data['total_questions']), int)
        self.assertEqual(type(data['questions']), list )

        # verify question interface
        question = data['questions'][0]

        fieldnames = list(question.keys() )
        self.assertEqual(fieldnames[0],'answer' )
        self.assertEqual(fieldnames[1],'category' )
        self.assertEqual(fieldnames[2],'difficulty' )
        self.assertEqual(fieldnames[3],'id' )
        self.assertEqual(fieldnames[4],'question' )

        self.assertEqual(type(question['answer']), str )
        self.assertEqual(type(question['category']), int)
        self.assertEqual(type(question['difficulty']), int )
        self.assertEqual(type(question['id']), int)
        self.assertEqual(type(question['question']), str)

    def STP_04(self):

        # test fieldnames and datatypes
        query = '/categories'
        server_response = self.client().get(query)
        data = server_response.get_json()

        fieldnames = list(data.keys())
        self.assertEqual(fieldnames[0],'categories')
        self.assertEqual(type(data['categories']), dict )

    def STP_05(self):

        # test creation of new question records
        query = '/questions'
        body = {'question': 'test question',
                'answer': 'test answer',
                'difficulty': 1,
                'category': 1}

        server_response = self.client().post(query, json=body)
        data = server_response.get_json()

        question = data['question']

        self.assertEqual(question['answer'], body['answer'] )
        self.assertEqual(question['category'], body['category'])
        self.assertEqual(question['difficulty'], body['difficulty'] )
        self.assertEqual(question['question'], body['question'])

    def STP_06(self):

        # test creation of new question failure
        query = '/questions'
        body = {'question': 'test question',
                'answer': 'test answer',
                'difficulty': 'create_failure',
                'category': 1}

        server_response = self.client().post(query, json=body)
        data = server_response.get_json()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Not Processable")

    def STP_07(self):

        # test delete of existing question record
        question_before = Question.query.\
            order_by(Question.id.desc()).first()

        # test delete of question
        query = '/questions/{}'.format(question_before.id)

        server_response = self.client().delete(query)
        data = server_response.get_json()

        self.assertEqual(server_response.status_code, 200)
        self.assertEqual(data['question_id'], question_before.id)
        self.assertEqual(Question.query.get(question_before.id), None)

    def STP_08(self):

        # test delete on question record that doesn't exist
        out_of_bounds_id = 10000
        query = '/questions/{}'.format(out_of_bounds_id)

        server_response = self.client().delete(query)
        data = server_response.get_json()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource Not Found")

    def STP_09(self):

        # test questions per category query
        questions_per_page = 10

        category_id = 2
        query = '/categories/{}/questions'.\
            format(category_id)

        server_response = self.client().get(query)
        data = server_response.get_json()

        # Verify that the questions queried meet the pagination criteria
        # of 10 or less per page
        self.assertLessEqual(len(data['questions']), questions_per_page,
                             'Number of questions queried did not '
                             'meet pagination criteria')

        result_ids = []
        for question in data['questions']:
            result_ids.append(question['id'])

        # Verify pagination does not repeat same questions in other pages
        self.assertEqual(len(set(result_ids)), len(result_ids),
                         'The question ids queried are not unique, and have'
                         'been repeated in more than one page')

    def STP_10(self):

        # test out of bounds pagination
        page = 10000
        category_id_base_0 = 1

        query = '/categories/{}/questions?page={}'.\
            format(category_id_base_0, page)
        server_response = self.client().get(query)
        data = server_response.get_json()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource Not Found")

    def STP_11(self):

        # test out of bounds category id
        page = 1
        category_id_base_0 = 1000

        query = '/categories/{}/questions?page={}'.\
            format(category_id_base_0, page)
        server_response = self.client().get(query)
        data = server_response.get_json()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource Not Found")

    def STP_12(self):

        # test  '/categories/{}/questions interface
        category_id_base_0 = 1
        query = '/categories/{}/questions'.\
            format(category_id_base_0)

        server_response = self.client().get(query)
        data = server_response.get_json()

        # verify category + question package interface
        fieldnames = list(data.keys())

        self.assertEqual(fieldnames[0],'current_category' )
        self.assertEqual(fieldnames[1],'questions' )
        self.assertEqual(fieldnames[2],'total_questions' )

        self.assertEqual(type(data['questions']), list )
        self.assertEqual(type(data['current_category']), str)
        self.assertEqual(type(data['total_questions']), int)


        # verify question interface
        question = data['questions'][0]

        fieldnames = list(question.keys() )
        self.assertEqual(fieldnames[0],'answer' )
        self.assertEqual(fieldnames[1],'category' )
        self.assertEqual(fieldnames[2],'difficulty' )
        self.assertEqual(fieldnames[3],'id' )
        self.assertEqual(fieldnames[4],'question' )

        self.assertEqual(type(question['answer']), str )
        self.assertEqual(type(question['category']), int)
        self.assertEqual(type(question['difficulty']), int )
        self.assertEqual(type(question['id']), int)
        self.assertEqual(type(question['question']), str)

    def STP_13(self):

        # test questions per search: pagination criteria
        questions_per_page = 10

        category_id_base_0 = 1
        query = '/questions'.format(category_id_base_0)
        body = {'searchTerm': 'title'}
        server_response = self.client().post(query, json=body)
        data = server_response.get_json()

        # Verify that the questions queried
        # meet the pagination criteria
        # of 10 or less per page
        self.assertLessEqual(len(data['questions']), questions_per_page,
                             'Number of questions queried did not '
                             'meet pagination criteria')

        result_ids = []
        for question in data['questions']:
            result_ids.append(question['id'])

        # Verify pagination does not repeat
        # same questions in other pages
        self.assertEqual(len(set(result_ids)), len(result_ids),
                         'The question ids queried are not unique, and have'
                         'been repeated in more than one page')

    def STP_14(self):

        # test questions per search: search criteria

        category_id_base_0 = 1
        query = '/questions'.format(category_id_base_0)
        body = {'searchTerm': 'title'}
        server_response = self.client().post(query, json=body)
        data = server_response.get_json()

        # Verify number of search
        self.assertEqual(len(data['questions']), 2,
                         'the expected search result '
                         'data does not match expected value')

    def STP_15(self):

        # questions per search:
        # Test assert triggers for no questions found
        questions_per_page = 10

        category_id_base_0 = 1
        query = '/questions'.format(category_id_base_0)
        body = {'searchTerm': 'unknown@#String'}
        server_response = self.client().post(query, json=body)
        data = server_response.get_json()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Not Processable")

    def STP_16(self):
        # test '/questions' search interface
        category_id_base_0 = 1
        query = '/questions'.format(category_id_base_0)
        body = {'searchTerm': 'title'}
        server_response = self.client().post(query, json=body)
        data = server_response.get_json()

        # verify category + question package interface
        fieldnames = list(data.keys())
        self.assertEqual(fieldnames[0],'currentCategory' )
        self.assertEqual(fieldnames[1],'questions' )
        self.assertEqual(fieldnames[2],'totalQuestions' )

        self.assertEqual(type(data['currentCategory']), str)
        self.assertEqual(type(data['totalQuestions']), int)
        self.assertEqual(type(data['questions']), list )

        # verify question interface
        question = data['questions'][0]

        fieldnames = list(question.keys() )
        self.assertEqual(fieldnames[0],'answer' )
        self.assertEqual(fieldnames[1],'category' )
        self.assertEqual(fieldnames[2],'difficulty' )
        self.assertEqual(fieldnames[3],'id' )
        self.assertEqual(fieldnames[4],'question' )

        self.assertEqual(type(question['answer']), str )
        self.assertEqual(type(question['category']), int)
        self.assertEqual(type(question['difficulty']), int )
        self.assertEqual(type(question['id']), int)
        self.assertEqual(type(question['question']), str)

    def STP_17(self):
        # test '/quizzes' trivia are
        # grouped by category and are randomness
        query = '/quizzes'

        # All Categories
        body_1 = {'previous_questions': [],
                'quiz_category': {'type': 'click',
                                  'id': 0}}

        # A specific category
        body_2 = {'previous_questions': [],
                'quiz_category': {'type': 'Geography',
                                  'id': 3}}

        bodies = [body_1, body_2]

        body_1_category = body_1['quiz_category']['type']
        body_2_category = body_2['quiz_category']['type']

        results = {body_1_category: [],
                   body_2_category: [] }

        for x in range(1,10):
            for body in bodies:
                server_response = self.client().post(query, json=body)
                data = server_response.get_json()

                results[body['quiz_category']['type']].\
                            append(data['question']['id'])

        # Verify the question per category were correct
        for fieldname in results.keys():

            if fieldname == 'click':
                # When all categories are requested verify that
                # that there two or more different categories
                selection = Question.query.filter(Question.id.in_(results[fieldname])). \
                                            with_entities(Question.category).\
                                            all()
                self.assertGreater(len(set(selection)), 1,
                                   'All categories requests '
                                   'should have more than one category')

            else:
                if fieldname == body_1_category:
                    # body 1 category
                    expected_category = body_1['quiz_category']['id']
                elif fieldname == body_2_category:
                    # body 2 category
                    expected_category = body_2['quiz_category']['id']
                else:
                    self.assertTrue(False, 'Undefined category under test')

                selection = Question.query.filter(Question.id.in_(results[fieldname])). \
                                            with_entities(Question.category).\
                                            all()
                categories = set(selection)

                self.assertEqual(1, len(categories),
                                'One category group is expected')

                self.assertEqual(expected_category, categories.pop()[0],
                                 'Category type did not match expected')

        # Verify randomness by checking questions ids

        # create a second result to simulate
        # a second play session of randomness
        results2 = {body_1_category: [],
                    body_2_category: []}

        for x in range(1,10):
            for body in bodies:
                server_response = self.\
                    client().post(query, json=body)
                data = server_response.get_json()

                results2[body['quiz_category']['type']].\
                            append(data['question']['id'])

        for fieldname in results.keys():

            self.assertNotEqual(results[fieldname],results2[fieldname],
                                'Question query are not random')


    def STP_18(self):
        # test that the questions do not
        # repeat previous trivia questions per game session
        query = '/quizzes'

        # All Categories
        body = {'previous_questions': [],
                'quiz_category': {'type': 'click',
                                  'id': 0}}

        # Exhaust all trivia questions queries
        result = []
        while True:
            server_response = self.client().\
                post(query, json=body)
            data = server_response.get_json()

            if data['question'] is None:
                break
            else:
                result.append(data['question']['id'])

            body['previous_questions'] = result


        self.assertEqual(len(result),len(set(result)),
                            'One or more trivia questions were repeated')

    def STP_19(self):
        # test that the questions do not
        # repeat previous trivia questions per game session
        query = '/quizzes'

        # All Categories
        body = {'previous_questions': ['CREATE_ASSERT'],
                'quiz_category': {'type': 'click',
                                  'id': 0}}


        server_response = self.client().post(query, json=body)
        data = server_response.get_json()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Not Processable")

    def STP_20(self):
        # test the interface for /quizzes
        query = '/quizzes'

        # All Categories
        body = {'previous_questions': [],
                'quiz_category': {'type': 'click',
                                  'id': 0}}


        server_response = self.client().\
            post(query, json=body)
        data = server_response.get_json()

        # verify category + question package interface
        fieldnames = list(data.keys())
        self.assertEqual(fieldnames[0],'question' )

        self.assertEqual(type(data['question']), dict )

        # verify question interface
        question = data['question']

        fieldnames = list(question.keys())
        self.assertEqual(fieldnames[0],'answer' )
        self.assertEqual(fieldnames[1],'category' )
        self.assertEqual(fieldnames[2],'difficulty' )
        self.assertEqual(fieldnames[3],'id' )
        self.assertEqual(fieldnames[4],'question' )

        self.assertEqual(type(question['answer']), str )
        self.assertEqual(type(question['category']), int)
        self.assertEqual(type(question['difficulty']), int )
        self.assertEqual(type(question['id']), int)
        self.assertEqual(type(question['question']), str)



# Make the tests conveniently executable
if __name__ == "__main__":

    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TriviaTestCase('STP_01'))
    suite.addTest(TriviaTestCase('STP_02'))
    suite.addTest(TriviaTestCase('STP_03'))
    suite.addTest(TriviaTestCase('STP_04'))
    suite.addTest(TriviaTestCase('STP_05'))
    suite.addTest(TriviaTestCase('STP_06'))
    suite.addTest(TriviaTestCase('STP_07'))
    suite.addTest(TriviaTestCase('STP_08'))
    suite.addTest(TriviaTestCase('STP_09'))
    suite.addTest(TriviaTestCase('STP_10'))
    suite.addTest(TriviaTestCase('STP_11'))
    suite.addTest(TriviaTestCase('STP_12'))
    suite.addTest(TriviaTestCase('STP_13'))
    suite.addTest(TriviaTestCase('STP_14'))
    suite.addTest(TriviaTestCase('STP_15'))
    suite.addTest(TriviaTestCase('STP_16'))
    suite.addTest(TriviaTestCase('STP_17'))
    suite.addTest(TriviaTestCase('STP_18'))
    suite.addTest(TriviaTestCase('STP_19'))
    suite.addTest(TriviaTestCase('STP_20'))

    unittest.TextTestRunner().run(suite)