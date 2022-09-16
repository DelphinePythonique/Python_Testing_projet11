from flask import session

from tests.conftest import refresh_datafiles, EMAIL_OK


class TestUnitServerLogoutClass:
    def setup_method(self):
        refresh_datafiles()

    def test_logout_with_no_username_authenticated(self, client):
        response = client.get("/logout")
        assert response.status_code == 302


    def test_logout_with_username_authenticated(self, client):

            session["username"] = EMAIL_OK

            assert  'username' in session
            response = client.get("/logout")
            assert response.status_code == 302
            assert not 'username' in session


