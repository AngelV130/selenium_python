# set_pythonpath.py
import sys
import os
# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Ignorar advertencias
import warnings
warnings.filterwarnings('ignore')



from confs.Scraper import Scraper
from confs.Build import BuildData
from confs.Json import Json

# Leer el archivo de configuración
data = Json(file_path="./mocks", file_name="data.json").read_json()

# Configuración para la URL de DataTables
config_datatables = data.get('data_table')

# Configuración para la URL de Mercado Libre
config_mercadolibre = data.get('mercado_libre')

# Configuración para la URL de Cyber Puerta
config_cyberpuerta = data.get('cyberpuerta')

build_data = BuildData({}, file_path='./temp')

print("DataTables")
# Instanciar y ejecutar el scraper para DataTables
scraper_datatables = Scraper(config_datatables)
datatable_data = scraper_datatables.navigate_to_page()
scraper_datatables.close_driver()
build_data.set_data(datatable_data)
build_data.show_data()
print("\n")
build_data.save_to_excel(file_name='datatables_results.xlsx')
build_data.save_to_json(file_name='datatables_results.json')
print("\n")
print("-------------------------------------------------")
print("\n")
print("MercadoLibre")
# Instanciar y ejecutar el scraper para Mercado Libre
scraper_mercadolibre = Scraper(config_mercadolibre)
mercadolibre_data = scraper_mercadolibre.navigate_to_page()
scraper_mercadolibre.close_driver()
build_data.set_data(mercadolibre_data)
build_data.show_data()
print("\n")
build_data.save_to_excel(file_name='mercadolibre_results.xlsx')
build_data.save_to_json(file_name='mercadolibre_results.json')
print("\n")
print("-------------------------------------------------")
print("\n")
print("CyberPuerta")
# Instanciar y ejecutar el scraper para CyberPuerta
scraper_cyberpuerta = Scraper(config_cyberpuerta)
cyberpuerta_data = scraper_cyberpuerta.navigate_to_page()
scraper_cyberpuerta.close_driver()
build_data.set_data(cyberpuerta_data)
build_data.show_data()
print("\n")
build_data.save_to_excel(file_name='cyberpuerta_results.xlsx')
build_data.save_to_json(file_name='cyberpuerta_results.json')
print("\n")