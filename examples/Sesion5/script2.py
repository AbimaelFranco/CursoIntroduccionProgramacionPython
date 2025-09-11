import modulo1

def main():

    valid_name = False
    valid_mail = False
    valid_pswd = False

    while True:

        if not valid_name:

            name = input("Ingrese un nombre: ")
            valid_name = modulo1.nombre_valido(name)
            continue

        elif not valid_mail:

            email = input("Ingrese un correo: ")
            valid_mail = modulo1.correo_valido(email)
            continue

        elif not valid_pswd:

            password = input("Ingrese una contraseña \n(mínimo 8 caracteres, alfanumerica y caracteres especiales): ")       
            valid_pswd = modulo1.psw_segura(password)
            continue

        else:
            print("Registro exitoso")
            break
main()