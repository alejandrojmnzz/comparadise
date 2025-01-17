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

@api.route('/games-search', methods=['GET'])
def search_games():
    try:
        search_query = request.args.get('query','').lower()

        if not search_query:
            return jsonify([])
        
        games = Game.query.filter(Game.name.ilike(f"%{search_query}%")).all()

        game_list = [game.serialize() for game in games]

        print(game_list)

        return jsonify(game_list)
    
    except Exception as error:
        print(error.args)

        return jsonify([])

@api.route('/get-game', methods = ['POST'])
def get_game():
    id = request.json
    game = Game.query.get(id)
    return jsonify(game.serialize())

@api.route('populate-games', methods = ['GET'])
def populate_games():
    game_populate = [
        {
            "name": "Cult of the Lamb",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1737148333/images_oyidub.jpg",
            "genre": "Adventure",
            "modes":"Campaign",
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
            "genre": "Metroidvania",
            "modes":"Campaign",
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
            "genre": "Action (shooter)",
            "modes":"Campaign",
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
            "genre": "Adventure",
            "modes":"Campaign",
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
            "genre": "Adventure",
            "modes":"Campaign",
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
            "genre": "Horror",
            "modes":"Campaign",
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
            "genre": "Adventure)",
            "modes":"Campaign",
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
            "genre": "MulAction (shooter)",
            "modes":"Multiplayer",
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
            "genre": "Adventure",
            "modes":"Multiplayer",
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
            "genre": "Adventure",
            "modes":"Campaign",
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
        game.cover_image = single_populate['cover_image']
        game.genre = single_populate['genre']
        game.modes = single_populate['modes']
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
        print(error.args)
        return jsonify ("Error"), 500
