from flask import Flask
from flask_testing import TestCase
from app import app_blueprint
from db import db, User, CreatedDocument
from unittest.mock import patch
import unittest
import json


def mock_google_create(a, b, c):
    return "87654321"


def mock_google_share(a, b, c, d):
    return True


class DBTests(TestCase):

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app.register_blueprint(app_blueprint)
        return self.app

    def setUp(self):
        self.client = self.app.test_client()
        with self.app.app_context():
            db.init_app(self.app)
            db.create_all()
            self.populate()

    def tearDown(self):
        self.app = Flask(__name__)
        with self.app.app_context():
            db.init_app(self.app)
            db.drop_all()

    def populate(self):
        user1 = User(
            id='1',
            forename='Conor',
            surname='Hanlon',
            email='conorbh97@gmail.com',
            image_url='http://mock.url',
            access_token='MockToken1'
        )
        user2 = User(
            id='2',
            forename='John',
            surname='Smith',
            email='johnsmith@gmail.com',
            image_url='http://mock2.url',
            access_token='MockToken2'
        )
        doc1 = CreatedDocument(
            id='25',
            uid='1',
            title='Test Doc 1'
        )
        doc2 = CreatedDocument(
            id='26',
            uid='1',
            title='Test Doc 2'
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(doc1)
        db.session.add(doc2)
        db.session.commit()

    def test_create_new_user(self):
        data = {
            'id': '3',
            'forename': 'Tony',
            'surname': 'Stark',
            'email': 'stark@gmail.com',
            'imageUrl': 'http://mock3.url',
            'accessToken': 'MockToken3'
        }
        response = self.client.post('/create_user', data=data).data
        response_data = json.loads(response)
        assert response_data['val'] == 'New user created.'

    def test_user_exists(self):
        data = {
            'id': '2',
            'forename': 'John',
            'surname': 'Smith',
            'email': 'johnsmith@gmail.com',
            'imageUrl': 'http://mock2.url',
            'accessToken': 'MockToken2'
        }
        response = self.client.post('/create_user', data=data).data
        response_data = json.loads(response)
        assert response_data['val'] == 'Access token up to date.'

    def test_update_access_token(self):
        data = {
            'id': '2',
            'forename': 'John',
            'surname': 'Smith',
            'email': 'johnsmith@gmail.com',
            'imageUrl': 'http://mock2.url',
            'accessToken': 'MockToken22'
        }
        response = self.client.post('/create_user', data=data).data
        response_data = json.loads(response)
        assert response_data['val'] == 'Access token updated.'

    @patch('app.share_doc', side_effect=mock_google_share)
    def test_share_document(self, mock_share):
        data = {
            'id': 26,
            'uid': 1,
            'emails[0]': 'david.weir3@mail.dcu.ie',
            'permission': 'reader'
        }
        response = self.client.post('/share_document', data=data).data
        response_data = json.loads(response)
        assert response_data['val'] == 'Document shared successfully.'

    @patch('app.create_doc', side_effect=mock_google_create)
    def test_create(self, mock_create):
        data = {
            'filename': 'TestFile5',
            'content': 'A document for my integration tests.',
            'accessToken': 'MockToken1'
        }
        response = self.client.post('/create', data=data).data
        print(response)
        response_data = json.loads(response)
        assert response_data['val'] == 'Google Doc Created'

    @patch('app.create_doc', side_effect=mock_google_create)
    def test_create_expired(self, mock_create):
        data = {
            'filename': 'Test File 11',
            'content': 'A document for my integration tests.',
            'accessToken': 'FakeToken1111111'
        }
        response = self.client.post('/create', data=data).data
        print(response)
        response_data = json.loads(response)
        assert response_data['val'] == 'Access token expired.'


if __name__ == "__main__":
    unittest.main()
