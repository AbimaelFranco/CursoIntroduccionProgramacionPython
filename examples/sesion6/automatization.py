import os
import webbrowser
import requests
import pandas as pd
from datetime import datetime

def iniciar_jornada():
    """Simula el inicio de un día de trabajo remoto en Windows."""

    # --- 1. Abrir navegador con pestañas ---
    urls = [
        "https://teams.microsoft.com/v2/?web=1",  # Forzar versión web
        "https://calendar.google.com/calendar/u/0/r?pli=1",
        "https://github.com/users/AbimaelFranco/projects/2",
        "https://open.spotify.com"  # Spotify web
    ]
    for url in urls:
        webbrowser.open(url)

    # --- 2. Obtener datos de una API ---
    api_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data["bpi"]).T
        df["updated"] = data["time"]["updated"]

    except Exception as e:
        print(f"⚠️ No se pudo obtener datos de la API ({e}). Se usarán datos locales de ejemplo.")
        df = pd.DataFrame({
            "code": ["USD", "EUR"],
            "rate": ["65,000.00", "61,000.00"],
            "description": ["United States Dollar", "Euro"],
            "updated": [datetime.today().strftime("%Y-%m-%d %H:%M:%S")] * 2
        })

    # --- 3. Guardar en Excel en el escritorio ---
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    today_folder = os.path.join(desktop, datetime.today().strftime("%Y-%m-%d"))
    os.makedirs(today_folder, exist_ok=True)

    file_path = os.path.join(today_folder, "api_data.xlsx")

    # Guardar con motor openpyxl
    df.to_excel(file_path, index=False, engine="openpyxl")

    print(f"✅ Archivo Excel generado en: {file_path}")

    # --- 4. Abrir el archivo Excel ---
    try:
        os.startfile(file_path)
    except Exception:
        print("⚠️ No se pudo abrir automáticamente el Excel. Ábrelo manualmente.")

if __name__ == "__main__":
    iniciar_jornada()
