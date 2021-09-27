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
            # TODO: Implement the following code
            # items_limit = request.args.get('limit', 10, type=int)
            # selected_page = request.args.get('page', 1, type=int)
            # current_index = selected_page - 1
            #
            # questions = \
            #     Question.query.order_by(
            #         Question.id
            #     ).limit(items_limit).offset(current_index * items_limit).all()
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
            logging.error(f"ERROR = {e}")
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
            logging.error(f"ERROR = {e}")
            abort(405)

    def is_empty(attribute):
        if attribute is None:
            raise Exception

    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        try:
            question = body.get('question')
            answer = body.get('answer')
            category = body.get('category')
            difficulty = body.get('difficulty')

            is_empty(question)
            is_empty(answer)
            is_empty(category)
            is_empty(difficulty)

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

    @app.route('/questions/search/', methods=['GET'])
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
            if 'search_term' not in request.args:
                raise Exception
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions/list/', methods=['GET'])
    def get_questions_list():
        try:
            if 'page' in request.args:
                page = request.args.get('page')
                return get_questions(int(page))
            if 'page' not in request.args:
                raise Exception
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
            if 'quiz_category' not in request.args:
                raise Exception
            if 'previous_questions' not in request.args:
                raise Exception
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
        }), 404\


    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': f'method not allowed: {error}'
        }), 405

    @app.errorhandler(422)
    def unable_to_process(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': f'unable to process: {error}'
        }), 422

    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    create_app().run(host='0.0.0.0', port=port)
