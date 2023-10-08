
import os
import re
import json

from utils import backup
from utils import misc

class DataBase:
    def __init__(self, path, user):
        self.file_path = path
        self.user = user
        self.all_data = { user : {} }
        self.readJson()

    def readJson(self):
        self.all_data  = misc.load_json(self.file_path)
        self.user_data = self.all_data.get(self.user) or {}

    def getUserData(self):
        return self.user_data

    def saveUserData(self, udata):
        data = self.all_data
        data[self.user] = udata
        backup.check_and_backup(self.file_path)
        misc.dump_json(self.file_path, data)


def init(datafile, user):
    return DataBase(datafile, user)
