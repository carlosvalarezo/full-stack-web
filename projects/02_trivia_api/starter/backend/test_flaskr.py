import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr.app import create_app
from flaskr.models import setup_db, Question, Category


DB_NAME = os.getenv("DB_TEST_NAME")
DB_USER = os.getenv("DB_TEST_USER")
DB_PASSWORD = os.getenv("DB_TEST_PASSWORD")
DB_HOST = os.getenv("DB_TEST_HOST")
DB_PORT = os.getenv("DB_TEST_PORT")
database_path = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
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


class CategoryTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
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

    def test_get_paginated_questions(self):
        res = self.client().get('/questions/list/?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fails_without_parameter_page_paginated_questions(self):
        res = self.client().get('/questions/list/')
        self.assertEqual(res.status_code, 422)

    def test_delete_particular_question(self):
        res = self.client().delete('/questions/1/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_receives_error_on_delete_question_without_id(self):
        res = self.client().delete('/questions/')
        self.assertEqual(res.status_code, 404)

    def test_create_particular_question(self):
        res = self.client().post('/questions', json={'question': 'my-question',
                                                     'answer': 'my-answer',
                                                     'category': 2,
                                                     'difficulty': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fails_on_creating_a_question_on_missing_parameters(self):
        res = self.client().post('/questions', json={})
        self.assertEqual(res.status_code, 422)

    def test_search_question_given_parameter(self):
        res = self.client().get('/questions/search/?search_term=nks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_fails_search_question_without_search_term(self):
        res = self.client().get('/questions/search/')

        self.assertEqual(res.status_code, 422)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_given_category_id(self):
        res = self.client().get('/questions/play/?quiz_category=1&previous_questions=1,2,3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_without_category_id(self):
        res = self.client().get('/questions/play/?previous_questions=1,2,3')

        self.assertEqual(res.status_code, 422)

    def test_play_without_previous_questions(self):
        res = self.client().get('/questions/play/?quiz_category=1')

        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
