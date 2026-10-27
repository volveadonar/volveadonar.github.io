"""Genera los íconos PNG de la app (gota blanca sobre fondo bordó) sin dependencias externas.

Uso: python herramientas/generar_iconos.py
"""
import math
import struct
import zlib
from pathlib import Path

FONDO = (163, 19, 47)
GOTA = (255, 255, 255)
SALIDA = Path(__file__).resolve().parent.parent / "icons"


def bezier(p0, p1, p2, p3, n=40):
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        yield (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
               u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def contorno_gota():
    """La misma gota del logo, en una caja de 24x24."""
    pts = list(bezier((12, 2.5), (15.4, 7.2), (18.8, 11), (18.8, 14.8)))
    pts += [(12 + 6.8 * math.cos(a), 14.8 + 6.8 * math.sin(a))
            for a in (math.pi * i / 60 for i in range(61))]
    pts += list(bezier((5.2, 14.8), (5.2, 11), (8.6, 7.2), (12, 2.5)))
    return pts


def adentro(x, y, poly):
    dentro = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            dentro = not dentro
        j = i
    return dentro


def png(tamano, ruta, muestras=4):
    # Escala la gota al 62% del ícono y la centra: queda dentro de la zona segura de los íconos "maskable"
    k = tamano * 0.62 / 24
    poly = [(tamano / 2 + (x - 12) * k, tamano / 2 + (y - 12.05) * k) for x, y in contorno_gota()]
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)

    filas = bytearray()
    for py in range(tamano):
        filas.append(0)
        for px in range(tamano):
            cobertura = 0.0
            if x0 - 1 <= px <= x1 + 1 and y0 - 1 <= py <= y1 + 1:
                hits = sum(adentro(px + (sx + 0.5) / muestras, py + (sy + 0.5) / muestras, poly)
                           for sx in range(muestras) for sy in range(muestras))
                cobertura = hits / muestras**2
            filas += bytes(round(f + (g - f) * cobertura) for f, g in zip(FONDO, GOTA))

    def bloque(tipo, datos):
        return struct.pack(">I", len(datos)) + tipo + datos + struct.pack(">I", zlib.crc32(tipo + datos))

    ruta.write_bytes(b"\x89PNG\r\n\x1a\n"
                     + bloque(b"IHDR", struct.pack(">IIBBBBB", tamano, tamano, 8, 2, 0, 0, 0))
                     + bloque(b"IDAT", zlib.compress(bytes(filas), 9))
                     + bloque(b"IEND", b""))
    print(f"{ruta.name}: {ruta.stat().st_size} bytes")


if __name__ == "__main__":
    SALIDA.mkdir(exist_ok=True)
    png(192, SALIDA / "icon-192.png")
    png(512, SALIDA / "icon-512.png")
    png(180, SALIDA / "apple-touch-icon.png")
