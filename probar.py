"""Prueba del upscaler sin interfaz, con una imagen de ejemplo."""
import time
from PIL import Image
from src.diffusion import achicar, linea_base, restaurar

foto = Image.open("assets/ejemplos/hoja_04.jpg")
print("Original:", foto.size)
print("Achicada:", achicar(foto).size)

linea_base(foto).save("salida_bicubica.png")

inicio = time.time()
resultado = restaurar(foto)
print("Restaurada:", resultado.size, f"en {time.time() - inicio:.0f} segundos")
resultado.save("salida_difusion.png")