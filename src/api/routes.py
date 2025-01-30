"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Game
from api.utils import generate_sitemap, APIException, compare_game_and_api
from flask_cors import CORS
from base64 import b64encode
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import cloudinary.uploader as uploader
import requests
import json

api = Blueprint('api', __name__)
app = Flask(__name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/register', methods=['POST'])
def add_new_user():
    try:
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
@jwt_required()
def submit_game():    
    
    user_id = int(get_jwt_identity())
    body_file = request.files
    cover_file =body_file.get("cover_image", None)
    additional_files = request.files.getlist("additional_images[]")

    data = request.form
    auto_related_games = compare_game_and_api(data)
    # print("Request data",data)
    # print("Request files", request.files)
    if not data.get('name') or not data.get('genres') or not data.get('release_date') or not data.get('modes') or not data.get('players') or not data.get('language') or not data.get('system_requirements'):
            return jsonify({"error": "Missing required fields"}), 400
 
    try:
        cover_file = uploader.upload(cover_file)
        cover_file = cover_file["secure_url"]
        
        additional_files_urls =[]
        for file in additional_files:
            upload_result = uploader.upload(file)
            additional_files_urls.append(upload_result["secure_url"])
    except Exception as error:
        print(error.args)
        return jsonify({"error": "Error uploading files", "details": str(error)}), 500
        # try:
    game = Game(
    user_id=user_id,
    name=data['name'],
    cover_image=cover_file,
    genres=data['genres'],
    modes=data.get('modes', ''),
    themes=data['themes'],
    keywords=data['keywords'],
    player_perspective=data['player_perspective'],
    release_date=data['release_date'],
    system_requirements=data['system_requirements'],
    achievements=data.get('achievements', ''),
    additional_images=json.dumps(additional_files_urls),
    rating=data['rating'],
    players=int(data['players']),
    related_games=data.get('related_games', ''),
    auto_related_games=json.dumps(auto_related_games),
    language=data['language'],
    summary=data['summary'],
    description=data['description'],
    trailer=data['trailer']
)

    db.session.add(game)

    try:
        db.session.commit()
        return jsonify({"message": "Game added successfully"}), 201
    except Exception as error:
        print(error)
        return jsonify ("Error submitting")
        # except Exception as e:
        #     return jsonify({"error": str(e)}), 500

        # return jsonify("added")

    # except Exception as error:
    #     print(error.args)
    #     return jsonify("error")


@api.route('/games-search', methods=['GET'])
def search_games():
    try:
        search_query = request.args.get('query','').lower()

        if not search_query:
            return jsonify([])

        games = Game.query.filter(Game.name.ilike(f"%{search_query}%")).all()

        game_list = [game.serialize() for game in games]


        return jsonify(game_list)

    except Exception as error:
        print(error.args)

        return jsonify([])

@api.route('/get-game', methods = ['POST'])
def get_game():
    id = request.json
    game = Game.query.get(id)
    return jsonify(game.serialize())

@api.route('/get-user', methods = ['POST'])
def get_user():
    id = request.json
    user = User.query.get(id)
    print(user.serialize())
    return jsonify(user.serialize())

@api.route('/populate-games', methods = ['GET'])
def populate_games():
    user = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    user.name = 'Populated User'
    user.email = 'populatedemail@gmail.com'
    user.password = hashed_password
    user.salt = salt

    db.session.add(user)
    db.session.commit()



    game_populate = [

        {
            "name": "Cult of the Lamb",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg",
            "genre": "Role-playing (RPG),Simulator,Strategy,Hack and slash/Beat 'em up,Adventure,Indie",
            "modes":"Single player,Multiplayer,Co-operative,Split screen",
            "player_perspective": "Bird view / Isometric",
            "themes": "Action,Fantasy,Comedy",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '07/21/2020',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "7/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "UAO2urG23S4"
        },
        {
            "name": "Hollow Knight",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1736987457/vwwqv55tyfbsli2cvnmg.jpg",
            "genre": "Platform, Adventure, Indie",
            "modes":"Single player",
            "player_perspective": "Side view",
            "themes": "Action, Fantasy",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '03/24/2017',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "9/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "rjeyYMuGZgU"
        },
        {
            "name": "Alan Wake 2",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737148519/2023102313405227_1_xx5epi.jpg",
            "genre": "Shooter,Adventure",
            "player_perspective": "Third person",
            "modes": "Single player",
            "themes": "Action,Horror,Survival",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '04/06/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "10/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "dlQ3FeNu5Yw"
        },
        {
            "name": "Cave Story",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737152572/cave-story-2017724132754_7_v3ikry.jpg",
            "genre": "Shooter,Platform,Adventure,Indie",
            "modes":"Single player",
            "player_perspective": "Side view",
            "themes": "Action,Fantasy,Science fiction,Drama",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '09/07/2012',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "6/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "dlQ3FeNu5Yw"
        },
        {
            "name": "Hotline Miami",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737152704/MV5BOWRlM2RkMjktYWQzMi00YmIxLTkyMWUtOTI0ZWRmODE1N2U5XkEyXkFqcGc_._V1__ee6kam.jpg",
            "genre": "Shooter,Indie,Arcade",
            "modes":"Single player",
            "player_perspective": "Bird view / Isometric",
            "themes": "Action",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '03/10/2013',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "6/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "mg5s5Dq50Rg"
        },
        {
            "name": "Silent Hill 2",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737152964/Silent_Hill_2_remake_cover_jjfae1.jpg",
            "genre": "Puzzle,Adventure",
            "modes":"Single player",
            "player_perspective": "Third person",
            "themes": "Action,Horror",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '01/22/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "6/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "pyC_qiW_4ZY"
        },
         {
            "name": "Deep Rock Galactic",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp",
            "genre": "Shooter,Adventure,Indie)",
            "modes":"Single player,Multiplayer,Co-operative",
            "player_perspective": "First person",
            "themes": "Action, Science fiction",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '05/11/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "9/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "2_GV33zBf3A"
        },
        {
            "name": "Sea of Stars",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153317/e327fc7a5f4f1c688c3d57cb0558af6b740b774154ba676b_upg5ko.avif",
            "genre": "Role-playing (RPG),Turn-based strategy (TBS),Adventure,Indie",
            "modes":"Single player,Multiplayer,Co-operative",
            "player_perspective": "Bird view / Isometric",
            "themes": "Fantasy,Open world",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '01/22/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "6/10",
            "players": 4,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "8jkeh6O1Rzs"
        },
        {
            "name": "Super Smash Bros. Ultimate",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp",
            "genre": "Fighting,Platform",
            "modes":"Single player,Multiplayer,Co-operative",
            "player_perspective": "Side view",
            "themes": "Action,Party",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '08/22/2017',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "9/10",
            "players": 4,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "WShCN-AYHqA"
        },
        {
            "name": "The Legend of Zelda: Tears of the Kingdom",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737154087/The_Legend_of_Zelda_Tears_of_the_Kingdom_cover_bv0ui1.jpg",
            "genre": "Role-playing (RPG),Adventure",
            "modes":"Single player",
            "player_perspective": "Third person",
            "themes": "Action,Fantasy,Science fiction,Sandbox,Open world",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153499/WWlywV3UCoEbldP1k7eR6sH5-Yk13rUm3KiXLI_cBSo_ndxgsa.webp", "https://res.cloudinary.com/dcdymggxx/image/upload/v1737153186/2JSde8PFCF6B4nO2EECrcR1m_s6xclp.webp"]),
            "keywords": "animals",
            "release_date": '08/22/2017',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            "achievements": """Achievement 1
                            Achievement 2
                            Achievement 3
                            Achievement 4
                            Achievement 5""",
            "rating": "9/10",
            "players": 1,
            "related_games": "x, x, x",
            "language": "Spanish, English",
            "summary": "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Aliquid, odit!",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "gp9aY09li1s"
        }

    ]
    for single_populate in game_populate:
        game = Game()
        game.name = single_populate['name']
        game.user_id = User.query.filter_by(email = 'populatedemail@gmail.com').one_or_none().id
        game.cover_image = single_populate['cover_image']
        game.genres = single_populate['genre']
        game.modes = single_populate['modes']
        game.player_perspective = single_populate["player_perspective"]
        game.themes = single_populate["themes"]
        game.additional_images = single_populate["additional_images"]
        game.keywords = single_populate["keywords"]
        game.release_date = single_populate['release_date']
        game.system_requirements = single_populate['system_requirements']
        game.achievements = single_populate['achievements']
        game.rating = single_populate['rating']
        game.players = single_populate['players']
        game.related_games = single_populate['related_games']
        game.language = single_populate['language']
        game.summary = single_populate['summary']
        game.description = single_populate['description']
        game.trailer = single_populate['trailer']
        db.session.add(game)
    try:
        db.session.commit()
        return jsonify({"message": "Populated succesfully"}), 201
    except Exception as error:
        print("hi")
        return jsonify ("Error"), 400

@api.route('/get-api-games', methods=['POST'])
def get_api_games():
    search = request.json
    url = "https://api.igdb.com/v4/games"
    headers = {
            'Accept': 'application/json',
            'Client-ID': os.getenv("CLIENT_ID"),
            'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN")}',
            'Content-Type': 'text/plain'
            }
    data = f'''fields name; where name ~ "{search}"*;
        sort rating desc;
        limit 100;'''

    response = requests.post(url, headers=headers, data=data)
    response = response.json()
    return jsonify(response)

@api.route('/multiquery-game', methods=['POST'])
def multiquery_game():
    id = request.json
    url = "https://api.igdb.com/v4/multiquery"
    headers = {
        'Accept': 'application/json',
        'Client-ID': os.getenv("CLIENT_ID"),
        'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN")}',
        'Content-Type': 'text/plain'
        }
    data = f'''query games "Multiquery" {{
	fields name,genres.name, themes.name, game_modes.name, player_perspectives.name, cover.url;
    where id = {id};
    }};'''
    response = requests.post(url, headers=headers, data=data)
    response = response.json()
    return jsonify(response)

@api.route('/compare-api-and-game', methods=['POST'])
def compare_api_and_game():
    body = request.json
    body_genres = body["genres"]
    body_modes = body["game_modes"]
    body_themes = body["themes"]
    body_player_perspectives = body["player_perspectives"]
    genres_array = []
    modes_array = []
    themes_array = []
    perspectives_array = []

    games = Game.query.all()
    for game in games:
        genres_array.append({'id': game.serialize()["id"], 'genres': game.serialize()["genres"].split(",")})
        modes_array.append({'id': game.serialize()["id"], 'modes': game.serialize()["modes"].split(",")})
        themes_array.append({'id': game.serialize()["id"], 'themes': game.serialize()["themes"].split(",")})
        perspectives_array.append({'id': game.serialize()["id"], 'player_perspectives': game.serialize()["player_perspective"].split(",")})
    filtered_genres = []
    filtered_modes = []
    filtered_themes = []
    filtered_perspectives = []

    total_coincidences = {}

    for genres in genres_array:
        for genre in genres["genres"]:
            for index in body_genres:
                if genre == index["name"]:
                    if total_coincidences.get(f'{str(genres["id"])}_total'):
                        total_coincidences[f'{str(genres["id"])}_total'] = {
                            "total": total_coincidences[f'{str(genres["id"])}_total']["total"] + 1,
                            "id": genres["id"]
                        }         
                    else:
                        total_coincidences[f'{str(genres["id"])}_total'] = {
                            "total": 1,
                            "id": genres["id"]
                        }
                
                    repeated_id = filter(lambda item: item["id"] == genres["id"], filtered_genres)
                    repeated_id_length = len(list(repeated_id))
                    if repeated_id_length == 0:
                        filtered_genres.append(genres)

    for modes in modes_array:
        for mode in modes["modes"]:
            for index in body_modes:
                if mode == index["name"]:
                    if total_coincidences.get(f'{str(modes["id"])}_total'):
                        total_coincidences[f'{str(modes["id"])}_total'] = {
                            "total": total_coincidences[f'{str(modes["id"])}_total']["total"] + 1,
                            "id": modes["id"]
                        }         
                    else:
                        total_coincidences[f'{str(modes["id"])}_total'] = {
                            "total": 1,
                            "id": modes["id"]
                        }
                    repeated_id = filter(lambda item: item["id"] == modes["id"], filtered_modes)
                    repeated_id_length = len(list(repeated_id))
                    if repeated_id_length == 0:
                        filtered_modes.append(modes)

    for themes in themes_array:
        for theme in themes["themes"]:
            for index in body_themes:
                if theme == index["name"]:
                    if total_coincidences.get(f'{str(themes["id"])}_total'):
                        total_coincidences[f'{str(themes["id"])}_total'] = {
                            "total": total_coincidences[f'{str(themes["id"])}_total']["total"] + 1,
                            "id": themes["id"]
                        }         
                    else:
                        total_coincidences[f'{str(themes["id"])}_total'] = {
                            "total": 1,
                            "id": themes["id"]
                        }
                    repeated_id = filter(lambda item: item["id"] == themes["id"], filtered_themes)
                    repeated_id_length = len(list(repeated_id))
                    if repeated_id_length == 0:
                        filtered_themes.append(themes)
                        

    for perspectives in perspectives_array:
        for perspective in perspectives["player_perspectives"]:
            for index in body_player_perspectives:
                if perspective == index["name"]:
                    if total_coincidences.get(f'{str(perspectives["id"])}_total'):
                        total_coincidences[f'{str(perspectives["id"])}_total'] = {
                            "total": total_coincidences[f'{str(perspectives["id"])}_total']["total"] + 1,
                            "id": perspectives["id"]
                        }         
                    else:
                        total_coincidences[f'{str(perspectives["id"])}_total'] = {
                            "total": 1,
                            "id": perspectives["id"]
                        }
                    repeated_id = filter(lambda item: item["id"] == perspectives["id"], filtered_perspectives)
                    repeated_id_length = len(list(repeated_id))
                    if repeated_id_length == 0:
                        filtered_perspectives.append(perspectives)

    total_coincidences_array = [] 

    for id in total_coincidences:
        total_coincidences_array.append({id: total_coincidences.get(id)})

    sorted_data = sorted(total_coincidences_array, key=lambda x: list(x.values())[0]['total'], reverse=True)
    return(sorted_data)

