from .find_elements import *
from .invoke_api import *
from .get_driver import *
import os

download_dir = "C:\\TMPIMGGI\\LAST_IMG\\"
download_kit = "C:\\TMPIMGKIT\\"
download_ggi = "C:\\TMPIMGGI\\"
driver = None

def create_dirs():
    global download_dir, download_kit, download_ggi
    for directory in [download_dir, download_kit, download_ggi]:

        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f" - Diretório criado: {directory}")

def initialize_driver():
    global driver
    if driver is None:
        driver = get_driver.start_instance(download_dir)

    return driver

def find_element_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.find_element_with_wait_backcode(driver, by, value, timeout=10, parent=None)

    else: raise ValueError("Error: Driver is None")

def find_elements_with_wait(by, value, timeout=10, parent=None):
    global driver
    if driver != None:
        return find_elements.find_elements_with_wait_backcode(driver, by, value, timeout=10, parent=None)

    else: raise ValueError("Error: Driver is None")

print(" --> Biblioteca BCFOX Importada")