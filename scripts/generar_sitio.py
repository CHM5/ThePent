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
    footer {{
      border-top: 1px solid #eee;
      background: #f8f9fa;
      border-radius: 0 0 10px 10px;
    }}
    #footer-redes a:hover {{
      opacity: 0.7;
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
    <div id="resto-nombre" style="font-size:2.2rem;font-weight:700;margin-bottom:0.2rem;"></div>
    <div id="resto-subtitulo" style="font-size:1.2rem;color:#ffc107;margin-bottom:1.2rem;"></div>
  </header>
  <div class="container">
    <div class="search-box">
      <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <input id="search" type="text" placeholder="Buscador..." autocomplete="off">
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
      <div id="noResults" style="display:none;color:#b00;text-align:center;margin:1rem 0;">No hay resultados.</div>
    </div>
  </div>
  <footer style="display:flex;justify-content:space-between;align-items:flex-end;max-width:900px;margin:2rem auto 0 auto;padding:1rem 1rem 2rem 1rem;">
    <div id="footer-direccion" style="font-size:1rem;color:#444;"></div>
    <div id="footer-redes" style="display:flex;gap:1.2rem;"></div>
  </footer>
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
        allRows = data.split("\\n").slice(1, 26).map(row => {{
          // Mejor parseo para precios con coma
          const cols = row.match(/(".*?"|[^",\\s]+)(?=\\s*,|\\s*$)/g) || [];
          return cols.map(col => col.replace(/"/g, ""));
        }});
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

        // Nombre y subtítulo
        const nombre = (rows[4]?.split(",")[1] || "").replace(/"/g, "").trim();
        const subtitulo = (rows[5]?.split(",")[1] || "").replace(/"/g, "").trim();
        document.getElementById("resto-nombre").textContent = nombre;
        document.getElementById("resto-subtitulo").textContent = subtitulo;

        // Dirección y horarios
        const direccion = (rows[6]?.split(",")[1] || "").replace(/"/g, "").trim();
        const horarios = (rows[7]?.split(",")[1] || "").replace(/"/g, "").trim();
        let direccionHtml = "";
        if (direccion) direccionHtml += `<div><strong>Dirección:</strong> ${direccion}</div>`;
        if (horarios) direccionHtml += `<div><strong>Horarios:</strong> ${horarios}</div>`;
        document.getElementById("footer-direccion").innerHTML = direccionHtml;

        // Redes sociales
        const redes = ["Whatsapp", "Instagram", "Facebook", "Rappi", "PedidosYa"];
        const iconos = [
          "📱", // Whatsapp
          '<svg width="20" height="20" fill="#E4405F" viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.9.2 2.3.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.3 1.1.4 2.3.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.9-.4 2.3-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.3-2.3.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.9-.2-2.3-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.3-1.1-.4-2.3C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.9.4-2.3.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.3 2.3-.4C8.4 2.2 8.8 2.2 12 2.2zm0-2.2C8.7 0 8.3 0 7 .1 5.7.2 4.7.4 3.9.7c-.9.3-1.6.7-2.3 1.4C.7 3.1.3 3.8 0 4.7c-.3.8-.5 1.8-.6 3.1C-.1 8.3-.1 8.7 0 12c.1 3.3.1 3.7.6 5 .1 1.3.3 2.3.6 3.1.3.9.7 1.6 1.4 2.3.7.7 1.4 1.1 2.3 1.4.8.3 1.8.5 3.1.6 1.3.1 1.7.1 5 .1s3.7 0 5-.1c1.3-.1 2.3-.3 3.1-.6.9-.3 1.6-.7 2.3-1.4.7-.7 1.1-1.4 1.4-2.3.3-.8.5-1.8.6-3.1.1-1.3.1-1.7.1-5s0-3.7-.1-5c-.1-1.3-.3-2.3-.6-3.1-.3-.9-.7-1.6-1.4-2.3C20.9.7 20.2.3 19.3 0c-.8-.3-1.8-.5-3.1-.6C15.7-.1 15.3-.1 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zm0 10.2a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-10.6a1.4 1.4 0 1 1-2.8 0 1.4 1.4 0 0 1 2.8 0z"/></svg>',
          '<svg width="20" height="20" fill="#1877F3" viewBox="0 0 24 24"><path d="M22.675 0h-21.35C.6 0 0 .6 0 1.326v21.348C0 23.4.6 24 1.326 24H12.82v-9.294H9.692v-3.622h3.128V8.413c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.797.143v3.24l-1.918.001c-1.504 0-1.797.715-1.797 1.763v2.313h3.587l-.467 3.622h-3.12V24h6.116C23.4 24 24 23.4 24 22.674V1.326C24 .6 23.4 0 22.675 0"/></svg>',
          '<svg width="20" height="20" fill="#00C300" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12"/></svg>',
          '<svg width="20" height="20" fill="#FF004F" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12"/></svg>'
        ];
        let redesHtml = "";
        for (let i = 10; i <= 14; i++) {{
          if (rows[i]) {{
            const cols = rows[i].split(",");
            let link = (cols[1] || "").replace(/"/g, "").trim();
            if (link) {{
              redesHtml += `<a href="${link}" target="_blank" rel="noopener" title="${redes[i-10]}" style="margin-right:0.7rem;text-decoration:none;font-size:1.3rem;">${iconos[i-10]}</a>`;
            }}
          }}
        }}
        document.getElementById("footer-redes").innerHTML = redesHtml;
      }})
      .catch(() => {{
        document.getElementById("resto-nombre").textContent = "Nombre";
        document.getElementById("footer-direccion").textContent = "Error al cargar datos fijos.";
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
