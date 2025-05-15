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
        current_game = game_likes.get(like.game_id, 0)
        if current_game == 0:
            game_likes[like.game_id] = { "likes": 1, "game": like.game.serialize() }
        else:
            game_likes[like.game_id] = { "likes": game_likes[like.game_id]["likes"] + 1, "game": like.game.serialize()}
    print(game_likes)
    game_likes_array = []
    count = 0

    for item in game_likes:

        game_likes_array.append({"likes": game_likes.get(item)["likes"], "game": game_likes[item]["game"]})

        count = count + 1
        print(game_likes.get(item))
    sorted_games = sorted(game_likes_array, key=lambda x: x["likes"], reverse=True)
    return jsonify(list(map(lambda item: item, sorted_games)))

@api.route('/get-all-game-likes/<int:id>', methods=['GET'])
def get_all_game_likes(id): 
    likes = Like.query.filter(Like.game_id == id, Like.is_liked == True)
    return jsonify(len(list(map(lambda item: item.serialize()["game_id"], likes))))

@api.route('/populate-games', methods = ['GET'])
def populate_games():
    kevin = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    kevin.name = 'Kevin'
    kevin.email = 'kevin@gmail.com'
    kevin.password = hashed_password
    kevin.salt = salt

    db.session.add(kevin)

    amanda = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    amanda.name = 'Amanda'
    amanda.email = 'amanda@gmail.com'
    amanda.password = hashed_password
    amanda.salt = salt

    db.session.add(amanda)

    alex = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    alex.name = 'Alex'
    alex.email = 'alex@gmail.com'
    alex.password = hashed_password
    alex.salt = salt

    db.session.add(alex)

    peter = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    peter.name = 'Peter'
    peter.email = 'peter@gmail.com'
    peter.password = hashed_password
    peter.salt = salt

    db.session.add(peter)

    jasper = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    jasper.name = 'Jasper'
    jasper.email = 'jasper@gmail.com'
    jasper.password = hashed_password
    jasper.salt = salt

    db.session.add(jasper)
    
    vanessa = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    vanessa.name = 'Vanessa'
    vanessa.email = 'vanessa@gmail.com'
    vanessa.password = hashed_password
    vanessa.salt = salt

    db.session.add(vanessa)

    jackson = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    jackson.name = 'Jackson'
    jackson.email = 'jackson@gmail.com'
    jackson.password = hashed_password
    jackson.salt = salt

    db.session.add(jackson)

    olivia = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    olivia.name = 'Olivia'
    olivia.email = 'olivia@gmail.com'
    olivia.password = hashed_password
    olivia.salt = salt

    db.session.add(olivia)

    michael = User()
    salt = b64encode(os.urandom(32)).decode('utf-8')
    hashed_password = generate_password_hash(f'populatepass{salt}')

    michael.name = 'Michael'
    michael.email = 'michael@gmail.com'
    michael.password = hashed_password
    michael.salt = salt

    db.session.add(michael)

    db.session.commit()




    game_populate = [

        {
            "name": "Ready or Not",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257355/Ready_or_Not_j1ids4.jpg",
            "genre": "Shooter,Simulator,Tactical",
            "modes":"Single player,Multiplayer,Co-operative",
            "player_perspective": "First person",
            "themes": "Action",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257355/12_ns3t0a.jpg",
                                            "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257355/ef8c85df-3a37-4055-aa89-d9210b32e5e7_1920x1080_d2ioda.jpg",
                                            "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257356/Ready-or-Not_screen03-scaled_xjsqga.jpg",
                                            "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257355/Single-Player-or-CO-OP-Experience_r6axqa.jpg"]),
            # "keywords": "animals",
            "release_date": '12/13/2023',
            "system_requirements": """Requires a 64-bit processor and operating system
OS: Windows 10, Windows 11
Processor: Intel Core i5-4430 / AMD FX-6300
Memory: 8 GB RAM
Graphics: NVIDIA GeForce GTX 960 2GB / AMD Radeon R7 370 2GB
DirectX: Version 11
Storage: 60 GB available space""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "18",
            "players": 4,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([76263, 37419, 36553]),
            "language": "English",
            "summary": "Ready or Not is an intense, tactical, first-person shooter that depicts a modern-da",
            "description": """- The LSPD reports a massive upsurge in violent crime across the greater Los Sueños area. Special Weapons and Tactics (SWAT) teams have been dispatched to respond to various scenes involving high-risk hostage situations, active bomb threats, barricaded suspects, and other criminal activities. Citizens are being advised to practice caution when traveling the city or to stay at home.

