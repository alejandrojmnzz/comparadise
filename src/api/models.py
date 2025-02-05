from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    salt = db.Column(db.String(255), unique=False, nullable=False)

    games = db.relationship('Game', back_populates='user')
    cart = db.relationship('Cart', back_populates='user', cascade='all, delete-orphan')
    purchases = db.relationship("Purchase", back_populates="user", cascade="all, delete-orphan")
    review = db.relationship('Review', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(255), nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    genres = db.Column(db.Text, nullable=False)
    modes = db.Column(db.Text, nullable=False)
    player_perspective = db.Column(db.Text, nullable=False)
    themes = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    system_requirements = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    additional_images = db.Column(db.Text, nullable=True)
    rating = db.Column(db.String(10), nullable=True)
    players = db.Column(db.Integer, nullable=False)
    related_games = db.Column(db.Text, nullable=True)
    auto_related_games = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(250), nullable=False)
    summary = db.Column(db.String(150), nullable=True)
    description = db.Column(db.Text, nullable=True)
    trailer = db.Column(db.String(255), nullable=True)
    rate = db.Column(db.Integer, nullable=True)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"))

    user = db.relationship('User', back_populates='games')
    cart = db.relationship("Cart", back_populates="game")
    review = db.relationship('Review', back_populates='games')


    def __repr__(self):
        return f"<Game {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "cover_image": self.cover_image,
            "genres": self.genres,
            "modes": self.modes,
            "player_perspective": self.player_perspective,
            "themes": self.themes,
            "keywords": self.keywords,
            "release_date": self.release_date.strftime("%Y-%m-%d"),
            "system_requirements": self.system_requirements,
            "achievements": self.achievements,
            "additional_images": json.loads(self.additional_images) if self.additional_images else [],
            "rating": self.rating,
            "review_id": self.review_id,
            "players": self.players,
            "related_games": self.related_games,
            "auto_related_games": json.loads(self.auto_related_games) if self.auto_related_games else [],
            "language": self.language,
            "summary": self.summary,
            "description": self.description,
            "trailer": self.trailer
        }

class Cart(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    
    user = db.relationship("User", back_populates="cart")
    game = db.relationship("Game", back_populates="cart")
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "game": self.game.serialize(),
        }

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    purchase_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="purchases")
    game = db.relationship("Game", backref="purchased_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "purchase_date": self.purchase_date.strftime("%Y-%m-%d"),
            "game": Game.query.get(self.game_id).serialize()
        }
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.String(255), nullable=False)

    user = db.relationship('User', back_populates='review')
    games = db.relationship('Game', back_populates='review')
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "rating": self.rating,
            "review": self.review
        }