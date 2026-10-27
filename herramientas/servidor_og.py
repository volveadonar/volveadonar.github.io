"""Servidor local para generar la imagen de vista previa para redes (og-imagen.jpg).

Uso: python herramientas/servidor_og.py
Después abrí http://localhost:8766/herramientas/og-imagen.html: la página dibuja la imagen
y este servidor la guarda en la raíz del proyecto.
"""
import http.server
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PUERTO = 8766
LIMITE = 2 * 1024 * 1024


class Manejador(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(RAIZ), **kwargs)

    def do_POST(self):
        if self.path != "/guardar-og":
            self.send_error(404)
            return
        largo = int(self.headers.get("Content-Length", 0))
        datos = self.rfile.read(min(largo, LIMITE))
        if not datos.startswith(b"\xff\xd8\xff"):
            self.send_error(400, "No es un JPG")
            return
        (RAIZ / "og-imagen.jpg").write_bytes(datos)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")


if __name__ == "__main__":
    print(f"Abrí http://localhost:{PUERTO}/herramientas/og-imagen.html")
    http.server.ThreadingHTTPServer(("127.0.0.1", PUERTO), Manejador).serve_forever()
