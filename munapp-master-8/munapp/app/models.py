from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    """load the user"""
    return User.query.get(int(id))

group_identifier = db.Table('group_identifier',
    db.Column('group_id',db.Integer, db.ForeignKey('group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

subscription_identifier = db.Table('subscription_identifier',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

notification_identifier = db.Table('notification_identifier',
    db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    """The table for store the information about the users. Also holds the methods to set and check password"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    comment = db.relationship('Comment', backref='author', lazy='dynamic')
    topic = db.relationship('Topic', backref='author', lazy='dynamic')
    groups = db.relationship('Group', secondary=group_identifier, back_populates='members')
    notifications = db.relationship('Topic', secondary=notification_identifier, backref='e', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Topic(db.Model):
    """The table for storing the information about each topic"""
    __tablename__ = "topic"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(64))
    body = db.Column(db.String(512))
    time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
    timestamp =  db.Column(db.String(100),default  = time)
    public = True
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    subscribers = db.relationship('User', secondary=subscription_identifier, backref='subscriptions', lazy='dynamic')
    comments = db.relationship('Comment', backref='topic', lazy='dynamic')

    def __repr__(self):
        return '<Topic {}>'.format(self.title)

class Comment(db.Model):
    """The table for storing the information about each comment within each topic thread"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    body = db.Column(db.String(512))
    time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
    timestamp =  db.Column(db.String(100),default  = time)

    def __repr__(self):
        return '<Comment {}>'.format(self.topic_id)

class Group(db.Model):
    """The table for storing the information about the groups a user can be in"""
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    members = db.relationship('User',secondary=group_identifier)
    time = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
    timestamp =  db.Column(db.String(100),default  = time)
    topics = db.relationship('Topic', backref='group', lazy='dynamic')
