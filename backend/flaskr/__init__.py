import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page -1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # Set up CORS. Allow '*' for origins. 
  CORS(app)

  # @app.after_request decorator sets Access-Control-Allow for Methods and Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
 
  # Creates an endpoint to handle GET requests for all available categories.
  @app.route('/categories')
  def retrieve_categories():
    categories = list(map(Category.format, Category.query.all()))

    if len(categories) == 0:
      abort(404)

    return jsonify({
        'success': True,
        'category': categories,
        'total_categories': len(Category.query.all())
      })

  # Creates an endpoint to handle GET requests for questions, with pagination (every 10 questions). 
  # This endpoint should return a list of questions, number of total questions, current category, categories. 
  @app.route('/questions')
  def retrieve_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    # categories = list(map(Category.format, Category.query.all()))

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'question': current_questions,
      'total_questions': len(Question.query.all()),
      # 'current category': None,
      # 'categories': categories
      })

  # TEST: At this point, when you start the application
  # you should see questions and categories generated,
  # ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 

  # Creates an endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      
      return jsonify({
        'success': True,
        'deleted_question_id': question_id,
        'total_questions_remaining': len(Question.query.all())
      })

    except:
      abort(422)

  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 

  # Creates an endpoint to POST a new question, which will require the question and answer text, 
  # category, and difficulty score.
  # AND creates a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term 
  # is a substring of the question. 
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search = body.get('search', None)

    try:
      if search:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions_in_search': len(current_questions)
        })
      else:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()

        return jsonify({
          'success': True,
          'created': question.id,
          'total_questions': len(Question.query.all())
        })
    except:
      abort(422)
      
  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  

  # TEST: Search by any phrase. The questions list will update to include 
  # only question that include that string within their question. 
  # Try using the word "title" to start. 
 
  # Creates a GET endpoint to get questions based on category.
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_from_category(category_id):
    try:
      questions = Question.query.filter(Question.category == category_id).all()

      if questions is None:
        abort(404)
      
      return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'category': category_id,
        'total_questions_in_category': len(questions)
      })

    except:
      abort(422)

  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 

  # TODO
  # Creates a POST endpoint to get questions to play the quiz. 
  # This endpoint takes a category and the previous question parameters 
  # and returns a random question within the given category,
  # if provided, and that is not one of the previous questions. 
  # @app.route('/quizzes', methods=['POST'])
  # def play_game():
  #   try:
  #     body = request.get_json()

  #     if 'quiz_category' not in body and 'previous_questions' not in body:
  #       abort(422)
      
  #     category = body.get('quiz_category')
  #     questions = body.get('previous_questions')

  #     if category['type'] == 'click':
  #       available_questions = Question.query.filter(Question.id.notin_(questions)).all()
      
  #     else:
  #       available_questions = Question.query.filter_by(category=category['id']).filter(Question.id.notin_((questions))).all()
        
  #     new_question = available_questions[random.randrange(0, len(available_questions))].format() if len(available_questions) > 0 else None

  #     return jsonify({
  #       'success': True,
  #       'question': new_question
  #     })

  #   except:
  #     abort(422)

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 

  # Creates error handlers for all expected errors 
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400, 
      'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422
  
  return app 