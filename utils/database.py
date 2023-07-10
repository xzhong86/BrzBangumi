
import json

class DataBase:
    def __init__(self, path, user):
        self.file_path = path
        self.user = user
        self.all_data = { user : {} }
        self.readJson()

    def readJson(self):
        with open(self.file_path, 'r', encoding='utf-8') as fh:
            self.all_data  = json.load(fh)
            self.user_data = self.all_data.get(self.user) or {}

    def getUserData(self):
        return self.user_data

    def saveUserData(self, udata):
        data = self.all_data
        data[self.user] = udata
        with open(self.file_path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=4, sort_keys=True, ensure_ascii=False)


def init(datafile, user):
    return DataBase(datafile, user)
