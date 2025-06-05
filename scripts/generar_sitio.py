import os
import json
from pathlib import Path
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# === CONFIG ===
TEMPLATE_SHEET_ID = "1bHOgSjbDydp69BeUS0Ln9JFke6Y2U0SGcwahUeAPAuc"
MENU_RANGE = "Carta Web Interactiva!A2:E26"  # Hasta 25 productos
FIJOS_RANGE = "Datos Fijos!B4:B15"
SHEET_FIELDS = ["Categoría", "Subcategoría", "Nombre", "Descripción", "Precio"]

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

# Permiso general: cualquiera con el enlace puede ver
drive_service.permissions().create(
    fileId=sheet_id,
    body={
        "type": "anyone",
        "role": "reader"
    },
    sendNotificationEmail=False
).execute()

# === LEER CONTENIDO DE SHEET DE AMBAS TABS ===
MENU_RANGE = "Carta Web Interactiva!A2:E26"
FIJOS_RANGE = "Datos Fijos!B4:B15"

# Leer menú
menu_result = sheets_service.spreadsheets().values().get(
    spreadsheetId=sheet_id,
    range=MENU_RANGE
).execute()
menu_rows = menu_result.get("values", [])

# Leer datos fijos
fijos_result = sheets_service.spreadsheets().values().get(
    spreadsheetId=sheet_id,
    range=FIJOS_RANGE
).execute()
fijos_rows = fijos_result.get("values", [])

# Opcional: convertir datos fijos a una lista simple (quita sublistas vacías)
fijos = [row[0] for row in fijos_rows if row]

