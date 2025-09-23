def nombre_valido(nombre):
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

def correo_valido(correo):
    """
    La siguiente función recibe una cadena de texto y verifica que contenga
    sea una dirección de correo válida
    Args:
        correo(str): Cadena de texto a verificar
    Return:
        return(bool): Resultado de validez
    """
    arroba = False
    punto = False

    if len(correo) == 0:
        return False

    for caracter in correo:
        if caracter == "@":
            arroba = True
        elif caracter == ".":
            punto = True

    if arroba == False or punto == False:
        return False

    return True

def psw_segura(psw):
    """
    Verifica que una cadena de texto contenga caracteres alfanuméricos,
    caracteres especiales y una longitud mínima de 8 caracteres.
    Args:
        psw(str): Cadena de texto a verficar
    Return:
        return(bool): Resultado de validez
    """

    longitud = False
    contiene_letras = False
    contiene_numeros = False
    contiene_caracteres_especiales = False

    letras = "abcdefghijklmnopqrstuvwxyz"
    numeros = "0123456789"
    caracteres_espciales = "!@#$%^&*()_+-={}[]|:;\"'<>,.?/~`"

    if len(psw) >= 8:
        longitud = True

    for caracter in psw:
        if caracter.lower() in letras:
            contiene_letras = True
        elif caracter in numeros:
            contiene_numeros = True
        elif caracter in caracteres_espciales:
            contiene_caracteres_especiales = True

    if longitud and contiene_letras and contiene_numeros and contiene_caracteres_especiales:
        return True
    else:
        return False