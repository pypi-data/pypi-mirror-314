import json
import os

def get_des_cap(user_input=None):
    """
    Obtiene las Desired Capabilities del usuario. Requiere que el usuario proporcione
    información esencial como la ruta del APK.
    """
    if not user_input:
        raise ValueError(
            "Las Desired Capabilities son obligatorias. Debes proporcionar al menos la ruta del APK, "
            "el paquete de la aplicación y la actividad principal."
        )

    # Validar que la ruta del APK esté presente
    if "app" not in user_input or not user_input["app"]:
        raise ValueError("La ruta del APK ('app') es obligatoria en las Desired Capabilities.")

    # Valores predeterminados que pueden complementarse
    default_des_cap = {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:noReset": True,
        "appium:newCommandTimeout": 120
    }

    # Mezclar valores predeterminados con los proporcionados por el usuario
    default_des_cap.update(user_input)

    return default_des_cap
