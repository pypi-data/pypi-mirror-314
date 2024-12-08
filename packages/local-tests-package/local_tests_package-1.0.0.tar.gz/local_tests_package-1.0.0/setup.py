from pathlib import Path  # Importa Path para manejar rutas de archivos
from setuptools import setup, find_packages

# Obtiene el directorio actual donde está el archivo setup.py
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
#asd
setup(
    name="local-tests-package",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "Appium-Python-Client",
    ],
    description="Paquete para pruebas locales en Android con Appium y Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
