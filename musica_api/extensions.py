"""
Módulo de extensiones para la aplicación Flask.

Este módulo define e inicializa las extensiones que serán utilizadas
a lo largo del proyecto, tales como la API RESTful y el ORM para la base de datos.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

api = Api(
    title="API de Música",
    version="1.0",
    description="API para gestionar Usuarios, Canciones y Favoritos",
    doc="/docs",
)
"""Instancia de Api para construir la API RESTful.

Configura:
- Título de la API
- Versión
- Descripción
- Ruta de la documentación Swagger UI (/docs)
"""

db = SQLAlchemy()
"""Instancia de SQLAlchemy para manejo ORM de la base de datos.

Actualmente no está inicializada con la aplicación Flask.
Se requiere configuración adicional para vincularla.
"""
