import json
import os.path

from jsonschema.validators import validate

from tests.conftest import (
    TableNameMocker,
    DataManagerMocker,
    DATABASE_DIRECTORY_FOR_TEST,
    CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST,
    CLUB_TABLE_READONLY,
    EMAIL_KO,
    EMAIL_OK, refresh_datafiles
)
from utils import DataManager, Table


class TestDatamanagerClass:
    def setup_method(self):
        refresh_datafiles()
    def test_init_should_be_ok(self, app, mocker):
        mocker.patch("utils.DataManager.TableName", TableNameMocker)
        data_manager = DataManager(app)
        assert len(data_manager.tables) == 3
        assert isinstance(data_manager.tables[TableNameMocker.CLUBS], Table)


class TestTableClass:
    def setup_method(self):
        refresh_datafiles()
    def test_init_should_be_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST)
        assert table.name == CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST

    def test__database_not_exist_file_path_should_be_ok(self):
        data_manager_mocker = DataManagerMocker()
        if os.path.isfile(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json"):
            os.remove(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json")
        table = Table(data_manager_mocker, CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST)
        assert table._database_file_path == f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json"

    def test__database_exist_file_path_should_be_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST)
        assert table._database_file_path == f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json"
        table = Table(data_manager_mocker, CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST)
        assert table._database_file_path == f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json"

    def test_should_init_database_file(self, clubs_schema_empty_fixture):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST)
        if os.path.isfile(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json"):
            os.remove(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json")
        table._init_database_file(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json")
        with open(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json") as c:
            datas = json.load(c)
        assert validate(instance=datas, schema=clubs_schema_empty_fixture) is None

    def test_should_all_is_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUB_TABLE_READONLY)
        clubs = table.all()
        assert len(clubs) == 3
        assert clubs[0] == {
            "name": "test1",
            "email": "test1@project11.fr",
            "points": "13",
        }

    def test_should_filter_first_elem_is_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUB_TABLE_READONLY)
        club = table.filter_first_element({"email": EMAIL_OK})
        assert club
        assert club == {"name": "test1", "email": "test1@project11.fr", "points": "13"}

    def test_should_filter_first_elem_result_is_empty_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUB_TABLE_READONLY)
        club = table.filter_first_element({"email": EMAIL_KO})
        assert not club

    def test_should_save(self, clubs_fixture, clubs_ready_to_dump_fixture):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST)
        if os.path.isfile(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json"):
            os.remove(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json")

        table.save(clubs_fixture)
        assert os.path.isfile(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json")
        with open(f"{DATABASE_DIRECTORY_FOR_TEST}{CLUB_TABLE_FOR_INIT_AND_DESTROY_TEST}.json") as c:
            datas = json.load(c)
            assert datas == clubs_ready_to_dump_fixture
