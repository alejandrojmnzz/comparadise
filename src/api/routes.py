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
        return jsonify('Name, email and password keys are required'), 400
    
    if name.strip() == "" or email.strip() == "" or password.strip() == "": 
        return jsonify('All credentials are required'), 400
    else:
        user = User()
        user_exist = user.query.filter_by(email = email).one_or_none()

        if user_exist is not None:
            return jsonify('User with that email already exists'), 409
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
                return jsonify('User created'), 201
            except Exception as error:

                print(error.args)
                return jsonify('Error'), 500

@api.route('/login', methods=['POST'])
def login():
    body = request.json
    email = body.get('email', None)
    password = body.get('password', None)

    if email is None or password is None:
        return jsonify('Email and password keys are required'), 400
    if email.strip() == "" or password.strip() == "": 
        return jsonify('All credentials are required'), 400

    user = User.query.filter_by(email = email).first()
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
            print(error.args)
            return jsonify('Error'), 500

@api.route('/api/games', methods=['POST'])
def add_game():
    try:
        # Accede a los datos enviados desde el frontend
        data = request.form
        image = request.files.get('image')  # Obtén la imagen (si se envió)

        # Guarda la imagen en un directorio si es necesario (opcional)
        if image:
            image.save(f"./uploads/{image.filename}")  # Cambia el path según tus necesidades

        # Crea una nueva instancia del modelo Game
        new_game = Game(
            game_name=data.get('gameName'),
            genre=data.get('genre'),
            modes=data.get('modes'),
            release_date=data.get('releaseDate'),
            system_requirements=data.get('systemRequirements'),
            achievements=data.get('achievements'),
            media=image.filename if image else None,  # Guarda el nombre del archivo de imagen
            rating=data.get('rating'),
            players=data.get('players'),
            related_games=data.get('relatedGames'),
            language=data.get('language'),
        )

        # Guarda en la base de datos
        db.session.add(new_game)
        db.session.commit()

        # Responde con éxito
        return jsonify({"message": "Game added successfully"}), 201

    except Exception as e:
        # Maneja errores
        return jsonify({"error": str(e)}), 400
