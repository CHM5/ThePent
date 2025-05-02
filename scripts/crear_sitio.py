import os
from pathlib import Path

# Datos de ejemplo
nombre = "juan"
titulo = "Menú de Juan"
items = ["Pizza", "Empanadas", "Ensalada"]

# Ruta del nuevo sitio
carpeta = Path(f"clientes/menu-{nombre}")
carpeta.mkdir(parents=True, exist_ok=True)

# Generar archivo index.html
html = f"""<html>
  <head><title>{titulo}</title></head>
  <body>
    <h1>{titulo}</h1>
    <ul>
      {''.join(f"<li>{item}</li>" for item in items)}
    </ul>
  </body>
</html>"""

with open(carpeta / "index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Sitio generado en", carpeta)
