

from tests.conftest import refresh_datafiles


class TestIntegrationServerBookPlaceClass:
    def setup_method(self):
        refresh_datafiles()

    def test_display_club(self, client):
        response = client.get(f"/display_clubs")
        assert  response.status_code == 302

        with client.session_transaction() as session:
            session['username'] = 'fakeemail'
        response = client.get(f"/display_clubs")
        assert b"Clubs" in response.data
        assert b"available points" in response.data
        assert b"competitions" in response.data
        assert b"competition test2:" in response.data
        assert b"competition test1:" in response.data
        assert b"test1" in response.data
        assert b"13" in response.data