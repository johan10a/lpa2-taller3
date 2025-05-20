"""
Módulo de recursos de la API.
Define los endpoints, controladores y la lógica de negocio de la API.
"""
from flask import request
from flask_restx import Resource, Namespace
from .api_models import (
    usuario_model, usuario_base, 
    cancion_model, cancion_base,
    favorito_model, favorito_input, 
    favoritos_usuario_model, mensaje_model
)
from .extensions import db
from .models import Usuario, Cancion, Favorito

# Namespace para agrupar los recursos de la API
ns = Namespace("api", description="Operaciones de la API de música")

# Recurso para probar la API
@ns.route("/ping")
class Ping(Resource):
    @ns.response(200, "API funcionando correctamente")
    @ns.marshal_with(mensaje_model)
    def get(self):
        """Endpoint para verificar que la API está funcionando"""
        return {"mensaje": "La API está funcionando correctamente"}, 200

# Recursos para Usuarios
@ns.doc("Listar todos los usuarios con paginación")
@ns.param("page", "Número de página (por defecto 1)")
@ns.param("per_page", "Cantidad por página (por defecto 4)")
@ns.response(200, "Lista de usuarios obtenida con éxito")
@ns.marshal_list_with(usuario_model)
def get(self):
    """Obtiene todos los usuarios registrados (paginados)"""
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 4))
    
    usuarios = Usuario.query.paginate(page=page, per_page=per_page, error_out=False)
    return usuarios.items, 200

    
    @ns.doc("Crear un nuevo usuario")
    @ns.expect(usuario_base)
    @ns.response(201, "Usuario creado con éxito")
    @ns.response(400, "Datos inválidos o correo ya existe")
    @ns.marshal_with(usuario_model)
    def post(self):
        """Crea un nuevo usuario"""
        data = request.json
        
        if Usuario.query.filter_by(correo=data["correo"]).first():
            ns.abort(400, "El correo electrónico ya está registrado")
        
        usuario = Usuario(
            nombre=data["nombre"],
            correo=data["correo"]
        )
        
        try:
            db.session.add(usuario)
            db.session.commit()
            return usuario, 201
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al crear usuario: {str(e)}")

@ns.route("/usuarios/<int:id>")
@ns.param("id", "Identificador único del usuario")
@ns.response(404, "Usuario no encontrado")
class UsuarioAPI(Resource):
    @ns.doc("Obtener un usuario por su ID")
    @ns.marshal_with(usuario_model)
    def get(self, id):
        """Obtiene un usuario por su ID"""
        return Usuario.query.get_or_404(id), 200
    
    @ns.doc("Actualizar un usuario")
    @ns.expect(usuario_base)
    @ns.marshal_with(usuario_model)
    def put(self, id):
        """Actualiza un usuario existente"""
        usuario = Usuario.query.get_or_404(id)
        data = request.json
        
        if "correo" in data and data["correo"] != usuario.correo:
            if Usuario.query.filter_by(correo=data["correo"]).first():
                ns.abort(400, "El correo electrónico ya está registrado")
        
        usuario.nombre = data.get("nombre", usuario.nombre)
        usuario.correo = data.get("correo", usuario.correo)
        
        try:
            db.session.commit()
            return usuario
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al actualizar usuario: {str(e)}")
    
    @ns.doc("Eliminar un usuario")
    @ns.response(204, "Usuario eliminado con éxito")
    def delete(self, id):
        """Elimina un usuario existente"""
        usuario = Usuario.query.get_or_404(id)
        try:
            db.session.delete(usuario)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al eliminar usuario: {str(e)}")

# Recursos para Canciones
@ns.route("/canciones")
class CancionListAPI(Resource):
    @ns.doc("Listar todas las canciones con paginación")
    @ns.param("page", "Número de página (por defecto 1)")
    @ns.param("per_page", "Cantidad por página (por defecto 4)")
    @ns.response(200, "Lista de canciones obtenida con éxito")
    @ns.marshal_list_with(cancion_model)
    def get(self):
        """Obtiene todas las canciones registradas (paginadas)"""
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 4))
        
        canciones = Cancion.query.paginate(page=page, per_page=per_page, error_out=False)
        return canciones.items, 200

    
    @ns.doc("Crear una nueva canción")
    @ns.expect(cancion_base)
    @ns.response(201, "Canción creada con éxito")
    @ns.marshal_with(cancion_model)
    def post(self):
        """Crea una nueva canción"""
        data = request.json
        
        cancion = Cancion(
            titulo=data["titulo"],
            artista=data["artista"],
            album=data.get("album"),
            duracion=data.get("duracion"),
            año=data.get("año"),
            genero=data.get("genero")
        )
        
        try:
            db.session.add(cancion)
            db.session.commit()
            return cancion, 201
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al crear canción: {str(e)}")

