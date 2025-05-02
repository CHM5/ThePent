import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# === CONFIG ===
TEMPLATE_SHEET_ID = "1bHOgSjbDydp69BeUS0Ln9JFke6Y2U0SGcwahUeAPAuc"
SHEET_RANGE = "A2:D26"  # Hasta 25 productos
SHEET_FIELDS = ["Categoría", "Nombre", "Descripción", "Precio"]

# === AUTENTICACIÓN ===
credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(
    credentials_info,
    scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets.readonly"]
)

drive_service = build("drive", "v3", credentials=creds)
sheets_service = build("sheets", "v4", credentials=creds)

# === GENERAR NOMBRE Y COPIAR SHEET ===
fecha_id = datetime.now().strftime("%Y%m%d-%H%M")
nombre_copia = f"Menu Base {fecha_id}"

copia = drive_service.files().copy(
    fileId=TEMPLATE_SHEET_ID,
    body={"name": nombre_copia}
).execute()

sheet_id = copia["id"]  # 👈 ESTA LÍNEA ES CLAVE
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
print("🔗 CSV para menú en vivo:", csv_url)

# === LEER EL CORREO DEL CLIENTE ===
cliente_email = os.environ.get("CLIENT_EMAIL", "default_email@example.com")  # Usando una variable de entorno o pasando por el flujo de GitHub

# Si el correo no es pasado por el entorno, puedes también tomarlo directamente de la variable del flujo
cliente_email = cliente_email or "default_email@example.com"  # Aquí usas el email pasado por el flujo si está disponible

# === DAR PERMISOS DE EDICIÓN AL CLIENTE ===
def share_sheet_with_client(sheet_id, client_email):
    try:
        # Crear el servicio de Drive
        service = build('drive', 'v3', credentials=creds)

        # Llamada para otorgar permisos de edición al cliente
        permission = {
            'type': 'user',
            'role': 'writer',  # 'writer' para permisos de edición
            'emailAddress': client_email
        }

        # Crear el permiso
        service.permissions().create(
            fileId=sheet_id,
            body=permission
        ).execute()

        print(f"Se ha dado acceso de escritura a: {client_email}")

    except HttpError as error:
        print(f'Ha ocurrido un error al compartir el archivo: {error}')
# Llamada a la función para compartir el sheet con el cliente
share_sheet_with_client(sheet_id, cliente_email)

# Compartir automáticamente la copia con tu cuenta personal
drive_service.permissions().create(
    fileId=sheet_id,
    body={
        "type": "user",
        "role": "writer",
        "emailAddress": "chmedina1994@gmail.com"
    },
    sendNotificationEmail=False
).execute()

# === LEER CONTENIDO DE SHEET ===
result = sheets_service.spreadsheets().values().get(
    spreadsheetId=sheet_id,
    range=SHEET_RANGE
).execute()

rows = result.get("values", [])

# === GENERAR HTML ===
output_dir = Path(f"planes/menu-{fecha_id}")
output_dir.mkdir(parents=True, exist_ok=True)

html_file = output_dir / "index.html"

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Menú Base</title>
  <style>
    body {{ font-family: sans-serif; padding: 20px; }}
    h1 {{ text-align: center; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th, td {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
    th {{ background: #eee; }}
  </style>
</head>
<body>
  <h1>Menú Base</h1>
  <p>Este menú está conectado a <a href="{sheet_url}" target="_blank">esta planilla</a> y se actualiza automáticamente.</p>

  <table id="menuTable">
    <thead>
      <tr>
        <th>Categoría</th>
        <th>Nombre</th>
        <th>Descripción</th>
        <th>Precio</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>

  <script>
    const CSV_URL = "{csv_url}";

    fetch(CSV_URL)
      .then(response => response.text())
      .then(data => {{
        const rows = data.split("\\n").slice(0, 25);
        const tbody = document.querySelector("#menuTable tbody");

        rows.forEach(row => {{
          const cols = row.split(",").map(col => col.replace(/\"/g, ""));
          if (cols.length >= 4) {{
            const tr = document.createElement("tr");
            cols.slice(0, 4).forEach(cell => {{
              const td = document.createElement("td");
              td.textContent = cell;
              tr.appendChild(td);
            }});
            tbody.appendChild(tr);
          }}
        }});
      }})
      .catch(err => {{
        console.error("Error al cargar el CSV:", err);
      }});
  </script>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Menú generado:", html_file)
print("📄 Planilla editable:", sheet_url)

# NUEVO → exportar urls para el workflow
with open("menu_url.txt", "w") as f:
    # ruta pública en GitHub Pages
    f.write(f"planes/menu-{fecha_id}/index.html")

with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)
