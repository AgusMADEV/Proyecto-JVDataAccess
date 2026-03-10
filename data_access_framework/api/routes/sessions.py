"""
Game Sessions API Routes - Endpoints de gestión de sesiones de juego

Maneja operaciones CRUD para sesiones de juego y compras.

Autor: DAM2526
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from ..app import token_required

bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')


@bp.route('', methods=['GET'])
def get_sessions():
    """Obtener lista de sesiones con filtros opcionales."""
    try:
        # Parámetros de consulta
        player_id = request.args.get('player_id')
        game_id = request.args.get('game_id')
        status = request.args.get('status')  # active, completed, abandoned
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))

        session_repo = current_app.framework.get_repository('GameSession')
        
        # Obtener sesiones según filtros
        if player_id:
            sessions = session_repo.find_by(player_id=player_id)
        elif game_id:
            sessions = session_repo.find_by(game_id=game_id)
        else:
            sessions = session_repo.load_all()
        
        # Filtrar por status
        if status:
            sessions = [s for s in sessions if s.status == status]

        # Paginación
        start = (page - 1) * per_page
        end = start + per_page
        paginated_sessions = sessions[start:end]

        # Convertir a diccionarios
        result = []
        for session in paginated_sessions:
            result.append({
                "id": session.id,
                "player_id": session.player_id,
                "game_id": session.game_id,
                "purchase_date": session.purchase_date.isoformat(),
                "playtime_hours": session.playtime_hours,
                "completed": session.completed,
                "achievements_unlocked": session.achievements_unlocked,
                "last_played": session.last_played.isoformat() if session.last_played else None,
                "status": session.status,
                "rating": session.rating,
                "notes": session.notes
            })

        return jsonify({
            "sessions": result,
            "total": len(sessions),
            "page": page,
            "per_page": per_page,
            "pages": (len(sessions) + per_page - 1) // per_page
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<session_id>', methods=['GET'])
def get_session(session_id):
    """Obtener detalles de una sesión específica."""
    try:
        session_repo = current_app.framework.get_repository('GameSession')
        session = session_repo.load(session_id)

        if not session:
            return jsonify({"error": "Sesión no encontrada"}), 404

        # Obtener información del juego y jugador
        game_repo = current_app.framework.get_repository('Game')
        player_repo = current_app.framework.get_repository('Player')
        
        game = game_repo.load(session.game_id)
        player = player_repo.load(session.player_id)

        return jsonify({
            "id": session.id,
            "player_id": session.player_id,
            "game_id": session.game_id,
            "purchase_date": session.purchase_date.isoformat(),
            "playtime_hours": session.playtime_hours,
            "completed": session.completed,
            "achievements_unlocked": session.achievements_unlocked,
            "last_played": session.last_played.isoformat() if session.last_played else None,
            "status": session.status,
            "rating": session.rating,
            "notes": session.notes,
            "days_since_last_played": session.days_since_last_played,
            "game": {
                "id": game.id,
                "title": game.title,
                "platform": game.platform,
                "genre": game.genre,
                "rating": game.rating
            } if game else None,
            "player": {
                "id": player.id,
                "username": player.username,
                "level": player.level
            } if player else None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('', methods=['POST'])
@token_required
def create_session(current_user):
    """Crear una nueva sesión de juego (compra)."""
    try:
        data = request.get_json()

        # Validar campos requeridos
        if 'game_id' not in data:
            return jsonify({"error": "game_id es requerido"}), 400
        
        # Por defecto el jugador es el usuario actual
        player_id = data.get('player_id', current_user.id)
        
        # Solo admin puede crear sesiones para otros jugadores
        if player_id != current_user.id and current_user.role != 'admin':
            return jsonify({"error": "No puedes crear sesiones para otros jugadores"}), 403

        session_service = current_app.framework.get_service('session')
        
        try:
            session = session_service.create_session(
                game_id=data['game_id'],
                player_id=player_id
            )

            return jsonify({
                "message": "Juego comprado exitosamente",
                "session_id": session.id,
                "session": {
                    "id": session.id,
                    "game_id": session.game_id,
                    "player_id": session.player_id,
                    "purchase_date": session.purchase_date.isoformat()
                }
            }), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<session_id>/playtime', methods=['POST'])
@token_required
def add_playtime(current_user, session_id):
    """Añadir horas de juego a una sesión."""
    try:
        data = request.get_json()

        if 'hours' not in data:
            return jsonify({"error": "hours es requerido"}), 400

        hours = float(data['hours'])
        achievements = int(data.get('achievements', 0))

        session_service = current_app.framework.get_service('session')
        
        # Verificar que la sesión pertenece al usuario actual o es admin
        session_repo = current_app.framework.get_repository('GameSession')
        session = session_repo.load(session_id)
        
        if not session:
            return jsonify({"error": "Sesión no encontrada"}), 404
        
        if session.player_id != current_user.id and current_user.role != 'admin':
            return jsonify({"error": "No puedes modificar sesiones de otros jugadores"}), 403

        result = session_service.add_playtime(session_id, hours, achievements)

        return jsonify({
            "message": "Tiempo de juego añadido exitosamente",
            **result
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<session_id>/complete', methods=['POST'])
@token_required
def mark_completed(current_user, session_id):
    """Marcar un juego como completado."""
    try:
        data = request.get_json() or {}
        rating = data.get('rating')

        session_service = current_app.framework.get_service('session')
        
        # Verificar permisos
        session_repo = current_app.framework.get_repository('GameSession')
        session = session_repo.load(session_id)
        
        if not session:
            return jsonify({"error": "Sesión no encontrada"}), 404
        
        if session.player_id != current_user.id and current_user.role != 'admin':
            return jsonify({"error": "No puedes modificar sesiones de otros jugadores"}), 403

        session = session_service.mark_completed(session_id, rating)

        return jsonify({
            "message": "Juego marcado como completado",
            "session": {
                "id": session.id,
                "status": session.status,
                "completed": session.completed,
                "rating": session.rating
            }
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<session_id>/abandon', methods= ['POST'])
@token_required
def mark_abandoned(current_user, session_id):
    """Marcar un juego como abandonado."""
    try:
        session_service = current_app.framework.get_service('session')
        
        # Verificar permisos
        session_repo = current_app.framework.get_repository('GameSession')
        session = session_repo.load(session_id)
        
        if not session:
            return jsonify({"error": "Sesión no encontrada"}), 404
        
        if session.player_id != current_user.id and current_user.role != 'admin':
            return jsonify({"error": "No puedes modificar sesiones de otros jugadores"}), 403

        session = session_service.mark_abandoned(session_id)

        return jsonify({
            "message": "Juego marcado como abandonado",
            "session": {
                "id": session.id,
                "status": session.status
            }
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/player/<player_id>/library', methods=['GET'])
def get_player_library(player_id):
    """Obtener biblioteca de juegos de un jugador."""
    try:
        session_service = current_app.framework.get_service('session')
        library = session_service.get_player_library(player_id)

        result = []
        for session in library:
            result.append({
                "id": session.id,
                "game_id": session.game_id,
                "purchase_date": session.purchase_date.isoformat(),
                "playtime_hours": session.playtime_hours,
                "completed": session.completed,
                "status": session.status,
                "rating": session.rating
            })

        return jsonify({
            "player_id": player_id,
            "library": result,
            "total_games": len(result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/player/<player_id>/stats', methods=['GET'])
def get_player_stats(player_id):
    """Obtener estadísticas de un jugador."""
    try:
        session_service = current_app.framework.get_service('session')
        stats = session_service.get_player_stats(player_id)
        
        return jsonify(stats)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/completed', methods=['GET'])
def get_completed_sessions():
    """Obtener todas las sesiones completadas."""
    try:
        session_service = current_app.framework.get_service('session')
        sessions = session_service.get_completed_sessions()

        result = []
        for session in sessions:
            result.append({
                "id": session.id,
                "player_id": session.player_id,
                "game_id": session.game_id,
                "playtime_hours": session.playtime_hours,
                "achievements_unlocked": session.achievements_unlocked,
                "rating": session.rating,
                "completed_date": session.updated_at.isoformat() if session.updated_at else None
            })

        return jsonify({
            "completed_sessions": result,
            "total": len(result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
