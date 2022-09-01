import json
import os.path

from jsonschema.validators import validate

from tests.conftest import (
    TableNameMocker,
    DataManagerMocker,
    DATABASE_DIRECTORY_FOR_TEST,
    CLUBS_TABLE,
    EMAIL_KO,
    EMAIL_OK,
    refresh_datafiles,
    BOOKINGS_TABLE,
    clubs_fixture
)
from utils import DataManager, Table, ClubCompetition


class TestDatamanagerClass:
    def test_init(self, app_test, mocker):
        mocker.patch("utils.DataManager.TableName", TableNameMocker)
        data_manager = DataManager(app_test)
        assert len(data_manager.tables) == 3
        assert isinstance(data_manager.tables[TableNameMocker.CLUBS], Table)
        assert data_manager.tables[TableNameMocker.CLUBS].name == "clubs"
        assert data_manager.app.config["DB_PATH"] == app_test.config["DB_PATH"]


class TestTableClass:
    @staticmethod
    def setup_method(self):
        refresh_datafiles()

    def test_init(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUBS_TABLE)
        assert table.name == CLUBS_TABLE
        assert table.app == data_manager_mocker.app

    def test__database_file_not_exist(self):
        data_manager_mocker = DataManagerMocker()
        database_file_path = f"{DATABASE_DIRECTORY_FOR_TEST}{CLUBS_TABLE}.json"
        os.remove(database_file_path)

        table = Table(data_manager_mocker, CLUBS_TABLE)
        assert (
            table._database_file_path
            == f"{DATABASE_DIRECTORY_FOR_TEST}{CLUBS_TABLE}.json"
        )

    def test__database_file_exist(self):
        data_manager_mocker = DataManagerMocker()
        database_file_path = f"{DATABASE_DIRECTORY_FOR_TEST}{CLUBS_TABLE}.json"

        table = Table(data_manager_mocker, CLUBS_TABLE)
        assert table._database_file_path == database_file_path

    def test__init_database_file(self, clubs_schema_empty_fixture):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUBS_TABLE)

        table._init_database_file(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUBS_TABLE}.json")
        with open(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUBS_TABLE}.json") as c:
            datas = json.load(c)
        assert validate(instance=datas, schema=clubs_schema_empty_fixture) is None

    def test_all(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUBS_TABLE)
        clubs = table.all()
        assert len(clubs) == 3
        assert clubs[0] == {
            "name": "test1",
            "email": "test1@project11.fr",
            "points": "13",
        }

    def test_filter_first_element_is_dict(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUBS_TABLE)
        club = table.filter_first_element({"email": EMAIL_OK})
        assert club == {"name": "test1", "email": "test1@project11.fr", "points": "13"}

    def test_filter_first_elem_is_None(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUBS_TABLE)
        club = table.filter_first_element({"email": EMAIL_KO})
        assert club is None

    def test_filter(self, mocker):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUBS_TABLE)
        clubs = table.filter({"email": EMAIL_OK})
        assert clubs == [{"name": "test1", "email": "test1@project11.fr", "points": "13"}]
        clubs = table.filter({"email": EMAIL_KO})
        assert clubs == []

        mocker.patch("utils.Table.all", return_value=[])
        clubs = table.filter({"email": EMAIL_OK})
        assert clubs == []

    def test_save(self, clubs_fixture):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUBS_TABLE)
        database_file_path = f"{DATABASE_DIRECTORY_FOR_TEST}{CLUBS_TABLE}.json"
        os.remove(database_file_path)
        table.save(clubs_fixture)
        assert os.path.isfile(database_file_path)
        with open(database_file_path) as c:
            datas = json.load(c)[CLUBS_TABLE]
            assert datas == [
        {
            "name": "test1",
            "email": "test1@project11.fr",
            "points": "5"
        },
        {
            "name": "test2",
            "email": "test2@project11.fr",
            "points": "4"
        },
        {
            "name": "test3",
            "email": "test3@project11.fr",
            "points": "12"
        }
    ]


class TestClubCompetitionClass:
    @staticmethod
    def setup_method(self):
        refresh_datafiles()

    def test_init(self, club_fixture, competition_fixture):
        data_manager_mocker = DataManagerMocker()
        club_competition = ClubCompetition(
            data_manager_mocker,
            BOOKINGS_TABLE,
            club_fixture[0],
            competition_fixture[0],
        )
        assert club_competition.name == BOOKINGS_TABLE
        assert club_competition.app == data_manager_mocker.app
        assert club_competition.club['name'] == "test1"
        assert club_competition.competition['name'] == "competition test2"

    def test_total_booked_places(self, club_fixture, competition_fixture):
        data_manager_mocker = DataManagerMocker()
        club_competition = ClubCompetition(
            data_manager_mocker,
            BOOKINGS_TABLE,
            club_fixture[0],
            competition_fixture[0],
        )
        assert club_competition.total_booked_places == 7
