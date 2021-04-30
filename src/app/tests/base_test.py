"""
BaseTest
This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from run import APP
from db import DB


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    @classmethod
    def setUpClass(cls):
        """
        Runs once for each test case
        """
        APP.config["SQLALCHEMY_DATABASE_URI"] = BaseTest.SQLALCHEMY_DATABASE_URI
        APP.config["DEBUG"] = False
        with APP.app_context():
            DB.init_app(APP)

    def setUp(self):
        """
        Checks if database exists
        Runs for each test method
        """
        with APP.app_context():
            DB.create_all()
        self.APP = APP.test_client
        self.app_context = APP.app_context

    def tearDown(self):
        """
        Blanks database
        """
        with APP.app_context():
            DB.session.remove()
            DB.drop_all()