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

    # TODO
    # Write at least one test for each test for successful operation and for expected errors.
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])
        self.assertEqual(data['total_categories'], 6)

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(len(data['question']), 10)
        # self.assertEqual(data['total_questions'], 19)

    def test_error_for_invalid_questions_page(self):
        response = self.client().get('/questions?page=100000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_question_delete(self):
        response = self.client().delete('/questions/4')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    #     self.assertEqual(data['total_questions_remaining'], 19)

    def test_error_question_delete_id_does_not_exist(self):
        response = self.client().delete('/questions/456789')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')       

    def test_error_question_delete_invalid_id(self):
        response = self.client().delete('/questions/CATSPAJAMAS')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 

    def test_create_question(self):
        dummy_data = {
            'question': 'TEST QUESTION',
            'answer': 'TEST ANSWER',
            'difficulty': 1,
            'category': 1
        }

        response = self.client().post('/questions', json=dummy_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        # self.assertEqual(data['total_questions'], 19)

    # def test_error_create_question_with_missing_data(self):
    # def test_search_question(self):
    # def test_error_search_question_with_no_search(self):
    # def test_get_questions_by_catgeory(self):
    # def test_error_get_questions_by_category_id_does_not_exist(self):
    # def test_error_get_questions_by_category_invalid_id(self):
    # def test_quiz_question(self):
    # def test_error_quiz_question_with_no_data(self):

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()