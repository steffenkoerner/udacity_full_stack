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
        self.database_name = "trivia"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format(
            'localhost:5432', self.database_name)
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

    def test_get_all_categories(self):
        result = self.client().get('/categories')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions_for_category(self):
        result = self.client().get('/categories/1/questions')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['totalQuestions'], 3)
        self.assertTrue(data['currentCategory'], 1)

    def test_to_get_questions_for_page(self):
        result = self.client().get('/questions?page=1')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['currentCategory'], None)

    def test_for_to_high_page(self):
        result = self.client().get('/questions?page=99')
        self.assertEqual(result.status_code, 404)

        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        question = Question(
            question="question",
            answer="answer",
            category=2,
            difficulty=3
        )
        question.insert()

        result = self.client().delete(f'/questions/{question.id}')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['question_id'], question.id)

    def test_delete_non_existing_question(self):
        result = self.client().delete('/questions/100000')
        self.assertEqual(result.status_code, 422)

        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "unprocessable")

    def test_create_question(self):
        question = {
            "question": "This is my question",
            "answer": "This is my answer",
            "difficulty": 2,
            "category": 1,
        }

        result = self.client().post('/questions', json=question)
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertTrue(data['success'])
        deleted_question_id = data['question_id']

        result_delete = self.client().delete(
            f'/questions/{deleted_question_id}')

    def test_create_question_with_invalid_input(self):
        question = {
            "answer": "answer",
            "difficulty": 1,
            "category": 2
        }

        result = self.client().post('/questions', json=question)
        self.assertEqual(result.status_code, 422)

    def test_search_for_question(self):

        search = {
            "searchTerm": "was"
        }
        result = self.client().post('/questions/search', json=search)
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertTrue(data['success'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['questions'])

    def test_search_without_search_string(self):
        result = self.client().post('/questions/search', json={})
        self.assertEqual(result.status_code, 404)

        data = json.loads(result.data)
        self.assertFalse(data['success'])

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
