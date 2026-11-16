"""Interfaz web: agranda fotos de hojas y muestra qué agregó la IA."""
import gradio as gr
from src.analysis import analizar
from src.diffusion import linea_base, restaurar
from src.honesty import mapa_de_diferencias
AVISO = (
    "### ⚠️ Atención\n"
    "La foto agrandada con IA tiene detalles que dibujó el programa y que pueden "
    "no estar en la hoja real. No la mandes sola: enviale al ingeniero también la foto original."
)


def procesar(imagen, progreso=gr.Progress()):
    """Devuelve la versión sin IA y la versión con IA de la misma foto."""
    if imagen is None:
        raise gr.Error("Debes subir una foto primero.")
    progreso(0.1, desc="Agrandando la foto sin IA...")
    sin_ia = linea_base(imagen)
    progreso(0.3, desc="Dibujando los detalles con IA. Puede tardar unos minutos...")
    con_ia = restaurar(imagen)
    mapa = mapa_de_diferencias(sin_ia, con_ia)
    progreso(0.9, desc="Revisando qué cambió entre las dos fotos...")
    informe = analizar(sin_ia, con_ia)
    return (sin_ia, con_ia), AVISO, mapa, informe


with gr.Blocks(title="Agrandar fotos de hojas") as demo:
    gr.Markdown("# Agrandar fotos de hojas")
    gr.Markdown("Subí una foto de una hoja y hacé clic en 'Agrandar foto'. Vas a ver la misma foto agrandada de dos formas: sin IA y con IA.")
    entrada = gr.Image(type="pil", label="Foto de la hoja")
    boton = gr.Button("Agrandar foto")
    aviso = gr.Markdown()
    comparador = gr.ImageSlider(label="Izquierda: sin IA  |  Derecha: con IA")
    mapa = gr.Image(label="Dónde dibujó la IA (negro = sin cambios, amarillo = mucho cambio)", interactive=False)
    informe = gr.Markdown()
    boton.click(procesar, entrada, [comparador, aviso, mapa, informe])
demo.launch()