# set_pythonpath.py
import sys
import os
import warnings

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Ignorar advertencias
warnings.filterwarnings('ignore')

from confs.Scraper import Scraper
from confs.Build import BuildData
from confs.Json import Json

# Leer el archivo de configuración
data = Json(file_path="./mocks", file_name="data.json").read_json()

config_siautt = data.get('uttorreon')
config_datatables = data.get('data_table')
config_mercadolibre = data.get('mercado_libre')
config_cyberpuerta = data.get('cyber_puerta')

def _ensure_directory_exists(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directorio {path} creado.")
        except Exception as e:
            print(f"Error al crear el directorio {path}: {e}")
def scrape_and_save(config, scraper_name):
    build_data = BuildData({}, file_path='./temp')
    scraper = Scraper(config)
    data_list = scraper.navigate_to_page()
    scraper.close_driver()
    for index, data in enumerate(data_list):
        build_data.set_data(data)
        path_json = f'{build_data.file_path}/json/{scraper_name}'
        path_excel = f'{build_data.file_path}/excel/{scraper_name}'
        _ensure_directory_exists(path_json)
        _ensure_directory_exists(path_excel)
        build_data.save_to_excel(file_path=f'{path_excel}', file_name=f"{scraper_name}_results{index}.xlsx")
        build_data.save_to_json(file_path=f'{path_json}', file_name=f"{scraper_name}_results{index}.json")
    print(f"Obtención de datos de {scraper_name} completada y datos guardados.\n")

def menu():
    while True:
        print("Seleccione un opción:")
        print("1. DataTables")
        print("2. CyberPuerta")
        print("3. Siautt")
        print("4. MercadoLibre")
        print("5. Salir")
        option = input("Opción: ")
        
        if option == '1':
            print("DataTables")
            scrape_and_save(config_datatables, 'datatables')
        elif option == '2':
            print("CyberPuerta")
            scrape_and_save(config_cyberpuerta, 'cyberpuerta')
        elif option == '3':
            print("Siautt")
            scrape_and_save(config_siautt, 'siautt')
        elif option == '4':
            print("MercadoLibre")
            scrape_and_save(config_mercadolibre, 'mercadolibre')
        elif option == '5':
            print("Saliendo...")
            break
        else:
            print("Entrada no valida.")

if __name__ == "__main__":
    menu()
