"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, bcrypt, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transactions."""

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="UNHASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

        # Check User attributes
        self.assertEqual(u.email, 'test@test.com')
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.password, 'UNHASHED_PASSWORD') # at this point password has not been hashed
        self.assertEqual(u.image_url, "/static/images/default-pic.png")
        self.assertEqual(u.header_image_url, "/static/images/warbler-hero.jpg")

    def test_signup(self):
        """Tests signup process"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )
        db.session.commit()

        self.assertEqual(u.username, "testuser")
        self.assertEqual(u.image_url, "/static/images/default-pic.png")
        self.assertNotEqual(u.password, "HASHED_PASSWORD")

    def test_authenticate(self):
        """Tests authentication"""
        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=None
        )
        db.session.commit()

        authenticated1 = User.authenticate(username="testuser", password="hash_it_up")
        self.assertEqual(authenticated1, False)

        authenticated2 = User.authenticate(username="testuser", password="HASHED_PASSWORD")
        self.assertNotEqual(authenticated2.password, "HASHED_PASSWORD")
        self.assertEqual(authenticated2.password, u.password)

    







