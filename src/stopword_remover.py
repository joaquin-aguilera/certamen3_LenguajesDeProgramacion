
# Importamos módulos para manejar archivos y copiar datos
import os
import shutil

# Lista de palabras vacías (stopwords) en inglés. Si una palabra está aquí, la ignoramos del índice.
STOPWORDS = {
    'a', 'an', 'the', 'of', 'to', 'in', 'is', 'it', 'for', 'with', 'on', 'at', 'by', 'from', 'that', 'but', 'not',
    'more', 'if', 'my', 'your', 'he', 'she', 'we', 'has', 'have', 'his', 'her', 'me', 'you', 'him', 'them', 'and',
    'or', 'this', 'these', 'those'
}


# Carpeta de entrada: índices "crudos" (con stopwords)
INPUT_DIR = "index/raw"
# Carpeta de salida: índices limpios (sin stopwords)
OUTPUT_DIR = "index/clean"


# Nos aseguramos de que la carpeta de salida exista antes de copiar archivos
os.makedirs(OUTPUT_DIR, exist_ok=True)



def procesar_archivos_recursivo(archivos):
    """
    Procesa recursivamente todos los archivos de índice.
    Si el archivo corresponde a una stopword, la reporta y NO la copia al índice limpio.
    Si no es stopword, copia el archivo al directorio limpio.
    """
    if not archivos:
        # Si ya no quedan archivos, terminamos la recursión
        return
    # Tomamos el primer archivo de la lista
    nombre_archivo_idx = archivos[0]
    # La palabra es el nombre del archivo (sin extensión)
    palabra = nombre_archivo_idx.rsplit('.', 1)[0].lower()
    ruta_origen = os.path.join(INPUT_DIR, nombre_archivo_idx)
    ruta_destino = os.path.join(OUTPUT_DIR, nombre_archivo_idx)
    if palabra in STOPWORDS:
        # Si la palabra es una stopword, la reportamos y no la copiamos
        try:
            with open(ruta_origen, 'r', encoding='utf-8') as f:
                documentos = [doc.strip() for doc in f if doc.strip()]
            print(f"[-] STOPWORD removida: '{palabra}'. Aparecía en: {', '.join(documentos)}")
        except FileNotFoundError:
            # Si el archivo no existe, simplemente lo ignoramos
            pass
    else:
        # Si no es stopword, copiamos el archivo al índice limpio
        shutil.copy2(ruta_origen, ruta_destino)
    # Procesamos el resto de los archivos (llamada recursiva)
    procesar_archivos_recursivo(archivos[1:])


# --- Lógica Principal ---
if __name__ == "__main__":
    try:
        # Listamos todos los archivos de índice "crudo"
        archivos_raw = os.listdir(INPUT_DIR)
        print(f"Iniciando limpieza de {len(archivos_raw)} archivos de índice...")
        # Procesamos todos los archivos recursivamente
        procesar_archivos_recursivo(archivos_raw)
        print("\n Proceso de limpieza finalizado.")
        print(f"Índice limpio generado en: {OUTPUT_DIR}")
    except FileNotFoundError:
        # Si la carpeta de entrada no existe, avisamos al usuario
        print(f"Error: El directorio {INPUT_DIR} no existe. Ejecute la construcción de índice ('make index') primero.")