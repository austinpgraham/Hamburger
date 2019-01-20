import os
import json
import shutil
import tempfile
import unittest

from pyramid import testing

from pyramid.compat import configparser

from hamburger import main


# Path to testing.ini
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "conf")


class AppTestBase(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        dbpath = os.path.join(self._tmpdir, 'test.db')
        uri = "file://" + dbpath
        config = configparser.ConfigParser()
        config.read(os.path.join(CONFIG_PATH, "testing.ini"))
        settings = dict(config['app:main'])
        settings['zodbconn.uri'] = uri
        settings['profile.store'] = self._tmpdir
        app = main({}, **settings)
        self.db = app.registry._zodb_databases['']
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        self.db.close()
        shutil.rmtree(self._tmpdir)

    def _create_user(self, **kwargs):
        resp = self.testapp.post('/users', params=json.dumps(kwargs))
        assert resp.status_code == 201

    def setup_autheduser(self, **kwargs):
        self._create_user(**kwargs)
        username = kwargs['username']
        route = "/users/{}/login".format(username)
        resp = self.testapp.post(route, params=json.dumps(kwargs))
        assert resp.status_code == 200

    def setup_nonauthed(self, **kwargs):
        self._create_user(**kwargs)
