""" TestHelper module provides functionality for testing the application,
making dealing with the app context easier.
"""

__all__ = ["register", "login", "logout", "create_topic"]

def register(app, username, email, password, password2):
    """Mimics POST request on WTF registration form using the
    flask test_client
    args:
        app: flask test client object
        username: string
        email: string
        password: string
        password2: string
    """
    return app.post('/register', data=dict(username=username, email=email,
     password=password, password2=password2),follow_redirects=True)

def login(app, username, password):
    """Mimics POST request on WTF login form using flask test_client
    args:
        app: flask test client object
        username: string
        password: string
    """
    return app.post('/login', data=dict(username=username,
    password=password, remember_me=False),follow_redirects=True)

def logout(app):
    """Mimics GET request on /logout route changing test_client from
    authorized user to anonymous user.
    args:
        app: flask test client object
    """
    return app.get('/logout', follow_redirects=True)

def create_topic(app, user_id, title, body, group_id=None):
    """Mimics POST request using WTF TopicForm on /create_topic route.
    args:
        app: flask test client object
        user_id: int
        title: string
        body: string
    """
    return app.post('/create_topic/', data=dict(user_id=user_id,
    title=title, body=body),follow_redirects=True)
