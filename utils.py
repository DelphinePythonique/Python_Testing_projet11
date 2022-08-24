import enum
import json
import os.path


class DataManager:
    class TableName(enum.Enum):
        CLUBS = "clubs"
        COMPETITIONS = "competitions"
        BOOKINGS = "bookings"

    def __init__(self, app):
        self.app = app
        self.tables = {}
        for name in self.TableName:
            self.tables[name] = Table(self, name.value)





class Table:
    def __init__(self, manager, name):
        self.manager = manager
        self.name = name

    @property
    def app(self):
        return self.manager.app

    @property
    def _database_file_path(self):
        database_directory_path = self.app.config["DB_PATH"]
        file_path = f"{database_directory_path}{self.name}.json"
        if not os.path.isfile(file_path):
            self._init_database_file(file_path)
        return file_path

    def _init_database_file(self, file_path):
        data = {self.name: []}
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def all(self):
        with open(self._database_file_path) as c:
            list_dataset = json.load(c)[self.name]
            return list_dataset

    def filter_first_element(self, filters):
        datas = self.filter(filters)
        if len(datas)>0:
            return datas[0]
        else:
            return False

    def _match_filters(self, elem, filters):
        match = True
        for key, value in filters.items():
            if elem[key] != value:
                return False
        return match

    def filter(self, filters):
        dataset = self.all()
        founded_element = []

        if len(dataset) <= 0:
            return founded_element

        for elem in dataset:
            if self._match_filters(elem, filters):
                founded_element.append(elem)
        return founded_element


    def save(self, datas):
        datas_to_write = {self.name: datas}
        with open(self._database_file_path, "w") as f:
            json.dump(datas_to_write, f, indent=4)
