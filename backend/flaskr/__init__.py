import os
import re
from flask import Flask, request, abort, jsonify, Response
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sqlalchemy
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
    response.headers.add('Access-Control-Allow-Headers', \
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', \
                         'GET,PUT,POST,DELETE,OPTIONS')
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

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_category_questions(id):
    return get_questions(category_filter=id)


  @app.route('/questions', methods=['GET'])
  def get_questions(get_dict_type=False, search_term=None, category_filter=None):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # IF a search request is enabled
    if search_term is not None:
      questions = Question.query.filter(
        Question.question.ilike(r"%{}%".format(search_term)))
    
    #ELSE IF a category restriction is requested
    elif category_filter is not None:
      questions = Question.query.filter(Question.category==category_filter)

    # IF just gathering all questions for the home screen
    else:
      questions = Question.query.all()
    categories = get_categories(True)
    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions[start:end]) == 0:
      abort(404)
    if not get_dict_type:
      return jsonify({
        "questions" : formatted_questions[start:end],
        "total_questions" : len(formatted_questions),
        "current_category" : categories[1],
        "categories" : get_categories(True)
      })
    else:
      return {
        "questions" : formatted_questions[start:end],
        "total_questions" : len(formatted_questions),
        "current_category" : categories[1],
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
  def handle_post_questions_endpoint():
    data = request.get_json()
    if 'searchTerm' in data:
      return get_questions(search_term=data['searchTerm'])
    else:
      try:
        new_question = Question(data['question'],
                                data['answer'],
                                data['category'], 
                                data['difficulty'])
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
    prev_questions = data['previous_questions']
    category_id = (data['quiz_category'])['id']

    try:
      # IF requested category for quizzes != 'ALL'
      # (frontend handles this user input Category id: 0)
      if (category_id != 0):
        questions = Question.query.filter(
          Question.category==category_id, Question.id.not_in(prev_questions))
      # ELSE requested quiz requires no category restriction 
      else:
        questions = Question.query.filter(Question.id.not_in(prev_questions))
    except sqlalchemy.exc.ArgumentError:
      # if this is reached, a non-list type was likely used for prev_questions.
      # The HTTP code returned is 500 without an explicit function
      # call of abort(500), but flask returns content with the Werkzeug Debugger
      # and thus prevents the automatic error handler in @app.errorhandler(500)
      # to trigger
      abort (500) 
    
    list_questions = []
    for question in questions:
      list_questions.append(question.id)
    try:
      random_question = random.choice(list_questions)
      random_question_data = Question.query.filter(
        Question.id==random_question).first()
      result =  {
        "question" : {
          "question" : random_question_data.question,
          "id" : random_question_data.id,
          "answer" : random_question_data.answer,
          "category" : random_question_data.category}
        }
    except IndexError:
       result =  {"question" : "",
                  "message" : "no more quiz questions left!"}
    return jsonify(result)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "error": 404,
        "message": "Data was not found."
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "error": 422,
        "message": "The request was well-formed but was" \
         "unable to be followed due to semantic errors."
        }), 422

  @app.errorhandler(400)
  def bad_syntax(error):
    return jsonify({
        "error": 400,
        "message": "The server could not understand" \
          "the request due to invalid syntax."
        }), 400

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        "error": 500,
        "message": "The server could not handle the last reqeust."
        }), 500

  @app.errorhandler(405)
  def bad_method(error):
    return jsonify({
        "error": 405,
        "message": "The server is not prepared to handle the requested method."
        }), 405
    
  return app

    