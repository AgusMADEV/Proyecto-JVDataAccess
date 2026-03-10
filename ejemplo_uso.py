"""
Ejemplo de uso del Data Access Framework

Este archivo muestra cómo utilizar el framework de acceso a datos
para crear una aplicación de gestión de videojuegos simple.

Autor: DAM2526
"""

from data_access_framework import create_framework
from data_access_framework.models import Game, Studio, Player
import json


def main():
    """Ejemplo de uso del framework."""

    # Crear instancia del framework
    framework = create_framework(
        data_format='json',  # Usar JSON para persistencia
        config={
            'api.enabled': True,
            'api.port': 5000,
            'ui.theme': 'corporate'
        }
    )

    print("🚀 Framework inicializado exitosamente!")

    # Obtener servicios
    auth_service = framework.get_service('auth')
    game_repo = framework.get_repository('Game')
    studio_repo = framework.get_repository('Studio')
    player_repo = framework.get_repository('Player')
    session_service = framework.get_service('session')

    print("\n🎮 Creando datos de ejemplo...")

    # Crear estudios de desarrollo
    studio1 = Studio(
        name='CD Projekt Red',
        founded_year=1994,
        country='Polonia',
        website='https://cdprojektred.com',
        description='Creadores de The Witcher y Cyberpunk 2077'
    )
    studio_repo.save(studio1)

    studio2 = Studio(
        name='FromSoftware',
        founded_year=1986,
        country='Japón',
        website='https://www.fromsoftware.jp',
        description='Creadores de Dark Souls, Elden Ring y Sekiro'
    )
    studio_repo.save(studio2)

    print(f"✅ Estudio creado: {studio1.display_name}")
    print(f"✅ Estudio creado: {studio2.display_name}")

    # Crear juegos
    game1 = Game(
        title='The Witcher 3: Wild Hunt',
        studio_id=studio1.id,
        platform='Multi-platform',
        genre='RPG',
        release_year=2015,
        rating=9.5,
        price=39.99,
        playtime_hours=100,
        multiplayer=False,
        available=True
    )
    game_repo.save(game1)

    game2 = Game(
        title='Elden Ring',
        studio_id=studio2.id,
        platform='Multi-platform',
        genre='Action RPG',
        release_year=2022,
        rating=9.7,
        price=59.99,
        playtime_hours=80,
        multiplayer=True,
        available=True
    )
    game_repo.save(game2)

    print(f"✅ Juego creado: {game1.title}")
    print(f"✅ Juego creado: {game2.title}")

    # Crear jugador (o usar existente)
    existing_players = player_repo.find_by(email='gamer@email.com')
    if existing_players:
        player = existing_players[0]
        print(f"✅ Jugador existente encontrado: {player.username} ({player.email})")
    else:
        # Crear jugador directamente
        player = Player(
            username='ProGamer123',
            email='gamer@email.com',
            role='player',
            active=True,
            level=1
        )
        player.set_password('password123')
        player_repo.save(player)
        print(f"✅ Jugador creado: {player.username} ({player.email})")

    # Crear sesión de juego (compra)
    try:
        session = session_service.create_session(
            player_id=player.id,
            game_id=game1.id
        )
        session_created = True
        print(f"✅ Juego comprado: {game1.title} -> {player.username}")
        print(f"   Fecha de compra: {session.purchase_date.strftime('%Y-%m-%d')}")
        
        # Añadir horas de juego
        result = session_service.add_playtime(session.id, hours=15.5, achievements=5)
        print(f"✅ Añadidas 15.5 horas de juego y 5 logros")
        print(f"   Total de horas: {result['total_playtime']}")
        print(f"   Nivel del jugador: {result['player_level']}")
        
    except ValueError as e:
        print(f"⚠️ No se pudo crear sesión: {e}")
        print("ℹ️ Continuando con el ejemplo...")
        session_created = False

    # Obtener estadísticas
    stats = framework.get_stats()
    print("\n📊 Estadísticas del sistema:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    # Obtener estadísticas del jugador
    if player:
        player_stats = session_service.get_player_stats(player.id)
        print("\n🎮 Estadísticas del jugador:")
        print(f"  - Usuario: {player_stats['username']}")
        print(f"  - Nivel: {player_stats['level']}")
        print(f"  - Total de juegos: {player_stats['total_games']}")
        print(f"  - Juegos completados: {player_stats['completed_games']}")
        print(f"  - Horas totales jugadas: {player_stats['total_playtime_hours']:.1f}")
        print(f"  - Logros totales: {player_stats['total_achievements']}")

    # Juegos en tendencia
    trending = session_service.get_trending_games(limit=5)
    if trending:
        print("\n🔥 Juegos en tendencia:")
        for idx, game in enumerate(trending, 1):
            print(f"  {idx}. {game['title']} ({game['platform']}) - Rating: {game['rating']}")

    print("\n🎉 ¡Ejemplo completado exitosamente!")
    print("💡 El framework está listo para usar en tus aplicaciones!")

    # Iniciar API si está habilitada
    if framework.config_manager.get('api.enabled', False):
        print("\n🌐 Iniciando API REST...")
        framework.start_api()
    else:
        print("\nℹ️  Ejecuta con api.enabled=True para iniciar el servidor REST.")


if __name__ == '__main__':
    main()