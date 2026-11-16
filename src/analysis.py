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
    """Arma una tabla que compara los puntajes y le explica a Ramón cómo leerla."""
    antes = puntajes(sin_ia)
    despues = puntajes(con_ia)
    lineas = [
        "| Qué se ve en la foto | Sin IA | Con IA |",
        "|---|---|---|",
    ]
    for nombre in antes:
        lineas.append(f"| {nombre} | {antes[nombre]:.0%} | {despues[nombre]:.0%} |")

    # Explicación para Ramón, debajo de la tabla
    lineas.append("")  
    lineas.append(
        "**Cómo leer esta tabla:** cada porcentaje indica qué tan seguro está el "
        "programa de que la foto muestra eso. Cada fila se evalúa por separado, "
        "por eso los números no suman 100%."
    )

    # Buscamos el síntoma que más cambió entre la foto sin IA y la foto con IA
    mayor_cambio = max(antes, key=lambda nombre: abs(despues[nombre] - antes[nombre]))
    diferencia = despues[mayor_cambio] - antes[mayor_cambio]

    if abs(diferencia) >= 0.15:
        sentido = "bajó" if diferencia < 0 else "subió"
        lineas.append("")
        lineas.append(
            f"⚠️ **Ojo:** «{mayor_cambio}» {sentido} {abs(diferencia):.0%} con la IA. "
            "Puede ser que la IA haya borrado o dibujado manchas. Compará las dos "
            "fotos con el deslizador y mandale al ingeniero también la foto original."
        )
    else:
        lineas.append("")
        lineas.append(
            "✅ Los resultados son parecidos en las dos fotos: la IA no parece "
            "haber cambiado lo que se ve en la hoja. Igual, revisá los detalles."
        )

    return "\n".join(lineas)