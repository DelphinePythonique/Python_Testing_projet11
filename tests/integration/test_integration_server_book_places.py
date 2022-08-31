from flask import get_flashed_messages

from tests.conftest import COMPETITION_KO, COMPETITION_OK, CLUB_OK, CLUB_KO, DATABASE_DIRECTORY_FOR_TEST, \
    refresh_datafiles


class TestIntegrationServerBookPlaceClass:
    def setup_method(self):
        refresh_datafiles()

    def test_should_display_form_place_with_club_and_competition_ok(self, client):

        response = client.get(f"/book/{COMPETITION_OK}/{CLUB_OK}")

        assert response.status_code == 200

        assert f"{COMPETITION_OK}" in response.data.decode("utf-8")
        assert b"Places available: 6" in response.data
        assert f'type="hidden" name="club" value="{CLUB_OK}"' in response.data.decode(
            "utf-8"
        )
        assert (
            f'type="hidden" name="competition" value="{COMPETITION_OK}"'
            in response.data.decode("utf-8")
        )
        assert f'type="number" name="places"' in response.data.decode("utf-8")

    def test_should_display_form_place_with_club_ok_and_competition_ko(self, client):

        response = client.get(f"/book/{COMPETITION_KO}/{CLUB_OK}")

        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "competition not found" in flash_messages

        assert b"test1@project11.fr" in response.data
        assert b"Competitions:" in response.data
        assert b"competition test1" in response.data


        assert b"competition test2" in response.data


    def test_should_display_form_place_with_club_ko_and_competition_ok(self, client):
        response = client.get(f"/book/{COMPETITION_OK}/{CLUB_KO}")

        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "club not found" in flash_messages
        assert b"Page not found" in response.data

    def test_should_not_purchase_with_unknow_club(self, client):
        response = client.post(
            "/purchasePlaces", data={"club": CLUB_KO, "competition": COMPETITION_OK, "places": 1}
        )
        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "club not found" in flash_messages
        assert b"Page not found" in response.data

    def test_should_not_purchase_with_unknow_competition(self, client):
        response = client.post(
            "/purchasePlaces", data={"club": CLUB_OK, "competition": COMPETITION_KO, "places": 1}
        )
        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "competition not found" in flash_messages

        assert b"test1@project11.fr" in response.data
        assert b"Competitions:" in response.data
        assert b"competition test1" in response.data
        assert b"Date: 2020-03-27 10:00:00" in response.data
        assert b"Number of Places:" in response.data


        assert b"competition test1" in response.data
        assert b"Date: 2020-10-22 13:30:00" in response.data


    def test_should_not_purchase_more_than_available(self, client):
        response = client.post(
            "/purchasePlaces", data={"club": CLUB_OK, "competition": COMPETITION_OK, "places": 7}
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "enter less places!" in flash_messages
        assert f'type="number" name="places"' in response.data.decode("utf-8")

    def test_should_not_purchase_more_than_points(self, client):
        response = client.post(
            "/purchasePlaces", data={"club": CLUB_OK, "competition": COMPETITION_OK, "places": 50}
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "enter less places!" in flash_messages
        assert f'type="number" name="places"' in response.data.decode("utf-8")

    def test_should_purchase_ok(self, client):
        response = client.post(
            "/purchasePlaces", data={"club": CLUB_OK, "competition": COMPETITION_OK, "places": 1}
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "Great-booking complete!" in flash_messages
        assert b'Summary | GUDLFT Registration' in response.data