It has been noted that while Los Sueños is still seen as a city where riches can be found, for many more the finer things in life are becoming less and less obtainable. “The city is sprawling with cramped high-rise apartments and decaying affordable housing, which has been exploited by the criminal underground like a malevolent parasite,” states Chief Galo Álvarez. “In a city where people are just trying to survive, lawful action from the LSPD and the LSPD SWAT team remains an integral force preventing the stretched thin social fabric in this city from snapping under this chaotic strain.”""",
            "trailer": "jW3zr1Jn5bM"
        },
        {
            "name": "Death's Door",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257388/Death_s_Door_fljaak.jpg",
            "genre": """
Role-playing (RPG),Hack and slash/Beat 'em up,Adventure""",
            "modes":"Single player",
            "player_perspective": "Third person, Bird view / Isometric",
            "themes": "Action, Fantasy",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/deathsdoorlaunchtrailerblogroll-1626789054181_g114ty.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/deathsdoordevolverdigitalshowcase2021trailerblogroll-1623459927431_isvkjs.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/deathsdoorgameplaytrailer2blogroll-1626276533633_uo9oqu.jpg",
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/Grove-of-Spirit-Featured-Image-Deaths-Door-Walkthrough-1_vphf7m.jpg"]),
            # "keywords": "animals",
            "release_date": '07/20/2021',
            "system_requirements": """OS: Windows 10 x64
Processor: Intel Core i5-8250U (4 * 1800) or equivalent; AMD Phenom II X4 965 (4 * 3400) or equivalent
Memory: 8 GB RAM
Graphics: GeForce MX 150 ( 2048 MB); Radeon R7 260X (2048 MB)
Storage: 5 GB available space""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "3",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([96217, 106987, 105049]),
            "language": "Spanish",
            "summary": "Reaping souls of the dead and punching a clock might get monotonous but it's honest work for a Crow.",
            "description": """Reaping souls of the dead and punching a clock might get monotonous but it's honest work for a Crow. The job gets lively when your assigned soul is stolen and you must track down a desperate thief to a realm untouched by death - where creatures grow far past their expiry and overflow with greed and power.

Talon Sharp Combat: Utilize melee weapons, arrows and magic to overcome a fantastic array of beasts and demigods. Mistakes are punished and victory is rewarded. Gain an edge by customizing your character stats and mastering the abilities and upgrades you obtain.

A Beautifully Bleak World: Venture beyond the Doors and explore a land full of twisted inhabitants and countless secrets, bringing hope to the weird and wonderful characters you’ll meet along the way.

A Dark Mystery to Unravel: Track down and defeat colossal tyrants with stories and motivations of their own. Experience a somber yet darkly comedic tale, uncovering the truths behind the flow of souls, the role of the Crows and the origin of the Doors.""",
            "trailer": "NjnEg3ucXpc"
        },
        {
            "name": "Deck of Ashes",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/Deck_of_Ages_wsly37.png",
            "genre": "Role-playing (RPG),Strategy,Adventure,Card & Board Game",
            "player_perspective": "Third person",
            "modes": "Single player",
            "themes": "Fantasy",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257388/Deck-of-Ashes-Complete-Edition-gameplay_efbn8v.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/deck-of-ashes-complete-edition-review-1-640x360_xacts1.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/ss_6d6d48ae205c4e218f9489c0bdc6644aac8bb7c3.1920x1080_no8jrr.jpg",
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257390/ss_a75eb85804eac3d3ec90e6f4ef7fc3d28d3c3b20.1920x1080_zgze61.jpg"]),
            # "keywords": "animals",
            "release_date": '06/09/2020',
            "system_requirements": """OS *: Windows 7, 8, 10, 11
