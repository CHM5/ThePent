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

sheet_id = copia["id"]
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"

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
  <meta charset="UTF-8">
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
  <p>Este menú fue generado automáticamente. Podés editarlo desde <a href="{sheet_url}" target="_blank">esta planilla</a>.</p>
  <table>
    <tr>{"".join(f"<th>{col}</th>" for col in SHEET_FIELDS)}</tr>
"""

for row in rows:
    cells = [row[i] if i < len(row) else "" for i in range(4)]
    html += "    <tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>\n"

html += """
  </table>
</body>
</html>
"""

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Menú generado:", html_file)
print("📄 Planilla editable:", sheet_url)
