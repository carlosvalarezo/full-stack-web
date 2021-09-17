import json
import os
import string

from flask import Flask, request, abort, jsonify
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import random
from models import db, setup_db, Question, Category
from random import seed
from random import randint
import logging

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Origin,Content-Type,Accept,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/')
    def hello():
        return jsonify({'message': 'hello trivia!'})

    @app.route('/categories/', methods=['GET'])
    def get_categories():
        categories_data = db.session.query(Category)
        formatted_categories = [category.format() for category in categories_data]
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    def get_questions(page):
        try:
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            questions_data = db.session.query(Question).all()
            formatted_questions = [question.format() for question in questions_data]
            category_data = db.session.query(Category).all()
            formatted_categories = [category.format() for category in category_data]
            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': len(formatted_questions),
                'categories': formatted_categories,
                'current_category': page
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions/<int:id>/', methods=['DELETE'])
    def delete_question(id):
        try:
            Question.query.filter(Question.id == id).delete()
            db.session.commit()

            return jsonify({
                'success': True
            })
        except Exception as e:
            print(e)
            return jsonify({
                'success': False
            })

    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        try:
            question = body.get('question', '')
            answer = body.get('answer', '')
            category = body.get('category')
            difficulty = body.get('difficulty')

            question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
            question.insert()

            current_questions = Question.query.order_by(Question.id).all()
            questions = [question.format() for question in current_questions]

            return jsonify({
                'success': True,
                'created': question.id,
                'questions': questions,
                'total_questions': len(questions)
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions/', methods=['GET'])
    def search_question():
        try:
            if 'search_term' in request.args:
                term = request.args.get('search_term')
                questions_data = Question.query.filter(Question.question.ilike(f'%{term}%')).all()
                formatted_questions = [question.format() for question in questions_data]
                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                })
            if 'page' in request.args:
                page = request.args.get('page')
                return get_questions(int(page))

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/categories/<id>/questions', methods=['GET'])
    def questions_by_category(id):
        try:
            questions_data = Question.query.filter(Question.category == id).all()
            formatted_questions = [question.format() for question in questions_data]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions/play/', methods=['GET'])
    def play():
        question = ""
        category_id = 0
        answer = ""
        id = 0
        try:
            if 'quiz_category' in request.args:
                category_id = request.args.get('quiz_category')
            if 'previous_questions' in request.args:
                previous_questions = request.args.get('previous_questions')
            questions_in_category = Question.query.filter(Question.category == category_id).all()
            for question_in_category in questions_in_category:
                if str(question_in_category.id) not in previous_questions.split(','):
                    question = question_in_category.question
                    answer = question_in_category.answer
                    id = question_in_category.id
                    break
            return jsonify({
                'success': True,
                'question': question,
                'number_of_questions': len(questions_in_category),
                'answer': answer,
                'id': id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': f'resource not found: {error}'
        }), 404

    @app.errorhandler(422)
    def unable_to_process(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': f'unable to process: {error}'
        }), 422
    '''
    DONE
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''

    '''
    DONE
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    '''
    @TODO:
    DONE
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    '''
    @TODO:
    DONE
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    '''
    @TODO:
    DONE 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO:
    DONE
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO:
    DONE 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO:
    DONE
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO:
    DONE
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
    DONE
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    create_app().run(host='0.0.0.0', port=port)
