from base import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    text = db.Column(db.String(140), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

class Follow(db.Model):
    __tablename__ = "follows"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    follower = db.relationship('User', backref=db.backref('followers', lazy=True), foreign_keys=[follower_id])
    followee = db.relationship('User', backref=db.backref('followees', lazy=True), foreign_keys=[followee_id])
