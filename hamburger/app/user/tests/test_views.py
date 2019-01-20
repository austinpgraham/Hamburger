from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that

from hamburger.app.user.tests import UserAppTestBase


class TestUserViews(UserAppTestBase):

    def test_profile_upload(self):
        # Test that the profile pic is originally empty
        response = self.testapp.get("/users/pgreazy")
        assert_that(response.json['profile_pic'], is_(""))

        # Define fake file upload
        contents = "This is a test file".encode()
        response = self.testapp.post("/users/pgreazy/avatar", upload_files=[(
            'file',
            'filename.png',
            contents
        )])
        assert_that(response.status_code, is_(200))
        # Check the user now has a profile picture
        response = self.testapp.get("/users/pgreazy")
        assert_that(response.json['profile_pic'], is_not(""))
