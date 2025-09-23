import requests

def obtener_pokemon_generacion(generacion_id):
    url = f"https://pokeapi.co/api/v2/generation/{generacion_id}/"
    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        print("Error al obtener datos:", respuesta.status_code)
        return []
    data = respuesta.json()
    # data["pokemon_species"] es una lista de species, con name y url
    return data["pokemon_species"]

def obtener_detalles_pokemon(pokemon_species_url):
    respuesta = requests.get(pokemon_species_url)
    if respuesta.status_code != 200:
        print("Error al obtener species:", respuesta.status_code)
        return None
    species_data = respuesta.json()
    # para obtener más detalles (como tipos, stats, etc.), hay que hacer otra petición
    # species_data tiene muchos datos, pero puedes escoger algunas claves
    return {
        "name": species_data.get("name"),
        "id": species_data.get("id"),
        # Aquí solo como ejemplo; hay que buscar cómo obtener tipos desde otra parte (pokemon endpoint)
    }

def main():
    generacion = 1  # generación I → región Kanto
    lista_species = obtener_pokemon_generacion(generacion)
    
    with open("pokemon_kanto.txt", "w", encoding="utf-8") as f:
        for species in lista_species:
            # species tiene "name" y "url" hacia species, pero para id u otros atributos detalles extra
            detalles = obtener_detalles_pokemon(species["url"])
            if detalles:
                # escribir cada clave y valor línea por línea, sin llaves
                for clave, valor in detalles.items():
                    f.write(f"{clave}: {valor}\n")
                f.write("\n")  # separar entre pokemon


main()
