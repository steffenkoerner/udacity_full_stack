import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    questions_page = questions[start:end]

    return questions_page


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    CORS(app)

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.route('/categories')
    def categories():
        categories = Category.query.all()
        results = []
        for category in categories:
            result = category.format()['type']
            results.append(result)

        json_result = {
            "success": True,
            "categories": results}
        return jsonify(json_result)

    @app.route('/questions')
    def get_questions():
        query = Question.query.all()
        questions = pagination(request, query)
        categories = Category.query.all()

        if len(questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": questions,
            "total_questions": len(query),
            "categories": {category.id: category.type for category in categories},
            "current_category": None
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                "question_id": question_id
            })
        except:
            abort(422)

        '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_new_question():

        try:
            data = request.get_json()

            question = Question(
                question=data['question'],
                answer=data['answer'],
                category=data['category'],
                difficulty=data['difficulty']
            )
            question.insert()
            return jsonify({
                'success': True,
                'question_id': question.id,
            })
        except:
            abort(422)
        '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

        '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:category_id>/questions')
    def questions_for_category(category_id):

        try:
            query = Question.query.filter(
                Question.category == category_id).all()
            total_questions = len(query)
            questions = []
            for element in query:
                questions.append(element.format()['question'])

            result = {
                "questions": questions,
                "totalQuestions": total_questions,
                "currentCategory": category_id
            }
            return jsonify(result)
        except:
            abort()

        '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        pass

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
