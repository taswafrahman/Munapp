
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db, DatabaseManager
from app.forms import *
from app.models import User,Topic,Comment,Group
from werkzeug.urls import url_parse

@app.before_request
def before_request():
    """functions to be run before each application request
    currently assigns user search bar form to g    
    """
    g.user = current_user
    if g.user.is_authenticated:
        g.profile_search = FindUserForm()

@app.route('/')
@app.route('/home')
def home():
    """loads the homepage"""
    ## Check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    ## Create a login and registration FlaskForm
    loginForm = LoginForm()
    regForm = RegistrationForm()
    ## Pass created forms into template
    return render_template('home.html', title="munapp", loginForm=loginForm, regForm=regForm)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """loads the register template/forms"""
    ## Check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    ## Create FlaskForm child object defined in forms.py
    form = RegistrationForm()
    ## Checks if request is POST request and validates form This also checks
    ## for duplicate usernames/emails and matching password fields
    if form.validate_on_submit():
        ## Create new user and add to database
        DatabaseManager.addUser(form.username.data, form.email.data, \
        form.password.data)
        return redirect(url_for('login'))
    ## If form isn't valid we send user back to registration page
    ## and display correct error messages
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs a user in"""
    ## Check if current user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    ## Create FlaskForm child object defined in forms.py
    form = LoginForm()
    if form.validate_on_submit():
        ## Check user submitted information with database via DatabaseManager
        ## and if correct log in user under account matching that information
        return DatabaseManager.login(form.username.data, form.password.data, \
        form.remember_me.data)
    ## If information does not match any accounts, return user to login page
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    """logs a user out"""
    return DatabaseManager.logout();

@app.route('/index', methods = ['GET','POST'])
@login_required
def index():
    """loads the index page"""
    users = DatabaseManager.getAllUsers()
    topics = DatabaseManager.getAllPublicTopics()
    comments = DatabaseManager.getAllComments()
    numNots =  DatabaseManager.countNotifications(current_user)
    form = FindUserForm()
    if form.validate_on_submit():
            user = DatabaseManager.getUserByUsername(form.username.data)
            if user is None:
                flash('No such user exists','error')
            else:
                return redirect(url_for('generalProfile',id=user.id))
    return render_template('index.html', title='Home', users=users, topics=topics, comments=comments, form=form, numNots=numNots)


@app.route('/create_topic/', methods = ['GET', 'POST'])
@app.route('/create_topic/<group_id>', methods = ['GET', 'POST'])
@login_required
def createTopic(group_id=None):
    """loads the create topic page"""
    form = TopicForm()
    if form.validate_on_submit():
        topic = DatabaseManager.addTopic(user_id=current_user.id,\
        title=form.title.data,body=form.body.data,group_id=group_id)
        flash('Topic created!','info')
        ## User will be automatically subscribed to a topic they themselves create.
        DatabaseManager.addSubscription(current_user.id, topic.id)
        return redirect(url_for('viewTopic',id=topic.id))
    return render_template('create_topic.html', title='Create New Topic', form=form)

@app.route('/post/<id>', methods = ['GET', 'POST'])
@login_required
def viewTopic(id):
    """Loads the form/page to view a post"""
    form = CommentForm()
    sub_btn = SubscriptionForm()
    unsub_btn = UnsubscriptionForm()
    topic = DatabaseManager.getTopic(id)
    DatabaseManager.removeNotification(current_user.id, id)
    if topic.group_id is not None:
        group = DatabaseManager.getGroup(topic.group_id)
        if DatabaseManager.checkMember(current_user,group):
            if form.validate_on_submit():
                DatabaseManager.addComment(user_id=current_user.id,topic_id=id,body=form.comment.data)
                DatabaseManager.notifyUsers(id)
                return redirect(url_for('viewTopic',id=id))
            if request.method == "POST" and request.form['btn'] == "sub":
                ## add topic to user subscriptions
                DatabaseManager.addSubscription(current_user.id, id)
                return redirect(url_for('viewTopic',id=id))
            elif request.method == "POST" and request.form['btn'] == "unsub":
                ## Remove the topic from user subscriptions
                DatabaseManager.removeSubscription(current_user.id, id)
                return redirect(url_for('viewTopic',id=id))
            if DatabaseManager.checkForSub(current_user.id, id):
                return render_template('post.html', title='View Topic',\
                topic=topic,form=form,btn=unsub_btn,val="unsub")
            else:
                return render_template('post.html', title='View Topic',\
                topic=topic,form=form,btn=sub_btn,val="sub")
        else:
            flash('You are not a member of the group this topic belongs to','error')
            return redirect(url_for('home'))
    else:
        if form.validate_on_submit():
            DatabaseManager.addComment(user_id=current_user.id,topic_id=id,body=form.comment.data)
            DatabaseManager.notifyUsers(id)
            return redirect(url_for('viewTopic',id=id))
        if request.method == "POST" and request.form['btn'] == "sub":
            ## add topic to user subscriptions
            DatabaseManager.addSubscription(current_user.id, id)
            return redirect(url_for('viewTopic',id=id))
        elif request.method == "POST" and request.form['btn'] == "unsub":
            ## Remove the topic from user subscriptions
            DatabaseManager.removeSubscription(current_user.id, id)
            return redirect(url_for('viewTopic',id=id))
        ## Check if user is subscribed to this topic. If true, show unsub button
        if DatabaseManager.checkForSub(current_user.id, id):
            return render_template('post.html', title='View Topic',\
            topic=topic,form=form,btn=unsub_btn,val="unsub")
        else:
            return render_template('post.html', title='View Topic',\
            topic=topic,form=form,btn=sub_btn,val="sub")

@app.route('/edit_comment/<id>', methods = ['GET', 'POST'])
@login_required
def editComment(id):
    """loads the form/page to edit a comment"""
    comment = DatabaseManager.getComment(id)
    form = CommentForm(comment=comment.body)
    if DatabaseManager.checkCommentAuthor(current_user,comment):
        if form.validate_on_submit():
            DatabaseManager.editComment(id=id,body=form.comment.data)
            return redirect(url_for('viewTopic',id=comment.topic_id))
        return render_template('edit_comment.html', title='Edit Comment',form=form,comment=comment)
    else:
        flash('You are not eligible to edit this comment','error')
        return redirect(url_for('home'))

@app.route('/edit_topic/<id>', methods = ['GET', 'POST'])
@login_required
def editTopic(id):
    """loads the form/page to edit a post"""
    form = TopicForm()
    topic = DatabaseManager.getTopic(id)
    if DatabaseManager.checkTopicAuthor(current_user,topic):
        if form.validate_on_submit():
            DatabaseManager.editTopic(id=id,title=form.title.data, body=form.body.data)
            return redirect(url_for('viewTopic',id=id))
        return render_template('edit_topic.html', title='Edit Topic',form=form,topic=topic)
    else:
        flash('You are not elgible to edit this topic','error')
        return redirect(url_for('home'))

@app.route('/create_group', methods = ['GET', 'POST'])
@login_required
def createGroup():
    """loads the form/page to create a group"""
    ## Allows current user to create a new group
    form = GroupForm()
    if form.validate_on_submit():
        group_id = DatabaseManager.addGroup(name=form.name.data)
        return redirect(url_for('viewGroup',id=group_id))
    return render_template('create_group.html',form=form)

@app.route('/group/<id>', methods = ['GET', 'POST'])
@login_required
def viewGroup(id):
    """loads the form/page to view a group"""
    group = DatabaseManager.getGroup(id)
    leaveGroup = LeaveGroupForm(prefix="leaveGroup")
    if DatabaseManager.checkMember(current_user,group):
        form = AddUserForm(prefix="form")
        if form.submit.data and form.validate_on_submit():
            user = DatabaseManager.getUserByUsername(form.username.data)
            if user is None:
                flash('No such user exists','error')
            else:
                DatabaseManager.addGroupMember(user=user,group=group)
                flash('You have successfully added a user to the group','info')
                return render_template('group.html', group=group, title=group.name,form=form,leaveGroup=leaveGroup)
        elif leaveGroup.submit.data and leaveGroup.validate_on_submit():
            DatabaseManager.leaveGroup(current_user,group)
            flash('You have left the group','info')
            return redirect(url_for('home'))
        return render_template('group.html', group=group, title=group.name,form=form,leaveGroup=leaveGroup)
    else:
        flash('You are not a member of the specified group','error')
        return redirect(url_for('home'))

@app.route('/my_profile', methods = ['GET', 'POST'])
@login_required
def myProfile():
    subs = DatabaseManager.getUserSubscriptions(current_user.id)
    notifications = DatabaseManager.getUserNotifications(current_user.id)
    return render_template('my_profile.html', title = 'My Profile', subs=subs, nots=notifications)

@app.route('/general_profile/<id>', methods = ['GET', 'POST'])
@login_required
def generalProfile(id):
    """loads the form/page to view any users profile"""
    user = DatabaseManager.getUser(id)
    if user is None:
        return render_template('500.html')
    return render_template('general_profile.html', user=user, title = 'User Profile')

@app.route('/search_user/', methods = ['GET', 'POST'])
def searchUser():
    """loads the functionality of the search bar for searching for users."""
    if g.profile_search.validate_on_submit():
        user = DatabaseManager.getUserByUsername(g.profile_search.username.data)
        if user is None:
            flash('No such user exists','error')
            return redirect(url_for('home'))
        else:
            return redirect(url_for('generalProfile',id=user.id))
    else:
        return redirect(url_for('home'))
