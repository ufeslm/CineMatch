from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    favorite_movies = db.relationship('FavoriteMovie', backref='user', lazy=True)
    watch_later_movies = db.relationship('WatchLater', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FavoriteMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<FavoriteMovie {self.title}>'

class WatchLater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    added_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<WatchLater {self.title}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 