Processor: 2.0 Ghz
Memory: 2 GB RAM
Graphics: 512 Mb capable of OpenGL 2.0+ support
Storage: 5 GB available space""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "12",
            "players": 3,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([19404, 96217, 106987]),
            "language": "French",
            "summary": "One character at a time, lead the cast of antiheroes on a quest for redemption.",
            "description": """Deck of Ashes is an adventure game with tactical card combat. One character at a time, lead the cast of antiheroes on a quest for redemption. Explore the cursed fantasy world and hunt down powerful cards. Put your survival and resource management skills to the test when upgrading your Camp of allies.

The choices that drive your journey - where to go, which resource to collect, which risk to take, and which card to craft - are the difference between success and untimely demise.""",
            "trailer": "cDcfbJqUH6k"
        },
        {
            "name": "Dredge",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/Dredge_b7bfqn.jpg",
            "genre": "Role-playing (RPG),Simulator,Adventure",
            "modes":"Single player",
            "player_perspective": "Bird view / Isometric",
            "themes": "Action,Horror,Open world,Mystery",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/ss_87d0d9ba6e7851a07778ac696d56af8e0ab71a21.1920x1080_aj8hsg.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/Dredge-gameplay_fldcbe.jpgp", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/ss_d98d0c25d9cdb72f4d8e78818a49a34ace974d47.1920x1080_x7kuvo.jpg",
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257389/c1a02c0616b779f82ac442f73b4b1241bdfe3f53ed6a84e59ba04e6560d74a9a_product_card_v2_mobile_slider_639_kn9vyu.jpg"]),
            # "keywords": "animals",
            "release_date": '03/30/2023',
            "system_requirements": """OS: Windows 10
Processor: Intel Core i3-2100 | AMD Phenom II X4 965
Memory: 4 GB RAM
Graphics: Nvidia 8800 GT 512MB | Radeon HD 6570 1GB
DirectX: Version 11
Storage: 2 GB available space
Additional Notes: 720p @ 30 FPS""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "16",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([18225, 26574, 114455]),
            "language": "Spanish, English",
            "summary": "DREDGE is a single-player fishing adventure with a sinister undercurrent.",
            "description": "Captain your fishing trawler to explore a collection of remote isles, and their surrounding depths, to see what lies below. Sell your catch to the locals and complete quests to learn more about each area’s troubled past. Outfit your boat with better equipment to trawl deep-sea trenches and navigate to far-off lands, but keep an eye on the time. You might not like what finds you in the dark...",
            "trailer": "s3ws82dj_fA"
        },
        {
            "name": "Buck Up And Drive!",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257390/Buck_up_and_drive_hvlkup.png",
            "genre": "Fighting,Racing,Arcade",
            "modes":"Single player, Multiplayer, Split screen",
            "player_perspective": "Third person",
            "themes": "Action",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257390/hq720_l21dlk.jpg",
                                              "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257390/BuckUpAndDrive-1_thedf6.jpg", 
                                              "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257390/20220115232242_1_b3paq2.jpg",
                                              "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257390/ss_5cc1697b9a6265c8b644341e2e0a92970895a5db.1920x1080_nw4g0r.jpg"]),
            # "keywords": "animals",
            "release_date": '06/10/2022',
            "system_requirements": """Requires a 64-bit processor and operating system
OS *: 64bit Windows Vista or more recent
Processor: 2Ghz Dual Core
Memory: 4 GB RAM
Graphics: 512MB
Storage: 100 MB available space""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "3",
            "players": 4,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([115563, 119207, 43367]),
            "language": "Japanase",
            "summary": "Where are we going? As individuals... as a species... what awaits us at the end of this road?",
            "description": """Features:
- Endless driving game inspired by arcade classics, with simple yet intense gameplay featuring a total slap in the face of realism. And a kick in the spleen, too!
- Procedurally generated track with multiple environments to visit, ranging from the somewhat realistic to the completely absurd. GO TO HELL!... literally!
- PINK. BACKFLIPPING. TRUCKS. ON THE FUCKING MOON.
- Go 1v1 against another player (or a CPU) in a fighting mode. With cars. I dunno either, I came up with it while in the shower.
- Customizable car decals through external image files. Put "eggplants" all over the cars, for all I care!
- Controls for both game modes are 8 directions and one button. Play one-handed, if you want! Keep your other hand for... holding orange juice! Yes!
- Available for both Windows and Ubuntu (other Linux distros may work).""",
            "trailer": "lkmwP2vei3c"
        },
        {
            "name": "Lost Alone Ultimate",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257391/Lost_Alone_Ultimate_h736u5.jpg",
            "genre": "Strategy,Adventure",
            "modes":"Single player",
            "player_perspective": "First person",
            "themes": "Action,Horror,Thriller,Mystery",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257391/ss_6085d8198bb7d67840ea1364c78042f1c696efea.1920x1080_qd120d.jpg",
                                              "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257391/ss_8f0067788417e54f3323b6fe06179a4d9830516f.1920x1080_ycrkb0.jpg", 
                                              "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257391/ss_971973a5f50bb44b6acfaa5ba273604797e50c06.1920x1080_pmdohj.jpg",
                                              "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257391/ss_0cdbe4eb17cfe5013ecbde4dad5abfc4285ed672.1920x1080_hwgsif.jpg"]),
            # "keywords": "animals",
            "release_date": '04/25/2023',
            "system_requirements": """OS *: WINDOWS® 7, 8, 8.1, 10, 11
Processor: Intel® Core™ i3 or AMD Ryzen™ 3
Memory: 6 GB RAM
Graphics: NVIDIA® GeForce® GTX 950 or AMD Radeon™ R7 370
DirectX: Version 10
Storage: 15 GB available space""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "12",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([114455, 111130, 25646]),
            "language": "Spanish",
            "summary": " first-person psychological horror game designed to convey anxiety, distress, and terror.",
            "description": " Lorem ipsum dolor sit amet consectetur adipisicing elit. Quas excepturi accusantium quasi at. Explicabo provident doloribus et tempora, facere facilis ullam debitis recusandae magnam eum ad, error nemo aliquam architecto aut asperiores? Commodi ad accusamus placeat ab? Iste nesciunt ducimus sapiente accusamus totam adipisci, facilis ullam, fugit saepe reiciendis optio!",
            "trailer": "pyC_qiW_4ZY"
        },
         {
            "name": "Evergate",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257393/Evergate_xkappd.jpg",
            "genre": "Platform,Puzzle,Adventure",
            "modes":"Single player",
            "player_perspective": "Side view",
            "themes": "Action",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257393/preview-Q9d.1024x576_indd3t.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257393/2_ktsmz3.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257393/3729466-eg2bfzou0aup9kw-orig_w9zttw.jpg",
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257393/1_b2zz4d.jpg"]),
            # "keywords": "animals",
            "release_date": '11/09/2020',
            "system_requirements": """OS: 7