@ns.route("/canciones/<int:id>")
@ns.param("id", "Identificador único de la canción")
@ns.response(404, "Canción no encontrada")
class CancionAPI(Resource):
    @ns.doc("Obtener una canción por su ID")
    @ns.marshal_with(cancion_model)
    def get(self, id):
        """Obtiene una canción por su ID"""
        return Cancion.query.get_or_404(id), 200
    
    @ns.doc("Actualizar una canción")
    @ns.expect(cancion_base)
    @ns.marshal_with(cancion_model)
    def put(self, id):
        """Actualiza una canción existente"""
        cancion = Cancion.query.get_or_404(id)
        data = request.json
        
        cancion.titulo = data.get("titulo", cancion.titulo)
        cancion.artista = data.get("artista", cancion.artista)
        cancion.album = data.get("album", cancion.album)
        cancion.duracion = data.get("duracion", cancion.duracion)
        cancion.año = data.get("año", cancion.año)
        cancion.genero = data.get("genero", cancion.genero)
        
        try:
            db.session.commit()
            return cancion
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al actualizar canción: {str(e)}")
    
    @ns.doc("Eliminar una canción")
    @ns.response(204, "Canción eliminada con éxito")
    def delete(self, id):
        """Elimina una canción existente"""
        cancion = Cancion.query.get_or_404(id)
        try:
            db.session.delete(cancion)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al eliminar canción: {str(e)}")

# Recursos para buscar canciones
@ns.route("/canciones/buscar")
class CancionBusquedaAPI(Resource):
    @ns.doc("Buscar canciones por título, artista o género")
    @ns.param("titulo", "Título de la canción (búsqueda parcial)")
    @ns.param("artista", "Nombre del artista (búsqueda parcial)")
    @ns.param("genero", "Género musical (búsqueda exacta)")
    @ns.marshal_list_with(cancion_model)
    def get(self):
        """Busca canciones por título, artista o género"""
        titulo = request.args.get("titulo")
        artista = request.args.get("artista")
        genero = request.args.get("genero")
        
        query = Cancion.query
        
        if titulo:
            query = query.filter(Cancion.titulo.ilike(f"%{titulo}%"))
        if artista:
            query = query.filter(Cancion.artista.ilike(f"%{artista}%"))
        if genero:
            query = query.filter(Cancion.genero == genero)
            
        return query.all(), 200

# Recursos para Favoritos
@ns.doc("Listar todos los favoritos con paginación")
@ns.param("page", "Número de página (por defecto 1)")
@ns.param("per_page", "Cantidad por página (por defecto 4)")
@ns.response(200, "Lista de favoritos obtenida con éxito")
@ns.marshal_list_with(favorito_model)
def get(self):
    """Obtiene todos los registros de favoritos (paginados)"""
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 4))
    
    favoritos = Favorito.query.paginate(page=page, per_page=per_page, error_out=False)
    return favoritos.items, 200

    
    @ns.doc("Marcar una canción como favorita")
    @ns.expect(favorito_input)
    @ns.response(201, "Canción marcada como favorita")
    @ns.response(400, "Datos inválidos o relación ya existe")
    @ns.response(404, "Usuario o canción no encontrada")
    @ns.marshal_with(favorito_model)
    def post(self):
        """Marca una canción como favorita para un usuario"""
        data = request.json
        
        usuario = Usuario.query.get(data["id_usuario"])
        cancion = Cancion.query.get(data["id_cancion"])
        
        if not usuario:
            ns.abort(404, "Usuario no encontrado")
        if not cancion:
            ns.abort(404, "Canción no encontrada")
        
        favorito_existente = Favorito.query.filter_by(
            id_usuario=data["id_usuario"],
            id_cancion=data["id_cancion"]
        ).first()
        
        if favorito_existente:
            ns.abort(400, "La canción ya está marcada como favorita para este usuario")
        
        favorito = Favorito(
            id_usuario=data["id_usuario"],
            id_cancion=data["id_cancion"]
        )
        
        try:
            db.session.add(favorito)
            db.session.commit()
            return favorito, 201
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al marcar como favorito: {str(e)}")

