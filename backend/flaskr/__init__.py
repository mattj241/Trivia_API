import os
import re
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
  def get_categories(get_dict_type=False):
    categories = Category.query.all()
    dict = {}
    for category in categories:
      dict.update({category.id : category.type})
    if get_dict_type:
      return dict
    else:
      return jsonify({
        "categories" : dict
      })

  @app.route('/questions', methods=['GET'])
  def get_questions(get_dict_type=False, search_term=None, category_id=None, excluded_questions=None):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # IF Search is enabled
    if search_term is not None:
      questions = Question.query.filter(Question.question.ilike(r"%{}%".format(search_term)))

    # IF just gathering all questions for the home screen
    else:
      questions = Question.query.all()
    categories = get_categories(True)
    formatted_questions = [question.format() for question in questions]
    if not get_dict_type:
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

  @app.route('/questions', methods=['POST'])
  def add_question():
    data = request.get_json()
    if 'searchTerm' in data:
      return get_questions(search_term=data['searchTerm'])
    else:
      try:
        new_question = Question(data['question'], data['answer'], data['category'], data['difficulty'])
        Question.insert(new_question)
      except Exception:
        session_revert()
        abort(422)
      finally:
        session_close()
      return jsonify({
        "message" : "201 Question successfully created" 
      })

  @app.route('/quizzes', methods=['POST'])
  def make_quiz():
    data = request.get_json()
    list_prev_questions = data['previous_questions']
    category_id = (data['quiz_category'])['id']
    if category_id is not None:
      if (category_id != 0):
        questions = Question.query.filter(Question.category==category_id, Question.id.not_in(list_prev_questions))
      else:
        questions = Question.query.filter(Question.id.not_in(list_prev_questions))
    list_questions = []
    for question in questions:
      list_questions.append(question.id)
    try:
      random_question = random.choice(list_questions)
      random_question_data = Question.query.filter(Question.id==random_question).first()
      result =  {
        "question" : {
          "question" : random_question_data.question,
          "id" : random_question_data.id,
          "answer" : random_question_data.answer}
        }
    except IndexError:
       result =  {"question" : "",
                  "message" : "no more quiz questions left!"}
    return jsonify(result)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "error": 404,
        "message": "Data was not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "error": 422,
        "message": "Request was unprocessable"
        }), 422

  return app

    