import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''


db_drop_and_create_all()


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
    it should be a public endpoint
    it should contain only the drink.short() data representation
    returns status code 200 and json
    {"success": True, "drinks": drinks}
    where drinks is the list of drinks
    or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drink_short():
    try:
        drink = Drink.query.all()

        drinks = [element.short() for element in drink]
    except:
        abort(404)

    return jsonify({"success": True,
                    "drinks": drinks})


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json
        {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def get_drink_long(payload):
    try:
        drink = Drink.query.all()

        drinks = [element.long() for element in drink]
    except:
        abort(404)

    return jsonify({"success": True,
                    "drinks": drinks})


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json
        {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def create_drink(payload):
    body = request.get_json()
    new_title = body.get('title', None)
    new_recipe = body.get('recipe', None)

    if type(new_recipe) is dict:
        new_recipe = [new_recipe]
        new_recipe = str(json.dumps(new_recipe))
    elif type(new_recipe) is list:
        new_recipe = str(json.dumps(new_recipe))
    else:
        abort(400)

    try:
        drink = Drink(title=new_title,
                      recipe=new_recipe)
        drink.insert()

    except:
        abort(400)

    return jsonify({'success': True,
                    "drinks": [drink.long()]})


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json
        {"success": True, "drinks": drink} where drink
        an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:a_id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drink(payload, a_id):
    drink = Drink.query.get(a_id)

    body = request.get_json()
    new_title = body.get('title', None)

    try:
        drink.title = new_title
        drink.update()
    except:
        abort(404)

    return jsonify({"success": True,
                    "drinks": [drink.long()]})


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json
        {"success": True, "delete": id} where id
        is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:a_id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(payload, a_id):
    drink = Drink.query.get(a_id)

    try:
        drink.delete()
    except:
        abort(404)

    return jsonify({"success": True,
                    "delete": a_id})


# Error Handling
'''
Example error handling for unprocessable entity
'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
