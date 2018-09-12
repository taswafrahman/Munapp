""" Test module uses python's unit testing framework unittest. Provides
a series of tests for each module used in the application.
"""

import sys
sys.path.append('../../')
import os
from flask_login import current_user, login_user, logout_user
from app import app, db, DatabaseManager
from app.models import User
from datetime import datetime, timedelta
from TestHelper import *
import unittest

class DatabaseManagerTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_table_empty(self):
        users = DatabaseManager.getAllUsers()
        self.assertEqual(len(users), 0, "User table is not empty.")

    def test_topic_table_empty(self):
        topics = DatabaseManager.getAllTopics()
        self.assertEqual(len(topics), 0, "Topic table is not empty.")

    def test_comment_table_empty(self):
        comments = DatabaseManager.getAllComments()
        self.assertEqual(len(comments), 0, "Comment table is not empty")

    def test_group_table_empty(self):
        groups = DatabaseManager.getAllGroups()
        self.assertEqual(len(groups), 0, "Group table is not empty.")

    def test_get_user_by_id(self):
        response = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you have successfully registered.', response.data)
        u = DatabaseManager.getUser(1)
        self.assertEqual(u.id, 1)
        self.assertEqual(u.username, 'Tester')
        self.assertEqual(u.email, 'tester@example.com')

    def test_get_user_by_username(self):
        response = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you have successfully registered.', response.data)
        u = DatabaseManager.getUserByUsername("Tester")
        self.assertEqual(u.id, 1)
        self.assertEqual(u.username, 'Tester')
        self.assertEqual(u.email, 'tester@example.com')

    def test_check_topic_author(self):
        response1 = register(self.app, 'Tester', 'tester@example.com',
            'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = register(self.app, 'Tester2', 'tester2@example.com',
            'password!', 'password!')
        self.assertEqual(response2.status_code, 200)
        response3 = login(self.app, 'Tester', 'password!')
        self.assertEqual(response3.status_code, 200)
        response4 = create_topic(self.app, 1, "the topic title", "the topic body")
        self.assertEqual(response4.status_code, 200)
        self.assertIn(b'Topic created!', response4.data)

        t = DatabaseManager.getTopic(1)
        u1 = DatabaseManager.getUserByUsername("Tester")
        u2 = DatabaseManager.getUserByUsername("Tester2")
        result1 = DatabaseManager.checkTopicAuthor(u1, t)
        result2 = DatabaseManager.checkTopicAuthor(u2, t)
        self.assertTrue(result1)
        self.assertFalse(result2)

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_host_status_code(self):
        code = self.app.get('/')
        self.assertEqual(code.status_code, 200)

    def test_home_status_code(self):
        code = self.app.get('/home')
        self.assertEqual(code.status_code, 200)

    def test_require_login_error(self):
        code = self.app.get('/index')
        self.assertEqual(code.status_code, 401, \
        "Error: Unauthorized user can access hidden page '/index'.")

    def test_create_topic(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = login(self.app, 'Tester', 'password!')
        self.assertEqual(response2.status_code, 200)
        response3 = create_topic(self.app, 1, "the topic title", "the topic body")
        self.assertEqual(response3.status_code, 200)
        self.assertIn(b'Topic created!', response3.data)

    def test_accessing_topic(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = login(self.app, 'Tester', 'password!')
        self.assertEqual(response2.status_code, 200)
        response3 = create_topic(self.app, 1, "the topic title", "the topic body")
        self.assertEqual(response3.status_code, 200)
        self.assertIn(b'Topic created!', response3.data)
        response4 = self.app.get('/post/1')
        self.assertEqual(response4.status_code, 200)

class FormTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_registration(self):
        response = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you have successfully registered.', response.data)
        u = DatabaseManager.getUser(1)
        self.assertEqual(u.username, "Tester")

    def test_short_password_registration(self):
        response = register(self.app, 'Tester', 'tester@example.com', 'short!', 'short!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be at least 8 characters long.', response.data)

    def test_weak_password_registration(self):
        response = register(self.app, 'Tester', 'tester@example.com', 'nospecialchar', 'nospecialchar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must contain atleast 1 special character!', response.data)

    def test_passwords_match_error_registration(self):
        response = register(self.app, 'Tester', 'tester@example.com', 'password1!', 'password2!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password.', response.data)

    def test_duplicate_username_registration(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = register(self.app, 'Tester', 'different_email@example.com', 'password!', 'password!')
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'Please use a different username.', response2.data)

    def test_duplicate_email_registration(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = register(self.app, 'different', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'Please use a different email address.', response2.data)

    def test_valid_login_form(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = login(self.app, 'Tester', 'password!')
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'Welcome to MUNAPP, Tester', response2.data)

    def test_invalid_pass_login(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = login(self.app, 'Tester', 'incorrect_password')
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'Invalid username or password', response2.data)

    def test_create_topic(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = login(self.app, 'Tester', 'password!')
        self.assertEqual(response2.status_code, 200)
        response3 = create_topic(self.app, 1, "the topic title", "the topic body")
        self.assertEqual(response3.status_code, 200)
        self.assertIn(b'Topic created!', response3.data)

    def test_empty_field_create_topic(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = login(self.app, 'Tester', 'password!')
        self.assertEqual(response2.status_code, 200)
        response3 = create_topic(self.app, 1, "", "")
        self.assertEqual(response3.status_code, 200)
        self.assertNotIn(b'Topic created!', response3.data,
        "Topic was created with an empty title or body field.")

class ErrorsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_custom_error_401_displayed(self):
        response = self.app.get('/index')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized', response.data)

    def test_custom_error_404_displayed(self):
        response = self.app.get('/windex')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"This page isn't available", response.data)

    def test_custom_error_500_displayed(self):
        response1 = register(self.app, 'Tester', 'tester@example.com', 'password!', 'password!')
        self.assertEqual(response1.status_code, 200)
        response2 = login(self.app, 'Tester', 'password!')
        self.assertEqual(response2.status_code, 200)
        response3 = self.app.get('/general_profile/30')
        self.assertIn(b"An unexpected error has occured", response3.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
