# Volvé a Donar

App web gratuita y sin fines de lucro para que las personas que donan sangre en Rosario sepan cuándo pueden volver a donar y encuentren colectas.

Rosario necesita unos 50 donantes por día. El objetivo es que más personas se vuelvan **donantes habituales**: la app les recuerda cuándo pueden volver y los lleva a la inscripción oficial de colectas del [CUDAIO](https://cudaio.gob.ar/colectas-sangre/).

> Proyecto independiente. No es una app oficial del CUDAIO ni del Ministerio de Salud de Santa Fe.

## Qué hace

- Calcula la próxima fecha posible para donar: 2 meses entre donaciones, hasta 3 por año (mujeres) o 4 (hombres).
- Agenda un recordatorio en Google Calendar.
- Muestra a qué grupos sanguíneos les sirve tu sangre.
- Guarda el historial de donaciones.
- Muestra los requisitos básicos para donar.
- Genera un código de copia de seguridad para recuperar los datos en otro teléfono.
- Se instala en el celular y funciona sin conexión.

## Privacidad

Los datos (nombre, grupo sanguíneo y donaciones) se guardan **solo en el navegador del usuario**. No hay servidor ni base de datos: nada se envía a ningún lado.

## Estructura

| Archivo | Para qué sirve |
|---|---|
| `index.html` | Toda la app: pantallas, estilos y lógica |
| `manifest.webmanifest` | Permite instalarla en el celular |
| `sw.js` | Guarda la app para que funcione sin conexión |
| `icons/` | Íconos de la app |
| `herramientas/generar_iconos.py` | Vuelve a generar los íconos PNG |
| `og-imagen.jpg` | Imagen que muestran WhatsApp y las redes al compartir el link |
| `herramientas/og-imagen.html` y `servidor_og.py` | Vuelven a generar esa imagen |

## Cambiar la imagen para redes

```bash
python herramientas/servidor_og.py
```

Abrí <http://localhost:8766/herramientas/og-imagen.html>: la página dibuja la imagen y la guarda en `og-imagen.jpg`.

## Probarla en la computadora

```bash
python -m http.server 8000
```

Después abrí <http://localhost:8000>.

## Publicar cambios

Cada vez que cambies algo, subí la versión en `sw.js` (por ejemplo, de `vad-v1` a `vad-v2`) para que los teléfonos descarguen la versión nueva.

## Licencia

[MIT](LICENSE): podés usar, copiar y adaptar el código libremente.
