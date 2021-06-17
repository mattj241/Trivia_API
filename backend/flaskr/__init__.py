import os
from flask import Flask, request, abort, jsonify, Response
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy.sql.expression import except_all

from models import setup_db, Question, Category, session_revert, session_close

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.config['DEBUG'] = True
  setup_db(app)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories(reuse=False):
    categories = Category.query.all()
    dict = {}
    for category in categories:
      dict.update({category.id : category.type})
    if reuse:
      return dict
    else:
      return jsonify({
        "categories" : dict
      })

  @app.route('/questions', methods=['GET'])
  def get_questions(reuse=False):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = Question.query.all()
    categories = get_categories(True)
    formatted_questions = [question.format() for question in questions]
    if not reuse:
      return jsonify({
        "questions" : formatted_questions[start:end],
        "total_questions" : len(formatted_questions),
        "current_category" : categories[1], #TODO
        "categories" : get_categories(True)
      })
    else:
      return {
        "questions" : formatted_questions[start:end],
        "total_questions" : len(formatted_questions),
        "current_category" : categories[1], #TODO
        "categories" : get_categories(True)
      }

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      target_question = Question.query.filter(Question.id==id).first()
      Question.delete(target_question)
    except Exception:
      session_revert()
      abort (404)
    finally:
      session_close()
    return jsonify(get_questions(True))

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "error": 404,
        "message": "Question not found"
        }), 404

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
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

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    