def es_nombre_valido(nombre):
    """
    La siguiente función recibe un nombre y verifica que no
    contenga números o caracteres especiales.
    Args:
        nombre(str): Nombre a recibir
    Return:
        return(bool): Validez del nombre
    """
    caracteres_invalidos = "0123456789!@#$%^&*()_+-={}[]|:;\"'<>,.?/~`"

    if len(nombre) == 0:
        return False

    for caracter in nombre:
        if caracter in caracteres_invalidos:
            return False

    return True

def main():

  while True:
      nombre = input("Ingrese un nombre: ")
      if es_nombre_valido(nombre):
          print("Registro exitoso")
          break
      else:
          print("Nombre inválido, intente de nuevo.")

main()