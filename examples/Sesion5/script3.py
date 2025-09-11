from modulo1 import nombre_valido, correo_valido, psw_segura

def main():

    valid_name = False
    valid_mail = False
    valid_pswd = False

    while True:

        if not valid_name:

            name = input("Ingrese un nombre: ")
            valid_name = nombre_valido(name)
            continue

        elif not valid_mail:

            email = input("Ingrese un correo: ")
            valid_mail = correo_valido(email)
            continue

        elif not valid_pswd:

            password = input("Ingrese una contraseña \n(mínimo 8 caracteres, alfanumerica y caracteres especiales): ")       
            valid_pswd = psw_segura(password)
            continue

        else:
            print("Registro exitoso")
            break
main()