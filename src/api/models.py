from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    salt = db.Column(db.String(255), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    modes = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    system_requirements = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    # media = db.Column(db.Text, nullable=True)  # Stores other media file paths
    rating = db.Column(db.String(10), nullable=True)
    players = db.Column(db.Integer, nullable=False)
    related_games = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(250), nullable=False)
    summary = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    trailer = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Game {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cover_image": self.cover_image,
            "genre": self.genre,
            "modes": self.modes.split(","),
            "release_date": self.release_date.strftime("%Y-%m-%d"),
            "system_requirements": self.system_requirements,
            "achievements": self.achievements,
            "rating": self.rating,
            "players": self.players,
            "related_games": self.related_games,
            "language": self.language,
            "summary": self.summary,
            "description": self.description,
            "trailer": self.trailer
        }