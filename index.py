# set_pythonpath.py
import sys
import os
import warnings

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Ignorar advertencias
warnings.filterwarnings('ignore')

from confs.Scraper.Main import Main
from confs.Build import BuildData
from confs.Json import Json

# Leer el archivo de configuración
data = Json(file_path="./mocks", file_name="data.local.json").read_json()

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
    scraper = Main()
    data_list = scraper.run(config)
    scraper.selenium.close_driver()
    build_data.set_data(data_list)
    _ensure_directory_exists(f"{build_data.file_path}/excel/{scraper_name}")
    build_data.save_to_excel(file_name=f"excel/{scraper_name}/{scraper_name}.xlsx")
    _ensure_directory_exists(f"{build_data.file_path}/json/{scraper_name}")
    build_data.save_to_json(file_name=f"json/{scraper_name}/{scraper_name}.json")

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
