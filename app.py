"""
Script principal para ejecutar la aplicación Flask.

Este módulo carga las variables de entorno, crea la aplicación utilizando
la función `create_app()` e inicia el servidor Flask.
"""

import os
from dotenv import load_dotenv
from musica_api import create_app

"""Cargar variables de entorno desde archivo .env si existe."""
load_dotenv()

"""Crear la instancia de la aplicación Flask."""
app = create_app()

if __name__ == "__main__":
    """Punto de entrada de la aplicación."""

    """Obtener puerto desde variables de entorno, o usar 5000 por defecto."""
    port = int(os.getenv("PORT", 5000))

    """Determinar si se debe usar el modo debug."""
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    """Ejecutar la aplicación Flask."""
    app.run(host="0.0.0.0", port=port, debug=debug)
