import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from pathlib import Path
import http.client
import ssl
import base64
import logging

from database.models import db, setup_db, db_drop_and_create_all, Drink
# import database.models as db
# from .auth.auth import AuthError, requires_auth
import auth.auth as auth

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
setup_db(app)
db_drop_and_create_all()

CORS(app, resources={r"/*": {"origins": '*'}})


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": f"unprocessable {error}"
    }), 422


@app.route('/health')
def hello():
    return jsonify({'status': 'up'})


@app.route('/drinks')
def get_drinks():
    try:
        drinks_data = db.session.query(Drink)
        drinks = [drink.short() for drink in drinks_data]
        if drinks:
            return jsonify({
                'success': True,
                'categories': drinks
            })
    except Exception as e:
        print(e)
        abort(422)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

# Error Handling
'''
Example error handling for unprocessable entity
'''

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     create_app().run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # certs_dir = Path('certs')
    certs_dir = os.path.abspath(os.getcwd())
    print(f"CERTS_DIR = {certs_dir}")
    port = int(os.getenv('APP_PORT', 443))
    app.secret_key = os.urandom(24)
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ctx.load_cert_chain(f'{certs_dir}/src/certs/localhost.crt', f'{certs_dir}/src/certs/localhost.key')
    app.run(debug=True, host='0.0.0.0', port=port, ssl_context=ctx)
