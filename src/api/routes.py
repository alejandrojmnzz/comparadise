"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Game, Review, Like, Cart, Purchase
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
    game_file = body_file.get("game_file", None)
    print(cover_file)

    data = request.form
    auto_related_games = compare_game_and_api(data)
    # print("Request data",data)
    # print("Request files", request.files)
    if not data.get('name') or not data.get('genres') or not data.get('release_date') or not data.get('modes') or not data.get('players') or not data.get('language') or not data.get('system_requirements'):
            return jsonify({"error": "Missing required fields"}), 400
 
    try:
        cover_file = uploader.upload(cover_file)
        cover_file = cover_file["secure_url"]
        game_file = uploader.upload(game_file)
        game_file = game_file["secure_url"]
        
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
    # keywords=data['keywords'],
    player_perspective=data['player_perspective'],
    release_date=data['release_date'],
    system_requirements=data['system_requirements'],
    # achievements=data.get('achievements', ''),
    additional_images=json.dumps(additional_files_urls),
    pegi=data['pegi'],
    players=int(data['players']),
    # related_games=data.get('related_games', ''),
    auto_related_games=json.dumps(auto_related_games),
    language=data['language'],
    summary=data['summary'],
    description=data['description'],
    trailer=data['trailer'],
    game_file=game_file
)

    db.session.add(game)

    try:
        db.session.commit()
        return jsonify({"message": "Game added successfully"}), 201
    except Exception as error:
        print(error)
        return jsonify ("Error submitting")


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
            # "keywords": "animals",
            "release_date": '07/21/2020',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "7/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '03/24/2017',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "9/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '04/06/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "10/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '09/07/2012',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "6/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '03/10/2013',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "6/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '01/22/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "6/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '05/11/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "9/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '01/22/2023',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "6/10",
            "players": 4,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '08/22/2017',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "9/10",
            "players": 4,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
            # "keywords": "animals",
            "release_date": '08/22/2017',
            "system_requirements": """OS *: Windows 7 (64bit)
                                    Processor: Intel Core 2 Duo E5200.
                                    Memory: 4 GB RAM.
                                    Graphics: GeForce 9800GTX+ (1GB)
                                    DirectX: Version 10.
                                    Storage: 9 GB available space.
                                    Additional Notes: 1080p, 16:9 recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "9/10",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([134, 573, 468]),
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
        # game.keywords = single_populate["keywords"]
        game.release_date = single_populate['release_date']
        game.system_requirements = single_populate['system_requirements']
        # game.achievements = single_populate['achievements']
        game.pegi = single_populate['pegi']
        game.players = single_populate['players']
        # game.related_games = single_populate['related_games']
        game.auto_related_games=single_populate['auto_related_games']
        game.language = single_populate['language']
        game.summary = single_populate['summary']
        game.description = single_populate['description']
        game.trailer = single_populate['trailer']
        game.is_liked = False
        game.game_file = "https://res.cloudinary.com/dcdymggxx/raw/upload/v1738861007/blacklist_za4hif.txt"
        db.session.add(game)
    try:
        db.session.commit()
        return jsonify({"message": "Populated succesfully"}), 201
    except Exception as error:
        return jsonify ("Error"), 400

@api.route('/get-api-games', methods=['POST'])
def get_api_games():
    print(os.getenv("CLIENT_ID"))
    print(os.getenv("ACCESS_TOKEN"))
    search = request.json
    url = "https://api.igdb.com/v4/games"
    headers = {
            'Accept': 'application/json',
            'Client-ID': os.getenv("CLIENT_ID"),
            'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN")}',
            'Content-Type': 'text/plain'
            }
    data = f'''fields name, genres, game_modes, player_perspectives, themes; where name ~ "{search}"*;
    
        sort rating desc;
        limit 100;'''
    
    response = requests.post(url, headers=headers, data=data)
    response = response.json()
    response_array = []
    for game in response:
        genre_exists = False
        mode_exists = False
        perspective_exists = False
        theme_exists = False
        for item in game:
            print(item)
            if item == "genres":
                genre_exists = True
            if item == "game_modes":
                mode_exists = True
            if item == "player_perspectives":
                perspective_exists = True
            if item == "themes":
                theme_exists = True            
        if genre_exists == True and mode_exists == True and perspective_exists == True and theme_exists == True:
            response_array.append(game)

    print(response_array)
    return jsonify(response_array)

@api.route('/multiquery-game', methods=['POST'])
def multiquery_game():
    try:
        id = request.json
        url = "https://api.igdb.com/v4/multiquery"
        headers = {
            'Accept': 'application/json',
            'Client-ID': os.getenv("CLIENT_ID"),
            'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN")}',
            'Content-Type': 'text/plain'
            }
        data = f'''query games "Multiquery" {{
        fields name,genres.name, themes.name, game_modes.name, player_perspectives.name, cover.url, rating;
        where id = {id};
 
        }};'''
        response = requests.post(url, headers=headers, data=data)
        response = response.json()
        return jsonify(response)
    except Exception as error:
        print(error.args)
        return jsonify(error.args)

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

@api.route("/add-to-cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.json
    game_id = data.get("game_id")

    if not game_id:
        return jsonify({"error": "Game ID is required"}), 400
    
    existing_cart_item = Cart.query.filter_by(user_id=user_id, game_id=game_id).first()
    if existing_cart_item:
        return jsonify({"message": "Game is already in the cart"}), 400
    
    new_cart_item = Cart(user_id=user_id, game_id=game_id)
    db.session.add(new_cart_item)
    db.session.commit()

    return jsonify({"message": "Game added to cart"}), 200

@api.route("/cart", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify(["No purchased games have been found"]), 404
    
    cart_data = []
    for item in cart_items:
        game = Game.query.get(item.game_id)
        if game:
            cart_data.append ({
                "id": item.id,
                "game": game.serialize()
            })
    return jsonify(cart_data)

@api.route("/remove-from-cart/<int:cart_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(cart_id):
    user_id = get_jwt_identity()
    cart_item = Cart.query.filter_by(id=cart_id, user_id=user_id).first()

    if not cart_item:
        return jsonify({"error": "Item not found"}), 404
    
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Game removed from cart"}), 200

@api.route('/my-games', methods=['GET'])
@jwt_required()
def get_current_user_games():
    try: 
        current_user = get_jwt_identity()
        user_games = Game.query.filter_by(user_id = current_user)

        return jsonify(list(map(lambda item: item.serialize(), user_games)))
    except Exception as error:
        print(error.args)
        return jsonify(False)
    
@api.route('/user-games', methods=['POST'])
def get_user_games():
    try: 
        user_id = request.json
        user_games = Game.query.filter_by(user_id = user_id)
        print(user_id)
        return jsonify(list(map(lambda item: item.serialize(), user_games)))
    except Exception as error:
        print(error.args)
        return jsonify(False)

@api.route('/purchase', methods=['POST'])
@jwt_required()
def purchase_games():
    user_id = get_jwt_identity()

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"success": False, "message": "Cart is empty"}), 400
    for item in cart_items:
        game = Game.query.get(item.game_id)
        if not game:
            return jsonify({"success": False, "message": "Game ID not found"}), 404
        purchased_game = Purchase(user_id=user_id, game_id=item.game_id)
        db.session.add(purchased_game)
        db.session.delete(item)

    db.session.commit()

    return jsonify({"success": True, "message": "Purchase completed"}), 200

@api.route('/library', methods=['GET'])
@jwt_required()
def get_library():
    try:
        user_id = get_jwt_identity()
        purchase_games = Purchase.query.filter_by(user_id=user_id).all()
        games = []
        for purchase in purchase_games:
            game = Game.query.get(purchase.game_id)
            if game:
                games.append(game.serialize())

        return jsonify(games), 200
    except Exception as error:
        print("Error fetching library: {error}")
        return jsonify(False), 500

@api.route('/add-review', methods=['POST'])
@jwt_required()
def add_review():
    body = request.json
    body_review = body["review"]
    body_rating = body["rating"]
    body_game_id = body["game_id"]
    review = Review()
    review.rating = body_rating
    review.review = body_review
    review.user_id = int(get_jwt_identity())
    review.game_id = body_game_id
    db.session.add(review)
    try:
        db.session.commit()
    except Exception as error:
        print(error)
        return jsonify("Error")
    # all_reviews = Review.query.all()
    # print(list(map(lambda item: item.serialize(), all_reviews)))
    return jsonify(body)

@api.route('/get-all-reviews/<int:id>', methods=['GET'])
def get_reviews(id):
    try: 
        user_reviews = Review.query.filter_by(game_id = id)
        return jsonify(list(map(lambda item: item.serialize(), user_reviews)))
    except Exception as error:
        print(error)
        return False
    
@api.route('/like-game/<int:id>', methods=['GET'])
@jwt_required()
def like_game(id):
    like = Like()
    like_exists = like.query.filter(Like.user_id == int(get_jwt_identity()), Like.game_id == id).one_or_none()

    if like_exists is None:
        like.user_id = int(get_jwt_identity())
        like.game_id = id
        like.is_liked = True

        db.session.add(like)
        try:
            db.session.commit()
            return jsonify("done")
        except Exception as error:
            print(error.args)
            return jsonify('Error')
    else:
        print("User already liked this game")

        return jsonify("User already liked this game"), 208
    

@api.route('update-like/<int:id>', methods=['GET'])
@jwt_required()
def update_like(id):
    like = Like.query.filter(Like.user_id == int(get_jwt_identity()), Like.game_id == id).one_or_none()
    if like is not None:
        if like.is_liked == True:
            like.is_liked = False
        else:
            like.is_liked = True
        try:
            db.session.commit()
            return jsonify("Disliked"), 200
        except Exception as error:
            print(error.args)
            return jsonify("error")
    else:
        print("does not exist")
        return jsonify("Like doesn't exist"), 208
    

@api.route('/get-game-likes', methods=['GET'])
def get_game_likes():
    all_likes = Like.query.filter_by(is_liked = True)
    game_likes = {}
    for like in all_likes:
        game_likes[like.game_id] = game_likes.get(like.game_id, 0) + 1
        
    game_likes_array = []
    count = 0
    for item in game_likes:
        game_likes_array.append({"likes": game_likes.get(item), "game": all_likes[count].game.serialize()})
        count = count + 1

    sorted_games = sorted(game_likes_array, key=lambda x: x["likes"], reverse=True)
    return jsonify(list(map(lambda item: item, sorted_games)))

@api.route('/get-all-game-likes/<int:id>', methods=['GET'])
def get_all_game_likes(id): 
    likes = Like.query.filter(Like.game_id == id, Like.is_liked == True)
    return jsonify(len(list(map(lambda item: item.serialize()["game_id"], likes))))
