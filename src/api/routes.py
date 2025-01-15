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
from werkzeug.utils import secure_filename
import cloudinary.uploader as uploader 

api = Blueprint('api', __name__)
app = Flask(__name__)

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
        
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit ('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/get-recent-games', methods=['GET'])
def get_recent_games():
    try:
        games = Game.query.order_by(Game.id.desc()).limit(10).all() 

        return jsonify(list(map(lambda item: item.serialize(), games)))
    except Exception as error:
        print(error.args)
        return jsonify(error.args), 500
    
@api.route('/submit-game', methods=['POST'])
def submit_game():    
    
    # if 'cover_image' not in request.files:
    #     return jsonify({"error": "Cover image is missing"}), 400
    
    body_file = request.files
    cover_file =body_file.get("cover_image", None)
    
    # # Save the cover media file (if provided)
    # if cover_file and allowed_file(cover_file.filename):
    #     filename = secure_filename(cover_file.filename)
    #     cover_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     cover_file.save(cover_path)
    # else:
    #     cover_path = None

    data = request.form
    print(data)
    print(cover_file)
    if not data.get('name') or not data.get('genre') or not data.get('release_date') or not data.get('modes') or not data.get('players') or not data.get('language'):
        return jsonify({"error": "Missing required fields"}), 400
    
    cover_file = uploader.upload(cover_file)
    cover_file = cover_file["secure_url"]
    # try:
    game = Game(
    name=data['name'],
    cover_image=cover_file,
    genre=data['genre'],
    modes=data.get('modes', ''),
    release_date=data['release_date'],
    system_requirements=data['system_requirements'],
    achievements=data.get('achievements', ''),
    rating=data['rating'],
    players=int(data['players']),
    related_games=data.get('related_games', ''),
    language=data['language'],
    summary=data['summary'],
    description=data['description'],
    trailer=data['trailer']
)

    print(game)
    db.session.add(game)
    try:
        db.session.commit()
        return jsonify({"message": "Game added successfully"}), 201
    except Exception as error:
        print(error.args)
        return jsonify ("Error submitting")
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

@api.route('/get-game', methods = ['POST'])
def get_game():
    id = request.json
    game = Game.query.get(id)
    return jsonify(game.serialize())