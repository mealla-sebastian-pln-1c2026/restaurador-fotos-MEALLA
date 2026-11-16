"""Procesamiento con difusión: agranda una imagen 4 veces."""
import torch
from diffusers import StableDiffusionUpscalePipeline
from PIL import Image

MODELO = "stabilityai/stable-diffusion-x4-upscaler"
LADO_MAXIMO = 128  # en CPU, entradas más grandes tardan demasiado


dispositivo = "cuda" if torch.cuda.is_available () else "cpu"

# El modelo se carga UNA sola vez, al importar el archivo
pipe = StableDiffusionUpscalePipeline.from_pretrained(MODELO)
pipe = pipe.to(dispositivo)


def achicar(imagen: Image.Image) -> Image.Image:
    """Reduce la imagen para que ningún lado supere LADO_MAXIMO."""
    imagen = imagen.convert("RGB")
    imagen.thumbnail((LADO_MAXIMO, LADO_MAXIMO))
    return imagen


def restaurar(imagen: Image.Image, pasos: int = 20) -> Image.Image:
    """Devuelve la imagen agrandada x4 por el modelo de difusión."""
    chica = achicar(imagen)
    resultado = pipe(
        prompt="foto de una hoja de planta",  # orienta al modelo: los detalles que genere serán de hoja
        image=chica,
        num_inference_steps=pasos,
    ).images[0]
    return resultado


def linea_base(imagen: Image.Image) -> Image.Image:
    """Agranda x4 con interpolación bicúbica, sin IA."""
    chica = achicar(imagen)
   
    return chica.resize((chica.width * 4, chica.height * 4), Image.BICUBIC)