"""
Flask API Application - API REST para el framework

Proporciona endpoints REST para acceder a todas las funcionalidades
del framework de manera remota.

Autor: DAM2526
"""

from flask import Flask, jsonify, request, make_response, current_app
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from functools import wraps
import os

from ..core.data_access_framework import DataAccessFramework


# Decorador para requerir autenticación
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token requerido"}), 401

        try:
            # Remover "Bearer " del token
            if token.startswith('Bearer '):
                token = token[7:]

            # Decodificar token
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['user_id']

            # Verificar que jugador existe
            player_repo = current_app.framework.get_repository('Player')
            player = player_repo.load(current_user_id)
            if not player or not player.active:
                return jsonify({"error": "Jugador no válido"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401

        # Agregar jugador al request
        request.current_user = player
        return f(*args, **kwargs)

    return decorated


# Función para generar tokens JWT
def generate_token(user_id: str, app: Flask) -> str:
    """Generar token JWT para usuario."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24),  # 24 horas
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')


def create_app(framework: DataAccessFramework) -> Flask:
    """
    Crear aplicación Flask configurada.

    Args:
        framework: Instancia del framework

    Returns:
        Flask app configurada
    """
    app = Flask(__name__)

    # Configuración
    app.config['SECRET_KEY'] = framework.config_manager.get('api.jwt_secret', 'default_secret')
    app.config['CORS_ENABLED'] = framework.config_manager.get('api.cors_enabled', True)

    if app.config['CORS_ENABLED']:
        CORS(app)

    # Referencia al framework
    app.framework = framework

    # Registrar rutas
    _register_routes(app)

    return app


def _register_routes(app: Flask):
    """Registrar todas las rutas de la API."""

    @app.route('/', methods=['GET'])
    def index():
        """Ruta raíz - Documentación de la API."""
        return jsonify({
            "message": "🚀 NousData-Lab API Framework v2.0.0",
            "description": "Framework de acceso a datos con API REST para videojuegos",
            "endpoints": {
                "system": {
                    "/": "Documentación de la API (esta página)",
                    "/health": "Health check del servidor",
                    "/stats": "Estadísticas del sistema"
                },
                "authentication": {
                    "/api/auth/login": "POST - Autenticar usuario",
                    "/api/auth/register": "POST - Registrar nuevo usuario",
                    "/api/auth/profile": "GET - Ver perfil (requiere token)",
                    "/api/auth/profile": "PUT - Actualizar perfil (requiere token)"
                },
                "games": {
                    "/api/games": "GET - Listar juegos (filtros: genre, platform, studio, min_rating, search)",
                    "/api/games/<id>": "GET - Obtener juego por ID",
                    "/api/games": "POST - Crear nuevo juego (requiere token)",
                    "/api/games/<id>": "PUT - Actualizar juego (requiere token)",
                    "/api/games/<id>": "DELETE - Eliminar juego (requiere token)",
                    "/api/games/trending": "GET - Juegos trending",
                    "/api/games/<id>/stats": "GET - Estadísticas del juego"
                },
                "sessions": {
                    "/api/sessions": "GET - Listar sesiones (filtros: player_id, game_id, status)",
                    "/api/sessions": "POST - Crear sesión/comprar juego (requiere token)",
                    "/api/sessions/<id>": "GET - Obtener sesión por ID (requiere token)",
                    "/api/sessions/<id>/playtime": "POST - Añadir horas y logros (requiere token)",
                    "/api/sessions/<id>/complete": "POST - Completar juego (requiere token)",
                    "/api/sessions/player/<id>/library": "GET - Biblioteca del jugador",
                    "/api/sessions/player/<id>/stats": "GET - Estadísticas del jugador"
                }
            },
            "authentication": "La mayoría de endpoints requieren token JWT. Obtén uno en /api/auth/login",
            "usage": "Incluye el token en el header: Authorization: Bearer <token>"
        })

    @app.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de health check."""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        })

    @app.route('/stats', methods=['GET'])
    def get_stats():
        """Obtener estadísticas del sistema."""
        try:
            stats = app.framework.get_stats()
            return jsonify(stats)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Incluir rutas específicas
    from .routes.games import bp as games_bp
    from .routes.auth import bp as auth_bp
    from .routes.sessions import bp as sessions_bp

    # Registrar blueprints
    app.register_blueprint(games_bp)
    app.register_blueprint(sessions_bp)
    app.register_blueprint(auth_bp)

    # Middleware de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Error interno del servidor"}), 500