# === GENERAR HTML RESPONSIVO CON BUSCADOR ===
output_dir = Path(f"planes/menu-base-{fecha_id}")
output_dir.mkdir(parents=True, exist_ok=True)
html_file = output_dir / "index.html"

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Menú Online</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <style>
    :root {{
      --primary: #ffc107;
      --bg: #fff;
      --text: #212529;
      --header: #343a40;
      --border: #dee2e6;
      --radius: 10px;
    }}
    body {{
      font-family: 'Segoe UI', Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 0;
    }}
    header {{
      background: var(--header);
      color: #fff;
      padding: 1.2rem 1rem 0.7rem 1rem;
      text-align: center;
      border-radius: 0 0 var(--radius) var(--radius);
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      padding: 1rem;
    }}
    .fijos {{
      margin: 1.5rem 0 1rem 0;
      padding: 0.7rem 1rem;
      background: #f8f9fa;
      border-radius: var(--radius);
      font-size: 1rem;
      color: #444;
    }}
    .search-box {{
      display: flex;
      align-items: center;
      margin-bottom: 1.2rem;
      background: #f8f9fa;
      border-radius: var(--radius);
      padding: 0.5rem 1rem;
      box-shadow: 0 2px 8px #0001;
    }}
    .search-box input {{
      flex: 1;
      border: none;
      background: transparent;
      font-size: 1.1rem;
      padding: 0.7rem 0.5rem;
      outline: none;
    }}
    .search-box svg {{
      margin-right: 0.7rem;
      opacity: 0.6;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
      background: #fff;
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: 0 2px 8px #0001;
    }}
    th, td {{
      padding: 0.8rem 0.5rem;
      border-bottom: 1px solid var(--border);
      text-align: left;
      font-size: 1rem;
    }}
    th {{
      background: #f1f1f1;
      font-weight: 700;
      color: #343a40;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    @media (max-width: 700px) {{
      .container {{
        padding: 0.5rem;
      }}
      th, td {{
        font-size: 0.97rem;
        padding: 0.6rem 0.3rem;
      }}
      .fijos {{
        font-size: 0.97rem;
        padding: 0.5rem 0.7rem;
      }}
      .search-box {{
        padding: 0.4rem 0.7rem;
      }}
    }}
    @media (max-width: 480px) {{
      header {{
        font-size: 1.2rem;
        padding: 0.8rem 0.3rem;
      }}
      .container {{
        padding: 0.2rem;
      }}
      th, td {{
        font-size: 0.93rem;
        padding: 0.4rem 0.2rem;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1 style="margin:0;font-size:2rem;">Menú Online</h1>
    <div style="font-size:1rem;font-weight:400;margin-top:0.2rem;">
      <a href="{sheet_url}" target="_blank" style="color:#ffc107;text-decoration:underline;">Ver planilla</a>
    </div>
  </header>
  <div class="container">
    <div class="fijos">
      <strong>Datos Fijos:</strong>
      <ul id="fijos-list" style="margin:0.5rem 0 0 1.2rem;">
        <li>Cargando...</li>
      </ul>
    </div>
    <div class="search-box">
      <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input id="search" type="text" placeholder="Buscar plato, categoría, descripción..." autocomplete="off">
    </div>
    <div style="overflow-x:auto;">
      <table id="menuTable">
        <thead>
          <tr>
            <th>Categoría</th>
            <th>Subcategoría</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Precio</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
    <div id="noResults" style="display:none;text-align:center;color:#dc3545;margin-top:1.5rem;font-size:1.1rem;">
      No se encontraron platos con ese criterio.
    </div>
  </div>
  <script>
    const CSV_URL = "{csv_url}";
    let allRows = [];

    function renderTable(rows) {{
      const tbody = document.querySelector("#menuTable tbody");
      tbody.innerHTML = "";
      let count = 0;
      rows.forEach(cols => {{
        if (cols.length >= 3 && cols.some(cell => cell.trim() !== "")) {{
          const tr = document.createElement("tr");
          cols.slice(0, 5).forEach(cell => {{
            const td = document.createElement("td");
            td.textContent = cell;
            tr.appendChild(td);
          }});
          tbody.appendChild(tr);
          count++;
        }}
      }});
      document.getElementById("noResults").style.display = count === 0 ? "block" : "none";
    }}

    function filterTable() {{
      const q = document.getElementById("search").value.toLowerCase();
      if (!q) {{
        renderTable(allRows);
        return;
      }}
      const filtered = allRows.filter(cols =>
        cols.join(" ").toLowerCase().includes(q)
      );
      renderTable(filtered);
    }}

    fetch(CSV_URL)
      .then(response => response.text())
      .then(data => {{
        allRows = data.split("\\n").slice(1, 26).map(row =>
          row.split(",").map(col => col.replace(/\"/g, ""))
        );
        renderTable(allRows);
      }})
      .catch(err => {{
        document.getElementById("noResults").style.display = "block";
        document.getElementById("noResults").textContent = "Error al cargar el menú.";
        console.error("Error al cargar el CSV:", err);
      }});

    document.getElementById("search").addEventListener("input", filterTable);

    // Cargar datos fijos en vivo
    const FIJOS_CSV_URL = "{sheet_url.replace('/edit', '')}/gviz/tq?tqx=out:csv&sheet=Datos%20Fijos";
    fetch(FIJOS_CSV_URL)
      .then(response => response.text())
      .then(data => {{
        const rows = data.split("\\n").map(row => row.trim()).filter(Boolean);
        const ul = document.getElementById("fijos-list");
        ul.innerHTML = "";

        // Mostrar B4:B8 (índices 3 a 7) como texto simple
        for (let i = 3; i <= 7; i++) {{
          if (rows[i]) {{
            const cols = rows[i].split(",");
            let valor = (cols[1] || "").replace(/"/g, "").trim();
            if (valor) {{
              ul.innerHTML += `<li>${{valor}}</li>`;
            }}
          }}
        }}

        // Mostrar B11:B15 (índices 11 a 15) como hipervínculo si hay valor
        const redes = ["Whatsapp", "Instagram", "Facebook", "Rappi", "PedidosYa"];
        for (let i = 11; i <= 15; i++) {{
          if (rows[i]) {{
            const cols = rows[i].split(",");
            let link = (cols[1] || "").replace(/"/g, "").trim();
            if (link) {{
              ul.innerHTML += `<li><a href="${{link}}" target="_blank" rel="noopener">${{redes[i-10]}}</a></li>`;
            }}
          }}
        }}

        if (!ul.innerHTML) {{
          ul.innerHTML = "<li>No hay datos fijos.</li>";
        }}
      }})
      .catch(() => {{
        document.getElementById("fijos-list").innerHTML = "<li>Error al cargar datos fijos.</li>";
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
    f.write(f"planes/menu-base-{fecha_id}/index.html")

with open("sheet_url.txt", "w") as f:
    f.write(sheet_url)