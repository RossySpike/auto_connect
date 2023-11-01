import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import configparser
import requests

# Nombre del archivo de configuración
config_file = "credenciales.ini"

# Intenta cargar las credenciales desde el archivo de configuración
config = configparser.ConfigParser()

try:
    config.read(config_file)
    username = config.get("Credenciales", "Usuario")
    password = config.get("Credenciales", "Contraseña")
except (configparser.NoSectionError, configparser.NoOptionError):
    # Si no se encuentran credenciales, solicita al usuario que las ingrese
    username = input("Ingresa tu nombre de usuario: ")
    password = input("Ingresa tu contraseña: ")

    # Guarda las credenciales en el archivo de configuración
    config["Credenciales"] = {"Usuario": username, "Contraseña": password}
    with open(config_file, "w") as configfile:
        config.write(configfile)

# Configuración del navegador (puedes elegir el navegador y la ruta del controlador)
driver = webdriver.Chrome(executable_path="/ruta/al/controlador/chromedriver")

# URL de la página de inicio de sesión
login_url = "URL_DE_LA_PÁGINA_DE_INICIO_DE_SESIÓN"

# Inicializa el tiempo de espera
retry_delay = 60  # Espera inicial de 1 minuto

while True:
    # Verifica la conectividad a Internet
    if not check_internet_connection():
        # La conexión a Internet ha fallado, inicia sesión nuevamente
        driver.get(login_url)

        # Encuentra los elementos para el nombre de usuario y la contraseña y envía las credenciales
        username_field = driver.find_element_by_id("id_del_campo_de_nombre_de_usuario")
        password_field = driver.find_element_by_id("id_del_campo_de_contraseña")

        username_field.send_keys(username)
        password_field.send_keys(password)

        # Envía el formulario (puede variar según la página web)
        password_field.send_keys(Keys.RETURN)

        # Espera a que se complete el proceso de inicio de sesión
        # Puedes agregar una espera explícita o manejar eventos específicos según la página de inicio de sesión

        # Reinicia el tiempo de espera a su valor inicial
        retry_delay = 60  # 1 minuto
    else:
        # La conexión a Internet es exitosa, aumenta el tiempo de espera exponencialmente
        retry_delay *= 2

    # Limita el tiempo de espera máximo (puedes ajustar este valor según tus necesidades)
    max_retry_delay = 3600  # 1 hora

    if retry_delay > max_retry_delay:
        retry_delay = max_retry_delay

    # Espera antes de volver a verificar
    time.sleep(retry_delay)
