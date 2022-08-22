import os

from flask import get_flashed_messages
from jsonschema import validate


from server import loadCompetitions, extract_first_club_with_name, extract_first_competition_with_name
from tests.conftest import COMPETITION_OK, CLUB_OK, COMPETITION_KO, CLUB_KO


class TestServerBookPointClass:
    def test_should_load_competitions(self, competitions_schema_fixture):
        assert os.path.exists("competitions.json")
        competitions = loadCompetitions()

        assert (
            validate(instance=competitions, schema=competitions_schema_fixture) is None
        )

    def test_should_extract_first_club_with_name_ok(self, clubs_fixture):
        assert extract_first_club_with_name(clubs_fixture, CLUB_OK)['name'] == CLUB_OK


    def test_should_extract_first_club_with_name_ko(self, clubs_fixture):
        assert not extract_first_club_with_name(clubs_fixture, CLUB_KO)


    def test_should_extract_first_competition_with_name_ok(self, competitions_fixture):
        assert extract_first_competition_with_name(competitions_fixture, COMPETITION_OK)['name'] == COMPETITION_OK


    def test_should_extract_first_competition_with_name_ko(self, competitions_fixture):
        assert not extract_first_competition_with_name(competitions_fixture, COMPETITION_KO)


    def test_should_book_club_and_competition_ok(
        self, client, mocker, clubs_fixture, competitions_fixture
    ):
        mocker.patch("server.loadClubs", return_value=clubs_fixture)
        mocker.patch("server.loadCompetitions", return_value=competitions_fixture)
        response = client.get(f"/book/{COMPETITION_OK}/{CLUB_OK}")
        assert response.status_code == 200

    def test_should_book_club_ok_and_competition_ko(
        self, client, mocker, clubs_fixture, competitions_fixture
    ):
        mocker.patch("server.loadClubs", return_value=clubs_fixture)
        mocker.patch("server.loadCompetitions", return_value=competitions_fixture)
        client.get(f"/book/{COMPETITION_KO}/{CLUB_OK}")
        flash_messages = get_flashed_messages()
        assert "competition not found" in flash_messages

    def test_should_book_club_ko_and_competition_ok(
        self, client, mocker, clubs_fixture, competitions_fixture
    ):
        mocker.patch("server.loadClubs", return_value=clubs_fixture)
        mocker.patch("server.loadCompetitions", return_value=competitions_fixture)
        response = client.get(f"/book/{COMPETITION_OK}/{CLUB_KO}")
        assert response.status_code == 404
        flash_messages = get_flashed_messages()
        assert "club not found" in flash_messages
