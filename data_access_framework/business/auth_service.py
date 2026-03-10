"""Auth Service - Servicio de autenticacion y autorizacion.

Maneja login, registro de usuarios y control de permisos
con hashing salteado (HMAC-SHA256).
"""

import hashlib
import secrets
from datetime import datetime
from typing import Optional, Dict, Any

from ..core.entity_manager import EntityManager
from ..models import Player


class AuthService:
    """
    Servicio que maneja autenticación y autorización de jugadores.
    """

    def __init__(self, entity_manager: EntityManager):
        """
        Inicializar servicio de autenticación.

        Args:
            entity_manager: Gestor de entidades
        """
        self.entity_manager = entity_manager
        self.player_repo = entity_manager.get_repository(Player)

    def authenticate(self, email: str, password: str) -> Optional[Player]:
        """
        Autenticar jugador con email y contraseña.

        Args:
            email: Email del jugador
            password: Contraseña en texto plano

        Returns:
            Player si autenticación exitosa, None si falla
        """
        # Buscar jugador por email
        players = self.player_repo.find_by(email=email)
        if not players:
            return None

        player = players[0]  # Asumimos que email es único

        # Verificar que jugador esté activo
        if not player.active:
            return None

        # Verificar contraseña
        if not player.check_password(password):
            return None

        return player

    def register_player(self, username: str, email: str,
                     password: str, role: str = "player") -> Player:
        """
        Registrar un nuevo jugador.

        Args:
            username: Nombre de usuario único
            email: Email único del jugador
            password: Contraseña en texto plano
            role: Rol del jugador (player, admin, moderator)

        Returns:
            Player: Jugador creado

        Raises:
            ValueError: Si el email o username ya existe o datos inválidos
        """
        # Verificar que el email no esté registrado
        existing_players = self.player_repo.find_by(email=email)
        if existing_players:
            raise ValueError(f"Email ya registrado: {email}")

        # Validar rol
        if role not in ["player", "admin", "moderator"]:
            raise ValueError(f"Rol inválido: {role}")

        # Crear jugador
        player = Player(
            username=username,
            email=email,
            role=role,
            active=True
        )

        # Hashear contraseña
        player.set_password(password)

        # Guardar jugador
        success = self.player_repo.save(player)
        if not success:
            raise RuntimeError("Error al guardar el jugador")

        return player

    def change_password(self, player_id: str, old_password: str, new_password: str) -> bool:
        """
        Cambiar contraseña de un jugador.

        Args:
            player_id: ID del jugador
            old_password: Contraseña actual
            new_password: Nueva contraseña

        Returns:
            bool: True si cambió exitosamente
        """
        player = self.player_repo.load(player_id)
        if not player:
            raise ValueError(f"Jugador no encontrado: {player_id}")

        # Verificar contraseña actual
        if not player.check_password(old_password):
            raise ValueError("Contraseña actual incorrecta")

        # Validar nueva contraseña
        if len(new_password) < 6:
            raise ValueError("La nueva contraseña debe tener al menos 6 caracteres")

        # Cambiar contraseña
        player.set_password(new_password)

        return self.player_repo.save(player)

    def deactivate_player(self, player_id: str, admin_player_id: str) -> bool:
        """
        Desactivar cuenta de jugador (solo admin).

        Args:
            player_id: ID del jugador a desactivar
            admin_player_id: ID del admin que realiza la acción

        Returns:
            bool: True si desactivó exitosamente
        """
        # Verificar permisos de admin
        admin = self.player_repo.load(admin_player_id)
        if not admin or admin.role != "admin":
            raise ValueError("Solo administradores pueden desactivar jugadores")

        # No permitir desactivar a sí mismo
        if player_id == admin_player_id:
            raise ValueError("No puedes desactivar tu propia cuenta")

        # Desactivar jugador
        player = self.player_repo.load(player_id)
        if not player:
            raise ValueError(f"Jugador no encontrado: {player_id}")

        player.active = False

        return self.player_repo.save(player)

    def update_player_profile(self, player_id: str, updates: Dict[str, Any]) -> bool:
        """
        Actualizar perfil de jugador.

        Args:
            player_id: ID del jugador
            updates: Campos a actualizar

        Returns:
            bool: True si actualizó exitosamente
        """
        player = self.player_repo.load(player_id)
        if not player:
            raise ValueError(f"Jugador no encontrado: {player_id}")

        # Campos permitidos para actualización
        allowed_fields = ["username", "email"]

        for field, value in updates.items():
            if field in allowed_fields:
                # Verificar email único si se cambia
                if field == "email" and value != player.email:
                    existing = self.player_repo.find_by(email=value)
                    if existing:
                        raise ValueError(f"Email ya en uso: {value}")

                setattr(player, field, value)
            else:
                raise ValueError(f"Campo no permitido para actualización: {field}")

        return self.player_repo.save(player)

    def authorize(self, player: Player, action: str, resource: str = None) -> bool:
        """
        Verificar si un jugador tiene permisos para una acción.

        Args:
            player: Jugador a verificar
            action: Acción a realizar (read, write, delete, admin)
            resource: Recurso específico (opcional)

        Returns:
            bool: True si tiene permisos
        """
        if not player or not player.active:
            return False

        # Definir permisos por rol
        permissions = {
            "player": ["read"],
            "moderator": ["read", "write"],
            "admin": ["read", "write", "delete", "admin"]
        }

        player_permissions = permissions.get(player.role, [])

        # Acciones básicas
        if action in player_permissions:
            return True

        # Permisos especiales
        if action == "admin" and player.role == "admin":
            return True

        # Permisos sobre recursos propios
        if resource and resource == player.id:
            return action in ["read", "write"]

        return False

    def get_player_permissions(self, player: Player) -> Dict[str, Any]:
        """
        Obtener permisos detallados de un jugador.

        Args:
            player: Jugador

        Returns:
            Dict con permisos
        """
        return {
            "role": player.role,
            "can_read": self.authorize(player, "read"),
            "can_write": self.authorize(player, "write"),
            "can_delete": self.authorize(player, "delete"),
            "is_admin": player.role == "admin",
            "is_moderator": player.role == "moderator"
        }

    def reset_password(self, email: str, new_password: str) -> bool:
        """
        Resetear contraseña (solo para administradores en producción).

        Args:
            email: Email del jugador
            new_password: Nueva contraseña

        Returns:
            bool: True si reseteó exitosamente
        """
        players = self.player_repo.find_by(email=email)
        if not players:
            return False  # No revelar si email existe

        player = players[0]
        player.set_password(new_password)

        return self.player_repo.save(player)

    def get_player_by_email(self, email: str) -> Optional[Player]:
        """
        Obtener jugador por email.

        Args:
            email: Email del jugador

        Returns:
            Player o None si no existe
        """
        players = self.player_repo.find_by(email=email)
        return players[0] if players else None

    def list_players(self, active_only: bool = True) -> list:
        """
        Listar jugadores con filtros.

        Args:
            active_only: Solo jugadores activos

        Returns:
            Lista de jugadores
        """
        all_players = self.player_repo.load_all()

        if active_only:
            return [player for player in all_players if player.active]

        return all_players