
""" DatabaseManager is a wrapper around sqlalchemy that acts as an interface
between the application and the database. It provides all the functionality
used to access data from the database.
"""

from flask import flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import app, db
from app.models import User, Topic, Comment, Group, group_identifier

def removeNotification(user_id, topic_id):
    """Finds user with id=user_id and removes topic with id=topic_id from
    that users notificaions list.
    args:
        user_id: int
        topic_id: int
    """
    user = User.query.get(user_id)
    topic = Topic.query.get(topic_id)
    if topic in user.notifications:
        user.notifications.remove(topic)
        db.session.commit()

def notifyUsers(topic_id):
    """Finds topic with id=topic_id from database and adds a notification
    to all users who are subscribed to that topic.
    args:
        topic_id: int
    """
    users = getAllSubscribers(topic_id)
    topic = Topic.query.get(topic_id)
    for u in users:
        if topic in u.notifications:
            u.notifications.remove(topic)
            db.session.commit()
        u.notifications.append(topic)
        db.session.commit()

def getAllSubscribers(topic_id):
    """Get topic with id=topic_id from database and returns a list of
    Users that subsribe to that topic as a list.
    args:
        topic_id: int
    """
    topic = Topic.query.get(topic_id)
    return topic.subscribers

def getUserNotifications(user_id):
    """Get user with id=user_id from database and returns all that users
    notifications as a list.
    args:
        user_id: int
    """
    user = User.query.get(user_id)
    return user.notifications

def getAllUsers():
    """Get all users in table and return them"""
    return User.query.all()

def getAllPosts():
    """Get all posts in a table and return them"""
    return Post.query.all()

def getAllComments():
    """Get all comments and return them"""
    return Comment.query.all()

def getAllGroups():
    """Get all groups from db and return them"""
    return Group.query.all()

def addUser(name, email, password):
    """Create new user object and returns that user, The form information has already been
    checked and validated by FlaskForm so there is no need to check again"""
    user = User(username=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you have successfully registered.','info')
    return user

def login(name, pw, remember_me):
    """ Log a user into the website and load the index page
    args:
        name: string
        pw: string
        remember_me: boolean
    """
    ## Get users and sort by username
    user = User.query.filter_by(username=name).first()
    ## Check if username is in database or if passwords match one in database
    if user is None or not user.check_password(pw):
        ## Redirect user to the login page with error message displayed
        flash('Invalid username or password','error')
        return redirect(url_for('login'))
    ## User information is correct, user flask_login to login user
    login_user(user, remember=remember_me)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return redirect(next_page)

def logout():
    """Log a user out of the website"""
    logout_user()
    return redirect(url_for('home'))

def addTopic(user_id, title, body, group_id, public=True):
    """ Add a topic to the database and commit the changes.
    Returns the topic.
    args:
        user_id: int
        title: string
        body: string
        group_id: int
        public: boolean
    """
    ## Initialize topic attributes
    topic = Topic(user_id=user_id,title=title,body=body,public=public,group_id=group_id)
    ## add new topic to the database and commit the change
    db.session.add(topic)
    db.session.commit()
    return topic

def addComment(user_id, topic_id, body):
    """Add a comment to the database and commit the change.
    args:
        user_id: int
        topic_id: int
        body: string
    """
    ## Initialize comment attributes
    comment = Comment()
    comment.user_id = user_id
    comment.topic_id = topic_id
    comment.body = body
    ## add new comment to the database and commit the change
    db.session.add(comment)
    db.session.commit()
    ## Display a message to make sure this works
    flash('Comment created!','info')

def getAllTopics():
    """Get all posts from the database"""
    topics = Topic.query.all()
    return topics

def getTopicComments(tid):
    """Get all comments on with topic_id = tid"""
    comments = Comment.query.filter_by(topic_id=tid)
    return comments

def getTopic(id):
	"""Get specific topic from database.
    args:
        id: int
    """
	topic = Topic.query.get(id)
	return topic

def getComment(id):
	""" Get specific comment from database.
    args:
        id: int
    """
	comment = Comment.query.get(id)
	return comment

def editComment(id, body):
    """Edit specific comment and commit to database
    args:
        id: int
        body: string
    """
    comment = getComment(id)
    comment.body = body
    db.session.commit()

def editTopic(id, title, body):
    """Edit specific topic and commit to database.
    args:
        id: int
        title: string
        body: strings
    """
    topic= getTopic(id)
    topic.title = title
    topic.body = body
    db.session.commit()

def getGroup(id):
	"""Get specific group from database.
    args:
        id: int
    """
	group = Group.query.get(id)
	return group

def addGroup(name):
    """Add group to database.
    args:
        name: string
    """
    group = Group()
    group.name = name
    group.members.append(current_user)
    db.session.add(group)
    db.session.commit()
    return group.id

def addGroupMember(user,group):
    """Add member to specified group.
    args:
        user: string
        group: Group object
    """
    group.members.append(user)
    db.session.commit()

def getUser(id):
    """Get specific user by user ID.
    args:
        id: int
    """
    user = User.query.get(id)
    return user

def getUserByUsername(username):
    """Searches the database for a given username.
    args:
        username: string
    """
    user = User.query.filter_by(username=username).first()
    return user

def checkMember(user,group):
    """Check if a user is a member of a group.
    args:
        user: id
        group: Group object
    """
    if user in group.members:
        return True
    else:
        return False

def getAllPublicTopics():
    """Returns all topics that have None as their group id (ie. all public topics)"""
    topics = Topic.query.filter_by(group_id=None)
    return topics

def checkTopicAuthor(user,topic):
    """Check if the current user is the author of a topic - used for when
    editing a topic.
    args:
        user: User object
        topic: Topic object
    """
    if user.id is topic.author.id:
        return True
    else:
        return False

def checkCommentAuthor(user,comment):
    """Check if the user is the author of a comment - used for when
    editing a comment.
    args:
        user: User object
        comment: Comment object
    """
    if user.id is comment.author.id:
        return True
    else:
        return False

def checkForSub(user_id, topic_id):
    """Check if user is subscribed to specific topic.
    args:
        user_id: int
        topic_id: int
    """
    user = User.query.filter_by(id=user_id).first()
    topic = Topic.query.filter_by(id=topic_id).first()
    if topic in user.subscriptions:
        return True
    return False

def addSubscription(user_id, topic_id):
    """Add new topic to user subscriptions.
    args:
        user_id: int
        topic_id: int
    """
    user = User.query.get(user_id)
    topic = Topic.query.get(topic_id)
    user.subscriptions.append(topic)
    db.session.commit()

def removeSubscription(user_id, topic_id):
    """Remove topic with id = topic_id from user subscriptions.
    args:
        user_id: int
        topic_id: int
    """
    user = User.query.get(user_id)
    topic = Topic.query.get(topic_id)
    if topic in user.subscriptions:
        user.subscriptions.remove(topic)
        db.session.commit()

def getUserSubscriptions(user_id):
    """Get a specific users subscriptions.
    args:
        user_id: int
    """
    user = User.query.get(user_id)
    return user.subscriptions

def leaveGroup(user,group):
    """Removes specified user from the specified group.
    args:
        user: User object
        group: Group object
    """
    group.members.remove(user)
    db.session.commit()

def countNotifications(user):
    """Count the number of notifications a user has.
	args:
		user: User object
    """
    counter = 0
    for n in user.notifications:
        counter += 1
    return str(counter)
