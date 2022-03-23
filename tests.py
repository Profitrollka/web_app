import unittest
from datetime import datetime, timedelta
from app import app, db
from app.models import User, Post, Tag, Comment

class TestUserModel(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        db.create_all()


    def test_password_hashing(self):
        u = User(nickname='katya', first_name='Katya', last_name='Volkova' )
        u.set_password('room')
        self.assertFalse(u.check_password('house'))
        self.assertTrue(u.check_password('room'))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main(verbosity=2)