@ns.route("/favoritos/<int:id>")
@ns.param("id", "Identificador único del favorito")
@ns.response(404, "Favorito no encontrado")
class FavoritoAPI(Resource):
    @ns.doc("Obtener un favorito por su ID")
    @ns.marshal_with(favorito_model)
    def get(self, id):
        """Obtiene un registro de favorito por su ID"""
        return Favorito.query.get_or_404(id), 200
    
    @ns.doc("Eliminar un favorito")
    @ns.response(204, "Favorito eliminado con éxito")
    def delete(self, id):
        """Elimina un registro de favorito existente"""
        favorito = Favorito.query.get_or_404(id)
        try:
            db.session.delete(favorito)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al eliminar favorito: {str(e)}")

@ns.route("/usuarios/<int:id>/favoritos")
@ns.param("id", "Identificador único del usuario")
@ns.response(404, "Usuario no encontrado")
class UsuarioFavoritosAPI(Resource):
    @ns.doc("Obtener las canciones favoritas de un usuario")
    @ns.marshal_with(favoritos_usuario_model)
    def get(self, id):
        """Obtiene todas las canciones favoritas de un usuario"""
        usuario = Usuario.query.get_or_404(id)
        
        favoritos = Favorito.query.filter_by(id_usuario=id).all()
        canciones_favoritas = [
            {
                "id": favorito.cancion.id,
                "titulo": favorito.cancion.titulo,
                "artista": favorito.cancion.artista
            }
            for favorito in favoritos
        ]
        
        return {
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre
            },
            "canciones_favoritas": canciones_favoritas
        }, 200

@ns.route("/usuarios/<int:id_usuario>/favoritos/<int:id_cancion>")
@ns.param("id_usuario", "Identificador único del usuario")
@ns.param("id_cancion", "Identificador único de la canción")
class UsuarioCancionFavoritoAPI(Resource):
    @ns.doc("Marcar o desmarcar una canción como favorita para un usuario")
    @ns.response(201, "Canción marcada como favorita")
    @ns.response(204, "Canción desmarcada como favorita")
    @ns.response(404, "Usuario o canción no encontrada")
    def post(self, id_usuario, id_cancion):
        """Marca una canción como favorita para un usuario"""
        usuario = Usuario.query.get(id_usuario)
        cancion = Cancion.query.get(id_cancion)
        
        if not usuario:
            ns.abort(404, "Usuario no encontrado")
        if not cancion:
            ns.abort(404, "Canción no encontrada")
        
        favorito = Favorito.query.filter_by(
            id_usuario=id_usuario,
            id_cancion=id_cancion
        ).first()
        
        if favorito:
            ns.abort(400, "La canción ya está marcada como favorita para este usuario")
        
        favorito = Favorito(
            id_usuario=id_usuario,
            id_cancion=id_cancion
        )
        
        try:
            db.session.add(favorito)
            db.session.commit()
            return {"mensaje": "Canción marcada como favorita"}, 201
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al marcar como favorito: {str(e)}")
    
    @ns.doc("Eliminar una canción de favoritos")
    @ns.response(204, "Canción eliminada de favoritos")
    @ns.response(404, "Relación de favorito no encontrada")
    def delete(self, id_usuario, id_cancion):
        """Elimina una canción de favoritos para un usuario"""
        favorito = Favorito.query.filter_by(
            id_usuario=id_usuario,
            id_cancion=id_cancion
        ).first_or_404("Relación de favorito no encontrada")
        
        try:
            db.session.delete(favorito)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            ns.abort(400, f"Error al eliminar favorito: {str(e)}")
@ns.route("/")
class Home(Resource):
    @ns.doc("Página principal de la API")
    @ns.marshal_with(mensaje_model)
    def get(self):
        """Mensaje de bienvenida en la raíz de la API"""
        return {"mensaje": "Bienvenido a la API de Música. Visita /docs para la documentación."}, 200
