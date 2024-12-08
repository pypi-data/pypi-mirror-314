from setuptools import setup, find_packages

setup(
    name="login_tests",
    version="1.1.0",
    packages=find_packages(include=["login_tests", "login_tests.*"]),
    install_requires=[
        "Appium-Python-Client==2.0.0",
        "selenium>=4.0.0",
        "pytest>=6.0.0"
    ],
    entry_points={
        "console_scripts": [
            "run-tests=tests.test_login:main",
            "run-tests-simple=tests.test_simple_login:main"
        ]
    },
    include_package_data=True,  # Asegura que se incluyan archivos como config.json
    package_data={
        "": ["*.json"]  # Incluir archivos JSON si es necesario
    }
)
