# 🎮 Juego de Preguntas con Diccionario y Funciones

# -----------------------------
# Diccionario de preguntas
# -----------------------------
PREGUNTAS = {
    1: {"pregunta": "¿Cuál es la capital de Francia?", "respuesta": "paris"},
    2: {"pregunta": "¿Cuánto es 5 + 7?", "respuesta": "12"},
    3: {"pregunta": "¿Cuál es el color resultante de mezclar rojo y azul?", "respuesta": "morado"},
    4: {"pregunta": "¿Cómo se le llama a la estrella del sistema solar?", "respuesta": "sol"}
}


# -----------------------------
# Funciones principales
# -----------------------------
def mostrar_menu():
# Muestra el menú principal del juego y devuelve la opción elegida.
    print("\n🎮 ¡Bienvenido al juego de preguntas!")
    print("1. Jugar")
    print("2. Ver puntuación anterior")
    print("3. Agregar nueva pregunta")
    print("4. Salir")
    return input("Elige una opción (1-4): ")


def seleccionar_dificultad():
#Permite elegir la dificultad y devuelve las vidas iniciales.
    while True:
        print("\nSelecciona dificultad:")
        print("1. Fácil - 5 vidas")
        print("2. Difícil - 3 vidas")
        print("3. Experto - 1 vida")
        opcion = input("Selecciona la dificultad (1-3): ")

        if opcion == "1":
            return 5, opcion
        elif opcion == "2":
            return 3, opcion
        elif opcion == "3":
            return 1, opcion
        else:
            print("Selección incorrecta")


def hacer_pregunta(pregunta, respuesta_correcta, vidas, puntuacion, errores, dificultad, es_tercera):
#Realiza una pregunta al jugador y actualiza puntuación, errores y vidas.
    while True:
        respuesta = input(pregunta + " ").lower()
        if respuesta == respuesta_correcta:
            puntuacion += 25
            print(f"✅ Correcto! Puntuación actual: {puntuacion}")

            # Vida extra en la tercera pregunta si no es dificultad "experto"
            if es_tercera and dificultad != "3":
                vidas += 1
                print("💚 Ganaste una vida extra!")

            return vidas, puntuacion, errores, False
        else:
            errores += 1
            print(f"❌ Incorrecto. Llevas {errores} fallos.")

            if errores >= vidas:
                print("💀 Has perdido. Demasiados errores.")
                return vidas, puntuacion, errores, True


def jugar_partida():
#Ejecuta una partida completa del juego.
    vidas, dificultad = seleccionar_dificultad()
    errores = 0
    puntuacion = 0

    print("\n¡Comienza el juego!")

    for i, datos in PREGUNTAS.items():
        pregunta = datos["pregunta"]
        respuesta = datos["respuesta"]

        es_tercera = (i == 3)  # Pregunta especial con vida extra
        vidas, puntuacion, errores, perdido = hacer_pregunta(
            pregunta, respuesta, vidas, puntuacion, errores, dificultad, es_tercera
        )

        if perdido:
            break

    jugador = input("\nIngresa el nombre del jugador: ")
    return jugador, puntuacion


def agregar_pregunta():
#Permite al usuario agregar una nueva pregunta al diccionario.
    nueva_pregunta = input("Escribe la nueva pregunta: ")
    nueva_respuesta = input("Escribe la respuesta correcta: ").lower()
    nuevo_id = max(PREGUNTAS.keys()) + 1  # siguiente clave numérica
    PREGUNTAS[nuevo_id] = {"pregunta": nueva_pregunta, "respuesta": nueva_respuesta}
    print("✅ Pregunta agregada correctamente.")


# -----------------------------
# Programa principal
# -----------------------------
def main():
    ultimo_nombre = ""
    ultima_puntuacion = 0

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            ultimo_nombre, ultima_puntuacion = jugar_partida()
            print("👋 ¡Gracias por jugar!")

        elif opcion == "2":
            print(f"El último jugador fue {ultimo_nombre} con una puntuación de {ultima_puntuacion}")

        elif opcion == "3":
            agregar_pregunta()

        elif opcion == "4":
          print("👋 ¡Gracias por jugar!")
          break

        else:
            print("❌ Opción no válida")


# -----------------------------
# Ejecutar programa
# -----------------------------
if __name__ == "__main__":  #Esta linea permite ejecutar el codigo al correr el script
    main()