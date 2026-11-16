"""Interfaz web: agranda fotos de hojas y muestra qué agregó la IA."""
import gradio as gr

from src.diffusion import linea_base, restaurar

AVISO = "### ⚠️ Atención: la foto agrandada con IA tiene detalles…"
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
    gr.Markdown("Subí una foto de una hoja y hacé clic en 'Agrandar foto'. Vas a ver la misma foto agrandada de dos formas: sin IA y con IA.")
    entrada = gr.Image(type="pil", label="Foto de la hoja")
    boton = gr.Button("Agrandar foto")
    aviso = gr.Markdown()
    comparador = gr.ImageSlider(label="Izquierda: sin IA  |  Derecha: con IA")
    boton.click(procesar, entrada, [comparador, aviso])

demo.launch()