"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Game
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from base64 import b64encode
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/register', methods=['POST'])
def add_new_user():
    body = request.json
    name = body.get("name", None)
    email = body.get("email",  None)
    password = body.get("password", None)

    if name is None or email is None or password is None:
        return jsonify('All credentials are required'), 400
    else:
        user = User()
        user_exist = user.query.filter_by(email = email).one_or_none()

        if user_exist is not None:
            return jsonify('User with that email already exists')
        else:
            salt = b64encode(os.urandom(32)).decode('utf-8')
            hashed_password = generate_password_hash(f'{password}{salt}')

            user.name = name
            user.email = email
            user.password = hashed_password
            user.salt = salt

            db.session.add(user)
            try:
                db.session.commit()
                return jsonify('User created'), 200
            except Exception as error:

                print(error.args)
                return jsonify('Error'), 500

@api.route('/login', methods=['POST'])
def login():
    body = request.json
    email = body.query.get('email', None)
    password = body.query.get('password', None)

    if email is None or password is None:
        return jsonify('All credentials are required'), 400
    
    user = body.query.filter_by(email = email).first()
    if user is None:
        return jsonify('User does not exist'), 404
    else:
        try:
            if check_password_hash(user.password, f'{password}{user.salt}'):
                token = create_access_token(identity = str(user.id))
                return jsonify({"token": token, "current_user": user.serialize()}), 200
            else:
                return jsonify("Incorrect credentials"), 404
        except Exception as error:
            return jsonify('Error'), 500

@api.route('/get-games', methods=['GET'])
def get_games():
    user = User()

    return user.serialize()