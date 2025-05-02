import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

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

drive_service.permissions().create(
    fileId=sheet_id,
    body={
        "type": "anyone",
        "role": "reader"
    }
).execute()

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
