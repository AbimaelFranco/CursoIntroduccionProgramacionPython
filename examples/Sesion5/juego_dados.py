import random

def lanzar_dados():
    """Lanza dos dados y devuelve sus valores como tupla."""
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    return dado1, dado2

def jugar():
    """Ejecuta el ciclo principal del juego de dados."""
    puntuacion = 0
    print("🎲 Bienvenido al juego de dados 🎲")

    while True:
        opcion = input("\n¿Quieres lanzar los dados? (jugar/salir): ").lower()

        if opcion == "salir":
            print(f"\nGracias por jugar. Tu puntuación final es: {puntuacion}")
            break
        elif opcion == "jugar":
            dado1, dado2 = lanzar_dados()
            suma = dado1 + dado2
            puntuacion += suma

            print(f"Lanzaste: {dado1} y {dado2} → total: {suma}")
            print(f"Puntuación acumulada: {puntuacion}")
        else:
            print("⚠️ Opción no válida. Escribe 'jugar' o 'salir'.")

jugar()