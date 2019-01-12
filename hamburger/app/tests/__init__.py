import os
import json
import shutil
import tempfile
import unittest

from pyramid import testing

from hamburger import main


class AppTestBase(unittest.TestCase):

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp()
        dbpath = os.path.join(self._tmpdir, 'test.db')
        uri = "file://" + dbpath
        settings = {
            'zodbconn.uri': uri,
            'pyramid.includes': ['pyramid_zodbconn', 'pyramid_tm'],
            'tutorial.secret': '98zd',
            'stripe.sk': 'sk_test_P413BkDG2R07lTOp5ERdyfli',
            'facebook.key': '361607684642526',
            'facebook.secret': '211bfd1b6b7140120a48a2bcafce4c05',
            'google.key': '227100062245-9mlhjnur45073ktn8apgu38geus4bhop.apps.googleusercontent.com',
            'google.secret': 'CVdnXvybSWRqshkCeb-6kPwC'
        }
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
