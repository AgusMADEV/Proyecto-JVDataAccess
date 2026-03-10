"""
Games API Routes - Endpoints para gestión de videojuegos

Proporciona operaciones CRUD para juegos vía API REST.

Autor: DAM2526
"""

from flask import Blueprint, request, jsonify, current_app
from ..app import token_required

bp = Blueprint('games', __name__, url_prefix='/api/games')


@bp.route('', methods=['GET'])
def get_games():
    """Obtener lista de juegos con filtros opcionales."""
    try:
        # Obtener parámetros de filtro
        genre = request.args.get('genre')
        platform = request.args.get('platform')
        studio = request.args.get('studio')
        available = request.args.get('available')
        search = request.args.get('search')
        min_rating = request.args.get('min_rating', type=float)

        # Convertir available a boolean
        if available is not None:
            available = available.lower() in ('true', '1', 'yes')

        # Obtener repositorio
        game_repo = current_app.framework.get_repository('Game')
        games = game_repo.load_all()

        # Aplicar filtros
        filtered_games = []
        for game in games:
            # Filtro por género
            if genre and game.genre != genre:
                continue

            # Filtro por plataforma
            if platform and platform not in game.platform:
                continue

            # Filtro por estudio
            if studio and studio not in game.studio_id:
                continue

            # Filtro por disponibilidad
            if available is not None and game.available != available:
                continue

            # Filtro por calificación mínima
            if min_rating and game.rating < min_rating:
                continue

            # Búsqueda por texto
            if search:
                search_lower = search.lower()
                if (search_lower not in game.title.lower() and
                    search_lower not in (game.genre or '').lower() and
                    search_lower not in (game.platform or '').lower()):
                    continue

            filtered_games.append(game)

        # Convertir a dict para JSON
        result = []
        for game in filtered_games:
            game_dict = {
                "id": game.id,
                "title": game.title,
                "studio_id": game.studio_id,
                "platform": game.platform,
                "genre": game.genre,
                "release_year": game.release_year,
                "rating": game.rating,
                "price": game.price,
                "playtime_hours": game.playtime_hours,
                "multiplayer": game.multiplayer,
                "available": game.available,
                "created_at": game.created_at.isoformat() if game.created_at else None
            }
            result.append(game_dict)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<game_id>', methods=['GET'])
def get_game(game_id):
    """Obtener detalles de un juego específico."""
    try:
        game_repo = current_app.framework.get_repository('Game')
        game = game_repo.load(game_id)

        if not game:
            return jsonify({"error": "Juego no encontrado"}), 404

        return jsonify({
            "id": game.id,
            "title": game.title,
            "studio_id": game.studio_id,
            "platform": game.platform,
            "genre": game.genre,
            "release_year": game.release_year,
            "rating": game.rating,
            "price": game.price,
            "playtime_hours": game.playtime_hours,
            "multiplayer": game.multiplayer,
            "genre_id": game.genre_id,
            "available": game.available,
            "created_at": game.created_at.isoformat() if game.created_at else None,
            "updated_at": game.updated_at.isoformat() if game.updated_at else None
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('', methods=['POST'])
@token_required
def create_game(current_user):
    """Crear un nuevo juego."""
    try:
        # Solo admin puede crear juegos
        if current_user.role != 'admin':
            return jsonify({"error": "Permiso denegado"}), 403

        data = request.get_json()

        # Validar campos requeridos
        required_fields = ['title', 'studio_id', 'platform']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido: {field}"}), 400

        # Crear juego
        from data_access_framework.models import Game
        game = Game(
            title=data['title'],
            studio_id=data['studio_id'],
            platform=data['platform'],
            genre=data.get('genre', ''),
            release_year=data.get('release_year', 2024),
            rating=data.get('rating', 0.0),
            price=data.get('price', 0.0),
            playtime_hours=data.get('playtime_hours', 0),
            multiplayer=data.get('multiplayer', False),
            genre_id=data.get('genre_id'),
            available=data.get('available', True)
        )

        # Guardar
        game_repo = current_app.framework.get_repository('Game')
        success = game_repo.save(game)

        if not success:
            return jsonify({"error": "Error al guardar el juego"}), 500

        return jsonify({
            "message": "Juego creado exitosamente",
            "game_id": game.id,
            "game": {
                "id": game.id,
                "title": game.title,
                "platform": game.platform
            }
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<game_id>', methods=['PUT'])
@token_required
def update_game(current_user, game_id):
    """Actualizar un juego existente."""
    try:
        # Solo admin puede actualizar juegos
        if current_user.role != 'admin':
            return jsonify({"error": "Permiso denegado"}), 403

        game_repo = current_app.framework.get_repository('Game')
        game = game_repo.load(game_id)

        if not game:
            return jsonify({"error": "Juego no encontrado"}), 404

        data = request.get_json()

        # Actualizar campos
        if 'title' in data:
            game.title = data['title']
        if 'studio_id' in data:
            game.studio_id = data['studio_id']
        if 'platform' in data:
            game.platform = data['platform']
        if 'genre' in data:
            game.genre = data['genre']
        if 'release_year' in data:
            game.release_year = data['release_year']
        if 'rating' in data:
            game.rating = data['rating']
        if 'price' in data:
            game.price = data['price']
        if 'playtime_hours' in data:
            game.playtime_hours = data['playtime_hours']
        if 'multiplayer' in data:
            game.multiplayer = data['multiplayer']
        if 'available' in data:
            game.available = data['available']

        success = game_repo.save(game)

        if not success:
            return jsonify({"error": "Error al actualizar el juego"}), 500

        return jsonify({
            "message": "Juego actualizado exitosamente",
            "game": {
                "id": game.id,
                "title": game.title,
                "platform": game.platform,
                "rating": game.rating
            }
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<game_id>', methods=['DELETE'])
@token_required
def delete_game(current_user, game_id):
    """Eliminar un juego."""
    try:
        # Solo admin puede eliminar juegos
        if current_user.role != 'admin':
            return jsonify({"error": "Permiso denegado"}), 403

        game_repo = current_app.framework.get_repository('Game')
        game = game_repo.load(game_id)

        if not game:
            return jsonify({"error": "Juego no encontrado"}), 404

        success = game_repo.delete(game_id)

        if not success:
            return jsonify({"error": "Error al eliminar el juego"}), 500

        return jsonify({"message": "Juego eliminado exitosamente"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/platforms', methods=['GET'])
def get_platforms():
    """Obtener lista de plataformas disponibles."""
    platforms = ["PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile", "Multi-platform"]
    return jsonify(platforms)


@bp.route('/trending', methods=['GET'])
def get_trending_games():
    """Obtener juegos en tendencia."""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        session_service = current_app.framework.get_service('session')
        trending = session_service.get_trending_games(limit=limit)
        
        return jsonify(trending)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/<game_id>/stats', methods=['GET'])
def get_game_stats(game_id):
    """Obtener estadísticas de un juego."""
    try:
        session_service = current_app.framework.get_service('session')
        stats = session_service.get_game_stats(game_id)
        
        return jsonify(stats)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
