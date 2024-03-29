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
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def categories():
        categories = Category.query.order_by(Category.type).all()

        json_result = {
            "success": True,
            "categories": {category.id: category.type for category in categories}}
        return jsonify(json_result)

    @app.route('/questions')
    def get_questions():
        query = Question.query.order_by(Question.id).all()
        questions = pagination(request, query)
        categories = Category.query.order_by(Category.type).all()

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

    @app.route('/questions/search', methods=['POST'])
    def find_questions():
        try:
            data = request.get_json()
            search = data['searchTerm']

            query = Question.query.filter(
                Question.question.ilike(f'%{search}%')).all()

            result = {
                "success": True,
                "total_questions": len(query),
                "questions": [question.format() for question in query],
            }
            return jsonify(result)
        except:
            abort(404)

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
                Question.category == category_id).order_by(Question.id).all()
            total_questions = len(query)
            questions = []
            for element in query:
                questions.append(element.format())

            result = {
                "questions": questions,
                "total_questions": total_questions,
                "current_category": category_id
            }
            return jsonify(result)
        except:
            abort(404)

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

        try:
            data = request.get_json()
            category = data['quiz_category']['id']
            previous_questions = data['previous_questions']

            possible_questions = []
            if category == 0:
                possible_questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                possible_questions = Question.query.filter(
                    Question.id.notin_(previous_questions), Question.category == category).all()

            if len(possible_questions) == 0:
                return jsonify({
                    "success": True,
                    "question": "",
                })

            random_question_index = random.randint(
                0, len(possible_questions)-1)

            new_question = possible_questions[random_question_index]

            if not new_question:
                return jsonify({})

            return jsonify({
                "success": True,
                "question": new_question.format(),
            })

        except:
            abort(422)

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

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
