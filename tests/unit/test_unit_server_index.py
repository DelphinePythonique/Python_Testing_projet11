from tests.conftest import refresh_datafiles, EMAIL_OK


class TestUnitServerIndexClass:
    def setup_method(self):
        refresh_datafiles()

    def test_index_with_no_username_authenticated(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Welcome to the GUDLFT Registration Portal!" in response.data
        assert b'<label for="email">Email:</label>' in response.data
        assert b'<input type="email" name="email" id=""/>' in response.data
        assert b'<button type="submit">Enter</button>' in response.data

    def test_index_with_username_authenticated(self, client):
        with client.session_transaction() as session:
            session["username"] = EMAIL_OK
        response = client.get("/")
        assert response.status_code == 200
        assert b"Welcome test1@project11.fr!" in response.data



