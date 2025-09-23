import requests

# Hacer una petición a una página web
respuesta = requests.get("https://jsonplaceholder.typicode.com/todos/")

# Ver el contenido recibido (en formato JSON)
print("Código de estado:", respuesta.status_code)
print("Contenido:")
print(respuesta.json())