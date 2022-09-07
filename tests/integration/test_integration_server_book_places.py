from flask import get_flashed_messages

from tests.conftest import (
    COMPETITION_KO,
    COMPETITION_OK,
    CLUB_OK,
    CLUB_KO,
    refresh_datafiles,
    COMPETITION2_OK,
)


class TestIntegrationServerBookPlaceClass:
    def setup_method(self):
        refresh_datafiles()

    def test_book(self, client):

        response = client.get(f"/book/{COMPETITION2_OK}/{CLUB_OK}")

        assert response.status_code == 200

        assert f"{COMPETITION2_OK}" in response.data.decode("utf-8")
        assert b"Places available: 6" in response.data
        assert f'type="hidden" name="club" value="{CLUB_OK}"' in response.data.decode(
            "utf-8"
        )
        assert (
            f'type="hidden" name="competition" value="{COMPETITION2_OK}"'
            in response.data.decode("utf-8")
        )
        assert 'type="number" name="places"' in response.data.decode("utf-8")

        response = client.get(f"/book/{COMPETITION_KO}/{CLUB_OK}")

        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "competition not found" in flash_messages

        assert b"test1@project11.fr" in response.data
        assert b"Competitions:" in response.data
        assert b"competition test1" in response.data

        assert b"competition test2" in response.data

        response = client.get(f"/book/{COMPETITION_OK}/{CLUB_OK}")

        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "too late the competition is over" in flash_messages

        assert b"test1@project11.fr" in response.data
        assert b"Competitions:" in response.data
        assert b"competition test1" in response.data

        assert b"competition test2" in response.data

    def test_book_with_club_ko_and_competition_ok(self, client):
        response = client.get(f"/book/{COMPETITION_OK}/{CLUB_KO}")

        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "club not found" in flash_messages
        assert b"Page not found" in response.data

    def test_purchase_places_with_club_ko(self, client):
        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_KO, "competition": COMPETITION_OK, "places": 1},
        )
        assert response.status_code == 404

        flash_messages = get_flashed_messages()
        assert "club not found" in flash_messages
        assert b"Page not found" in response.data

    def test_purchase_places_with_competition_ko(self, client):
        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_OK, "competition": COMPETITION_KO, "places": 1},
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
        assert b"Date: 2050-10-22 13:30:00" in response.data

    def test_purchase_places_more_than_available(self, client):
        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_OK, "competition": COMPETITION_OK, "places": 7},
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "enter less places!" in flash_messages
        assert 'type="number" name="places"' in response.data.decode("utf-8")

    def test_purchase_places_more_than_points(self, client):
        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_OK, "competition": COMPETITION_OK, "places": 50},
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "enter less places!" in flash_messages
        assert 'type="number" name="places"' in response.data.decode("utf-8")

    def test_purchase_places_more_than_twelve_points(self, client):
        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_OK, "competition": COMPETITION2_OK, "places": 2},
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "Great-booking complete!" in flash_messages

        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_OK, "competition": COMPETITION2_OK, "places": 11},
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "enter less places!" in flash_messages

    def test_purchase_places_zero_place(self, client):
        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_OK, "competition": COMPETITION_OK, "places": 0},
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "booking must be superior to 0" in flash_messages
        assert 'type="number" name="places"' in response.data.decode("utf-8")

    def test_purchase_places(self, client):
        response = client.post(
            "/purchasePlaces",
            data={"club": CLUB_OK, "competition": COMPETITION2_OK, "places": 1},
        )
        assert response.status_code == 200
        flash_messages = get_flashed_messages()
        assert "Great-booking complete!" in flash_messages
        assert b"Summary | GUDLFT Registration" in response.data
        assert b"Points available: 10" in response.data
