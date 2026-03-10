#!/usr/bin/env python3
"""
Demo simple del Framework de Acceso a Datos - Sistema de Videojuegos
"""

from data_access_framework import create_framework
from data_access_framework.models import Game, Studio

def main():
    print("🚀 Iniciando demo del framework...")

    # Crear framework con SQLite
    framework = create_framework(data_format='sqlite')

    # Obtener repositorios
    game_repo = framework.get_repository('Game')
    studio_repo = framework.get_repository('Studio')

    print("✅ Framework inicializado")

    # Crear y guardar estudio
    estudio = Studio(
        name='Demo Studio',
        founded_year=2020,
        country='España'
    )
    studio_repo.save(estudio)
    print(f"✅ Estudio guardado: {estudio.name}")

    # Crear y guardar juego
    juego = Game(
        title='Juego Demo',
        studio_id=estudio.id,
        platform='PC',
        genre='Aventura',
        release_year=2024,
        rating=8.5,
        price=29.99,
        playtime_hours=15
    )
    game_repo.save(juego)
    print(f"✅ Juego guardado: {juego.title}")

    # Mostrar estadísticas
    juegos = game_repo.load_all()
    estudios = studio_repo.load_all()

    print("\n📊 Estadísticas:")
    print(f"   🎮 Juegos totales: {len(juegos)}")
    print(f"   🏢 Estudios totales: {len(estudios)}")

    # Buscar juego
    juego_encontrado = game_repo.load(juego.id)
    if juego_encontrado:
        print(f"\n🔍 Juego encontrado: {juego_encontrado.title}")
        print(f"   Estudio ID: {juego_encontrado.studio_id}")
        print(f"   Plataforma: {juego_encontrado.platform}")
        print(f"   Rating: {juego_encontrado.rating}/10")

    print("\n🎉 ¡Demo completado exitosamente!")

if __name__ == '__main__':
    main()