# Preguntas y respuestas
pregunta1 = "¿Cuál es la capital de Francia?"
respuesta1 = "paris"

pregunta2 = "¿Cuánto es 5 + 7?"
respuesta2 = "12"

pregunta3 = "¿Cuál es el color resultante de mezclar rojo y azul?"
respuesta3 = "morado"

pregunta4 = "¿Cómo se le llama a la estrella del sistema solar"
respuesta4 = "sol"

ultimo_nombre = ""
ultima_puntuacion = 0

while True:
    print("🎮 ¡Bienvenido al juego de preguntas!")
    print("1. jugar")
    print("2. ver puntuacion anterior")
    print("3. salir")
    opcion = input("Elige una opción (1-3): ")

    if opcion == "1":
        while True:
            print("1. Fácil - 5 vidas")
            print("2. Dificil - 3 vidas")
            print("3. Experto - 1 vida")
            dificultad = input("Selecciona la dificultad (1-3): ")
            # Variables de control
            if dificultad == "1":
                vidas_iniciales = 5
                break
            elif dificultad == "2":
                vidas_iniciales = 3
                break
            elif dificultad == "3":
                vidas_iniciales = 1
                break
            else:
                print("Selección incorrecta")

        vidas_juego = vidas_iniciales
        errores = 0
        puntuacion = 0

        print("\n¡Comienza el juego!")

        # Pregunta 1
        while True:
            respuesta = input(pregunta1 + " ")
            if respuesta == respuesta1:
                puntuacion += 25
                print(f"✅ Correcto!, puntuacion actual: {puntuacion}")
                break
            else:
                errores += 1
                print(f"❌ Incorrecto. Llevas {errores} fallos.")
                if errores >= vidas_juego:
                    print("💀 Has perdido. Demasiados errores.")
                    break

        if errores >= 3:
            jugador = input("\nIngresa el nombre del jugador: ")
            jugar = input("\n¿Quieres jugar de nuevo? (s/n): ")
            ultimo_nombre = jugador
            ultima_puntuacion = puntuacion
            continue

        # Pregunta 2
        while True:
            respuesta = input(pregunta2 + " ")
            if respuesta == respuesta2:
                puntuacion += 25
                print(f"✅ Correcto!, puntuacion actual: {puntuacion}")
                break
            else:
                errores += 1
                print(f"❌ Incorrecto. Llevas {errores} fallos.")
                if errores >= vidas_juego:
                    print("💀 Has perdido. Demasiados errores.")
                    break

        if errores >= 3:
            jugador = input("\nIngresa el nombre del jugador: ")
            jugar = input("\n¿Quieres jugar de nuevo? (s/n): ")
            ultimo_nombre = jugador
            ultima_puntuacion = puntuacion
            continue

        # Pregunta 3
        while True:
            respuesta = input(pregunta3 + " ")
            if respuesta == respuesta3:
                puntuacion += 25
                print(f"✅ Correcto!, puntuacion actual: {puntuacion}")
                if dificultad != "3":
                    print("Ganaste una vida extra.")
                    vidas_juego += 1  # Vida extra
                break
            else:
                errores += 1
                print(f"❌ Incorrecto. Llevas {errores} fallos.")
                if errores >= vidas_juego:
                    print("💀 Has perdido. Demasiados errores.")
                    break

        if errores >= 3:
            jugador = input("\nIngresa el nombre del jugador: ")
            jugar = input("\n¿Quieres jugar de nuevo? (s/n): ")
            ultimo_nombre = jugador
            ultima_puntuacion = puntuacion
            continue

        # Pregunta 4
        while True:
            respuesta = input(pregunta4 + " ")
            if respuesta == respuesta4:
                print("🏆 ¡Correcto! ¡Has ganado el juego!")
                break
            else:
                errores += 1
                print(f"❌ Incorrecto. Llevas {errores} fallos.")
                if errores >= vidas_juego:
                    print("💀 Has perdido. Demasiados errores.")
                    break

        # Preguntar si desea jugar de nuevo
        jugador = input("\nIngresa el nombre del jugador: ")
        jugar = input("\n¿Quieres jugar de nuevo? (s/n): ")
        ultimo_nombre = jugador
        ultima_puntuacion = puntuacion

    if opcion == "2":
        print(f"El último jugador fue {ultimo_nombre} con una puntuación de {ultima_puntuacion}")
    if opcion == "3":
        print("👋 ¡Gracias por jugar!")
        break