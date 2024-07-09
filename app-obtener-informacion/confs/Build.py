from datetime import datetime
import pandas as pd
import os
from confs.Json import Json

class BuildData(Json):
    def __init__(self, data_dict = {}, file_path = './', file_name = 'data'):
        self.file_path = file_path
        self.file_name = file_name
        self.df = pd.DataFrame(data_dict)

    def save_to_excel(self, file_name = None, file_path = None, file_rute = None):
        file_name = file_name if file_name else self.file_name
        file_path = file_path if file_path else self.file_path
        file_rute = os.path.join(file_path, file_name)
        try:
            self.df.to_excel(file_rute, index=False)
            print(f"Datos guardados en {file_rute}")
        except Exception as e:
            print(f"Error al guardar en Excel: {e}")

    def save_to_json(self, file_name = None, file_path = None, file_rute = None):
        file_name = file_name if file_name else self.file_name
        file_path = file_path if file_path else self.file_path
        file_rute = os.path.join(file_path, file_name)
        try:
            self.write_json(self.df.to_dict(orient='records'), file_rute=file_rute)
            print(f"Datos guardados en {file_rute}")
        except Exception as e:
            print(f"Error al guardar en JSON: {e}")

    def show_data(self):
        try:
            print(self.df)
        except Exception as e:
            print(f"Error al mostrar los datos: {e}")
    def set_data(self, data_dict):
        try:
            self.df = pd.DataFrame(data_dict)
        except Exception as e:
            print(f"Error al establecer los datos: {e}")
    def get_data(self):
        return self.df