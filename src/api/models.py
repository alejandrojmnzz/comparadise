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
    genre = db.Column(db.String(100), nullable=False)
    modes = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    system_requirements = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    media = db.Column(db.Text, nullable=True)  # Stores other media file paths
    cover_media = db.Column(db.String(255), nullable=True)  # Stores the cover media file path
    rating = db.Column(db.String(10), nullable=True)
    players = db.Column(db.Integer, nullable=False)
    related_games = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Game {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "genre": self.genre,
            "modes": self.modes,
            "release_date": self.release_date.strftime("%Y-%m-%d") if self.release_date else None,
            "system_requirements": self.system_requirements,
            "achievements": self.achievements,
            "media": self.media,
            "cover_media": self.cover_media,  # Include the cover media in serialized output
            "rating": self.rating,
            "players": self.players,
            "related_games": self.related_games,
            "language": self.language,
        }