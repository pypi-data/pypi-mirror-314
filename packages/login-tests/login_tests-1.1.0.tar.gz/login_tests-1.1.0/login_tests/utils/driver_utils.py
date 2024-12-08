from appium import webdriver

def initialize_driver(user_input=None):
    if not user_input:
        raise ValueError("Las Desired Capabilities son obligatorias.")

    print(f"Desired Capabilities: {user_input}")  # Debug para verificar las capacidades

    # Inicializar el driver con Desired Capabilities
    driver = webdriver.Remote("http://localhost:4723/wd/hub", user_input)
    driver.implicitly_wait(10)
    return driver
