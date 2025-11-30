import os  # Para interactuar con el sistema de archivos

# Carpeta donde están los índices limpios (sin stopwords)
INDEX_DIR = "index/clean"


def cargar_indice_en_memoria(directorio):
    """
    Lee todos los archivos de índice (uno por palabra) y los carga en un diccionario.
    Así, cada palabra apunta a la lista de documentos donde aparece.
    """
    indice = {}
    print(f"Cargando índice desde: {directorio}...")
    try:
        for nombre_archivo_idx in os.listdir(directorio):
            # Solo procesar archivos .idx
            if not nombre_archivo_idx.endswith(".idx"):
                continue
            # La palabra es el nombre del archivo (sin extensión)
            palabra = nombre_archivo_idx.rsplit('.', 1)[0].lower()
            ruta_archivo = os.path.join(directorio, nombre_archivo_idx)
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    # Guardar la lista de documentos donde aparece la palabra
                    documentos = [doc.strip() for doc in f if doc.strip()]
                    indice[palabra] = sorted(documentos)
            except IOError as e:
                print(f"Advertencia: No se pudo leer el archivo {ruta_archivo}. Error: {e}")
    except FileNotFoundError:
        # Si el directorio no existe, avisar
        return None
    return indice

# --- FUNCIONES RECURSIVAS PARA INTERSECCIÓN ---


def interseccion_listas_recursiva(lista1, lista2, resultado_acumulado=None):
    """
    Toma dos listas ORDENADAS de documentos y devuelve solo los que están en ambas (intersección), usando recursión.
    Es útil para consultas con varias palabras (AND).
    """
    if resultado_acumulado is None:
        resultado_acumulado = []
    # Si alguna lista se vacía, ya no hay más intersección
    if not lista1 or not lista2:
        return resultado_acumulado
    doc1 = lista1[0]
    doc2 = lista2[0]
    if doc1 == doc2:
        # Si el documento está en ambas listas, lo agrego y sigo con el resto
        return interseccion_listas_recursiva(lista1[1:], lista2[1:], resultado_acumulado + [doc1])
    elif doc1 < doc2:
        # Avanzo en la primera lista
        return interseccion_listas_recursiva(lista1[1:], lista2, resultado_acumulado)
    else:
        # Avanzo en la segunda lista
        return interseccion_listas_recursiva(lista1, lista2[1:], resultado_acumulado)



def buscar_documentos(indice, consulta):
    """
    Recibe una consulta (palabras separadas por espacio) y busca los documentos que contienen TODAS esas palabras.
    Devuelve la lista de documentos que cumplen la consulta.
    """
    # Separar la consulta en palabras, todo a minúsculas
    terminos = [t.strip().lower() for t in consulta.split() if t.strip()]
    listas_posteo = []
    # Por cada término, buscar su lista de documentos
    for termino in terminos:
        if termino in indice:
            listas_posteo.append(indice[termino])
        else:
            print(f"Término '{termino}' no encontrado en el índice.")
            return []
    if not listas_posteo:
        return []
    # Si hay varias palabras, intersectar todas las listas de documentos
    def reducir_listas_recursivamente(listas):
        if len(listas) == 1:
            return listas[0]
        intersec_resto = reducir_listas_recursivamente(listas[1:])
        return interseccion_listas_recursiva(listas[0], intersec_resto)
    documentos_encontrados = reducir_listas_recursivamente(listas_posteo)
    return documentos_encontrados

# --- Lógica Principal del Buscador ---
if __name__ == "__main__":
    # Cargar el índice invertido en memoria al iniciar el programa
    indice_invertido = cargar_indice_en_memoria(INDEX_DIR)

    if indice_invertido is None or not indice_invertido:
        print("ERROR: No se pudo cargar el índice. Asegúrate de ejecutar 'make clean_index'.")
    else:
        print(f"Índice cargado en memoria con {len(indice_invertido)} términos.")
        print("--- Buscador Iniciado (Ingrese 'SALIR' para terminar) ---")

        while True:
            try:
                # Pedir consulta al usuario
                entrada_usuario = input("\n> Ingrese consulta de palabras: ")
                # Permitir salir escribiendo SALIR
                if entrada_usuario.upper() == 'SALIR':
                    break
                # Buscar documentos que cumplen la consulta
                resultados = buscar_documentos(indice_invertido, entrada_usuario)
                # Eliminar duplicados manteniendo el orden (por si acaso)
                resultados_unicos = list(dict.fromkeys(resultados))
                if resultados_unicos:
                    print("\n Documentos encontrados:")
                    print(f"-> {', '.join(resultados_unicos)}")
                else:
                    print("\n No se encontraron documentos que contengan todos los términos.")
            except EOFError:
                # Si el usuario presiona Ctrl+D o Ctrl+Z, salir
                break