"""
Game Session Service - Servicio de gestión de sesiones de juego

Implementa la lógica de negocio para compras de juegos, sesiones de juego,
tracking de horas jugadas, logros y estadísticas.

Autor: DAM2526
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from ..core.entity_manager import EntityManager
from ..models import GameSession, Game, Player


class GameSessionService:
    """
    Servicio que maneja toda la lógica de negocio relacionada
    con sesiones de juego y compras.
    """

    def __init__(self, entity_manager: EntityManager, config: Dict[str, Any] = None):
        """
        Inicializar servicio de sesiones de juego.

        Args:
            entity_manager: Gestor de entidades
            config: Configuración del servicio
        """
        self.entity_manager = entity_manager
        self.config = config or {
            "max_active_games": 10,
            "achievement_threshold": 50,
            "hours_for_completion": 20
        }

    def create_session(self, game_id: str, player_id: str) -> GameSession:
        """
        Crear una nueva sesión de juego (compra).

        Args:
            game_id: ID del juego a comprar
            player_id: ID del jugador que compra

        Returns:
            GameSession: Instancia de la sesión creada

        Raises:
            ValueError: Si las validaciones fallan
        """
        # Validar que el juego existe y está disponible
        game_repo = self.entity_manager.get_repository(Game)
        game = game_repo.load(game_id)
        if not game:
            raise ValueError(f"Juego no encontrado: {game_id}")

        if not game.available:
            raise ValueError(f"Juego no disponible: {game.title}")

        # Validar que el jugador existe y está activo
        player_repo = self.entity_manager.get_repository(Player)
        player = player_repo.load(player_id)
        if not player:
            raise ValueError(f"Jugador no encontrado: {player_id}")

        if not player.active:
            raise ValueError(f"Jugador inactivo: {player.display_name}")

        # Verificar límite de juegos activos por jugador
        active_sessions = self.get_active_sessions_by_player(player_id)
        if len(active_sessions) >= self.config["max_active_games"]:
            raise ValueError(f"Jugador ha alcanzado el límite de juegos activos ({self.config['max_active_games']})")

        # Verificar que el jugador no tenga ya este juego
        for session in active_sessions:
            if session.game_id == game_id:
                raise ValueError(f"Jugador ya posee este juego: {game.title}")

        # Crear sesión de juego
        session = GameSession(
            game_id=game_id,
            player_id=player_id,
            purchase_date=datetime.now(),
            status="active"
        )

        # Guardar sesión
        session_repo = self.entity_manager.get_repository(GameSession)
        success = session_repo.save(session)
        if not success:
            raise RuntimeError("Error al guardar la sesión de juego")

        return session

    def add_playtime(self, session_id: str, hours: float, achievements: int = 0) -> Dict[str, Any]:
        """
        Añadir horas de juego a una sesión.

        Args:
            session_id: ID de la sesión
            hours: Horas jugadas
            achievements: Logros desbloqueados en esta sesión

        Returns:
            Dict con información actualizada de la sesión
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        session = session_repo.load(session_id)

        if not session:
            raise ValueError(f"Sesión no encontrada: {session_id}")

        if session.status in ["abandoned"]:
            raise ValueError(f"No se puede añadir tiempo a una sesión abandonada")

        # Añadir horas de juego
        session.add_playtime(hours)
        session.achievements_unlocked += achievements

        # Actualizar nivel del jugador
        player_repo = self.entity_manager.get_repository(Player)
        player = player_repo.load(session.player_id)
        if player:
            player.add_playtime(hours)
            player_repo.save(player)

        # Verificar si completó el juego (basado en horas estimadas)
        game_repo = self.entity_manager.get_repository(Game)
        game = game_repo.load(session.game_id)
        if game and game.playtime_hours > 0:
            completion_ratio = session.playtime_hours / game.playtime_hours
            if completion_ratio >= 0.8 and not session.completed:
                session.mark_completed()

        session_repo.save(session)

        return {
            "session_id": session_id,
            "total_playtime": session.playtime_hours,
            "achievements": session.achievements_unlocked,
            "completed": session.completed,
            "status": session.status,
            "player_level": player.level if player else None
        }

    def mark_completed(self, session_id: str, rating: float = None) -> GameSession:
        """
        Marcar un juego como completado.

        Args:
            session_id: ID de la sesión
            rating: Calificación opcional del jugador (0-10)

        Returns:
            GameSession actualizada
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        session = session_repo.load(session_id)

        if not session:
            raise ValueError(f"Sesión no encontrada: {session_id}")

        session.mark_completed()
        if rating is not None:
            if rating < 0 or rating > 10:
                raise ValueError("La calificación debe estar entre 0 y 10")
            session.rating = rating

        session_repo.save(session)
        return session

    def mark_abandoned(self, session_id: str) -> GameSession:
        """
        Marcar un juego como abandonado.

        Args:
            session_id: ID de la sesión

        Returns:
            GameSession actualizada
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        session = session_repo.load(session_id)

        if not session:
            raise ValueError(f"Sesión no encontrada: {session_id}")

        session.mark_abandoned()
        session_repo.save(session)
        return session

    def get_active_sessions(self) -> List[GameSession]:
        """
        Obtener todas las sesiones activas.

        Returns:
            Lista de sesiones activas
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        all_sessions = session_repo.load_all()
        return [s for s in all_sessions if s.status == "active"]

    def get_completed_sessions(self) -> List[GameSession]:
        """
        Obtener sesiones completadas.

        Returns:
            Lista de sesiones completadas
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        all_sessions = session_repo.load_all()
        return [s for s in all_sessions if s.status == "completed"]

    def get_active_sessions_by_player(self, player_id: str) -> List[GameSession]:
        """
        Obtener sesiones activas de un jugador.

        Args:
            player_id: ID del jugador

        Returns:
            Lista de sesiones activas del jugador
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        player_sessions = session_repo.find_by(player_id=player_id)
        return [s for s in player_sessions if s.status == "active"]

    def get_player_library(self, player_id: str) -> List[GameSession]:
        """
        Obtener biblioteca completa de juegos de un jugador.

        Args:
            player_id: ID del jugador

        Returns:
            Lista de todas las sesiones del jugador
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        return session_repo.find_by(player_id=player_id)

    def get_game_sessions(self, game_id: str) -> List[GameSession]:
        """
        Obtener todas las sesiones de un juego específico.

        Args:
            game_id: ID del juego

        Returns:
            Lista de sesiones del juego
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        return session_repo.find_by(game_id=game_id)

    def get_player_stats(self, player_id: str) -> Dict[str, Any]:
        """
        Obtener estadísticas de un jugador.

        Args:
            player_id: ID del jugador

        Returns:
            Dict con estadísticas del jugador
        """
        player_repo = self.entity_manager.get_repository(Player)
        player = player_repo.load(player_id)

        if not player:
            raise ValueError(f"Jugador no encontrado: {player_id}")

        all_sessions = self.get_player_library(player_id)
        active_sessions = [s for s in all_sessions if s.status == "active"]
        completed_sessions = [s for s in all_sessions if s.status == "completed"]
        abandoned_sessions = [s for s in all_sessions if s.status == "abandoned"]

        total_playtime = sum(s.playtime_hours for s in all_sessions)
        total_achievements = sum(s.achievements_unlocked for s in all_sessions)
        avg_rating = sum(s.rating for s in all_sessions if s.rating) / len([s for s in all_sessions if s.rating]) if any(s.rating for s in all_sessions) else 0

        return {
            "player_id": player_id,
            "username": player.username,
            "level": player.level,
            "total_games": len(all_sessions),
            "active_games": len(active_sessions),
            "completed_games": len(completed_sessions),
            "abandoned_games": len(abandoned_sessions),
            "completion_rate": (len(completed_sessions) / len(all_sessions) * 100) if all_sessions else 0,
            "total_playtime_hours": total_playtime,
            "total_achievements": total_achievements,
            "average_rating": round(avg_rating, 2)
        }

    def get_game_stats(self, game_id: str) -> Dict[str, Any]:
        """
        Obtener estadísticas de un juego.

        Args:
            game_id: ID del juego

        Returns:
            Dict con estadísticas del juego
        """
        game_repo = self.entity_manager.get_repository(Game)
        game = game_repo.load(game_id)

        if not game:
            raise ValueError(f"Juego no encontrado: {game_id}")

        sessions = self.get_game_sessions(game_id)
        completed_sessions = [s for s in sessions if s.status == "completed"]

        total_playtime = sum(s.playtime_hours for s in sessions)
        avg_playtime = total_playtime / len(sessions) if sessions else 0
        avg_rating = sum(s.rating for s in sessions if s.rating) / len([s for s in sessions if s.rating]) if any(s.rating for s in sessions) else 0

        return {
            "game_id": game_id,
            "title": game.title,
            "total_players": len(sessions),
            "completions": len(completed_sessions),
            "completion_rate": (len(completed_sessions) / len(sessions) * 100) if sessions else 0,
            "total_playtime_hours": total_playtime,
            "average_playtime": round(avg_playtime, 2),
            "average_rating": round(avg_rating, 2)
        }

    def get_trending_games(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtener juegos más populares (más jugados recientemente).

        Args:
            limit: Número máximo de resultados

        Returns:
            Lista de juegos con estadísticas
        """
        session_repo = self.entity_manager.get_repository(GameSession)
        game_repo = self.entity_manager.get_repository(Game)

        # Obtener sesiones recientes (último mes)
        recent_date = datetime.now() - timedelta(days=30)
        all_sessions = session_repo.load_all()
        recent_sessions = [s for s in all_sessions if s.last_played and s.last_played >= recent_date]

        # Agrupar por juego
        game_playtime = {}
        for session in recent_sessions:
            if session.game_id not in game_playtime:
                game_playtime[session.game_id] = 0
            game_playtime[session.game_id] += session.playtime_hours

        # Ordenar por tiempo de juego
        sorted_games = sorted(game_playtime.items(), key=lambda x: x[1], reverse=True)[:limit]

        # Construir resultado
        trending = []
        for game_id, playtime in sorted_games:
            game = game_repo.load(game_id)
            if game:
                trending.append({
                    "game_id": game_id,
                    "title": game.title,
                    "platform": game.platform,
                    "recent_playtime_hours": playtime,
                    "rating": game.rating
                })

        return trending


# Exportar alias para compatibilidad si es necesario
# LoanService = GameSessionService
