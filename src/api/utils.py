from flask import jsonify, url_for
import os
import requests


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return """
        <div style="text-align: center;">
        <img style="max-height: 80px" src='https://storage.googleapis.com/breathecode/boilerplates/rigo-baby.jpeg' />
        <h1>Rigo welcomes you to your API!!</h1>
        <p>API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p>Start working on your project by following the <a href="https://start.4geeksacademy.com/starters/full-stack" target="_blank">Quick Start</a></p>
        <p>Remember to specify a real endpoint path like: </p>
        <ul style="text-align: left;">"""+links_html+"</ul></div>"

def compare_game_and_api(body):

    url = "https://api.igdb.com/v4/multiquery"
    headers = {
        'Accept': 'application/json',
        'Client-ID': os.getenv("CLIENT_ID"),
        'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN")}',
        'Content-Type': 'text/plain'
        }
    body_genres = body["genres"].split(',')
    genres_joined = ""
    for item in body_genres:
        lastIndex = body_genres[len(body_genres) - 1]
        if lastIndex == item:
            genres_joined = genres_joined + f'"{item}"'
        else:
            genres_joined = genres_joined + f'"{item}",' 

    body_modes = body["modes"].split(',')
    modes_joined = ""
    for item in body_modes:
        lastIndex = body_modes[len(body_modes) - 1]
        if lastIndex == item:
            modes_joined = modes_joined + f'"{item}"'
        else:
            modes_joined = modes_joined + f'"{item}",'
    body_themes = body["themes"].split(',')
    themes_joined = ""
    for item in body_themes:
        lastIndex = body_themes[len(body_themes) - 1]
        if lastIndex == item:
            themes_joined = themes_joined + f'"{item}"'
        else:
            themes_joined = themes_joined + f'"{item}",'

    body_perspectives = body["player_perspective"].split(',')
    perspectives_joined = ""
    for item in body_perspectives:
        lastIndex = body_perspectives[len(body_perspectives) - 1]
        if lastIndex == item:
            perspectives_joined = perspectives_joined + f'"{item}"'
        else:
            perspectives_joined = perspectives_joined + f'"{item}",'
    data = f'''query games "Multiquery" {{
	fields name,genres.name, themes.name, game_modes.name, player_perspectives.name;
    where genres.name = ({genres_joined});
    where player_perspectives.name = ({perspectives_joined});
    where game_modes.name = ({modes_joined});
    where themes.name = ({themes_joined});
    limit 500;
    }};'''
    response = requests.post(url, headers=headers, data=data)
    response = response.json()
    # myArray = ["Aventura", "Disparos"]
    # print((list(map(lambda item: item, body["genres"].split(",")))))

    filtered_genres = []
    filtered_modes = []
    filtered_perspectives = []
    filtered_themes = []
    total_coincidences = {}

    for game in response[0]["result"]:
        if game.get("genres"):
            for genre in game["genres"]:
                for index in body_genres:
                    if index == genre["name"]:
                        if total_coincidences.get(f'{str(game["id"])}_total'):
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": total_coincidences[f'{str(game["id"])}_total']["total"] + 1,
                                "id": game["id"]
                            }         
                        else:
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": 1,
                                "id": game["id"]
                            }
                    
                        repeated_id = filter(lambda item: item["id"] == game["id"], filtered_genres)
                        repeated_id_length = len(list(repeated_id))
                        if repeated_id_length == 0:
                            filtered_genres.append(game)

    for game in response[0]["result"]:
        if game.get("game_modes"):
            for mode in game["game_modes"]:
                for index in body_modes:
                    if index == mode["name"]:
                        if total_coincidences.get(f'{str(game["id"])}_total'):
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": total_coincidences[f'{str(game["id"])}_total']["total"] + 1,
                                "id": game["id"]
                            }         
                        else:
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": 1,
                                "id": game["id"]
                            }
                    
                        repeated_id = filter(lambda item: item["id"] == game["id"], filtered_modes)
                        repeated_id_length = len(list(repeated_id))
                        if repeated_id_length == 0:
                            filtered_modes.append(game)
    
    for game in response[0]["result"]:
        if game.get("themes"):
            for theme in game["themes"]:
                for index in body_themes:
                    if index == theme["name"]:
                        if total_coincidences.get(f'{str(game["id"])}_total'):
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": total_coincidences[f'{str(game["id"])}_total']["total"] + 1,
                                "id": game["id"]
                            }         
                        else:
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": 1,
                                "id": game["id"]
                            }
                        
                            repeated_id = filter(lambda item: item["id"] == game["id"], filtered_themes)
                            repeated_id_length = len(list(repeated_id))
                            if repeated_id_length == 0:
                                filtered_themes.append(game)
    
    for game in response[0]["result"]:
        if game.get("player_perspectives"):
            for perspective in game["player_perspectives"]:
                for index in body_perspectives:
                    if index == perspective["name"]:
                        if total_coincidences.get(f'{str(game["id"])}_total'):
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": total_coincidences[f'{str(game["id"])}_total']["total"] + 1,
                                "id": game["id"]
                            }         
                        else:
                            total_coincidences[f'{str(game["id"])}_total'] = {
                                "total": 1,
                                "id": game["id"]
                            }
                    
                        repeated_id = filter(lambda item: item["id"] == game["id"], filtered_perspectives)
                        repeated_id_length = len(list(repeated_id))
                        if repeated_id_length == 0:
                            filtered_perspectives.append(game)
    total_coincidences_array = [] 

    for id in total_coincidences:
        total_coincidences_array.append({id: total_coincidences.get(id)})

    sorted_data = sorted(total_coincidences_array, key=lambda x: list(x.values())[0]['total'], reverse=True)

    return [list(sorted_data[0].values())[0]["id"], list(sorted_data[1].values())[0]["id"], list(sorted_data[2].values())[0]["id"]]