Processor: Intel Core 2 Duo E4500 @ 2.2GHz or AMD Athlon 64 X2 5600+ @ 2.8 GHz
Memory: 4 GB RAM
Graphics: GeForce 240 GT or Radeon HD 6570 – 1024 MB (1 gig)
DirectX: Version 9.0c
Storage: 3 GB available space""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "3",
            "players": 4,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([89597, 55190, 20342]),
            "language": "Spanish",
            "summary": "Evergate is a haunting 2D puzzle-platformer set in a stunning hand-drawn vision of the Afterlife",
            "description": """When a lost soul named "Ki" awakens in the afterlife, her path back to earth is blocked by the ‘Evergate’. To return home, Ki must decipher her mysterious connection to kindred spirit as she navigates through memories of a time once past.

Navigate through each new memory via 85 challenging stages. Harness the ‘Soulflame’ mechanic, unlock new abilities and find your own creative ways to reach each end gate.""",
            "trailer": "5gA4Zp0Y-qE"
        },
        {
            "name": "Kenshi",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/Kenshi_gyndpu.jpg",
            "genre": """
Real Time Strategy (RTS),Role-playing (RPG),Strategy,Adventure""",
            "modes":"Single player",
            "player_perspective": "Third person,Bird view / Isometric",
            "themes": "Action,Fantasy,Science fiction,Stealth,Sandbox,Open world",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/unnamed_lufuz8.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/71a0078094be04846dbc31af318a30af659fa0a736e45f15b03eb17db01b1c12_product_card_v2_mobile_slider_639_swejub.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/maxresdefault_ydnfy0.jpg",
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/ss_166224e7abc243e23e8479154685d1ef007da373.1920x1080_fd2qcf.jpg"]),
            # "keywords": "animals",
            "release_date": '12/06/2018',
            "system_requirements": """OS:64-bit Windows
Processor:Dual-core 64-bit
Memory:6 GB RAM
Graphics:Pixel shader 5.0 capable card
DirectX®:11
Hard Drive:14GB HD space""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "18",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([17379, 1877, 26574]),
            "language": "English",
            "summary": "Focusing on open-ended sandbox gameplay features rather than a linear story. ",
            "description": """Research new equipment and craft new gear. Purchase and upgrade your own buildings to use as safe fortified havens when things go bad, or use them to start up a business. Aid or oppose the various factions in the world while striving for the strength and wealth necessary to simply survive in the harsh desert. Train your men up from puny victims to master warriors. Carry your wounded squad mates to safety and get them all home alive.""",
            "trailer": "Xd1XnmwD8zE"
        },
        {
            "name": "Pacific Drive",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257392/Pacific_drive_zc877g.jpg",
            "genre": "Simulator,Adventure",
            "modes":"Single player",
            "player_perspective": "First person",
            "themes": "Action,Sciencie fiction,Survival,Mystery",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257391/pacific-drive-guide_kwfdvd.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257392/ss_a753a13813556eb20e02763e82877485dac848ab.1920x1080_xz9a0w.jpg", 
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257392/ss_7dfb1b9087a859b49debadb941269f971b212277.1920x1080_adkfol.jpg",
                                             "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257391/759LZeZuzFgV3uMJz2ThWg-1200-80_h6fwk5.jpg"]),
            # "keywords": "animals",
            "release_date": '04/22/2014',
            "system_requirements": """Requires a 64-bit processor and operating system
OS: Windows 10
Processor: Intel Core i5 8600
Memory: 16 GB RAM
Graphics: Nvidia GTX 1060 6GB
DirectX: Version 12
Storage: 18 GB available space
Additional Notes: Requires a 64-bit processor and operating system""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "12",
            "players": 2,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([25311, 17479, 81680]),
            "language": "English",
            "summary": "Face the supernatural dangers of the Olympic Exclusion Zone with a car ",
            "description": "Pacific Drive is a first-person driving survival game with your car as your only companion. Navigate a surreal reimagining of the Pacific Northwest, and face supernatural dangers as you venture into the Olympic Exclusion Zone. Each excursion into the wilderness brings unique and strange challenges as you restore and upgrade your car from an abandoned garage that acts as your home base. Gather precious resources and investigate what’s been left behind in the Zone; unravel a long-forgotten mystery while learning exactly what it takes to survive in this unpredictable, hostile environment.",
            "trailer": "nvPPggQ-pHs"
        },
        {
            "name": "Axiom Verge 2",
            "cover_image": "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257393/Axiom_verge_2_vtdhda.jpg",
            "genre": "Platform,Adventure",
            "modes":"Single player",
            "player_perspective": "Side view",
            "themes": "Action,Science fiction",
            "additional_images": json.dumps(["https://res.cloudinary.com/dcdymggxx/image/upload/v1747257392/Axiom-Verge-2_08-11-21_ulpuh9.jpg",
                                              "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257392/ss_ce1b5a5d7d68fb9cbb8113cabcffe45b7aae94fa.1920x1080_ou55tb.jpg",
                                                "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257392/1_1_yakcai.jpg",
                                                "https://res.cloudinary.com/dcdymggxx/image/upload/v1747257394/ss_767247b42d4b275f9cb69cd0d4f381f19c8c9b0d.1920x1080_sovumr.jpg"]),
            # "keywords": "animals",
            "release_date": '08/11/2022',
            "system_requirements": """OS *: Windows 7
Processor: Intel Pentium E2180 2.0 GHz
Memory: 4 GB RAM
Graphics: Intel HD Graphics 4400
Storage: 500 MB available space
Additional Notes: XInput or controller recommended.""",
            # "achievements": """Achievement 1
            #                 Achievement 2
            #                 Achievement 3
            #                 Achievement 4
            #                 Achievement 5""",
            "pegi": "12",
            "players": 1,
            # "related_games": "x, x, x",
            "auto_related_games": json.dumps([28070, 105269, 55190]),
            "language": "Mandarin",
            "summary": "Explore a sprawling, alien world in the sequel to the award winning Axiom Verge.",
            "description": """You may have played Axiom Verge, or heard it referenced as a benchmark for indie action-exploration games. This long awaited sequel expands on the universe with completely new characters, abilities, and gameplay.

Indra, the billionaire behind the worldwide Globe 3 conglomerate, heads to Antarctica to investigate the disappearance of her daughter, but ultimately finds herself in an entirely different reality, infected by parasitic machines that both aid and confound her. Where is she? Who is the mysterious person goading her from the other end of the computer terminal?

Explore an alternate Earth-like world, replete with the ruins of an ancient, high-tech civilization. Hack machines. Battle monsters. Use your remote drone to enter the Breach, a parallel but connected reality that is filled with its own dangers. You’ll want to search every inch for the hidden items and upgrades you need to survive.""",
            "trailer": "EOlpRihgMZA"
        }

    ]
    index = 0
    
    for single_populate in game_populate:
        index += 1
        game = Game()
        game.name = single_populate['name']
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

        if index <= 3:
            game.user_id = User.query.filter_by(email = 'kevin@gmail.com').one_or_none().id
        elif index <= 6 and index > 3:
            game.user_id = User.query.filter_by(email = 'amanda@gmail.com').one_or_none().id
        elif index <= 10 and index > 6:
            game.user_id = User.query.filter_by(email = 'alex@gmail.com').one_or_none().id




        db.session.add(game)
    try:
        db.session.commit()

        review = Review()
        review.rating = 8
        review.review = 'Good game!'
        review.user_id = 2
        review.game_id = 1
        db.session.add(review)

        review2 = Review()
        review2.rating = 7
        review2.review = 'Nice!'
        review2.user_id = 4
        review2.game_id = 2
        db.session.add(review2)

        review3 = Review()
        review3.rating = 3
        review3.review = 'Did not like it...'
        review3.user_id = 6
        review3.game_id = 3
        db.session.add(review3)
        
        review4 = Review()
        review4.rating = 1
        review4.review = 'Bad'
        review4.user_id = 7
        review4.game_id = 4
        db.session.add(review4)

        review5 = Review()
        review5.rating = 9
        review5.review = 'Really fun!'
        review5.user_id = 8
        review5.game_id = 5
        db.session.add(review5)
        
        review6 = Review()
        review6.rating = 8
        review6.review = 'Terrifying!'
        review6.user_id = 9
        review6.game_id = 6
        db.session.add(review6)

        review7 = Review()
        review7.rating = 5
        review7.review = 'I like it'
        review7.user_id = 1
        review7.game_id = 7
        db.session.add(review7)

        review8 = Review()
        review8.rating = 4
        review8.review = 'Not good'
        review8.user_id = 3
        review8.game_id = 8
        db.session.add(review8)

        review9 = Review()
        review9.rating = 10
        review9.review = 'Great game!'
        review9.user_id = 5
        review9.game_id = 9
        db.session.add(review9)

        review10 = Review()
        review10.rating = 7
        review10.review = 'Nice'
        review10.user_id = 4
        review10.game_id = 10
        db.session.add(review10)
        
        review11 = Review()
        review11.rating = 6
        review11.review = 'Good'
        review11.user_id = 9
        review11.game_id = 1
        db.session.add(review11)

        review12 = Review()
        review12.rating = 2
        review12.review = 'Unfun'
        review12.user_id = 8
        review12.game_id = 2
        db.session.add(review12)

        review13 = Review()
        review13.rating = 9
        review13.review = 'I love it'
        review13.user_id = 7
        review13.game_id = 3
        db.session.add(review13)

        review14 = Review()
        review14.rating = 3
        review14.review = 'Bad design'
        review14.user_id = 6
        review14.game_id = 4
        db.session.add(review14)

        review15 = Review()
        review15.rating = 8
        review15.review = 'Very creative!'
        review15.user_id = 5
        review15.game_id = 5
        db.session.add(review15)

        review16 = Review()
        review16.rating = 7
        review16.review = 'Really nice'
        review16.user_id = 4
        review16.game_id = 6
        db.session.add(review16)

        review17 = Review()
        review17.rating = 2
        review17.review = 'Really bad...'
        review17.user_id = 3
        review17.game_id = 7
        db.session.add(review17)

        review18 = Review()
        review18.rating = 10
        review18.review = 'One of the best games of last year'
        review18.user_id = 2
        review18.game_id = 8
        db.session.add(review18)
        
        review19 = Review()
        review19.rating = 6
        review19.review = 'Mid game'
        review19.user_id = 6
        review19.game_id = 9
        db.session.add(review19)

        review20 = Review()
        review20.rating = 9
        review20.review = 'So fun!'
        review20.user_id = 4
        review20.game_id = 10
        db.session.add(review20)

        db.session.commit()

        for i in range(1, 7):      
            like1 = Like()
            like1.user_id = i
            like1.game_id = 7
            like1.is_liked = True
            db.session.add(like1)
            db.session.commit()

        
        for i in range(1, 6):      
            like2 = Like()
            like2.user_id = i
            like2.game_id = 2
            like2.is_liked = True
            db.session.add(like2)

            db.session.commit()
        

        for i in range(1, 5):      
            like3 = Like()
            like3.user_id = i
            like3.game_id = 3
            like3.is_liked = True
            db.session.add(like3)

            db.session.commit()


        for i in range(1, 4):      
            like4 = Like()
            like4.user_id = i
            like4.game_id = 6
            like4.is_liked = True
            db.session.add(like4)

            db.session.commit()

        for i in range(1, 3):      
            like5 = Like()
            like5.user_id = i
            like5.game_id = 5
            like5.is_liked = True
            db.session.add(like5)

            db.session.commit()

        return jsonify({"message": "Populated succesfully"}), 201


    except Exception as error:
        return jsonify ("Error"), 400
