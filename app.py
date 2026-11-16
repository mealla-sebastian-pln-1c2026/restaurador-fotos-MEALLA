"""Interfaz web: agranda fotos de hojas y muestra qué agregó la IA."""
import gradio as gr

from src.diffusion import linea_base, restaurar

AVISO = "foto agrandada con IA tiene detalles que dibujó el programa y que pueden no estar en la hoja real. No la mandes sola: enviale al ingeniero también la foto original."


def procesar(imagen, progreso=gr.Progress()):
    """Devuelve la versión sin IA y la versión con IA de la misma foto."""
    if imagen is None:
        raise gr.Error("Debes subir una foto primero.")
    progreso(0.1, desc="Agrandando la foto sin IA...")
    sin_ia = linea_base(imagen)
    progreso(0.3, desc="Dibujando los detalles con IA. Puede tardar unos minutos...")
    con_ia = restaurar(imagen)
    return (sin_ia, con_ia), AVISO


with gr.Blocks(title="Agrandar fotos de hojas") as demo:
    gr.Markdown("# Agrandar fotos de hojas")
    gr.Markdown("Suba una foto de una hoja y haz clic en 'Agrandar foto' para ver la diferencia entre la imagen original y la versión reconstruida con IA.")
    entrada = gr.Image(type="pil", label="Foto de la hoja")
    boton = gr.Button("Agrandar foto")
    comparador = gr.ImageSlider(label="Izquierda: sin IA  |  Derecha: con IA")
    aviso = gr.Markdown()
    boton.click(procesar, entrada, [comparador, aviso])

demo.launch()