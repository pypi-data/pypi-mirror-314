import pytest
from local_tests_package.driver_setup import get_driver

@pytest.fixture(scope="function")
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

def test_login(driver):
    """
    Prueba de ejemplo para validar el inicio de sesión.
    """
    username_field = driver.find_element_by_id("com.example.florales:id/username")
    password_field = driver.find_element_by_id("com.example.florales:id/password")
    login_button = driver.find_element_by_id("com.example.florales:id/login")

    username_field.send_keys("test_user")
    password_field.send_keys("test_password")
    login_button.click()

    assert "Bienvenido" in driver.page_source
