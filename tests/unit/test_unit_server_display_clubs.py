from tests.conftest import refresh_datafiles


class TestUnitServerDisplayClubClass:
    def setup_method(self):
        refresh_datafiles()

    def test_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Welcome to the GUDLFT Registration Portal!" in response.data
        assert b'<label for="email">Email:</label>' in response.data
        assert b'<input type="email" name="email" id=""/>' in response.data
        assert b'<button type="submit">Enter</button>' in response.data
