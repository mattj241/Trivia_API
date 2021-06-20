import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE_TEST = 10


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        database_username = "postgres"
        database_password = "marshall"
        self.database_path = "postgresql://{}:{}@{}/{}".format(database_username, database_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question" : "sss",
            "answer" : "yyy",
            "category" : 5,
            "difficulty" : "1"
        }

        self.new_question_to_delete = {
            "question" : "new_question_to_delete",
            "answer" : "yyy",
            "category" : 5,
            "difficulty" : "1"
        }

        self.new_question_bad_types = {
            "question" : "sss",
            "answer" : "yyy",
            "category" : "science",
            "difficulty" : 1
        }

        self.search_question_valid = {
            "searchTerm" : "Cassius Clay"
        }

        self.search_question_invalid = {
            "searchTerm" : "Mike Tyson"
        }

        self.new_quiz = {
            "previous_questions" : [],
            "quiz_category" : {
                        "type": "Science",
                        "id": "1"
                    }
        }

        self.new_quiz_targetting_1_sci_question = {
            "previous_questions" : [20, 21],
            "quiz_category" : {
                        "type": "Science",
                        "id": "1"
                    }
        }

        self.quiz_breaks_server = {
            "previous_questions" : "blank",
            "quiz_category" : {
                        "type": "Science",
                        "id": "1"
                    }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def testCategories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def testQuestionsPagination(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE_TEST)

    def testQuestionsPagination_fail(self):
        res = self.client().get('/questions?page=500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def testAddingQuestion(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(data['message'], "201 Question successfully created")

    def testAddingQuestion_fail(self):
        res = self.client().post('/questions', json=self.new_question_bad_types)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def testDeletion(self):
        res_post = self.client().post('/questions', json=self.new_question_to_delete)
        target = Question.query.filter(Question.question==self.new_question_to_delete['question']).first()
        self.assertEqual(target.question, "new_question_to_delete")
        delete_url = 'questions/{}'.format(target.id)
        res_delete = self.client().delete(delete_url)
        target = Question.query.filter(Question.question==self.new_question_to_delete['question']).first()
        self.assertEqual(target, None)

    def testSearch(self):
         res = self.client().post('/questions', json=self.search_question_valid)
         data = json.loads(res.data)

         self.assertEqual(len(data['questions']), 1)

    def testCategoryFilter(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        # number of all science questions = 3
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(res.status_code, 200)

    def testCategoryFilter_fail(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def testSearch_invalid(self):
         res = self.client().post('/questions', json=self.search_question_invalid)
         data = json.loads(res.data)

         self.assertEqual(res.status_code, 404)

    def testQuiz(self):
        # since it's a random question, category is the only thing we test with certainty
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)
        
        self.assertEqual((data['question'])['category'], 1)

    def testQuiz_edgeCase(self):
        # There's only 3 science questions in the training set. Therefore, this science test will always pass
        res = self.client().post('/quizzes', json=self.new_quiz_targetting_1_sci_question)
        data = json.loads(res.data)

        self.assertEqual((data['question'])['question'], "Hematology is a branch of medicine involving the study of what?")

    def test_500(self):
        res = self.client().post('/quizzes', json=self.quiz_breaks_server)

        self.assertEqual(res.status_code, 500)

    def test_405(self):
        res = self.client().patch('/quizzes')

        self.assertEqual(res.status_code, 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()