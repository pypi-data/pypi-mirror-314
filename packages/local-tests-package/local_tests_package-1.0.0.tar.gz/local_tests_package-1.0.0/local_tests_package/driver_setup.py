from appium import webdriver
from local_tests_package.des_cap import get_des_cap

def get_driver():
    """
    Inicializa y retorna un driver de Appium con las capacidades deseadas.
    """
    des_cap = get_des_cap()
    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", des_cap)
    return driver
