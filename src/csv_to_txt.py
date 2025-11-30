
# Script para convertir un archivo CSV de textos en archivos de texto individuales.
# Cada fila del CSV se guarda como un archivo .txt separado.
import csv
import os


# Ruta al archivo CSV de entrada
INPUT = "data/raw/train_data.csv"
# Carpeta donde se guardarán los archivos de texto generados
OUTPUT_DIR = "data/docs"
# Límite de documentos a procesar (para no crear demasiados archivos)
LIMIT = 100


# Nos aseguramos de que la carpeta de salida exista
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Abrimos el archivo CSV de entrada
with open(INPUT, "r", encoding="latin-1") as f:
    reader = csv.reader(f)
    next(reader, None)  # Saltamos la primera fila (cabecera)
    count = 0
    for row in reader:
        # Cada fila debería tener al menos una columna con el texto
        if len(row) < 1:
            continue
        # Tomamos el texto de la primera columna
        text = row[0].strip()
        # Creamos un nombre de archivo único para cada documento
        filename = f"doc_{count:06d}.txt"
        # Guardamos el texto en un archivo .txt
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as out:
            out.write(text)
        count += 1
        # Si llegamos al límite, dejamos de procesar
        if count >= LIMIT:
            break
