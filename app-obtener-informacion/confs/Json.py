import json
import os

class Json:
    def __init__(self, file_path = './', file_name = 'data.json'):
        self.file_path = file_path
        self.file_name = file_name
    def read_json(self, file_name = None, file_path = None, file_rute = None):
        file_name = file_name if file_name else self.file_name
        file_path = file_path if file_path else self.file_path
        file_rute = file_rute if file_rute else os.path.join(file_path, file_name)
        with open(file_rute, 'r') as file:
            return json.load(file)
    def write_json(self, data, file_name = None, file_path = None, file_rute = None):
        file_name = file_name if file_name else self.file_name
        file_path = file_path if file_path else self.file_path
        file_rute = file_rute if file_rute else os.path.join(file_path, file_name)
        with open(file_rute, 'w') as file:
            json.dump(data, file, indent=4)