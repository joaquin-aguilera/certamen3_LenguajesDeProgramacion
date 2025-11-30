
# Script AWK para construir un índice invertido simple a partir de archivos de texto.
# Cada palabra encontrada en los documentos se guarda en un archivo .idx con la lista de documentos donde aparece.
# Uso típico:
#   awk -v OUTDIR="index/raw" -f src/build_index.awk data/docs/*.txt

BEGIN {
    # Si no se especifica OUTDIR, usamos "index/raw" por defecto
    if (OUTDIR == "") OUTDIR = "index/raw"
}

function basename(path,   n, parts) {
    # Extrae el nombre del archivo desde la ruta completa
    n = split(path, parts, "/")
    return parts[n]
}

{
    # Para cada línea de cada archivo de texto (documento)
    # Obtenemos el nombre del documento actual
    doc = basename(FILENAME)
    # Recorremos cada palabra de la línea
    for (i = 1; i <= NF; i++) {
        # Convertimos la palabra a minúsculas
        w = tolower($i)
        # Quitamos cualquier carácter raro (solo dejamos letras y números, incluyendo tildes y ñ)
        gsub(/[^[:alnum:]áéíóúñü]/, "", w)
        if (w == "") continue  # Si la palabra quedó vacía, la saltamos
        # Creamos una clave única para la combinación palabra-documento
        key = w SUBSEP doc
        # Solo agregamos la palabra si no la hemos visto antes en este documento (evita duplicados)
        if (!(key in seen)) {
            seen[key] = 1
            # Guardamos el nombre del documento en el archivo correspondiente a la palabra
            fname = OUTDIR "/" w ".idx"
            print doc >> fname
        }
    }
}
