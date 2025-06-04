"""
Módulo de modelos de API para la serialización/deserialización de datos.

Define los esquemas utilizados por Flask-RESTX para la documentación y validación
de los recursos de la API: Usuarios, Canciones y Favoritos.
"""

from flask_restx import fields
from .extensions import api

mensaje_model = api.model(
    "Mensaje", {"mensaje": fields.String(description="Mensaje informativo")}
)
"""Modelo para respuestas simples con un mensaje informativo.

Campos:
- mensaje (str): Mensaje informativo.
"""

usuario_base = api.model(
    "UsuarioBase",
    {
        "nombre": fields.String(required=True, description="Nombre del usuario"),
        "correo": fields.String(
            required=True, description="Correo electrónico del usuario"
        ),
    },
)
"""Modelo base para Usuario.

Campos obligatorios:
- nombre (str): Nombre del usuario.
- correo (str): Correo electrónico del usuario.
"""

usuario_model = api.inherit(
    "Usuario",
    usuario_base,
    {
        "id": fields.Integer(description="Identificador único del usuario"),
        "fecha_registro": fields.DateTime(description="Fecha de registro del usuario"),
    },
)
"""Modelo completo de Usuario, heredando de UsuarioBase.

Campos adicionales:
- id (int): Identificador único del usuario.
- fecha_registro (datetime): Fecha de registro.
"""

cancion_base = api.model(
    "CancionBase",
    {
        "titulo": fields.String(required=True, description="Título de la canción"),
        "artista": fields.String(
            required=True, description="Artista/intérprete de la canción"
        ),
        "album": fields.String(description="Álbum al que pertenece la canción"),
        "duracion": fields.Integer(description="Duración en segundos"),
        "año": fields.Integer(description="Año de lanzamiento"),
        "genero": fields.String(description="Género musical"),
    },
)
"""Modelo base para Canción.

Campos obligatorios:
- titulo (str): Título de la canción.
- artista (str): Artista o intérprete.

Campos opcionales:
- album (str): Álbum al que pertenece.
- duracion (int): Duración en segundos.
- año (int): Año de lanzamiento.
- genero (str): Género musical.
"""

cancion_model = api.inherit(
    "Cancion",
    cancion_base,
    {
        "id": fields.Integer(description="Identificador único de la canción"),
        "fecha_creacion": fields.DateTime(description="Fecha de creación del registro"),
    },
)
"""Modelo completo de Canción, heredando de CancionBase.

Campos adicionales:
- id (int): Identificador único.
- fecha_creacion (datetime): Fecha de creación del registro.
"""

favorito_input = api.model(
    "FavoritoInput",
    {
        "id_usuario": fields.Integer(required=True, description="ID del usuario"),
        "id_cancion": fields.Integer(required=True, description="ID de la canción"),
    },
)
"""Modelo para entrada de Favorito.

Campos obligatorios:
- id_usuario (int): ID del usuario.
- id_cancion (int): ID de la canción.
"""

cancion_simple = api.model(
    "CancionSimple",
    {
        "id": fields.Integer(description="ID de la canción"),
        "titulo": fields.String(description="Título de la canción"),
        "artista": fields.String(description="Artista de la canción"),
    },
)
"""Modelo simple para representar una Canción con campos básicos."""

usuario_simple = api.model(
    "UsuarioSimple",
    {
        "id": fields.Integer(description="ID del usuario"),
        "nombre": fields.String(description="Nombre del usuario"),
    },
)
"""Modelo simple para representar un Usuario con campos básicos."""

favorito_model = api.model(
    "Favorito",
    {
        "id": fields.Integer(description="ID del favorito"),
        "id_usuario": fields.Integer(description="ID del usuario"),
        "id_cancion": fields.Integer(description="ID de la canción"),
        "fecha_marcado": fields.DateTime(
            description="Fecha en que se marcó como favorito"
        ),
        "usuario": fields.Nested(usuario_simple, description="Datos del usuario"),
        "cancion": fields.Nested(cancion_simple, description="Datos de la canción"),
    },
)
"""Modelo completo para representar un Favorito.

Incluye:
- información básica del favorito,
- datos anidados del usuario y la canción relacionados.
"""

favoritos_usuario_model = api.model(
    "FavoritosUsuario",
    {
        "usuario": fields.Nested(usuario_simple),
        "canciones_favoritas": fields.List(fields.Nested(cancion_simple)),
    },
)
"""Modelo para mostrar canciones favoritas de un usuario.

Campos:
- usuario (UsuarioSimple): Datos básicos del usuario.
- canciones_favoritas (list): Lista de canciones favoritas (CancionSimple).
"""
