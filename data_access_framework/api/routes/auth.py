"""
Auth API Routes - Endpoints de autenticación

Maneja login, registro y gestión de jugadores.

Autor: DAM2526
"""

from flask import Blueprint, request, jsonify, current_app
from ..app import generate_token, token_required

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión y obtener token JWT."""
    try:
        data = request.get_json()

        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email y contraseña requeridos"}), 400

        email = data['email']
        password = data['password']

        # Autenticar jugador
        auth_service = current_app.framework.get_service('auth')
        player = auth_service.authenticate(email, password)

        if not player:
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Generar token
        token = generate_token(player.id, current_app)

        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "player": {
                "id": player.id,
                "username": player.username,
                "email": player.email,
                "role": player.role,
                "level": player.level
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/register', methods=['POST'])
def register():
    """Registrar un nuevo jugador."""
    try:
        data = request.get_json()

        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido: {field}"}), 400

        # Registrar jugador
        auth_service = current_app.framework.get_service('auth')
        player = auth_service.register_player(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'player')
        )

        return jsonify({
            "message": "Jugador registrado exitosamente",
            "player_id": player.id
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Obtener perfil del jugador actual (requiere token)."""
    try:
        # El token_required ya verificó el jugador
        player = request.current_user

        return jsonify({
            "id": player.id,
            "username": player.username,
            "email": player.email,
            "role": player.role,
            "level": player.level,
            "active": player.active,
            "total_playtime_hours": player.total_playtime_hours,
            "created_at": player.created_at.isoformat() if player.created_at else None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Actualizar perfil del jugador actual."""
    try:
        player = request.current_user
        data = request.get_json()

        # Campos permitidos para actualización propia
        allowed_fields = ['username', 'email']

        updates = {}
        for field in allowed_fields:
            if field in data:
                updates[field] = data[field]

        if not updates:
            return jsonify({"error": "No hay campos válidos para actualizar"}), 400

        # Actualizar
        auth_service = current_app.framework.get_service('auth')
        success = auth_service.update_player_profile(player.id, updates)

        if not success:
            return jsonify({"error": "Error al actualizar perfil"}), 500

        return jsonify({"message": "Perfil actualizado exitosamente"})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    """Cambiar contraseña del jugador actual."""
    try:
        player = request.current_user
        data = request.get_json()

        if 'old_password' not in data or 'new_password' not in data:
            return jsonify({"error": "Contraseña actual y nueva requeridas"}), 400

        # Cambiar contraseña
        auth_service = current_app.framework.get_service('auth')
        success = auth_service.change_password(
            player.id,
            data['old_password'],
            data['new_password']
        )

        if not success:
            return jsonify({"error": "Error al cambiar contraseña"}), 500

        return jsonify({"message": "Contraseña cambiada exitosamente"})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/players', methods=['GET'])
@token_required
def list_players():
    """Listar jugadores (solo admin)."""
    try:
        player = request.current_user

        # Verificar permisos de admin
        auth_service = current_app.framework.get_service('auth')
        if not auth_service.authorize(player, 'admin'):
            return jsonify({"error": "Permisos insuficientes"}), 403

        # Listar jugadores
        players = auth_service.list_players(active_only=False)

        result = []
        for p in players:
            result.append({
                "id": p.id,
                "username": p.username,
                "email": p.email,
                "role": p.role,
                "level": p.level,
                "active": p.active,
                "created_at": p.created_at.isoformat() if p.created_at else None
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/players/<player_id>/deactivate', methods=['POST'])
@token_required
def deactivate_player(player_id):
    """Desactivar jugador (solo admin)."""
    try:
        admin = request.current_user

        # Verificar permisos de admin
        auth_service = current_app.framework.get_service('auth')
        if not auth_service.authorize(admin, 'admin'):
            return jsonify({"error": "Permisos insuficientes"}), 403

        # Desactivar jugador
        success = auth_service.deactivate_player(player_id, admin.id)

        if not success:
            return jsonify({"error": "Error al desactivar jugador"}), 500

        return jsonify({"message": "Jugador desactivado exitosamente"})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/permissions', methods=['GET'])
@token_required
def get_permissions():
    """Obtener permisos del jugador actual."""
    try:
        player = request.current_user

        auth_service = current_app.framework.get_service('auth')
        permissions = auth_service.get_player_permissions(player)

        return jsonify(permissions)

    except Exception as e:
        return jsonify({"error": str(e)}), 500