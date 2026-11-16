"""Análisis visual: compara qué 've' SigLIP en la foto sin IA y con IA."""
from transformers import pipeline

MODELO = "google/siglip2-base-patch16-224"

# Frase en inglés (la que lee el modelo) -> texto en español (el que lee Ramón)
ETIQUETAS = {
    "a healthy green plant leaf": "Hoja sana",
    "a plant leaf with disease spots": "Hoja con manchas de enfermedad",
    "a plant leaf with insect damage": "Hoja con daño de insectos",
    "a plant leaf with nutrient deficiency": "Hoja con deficiencia de nutrientes"
}

# El modelo se carga UNA sola vez, al importar el archivo
clasificador = pipeline("zero-shot-image-classification", model=MODELO)


def puntajes(imagen):
    """Devuelve un diccionario {etiqueta en español: puntaje entre 0 y 1}."""
    resultado = clasificador(imagen, candidate_labels=list(ETIQUETAS))
    return {ETIQUETAS[r["label"]]: r["score"] for r in resultado}


def analizar(sin_ia, con_ia):
    """Arma una tabla que compara los puntajes de las dos versiones."""
    antes = puntajes(sin_ia)
    despues = puntajes(con_ia)
    lineas = [
        "| Qué se ve en la foto | Sin IA | Con IA |",
        "|---|---|---|",
    ]
    for nombre in antes:
        lineas.append(f"| {nombre} | {antes[nombre]:.0%} | {despues[nombre]:.0%} |")
    # TODO 2: agregá una última línea de texto que le explique a Ramón cómo leer la tabla
    return "\n".join(lineas)