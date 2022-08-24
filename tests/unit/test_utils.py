import json
import os.path

from jsonschema.validators import validate

from tests.conftest import TableNameMocker, client, DataManagerMocker
from utils import DataManager, Table


class TestDatamanagerClass:
    def test_init_should_be_ok(self, app, mocker):
        mocker.patch("utils.DataManager.TableName", TableNameMocker)
        data_manager = DataManager(app)
        assert len(data_manager.tables) == 3
        assert isinstance(data_manager.tables[TableNameMocker.CLUBS], Table)


class TestTableClass:
    def test_init_should_be_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, "clubs_test")
        assert table.name == "clubs_test"

    def test__database_not_exist_file_path_should_be_ok(self):
        data_manager_mocker = DataManagerMocker()
        if os.path.isfile("database/test/clubs_test.json"):
            os.remove("database/test/clubs_test.json")
        table = Table(data_manager_mocker, "clubs_test")
        assert table._database_file_path == "database/test/clubs_test.json"

    def test__database_exist_file_path_should_be_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, "clubs_test")
        assert table._database_file_path == "database/test/clubs_test.json"
        table = Table(data_manager_mocker, "clubs_test")
        assert table._database_file_path == "database/test/clubs_test.json"

    def test_should_init_database_file(self, clubs_schema_empty_fixture):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, "clubs_test")
        if os.path.isfile("database/test/clubs_test.json"):
            os.remove("database/test/clubs_test.json")
        table._init_database_file("database/test/clubs_test.json")
        with open("database/test/clubs_test.json") as c:
            datas = json.load(c)
        assert validate(instance=datas, schema=clubs_schema_empty_fixture) is None

    def test_should_all_is_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, "clubs")
        clubs = table.all()
        assert len(clubs) == 3
        assert clubs[0] == {
            "name": "test1",
            "email": "test1@project11.fr",
            "points": "13",
        }

    def test_should_filter_first_elem_is_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, "clubs")
        club = table.filter_first_element({"email": "test1@project11.fr"})
        assert club
        assert club == {"name": "test1", "email": "test1@project11.fr", "points": "13"}

    def test_should_filter_first_elem_result_is_empty_ok(self):
        data_manager_mocker = DataManagerMocker()
        table = Table(data_manager_mocker, "clubs")
        club = table.filter_first_element({"email": "test1ko@project11.fr"})
        assert not club
