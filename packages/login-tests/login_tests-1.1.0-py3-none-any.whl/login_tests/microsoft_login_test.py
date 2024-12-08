import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MicrosoftLoginTest:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        # Implementación del flujo de login con Microsoft
        try:
            login_button = self.driver.find_element(By.XPATH, "//android.widget.Button[@content-desc='Iniciar sesión con Microsoft']")
            login_button.click()

            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@index='0']"))
            )
            email_field.send_keys(username)

            next_button = self.driver.find_element(By.XPATH, "//android.widget.Button[@text='Next']")
            next_button.click()
            time.sleep(5)
            password_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//android.widget.EditText[@index='0']"))
            )
            self.driver.press_keycode(2)
            password_field.send_keys(password)

            sign_in_button = self.driver.find_element(By.XPATH, "//android.widget.Button[@text='Sign in']")
            sign_in_button.click()
            time.sleep(5)
            return True

        except Exception as e:
            raise RuntimeError(f"Error en el flujo de login con Microsoft: {e}")
