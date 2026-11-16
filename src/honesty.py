"""Honestidad: muestra en qué partes de la foto la IA dibujó detalles nuevos."""
import numpy as np
from PIL import Image, ImageOps

AUMENTO = 4  # multiplica las diferencias para que se vean (ver README: decisiones de diseño)


def mapa_de_diferencias(sin_ia: Image.Image, con_ia: Image.Image) -> Image.Image:
    """Resta la foto con IA de la foto sin IA y pinta dónde hay más cambio."""
    # Pasamos las dos fotos a números (alto x ancho x 3 colores)
    a = np.asarray(sin_ia.convert("RGB"), dtype=np.float32)
    b = np.asarray(con_ia.convert("RGB").resize(sin_ia.size), dtype=np.float32)

    # Diferencia absoluta píxel a píxel, promediando los 3 canales de color
    diferencia = np.abs(a - b).mean(axis=2)

    # Escala fija (no relativa): así una foto con pocos cambios se ve casi negra
    diferencia = np.clip(diferencia * AUMENTO, 0, 255).astype(np.uint8)

    # Pintamos: negro = sin cambios, rojo = cambio medio, amarillo = mucho cambio
    gris = Image.fromarray(diferencia, mode="L")
    return ImageOps.colorize(gris, black="black", mid="red", white="yellow")